"""Operator prediction and optional context adapters; no source-specific joins."""

import json
import math
from datetime import UTC, datetime
from typing import Any

from pydantic import ValidationError

from .config import ConfigurationError, Settings
from .databricks_client import create_sql_connection
from .models import ApprovedModelFeatureValues, StudentPrediction, StudentSnapshot

STUDENT_ID_LENGTH = 16


class SourceDataError(RuntimeError):
    """Safe failure for invalid or unreadable operator data."""


SOURCE_ERROR = (
    "Data unavailable: the configured prediction source does not meet the data contract. Review data setup."
)


def validate_predictions(rows):
    try:
        predictions = [StudentPrediction.model_validate(row) for row in rows]
        ids = [row.student_id for row in predictions]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate")
        return predictions
    except (ValidationError, ValueError, TypeError):
        raise SourceDataError(SOURCE_ERROR) from None


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate context key")
        result[key] = value
    return result


def approved_context(raw, fields):
    try:
        values = json.loads(
            raw, object_pairs_hook=_object, parse_constant=lambda _: (_ for _ in ()).throw(ValueError())
        )
        if not isinstance(values, dict):
            raise ValueError()
        # Validate all values before projection; unknown keys never leave this adapter.
        for key, value in values.items():
            if not isinstance(key, str) or len(key) > 64:
                raise ValueError()
            if (
                isinstance(value, (dict, list))
                or (isinstance(value, str) and len(value) > 256)
                or (isinstance(value, (int, float)) and not math.isfinite(value))
            ):
                raise ValueError()
        return {key: value for key, value in values.items() if key in fields}
    except (ValueError, TypeError, OverflowError):
        raise SourceDataError("Approved context unavailable. Review data setup.") from None


class DatabricksStudentRepository:
    def __init__(self, settings: Settings):
        self.settings = settings

    def _query(self, statement: str, parameters: tuple[Any, ...] = ()):
        try:
            connection = create_sql_connection(self.settings)
            try:
                with connection.cursor() as cursor:
                    cursor.execute(statement, parameters)
                    columns = [column[0] for column in cursor.description or []]
                    return [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]
            finally:
                connection.close()
        except Exception:
            raise SourceDataError(SOURCE_ERROR) from None

    def _predictions(self):
        if not self.settings.prediction_table:
            raise ConfigurationError("Setup required: configure DATABRICKS_PREDICTION_TABLE and SQL access.")
        # Read named required columns only. Optional provenance is discovered separately.
        table = self.settings.prediction_table
        catalog, schema, name = table.split(".")
        metadata = self._query(
            f"SELECT column_name, data_type FROM {catalog}.information_schema.columns "
            "WHERE table_schema = ? AND table_name = ?",
            (schema, name),
        )
        types = {row["column_name"]: row["data_type"].upper() for row in metadata}
        numeric = {"DOUBLE", "FLOAT", "INT", "INTEGER", "BIGINT", "SMALLINT", "TINYINT", "DECIMAL"}
        if (
            types.get("student_id") != "STRING"
            or types.get("at_risk") != "BOOLEAN"
            or any(types.get(k, "").split("(")[0] not in numeric for k in ("risk_score", "threshold_score"))
        ):
            raise SourceDataError(SOURCE_ERROR)
        columns = ["student_id", "risk_score", "at_risk", "threshold_score"]
        if "model_reference" in types:
            if types["model_reference"] != "STRING":
                raise SourceDataError(SOURCE_ERROR)
            columns.append("model_reference")
        if "scored_at" in types:
            if types["scored_at"] != "TIMESTAMP":
                raise SourceDataError(SOURCE_ERROR)
            columns.append("scored_at")
        rows = self._query(f"SELECT {', '.join(columns)} FROM {table}")
        # The SQL TIMESTAMP type is an instant. Connector sessions use UTC; some
        # connector versions return UTC values without a tzinfo object.
        for row in rows:
            timestamp = row.get("scored_at")
            if isinstance(timestamp, datetime) and timestamp.tzinfo is None:
                row["scored_at"] = timestamp.replace(tzinfo=UTC)
        # Every read validates the unfiltered relation before selection/limit.
        return validate_predictions(rows)

    def get_prediction(self, student_id):
        return next((p for p in self._predictions() if p.student_id == student_id), None)

    def find_predictions_by_student_id(self, student_id):
        return [p for p in self._predictions() if p.student_id[:STUDENT_ID_LENGTH] == student_id][:2]

    def get_predictions(self):
        return self._predictions()

    def get_high_risk_students(self, limit):
        return sorted(
            (p for p in self._predictions() if p.at_risk), key=lambda p: p.risk_score, reverse=True
        )[:limit]

    def get_snapshot(self, student_id):
        if not self.settings.context_table:
            return None
        rows = self._query(
            f"SELECT attributes_json FROM {self.settings.context_table} WHERE student_id = ?", (student_id,)
        )
        if len(rows) > 1:
            raise SourceDataError("Approved context unavailable. Review data setup.")
        if not rows:
            return None
        return StudentSnapshot(
            attributes=approved_context(rows[0]["attributes_json"], self.settings.approved_context_fields)
        )

    def get_model_features(self, student_id):
        snapshot = self.get_snapshot(student_id)
        return ApprovedModelFeatureValues(values=snapshot.attributes) if snapshot else None

    def health_check(self):
        self._predictions()
        return True
