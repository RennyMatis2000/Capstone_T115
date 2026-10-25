"""Execute the generated SQL guard without Python prediction validation.

SQLite is an offline relational harness. Only the metadata/table binding and
numeric cast syntax are adapted. This is not Databricks integration evidence.
"""

import math
import re
import sqlite3

import pytest

from student_attrition_risk.config import ConfigurationError, Settings
from student_attrition_risk.dashboard import prediction_query, render_dashboard
from student_attrition_risk.student_repository import SOURCE_ERROR

TABLE = "operator.advising.predictions"


def run_query(rows, *, types=None, outer_filter="", missing=False, extra_metadata=()):
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.create_function(
        "regexp_like",
        2,
        lambda value, pattern: bool(re.search(pattern, str(value))) if value is not None else None,
    )
    db.create_function(
        "isnan", 1, lambda value: math.isnan(value) if isinstance(value, (int, float)) else False
    )
    db.execute("CREATE TABLE metadata (table_schema, table_name, column_name, data_type)")
    columns = [
        ("student_id", "STRING"),
        ("risk_score", "DOUBLE"),
        ("at_risk", "BOOLEAN"),
        ("threshold_score", "DOUBLE"),
    ]
    for col, typ in columns:
        db.execute(
            "INSERT INTO metadata VALUES ('advising','predictions',?,?)", (col, (types or {}).get(col, typ))
        )
    for column, kind in extra_metadata:
        db.execute("INSERT INTO metadata VALUES ('advising','predictions',?,?)", (column, kind))
    db.execute(
        "CREATE TABLE predictions (student_id TEXT, risk_score REAL, at_risk BOOLEAN, threshold_score REAL)"
    )
    db.executemany("INSERT INTO predictions VALUES (?,?,?,?)", rows)
    if missing:
        db.execute("ALTER TABLE predictions DROP COLUMN at_risk")
    sql = (
        prediction_query(TABLE)
        .replace("operator.information_schema.columns", "metadata")
        .replace(TABLE, "predictions")
    )
    # SQLite uses TEXT and INTEGER for typed NULL, but these values stay NULL.
    sql = sql.replace("AS STRING", "AS TEXT").replace("AS BOOLEAN", "AS INTEGER")
    try:
        return [dict(r) for r in db.execute("SELECT * FROM (" + sql + ") " + outer_filter)]
    finally:
        db.close()


def test_duplicate_pair_even_when_outer_filter_hides_one():
    rows = [("case-a", 75, True, 60), ("case-a", 25, False, 60)]
    result = run_query(rows)
    assert len(result) == 1 and result[0]["status"] == SOURCE_ERROR
    assert result[0]["total_students"] is None
    assert result[0]["at_risk_students"] is None
    assert run_query(rows, outer_filter="WHERE risk_score >= 60") == []


@pytest.mark.parametrize(
    "index,value",
    [
        (0, ""),
        (0, "bad id"),
        (0, "case-a\n"),
        (0, None),
        (1, None),
        (1, float("inf")),
        (1, float("nan")),
        (1, -1),
        (1, 101),
        (1, "bad"),
        (2, None),
        (2, False),
        (3, None),
        (3, float("inf")),
        (3, -1),
        (3, 101),
    ],
)
def test_invalid_input_returns_only_unavailable(index, value):
    row = ["case-a", 75, True, 60]
    row[index] = value
    result = run_query([row])
    assert len(result) == 1 and result[0]["status"] == SOURCE_ERROR
    assert result[0]["student_id"] is None and result[0]["total_students"] is None


@pytest.mark.parametrize(
    "types",
    [{"student_id": "INT"}, {"risk_score": "STRING"}, {"at_risk": "INT"}, {"threshold_score": "STRING"}],
)
def test_wrong_schema_invalid_even_when_empty(types):
    assert run_query([], types=types)[0]["status"] == SOURCE_ERROR


def test_missing_column_is_query_failure_never_empty_success():
    with pytest.raises(sqlite3.OperationalError):
        run_query([], missing=True)


def test_valid_and_empty_are_distinct():
    empty = run_query([])
    assert empty[0]["total_students"] == 0
    assert empty[0]["status"] == "No predictions available."
    result = run_query([("case-a", 75, True, 60), ("case-b", 25, False, 60)])
    assert result[0]["total_students"] == 2 and result[0]["at_risk_students"] == 1
    assert len([r for r in result if r["row_kind"] == "student"]) == 2


def test_binding_and_single_dataset_definition():
    settings = Settings(prediction_table=TABLE)
    with pytest.raises(ConfigurationError):
        render_dashboard(settings, "other.advising.predictions")
    with pytest.raises(ConfigurationError):
        render_dashboard(Settings(), TABLE)
    d = render_dashboard(settings, TABLE)
    assert len(d["datasets"]) == 1
    assert d["datasets"][0]["queryLines"] == [prediction_query(TABLE)]
    for layout in d["pages"][0]["layout"]:
        assert layout["widget"]["queries"][0]["query"]["datasetName"] == d["datasets"][0]["name"]
        assert layout["widget"]["spec"]["version"] == 2
        assert layout["widget"]["spec"]["data"] == {"queryName": "main_query"}
    status = d["pages"][0]["layout"][0]["widget"]
    assert status["queries"][0]["query"]["filters"] == [{"expression": "`row_kind` = 'status'"}]


def test_omitted_existing_provenance_columns_fail_setup_safely():
    result = run_query([], extra_metadata=[("model_reference", "STRING")])
    assert result[0]["status"] == SOURCE_ERROR
    assert result[0]["total_students"] is None
