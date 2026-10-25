"""FastMCP tools backed by the shared StudentService."""

from typing import Any

from .config import ConfigurationError
from .student_service import (
    BriefingNotProducedError,
    BriefingStorageError,
    BriefingStoreUnavailableError,
    StudentNotAtRiskError,
    StudentNotFoundError,
    StudentService,
)


def create_mcp_server(service: StudentService) -> Any:
    from fastmcp import FastMCP
    from fastmcp.exceptions import ToolError

    mcp = FastMCP("student-attrition-risk")

    @mcp.tool()
    def get_student_prediction(student_id: str) -> dict[str, Any]:
        try:
            return service.get_student_profile(student_id).prediction.model_dump(mode="json")
        except StudentNotFoundError:
            raise ToolError("student ID not found") from None
        except Exception:
            raise ToolError("Prediction source unavailable. Review data setup.") from None

    @mcp.tool()
    def get_student_profile(student_id: str) -> dict[str, Any]:
        try:
            return service.get_student_profile(student_id).model_dump(mode="json")
        except StudentNotFoundError:
            raise ToolError("student ID not found") from None
        except Exception:
            raise ToolError("Prediction source unavailable. Review data setup.") from None

    @mcp.tool()
    def get_high_risk_students(limit: int = 20) -> list[dict[str, Any]]:
        try:
            return [p.model_dump(mode="json") for p in service.get_high_risk_students(limit)]
        except Exception:
            raise ToolError("Prediction source unavailable or invalid limit.") from None

    @mcp.tool()
    def generate_student_briefing(student_id: str, regenerate: bool = False) -> dict[str, Any]:
        try:
            return service.request_briefing(student_id, regenerate=regenerate).model_dump(mode="json")
        except StudentNotFoundError as exc:
            raise ToolError("student ID not found") from exc
        except StudentNotAtRiskError as exc:
            raise ToolError("student is not flagged at risk") from exc
        except BriefingNotProducedError as exc:
            raise ToolError(f"briefing could not be produced ({exc.category})") from exc
        except BriefingStoreUnavailableError as exc:
            raise ToolError("validated briefing store unavailable") from exc
        except BriefingStorageError as exc:
            raise ToolError("validated briefing could not be stored") from exc
        except ConfigurationError as exc:
            raise ToolError(str(exc).lower()) from exc
        except Exception as exc:
            raise ToolError("databricks data source unavailable") from exc

    @mcp.tool()
    def get_student_briefing(student_id: str) -> dict[str, Any]:
        try:
            briefing = service.get_stored_briefing(student_id)
        except StudentNotFoundError as exc:
            raise ToolError("student ID not found") from exc
        except BriefingStorageError:
            raise BriefingStorageError("validated briefing store unavailable") from None
        except Exception as exc:
            raise ToolError("validated briefing store unavailable") from exc
        if briefing is None:
            return {"available": False, "student_id": student_id}
        return briefing.model_dump(mode="json")

    return mcp
