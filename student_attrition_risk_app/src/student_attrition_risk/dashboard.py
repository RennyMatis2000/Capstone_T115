"""Offline dashboard definition preparation. Does not contact or publish to a platform."""

import json
from pathlib import Path

from .config import ConfigurationError, validate_table_identifier
from .student_repository import SOURCE_ERROR


def prediction_query(table: str, *, model_reference=False, scored_at=False) -> str:
    validate_table_identifier(table)
    catalog, schema, name = table.split(".")
    optional = []
    if model_reference:
        optional.append("model_reference")
    if scored_at:
        optional.append("scored_at")
    projection = ", ".join(["student_id", "risk_score", "at_risk", "threshold_score"] + optional)
    optional_guard = ""
    if model_reference:
        optional_guard += (
            " OR (model_reference IS NOT NULL AND (length(model_reference) NOT BETWEEN 1 AND 128"
            " OR regexp_like(model_reference, '[^A-Za-z0-9_-]')))"
        )
    if scored_at:
        optional_guard += " OR (scored_at IS NOT NULL AND try_cast(scored_at AS TIMESTAMP) IS NULL)"
    # Missing required columns cause a query failure, not a successful empty result.
    # Schema metadata is checked inside the same dataset query as row validity.
    expected = (
        "('student_id','STRING'), ('risk_score','NUMBER'), "
        "('at_risk','BOOLEAN'), ('threshold_score','NUMBER')"
    )
    if model_reference:
        expected += ", ('model_reference','STRING')"
    if scored_at:
        expected += ", ('scored_at','TIMESTAMP')"
    omitted = [
        name
        for name, enabled in (("model_reference", model_reference), ("scored_at", scored_at))
        if not enabled
    ]
    omitted_check = ""
    if omitted:
        names = ", ".join(f"'{name}'" for name in omitted)
        omitted_check = (
            f" AND NOT EXISTS (SELECT 1 FROM {catalog}.information_schema.columns "
            f"WHERE table_schema = '{schema}' AND table_name = '{name}' "
            f"AND column_name IN ({names}))"
        )
    return f"""WITH expected(column_name, required_type) AS (VALUES {expected}),
schema_check AS (
 SELECT CASE WHEN COUNT(*) = {4 + len(optional)} AND MIN(CASE
   WHEN e.required_type = 'NUMBER' AND upper(c.data_type) IN
     ('DOUBLE','FLOAT','INT','INTEGER','BIGINT','SMALLINT','TINYINT','DECIMAL') THEN 1
   WHEN e.required_type = upper(c.data_type) THEN 1 ELSE 0 END) = 1{omitted_check} THEN 1 ELSE 0 END AS ok
 FROM expected e LEFT JOIN {catalog}.information_schema.columns c
 ON c.table_schema = '{schema}' AND c.table_name = '{name}' AND c.column_name = e.column_name
), source AS (SELECT {projection} FROM {table}),
checked AS (
 SELECT source.*, COUNT(*) OVER (PARTITION BY student_id) AS id_count FROM source
), validity AS (
 SELECT CASE WHEN (SELECT ok FROM schema_check) = 1 AND COUNT(CASE WHEN
   student_id IS NULL OR length(student_id) NOT BETWEEN 1 AND 128 OR regexp_like(student_id, '[^A-Za-z0-9_-]')
   OR id_count <> 1 OR risk_score IS NULL OR threshold_score IS NULL OR at_risk IS NULL
   OR isnan(risk_score) OR isnan(threshold_score)
   OR NOT (risk_score BETWEEN 0 AND 100) OR NOT (threshold_score BETWEEN 0 AND 100)
   OR at_risk <> (risk_score >= threshold_score){optional_guard}
   THEN 1 END) = 0 THEN 1 ELSE 0 END AS ok, COUNT(*) AS total FROM checked
), result AS (
 SELECT 'status' AS row_kind,
   CASE WHEN ok = 0 THEN '{SOURCE_ERROR}' WHEN total = 0 THEN 'No predictions available.'
        ELSE 'Data valid.' END AS status,
   CASE WHEN ok = 1 THEN total ELSE NULL END AS total_students,
   CASE WHEN ok = 1 THEN (SELECT COUNT(*) FROM source WHERE at_risk = TRUE) ELSE NULL END AS at_risk_students,
   CAST(NULL AS STRING) AS student_id, CAST(NULL AS DOUBLE) AS risk_score,
   CAST(NULL AS BOOLEAN) AS at_risk, CAST(NULL AS DOUBLE) AS threshold_score FROM validity
 UNION ALL
 SELECT 'student', 'Data valid.', NULL, NULL, student_id, risk_score, at_risk, threshold_score
 FROM checked WHERE (SELECT ok FROM validity) = 1
) SELECT row_kind, status, total_students, at_risk_students, student_id, risk_score, at_risk, threshold_score
FROM result"""


def render_dashboard(settings, bound_table, *, model_reference=False, scored_at=False):
    if not settings.prediction_table or bound_table != settings.prediction_table:
        raise ConfigurationError("Dashboard source binding must equal the application prediction source.")
    template = Path(__file__).resolve().parents[2] / "dashboard/Student Attrition Risk Overview.lvdash.json"
    definition = json.loads(template.read_text(encoding="utf-8"))
    definition["datasets"][0]["queryLines"] = [
        prediction_query(bound_table, model_reference=model_reference, scored_at=scored_at)
    ]
    return definition
