"""Explicit operator configuration. No bundled resource or data defaults."""

import os
import re
from dataclasses import dataclass

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_VOLUME_SEGMENT = re.compile(r"^[A-Za-z0-9_-]+$")
_CONTEXT_KEY = re.compile(r"^[a-z][a-z0-9_]{0,63}$")


class ConfigurationError(ValueError):
    """Safe configuration guidance without values."""


def validate_table_identifier(identifier: str) -> str:
    parts = identifier.split(".")
    if len(parts) != 3 or any(not _IDENTIFIER.fullmatch(part) for part in parts):
        raise ConfigurationError("Table identifiers must contain three safe name parts.")
    return identifier


def validate_volume_path(path: str) -> str:
    parts = path.split("/")
    if (
        len(parts) < 5
        or parts[:2] != ["", "Volumes"]
        or any(not _VOLUME_SEGMENT.fullmatch(part) for part in parts[2:])
    ):
        raise ConfigurationError("BRIEFING_VOLUME requires a safe /Volumes/catalog/schema/volume path.")
    return path


@dataclass(frozen=True)
class Settings:
    app_env: str = "local"
    databricks_config_profile: str | None = None
    databricks_host: str | None = None
    databricks_warehouse_id: str | None = None
    prediction_table: str | None = None
    context_table: str | None = None
    approved_context_fields: tuple[str, ...] = ()
    model_name: str | None = None
    app_port: int = 8000
    streamlit_port: int = 8501
    briefing_volume: str | None = None

    def __post_init__(self):
        for table in (self.prediction_table, self.context_table):
            if table:
                validate_table_identifier(table)
        fields = self.approved_context_fields
        if (
            len(fields) > 20
            or len(fields) != len(set(fields))
            or any(not _CONTEXT_KEY.fullmatch(field) for field in fields)
        ):
            raise ConfigurationError("APPROVED_CONTEXT_FIELDS requires up to 20 unique snake_case keys.")
        if self.briefing_volume:
            validate_volume_path(self.briefing_volume)

    @classmethod
    def from_env(cls) -> "Settings":
        try:
            return cls(
                app_env=os.getenv("APP_ENV", "local"),
                databricks_config_profile=os.getenv("DATABRICKS_CONFIG_PROFILE") or None,
                databricks_host=os.getenv("DATABRICKS_HOST") or None,
                databricks_warehouse_id=os.getenv("DATABRICKS_WAREHOUSE_ID") or None,
                prediction_table=os.getenv("DATABRICKS_PREDICTION_TABLE") or None,
                context_table=os.getenv("DATABRICKS_CONTEXT_TABLE") or None,
                approved_context_fields=tuple(
                    filter(None, (x.strip() for x in os.getenv("APPROVED_CONTEXT_FIELDS", "").split(",")))
                ),
                model_name=os.getenv("DATABRICKS_MODEL_NAME") or None,
                app_port=int(os.getenv("DATABRICKS_APP_PORT", "8000")),
                streamlit_port=int(os.getenv("STREAMLIT_PORT", "8501")),
                briefing_volume=os.getenv("BRIEFING_VOLUME") or None,
            )
        except ValueError:
            raise ConfigurationError("Review application settings and port configuration.") from None
