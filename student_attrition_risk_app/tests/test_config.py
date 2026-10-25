import pytest

from student_attrition_risk.config import (
    ConfigurationError,
    Settings,
    validate_table_identifier,
    validate_volume_path,
)


def test_no_resource_or_fixture_defaults(monkeypatch):
    for key in (
        "DATABRICKS_PREDICTION_TABLE",
        "DATABRICKS_CONTEXT_TABLE",
        "BRIEFING_VOLUME",
        "APPROVED_CONTEXT_FIELDS",
    ):
        monkeypatch.delenv(key, raising=False)
    settings = Settings.from_env()
    assert settings.prediction_table is None
    assert settings.context_table is None
    assert settings.briefing_volume is None
    assert settings.approved_context_fields == ()


@pytest.mark.parametrize("name", ["one.two", "one.two.three; DROP TABLE x", "a.b.`c`"])
def test_invalid_identifier(name):
    with pytest.raises(ConfigurationError):
        validate_table_identifier(name)


def test_explicit_settings(monkeypatch):
    monkeypatch.setenv("DATABRICKS_PREDICTION_TABLE", "operator.advising.predictions")
    monkeypatch.setenv("APPROVED_CONTEXT_FIELDS", "support_channel,meeting_requested")
    s = Settings.from_env()
    assert s.prediction_table == "operator.advising.predictions"
    assert s.approved_context_fields == ("support_channel", "meeting_requested")


@pytest.mark.parametrize("fields", [("bad-key",), ("same", "same"), tuple(f"key_{i}" for i in range(21))])
def test_invalid_allowlist(fields):
    with pytest.raises(ConfigurationError):
        Settings(approved_context_fields=fields)


@pytest.mark.parametrize(
    "path", ["main.advising.briefings", "/Volumes/a/b", "/Volumes/a/b/../secret", "/Volumes/a/b/c/"]
)
def test_invalid_volume(path):
    with pytest.raises(ConfigurationError):
        validate_volume_path(path)


def test_valid_volume():
    assert validate_volume_path("/Volumes/operator/advising/briefings").endswith("briefings")
