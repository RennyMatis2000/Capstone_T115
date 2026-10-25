"""API and domain models."""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator, model_validator


class StudentPrediction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    student_id: str = Field(pattern=r"^[A-Za-z0-9_-]{1,128}$")
    risk_score: float = Field(ge=0, le=100, allow_inf_nan=False)
    at_risk: StrictBool
    threshold_score: float = Field(ge=0, le=100, allow_inf_nan=False)
    model_reference: str | None = Field(default=None, pattern=r"^[A-Za-z0-9_-]{1,128}$")
    scored_at: datetime | None = None

    @field_validator("risk_score", "threshold_score", mode="before")
    @classmethod
    def numeric_only(cls, value):
        from decimal import Decimal

        if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
            raise ValueError("Scores must be numeric.")
        return value

    @field_validator("scored_at")
    @classmethod
    def aware_timestamp(cls, value):
        if value is not None and (value.tzinfo is None or value.utcoffset() is None):
            raise ValueError("Scoring timestamp must include a timezone.")
        return value

    @model_validator(mode="after")
    def consistent_flag(self):
        if self.at_risk != (self.risk_score >= self.threshold_score):
            raise ValueError("Classification must agree with score and threshold.")
        return self


class StudentSnapshot(BaseModel):
    attributes: dict[str, Any]


class StudentRiskProfile(BaseModel):
    prediction: StudentPrediction
    snapshot: StudentSnapshot | None = None


class StudentBriefing(BaseModel):
    student_id: str
    source: str
    text: str


class HealthStatus(BaseModel):
    status: str
    data_source: str
    details: str | None = None


# ---------------------------------------------------------------------------
# Feature-001 (US-08) briefing-workflow types.
#
# These are the objects that cross the generation / instructions / validation /
# retry / persistence seams. Feature-001 defines them once here so US-12/13/14/15
# and Feature-002 import rather than redefine them.
# ---------------------------------------------------------------------------

# Marker placed in ApprovedModelFeatureValues when a source column is absent from
# the Delta schema. Distinct from a SQL NULL value, which is preserved as None.
UNAVAILABLE = "__unavailable__"
SUPPRESSED = "__suppressed__"


class ApprovedModelFeatureValues(BaseModel):
    """Operator-approved context, carried as data and never as causal evidence."""

    values: dict[str, Any]


class DraftBriefing(BaseModel):
    """A briefing returned by the generation seam, not yet validated (FR-026).

    ``text`` must carry substance. A generation seam that produces no usable content has
    failed to produce a draft, so rejecting it here makes the seam contract enforceable
    rather than advisory: the rejection is raised inside ``generate``, which the existing
    orchestration already treats as a generation failure (Feature-002 spec Edge Cases,
    "The retry's generation attempt returns empty content").
    """

    student_id: str
    text: str

    @field_validator("text")
    @classmethod
    def _reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("A draft briefing must contain briefing text.")
        return value


class BriefingGenerationContext(BaseModel):
    """The assembled input handed to the generation seam (FR-009)."""

    student_id: str
    prediction: StudentPrediction
    features: ApprovedModelFeatureValues
    instructions_id: str
    composed_prompt: str


class ValidationOutcome(BaseModel):
    """Returned by the validation seam (FR-015)."""

    passed: bool
    failed_criteria: list[str] = Field(default_factory=list)
    feedback: str | None = None
    validator_id: str


class ValidatedBriefing(BaseModel):
    """A briefing the validation seam passed; the only briefing form returned to a
    caller or handed to the persistence seam (FR-018, FR-025, FR-029).

    ``storage_confirmed`` records that the validated-briefing store has confirmed it holds this
    briefing (Feature-002 FR-035, amendment 2026-09-22). Like ``source`` it is stamped by
    ``StudentService`` on the way out, never by a producer or a store: ``_persist`` sets it only
    after ``save_validated`` returns, and the retrieval paths set it because they read the
    briefing out of the store. It is a property of storage, not of the generation attempt, so it
    is identical for an attempt-1 and an attempt-2 briefing and carries no retry indication
    (FR-040, FR-032). A briefing is serialised into the store *before* its save is confirmed, so
    the stored document always records ``False``; the retrieval path restamps it, exactly as it
    already restamps ``source``.
    """

    student_id: str
    text: str
    source: str
    validated: bool = True
    storage_confirmed: bool = False
    validator_id: str
    generated_at: datetime
    attempt_count: int = 1
    model_reference: str | None = None
    risk_score: float
    at_risk: bool
    threshold_score: float
    scored_at: datetime | None = None


class GenerationFailed(BaseModel):
    """First-attempt outcome: the generation seam failed before a draft (FR-019)."""

    category: str = "generation"


class ValidationFailed(BaseModel):
    """First-attempt outcome: a draft was produced but did not pass validation."""

    outcome: ValidationOutcome
    category: str = "validation"


# The payload the backend hands to the retry seam.
FirstAttemptOutcome = GenerationFailed | ValidationFailed


class Produced(BaseModel):
    """Retry-seam outcome: a validated briefing (attempt 1, or Feature-002 attempt 2)."""

    briefing: ValidatedBriefing


class TerminalFailure(BaseModel):
    """Retry-seam outcome: no validated briefing; the backend returns an explicit error (FR-021)."""

    category: str


# The value the retry seam returns.
BriefingOutcome = Produced | TerminalFailure


def make_validated_briefing(
    *,
    student_id: str,
    prediction: StudentPrediction,
    text: str,
    validator_id: str,
    attempt_count: int,
    generated_at: datetime | None = None,
) -> ValidatedBriefing:
    """Build a ``ValidatedBriefing`` from a prediction snapshot.

    The single constructor shared by ``StudentService`` (first attempt) and the
    Feature-002 ``SingleRetryWorkflow`` (second attempt) so the two paths cannot
    diverge. ``source`` is always ``"generated"``; the retrieval path restamps it
    to ``"stored"``.
    """
    return ValidatedBriefing(
        student_id=student_id,
        text=text,
        source="generated",
        validated=True,
        validator_id=validator_id,
        generated_at=generated_at or datetime.now(UTC),
        attempt_count=attempt_count,
        model_reference=prediction.model_reference,
        risk_score=prediction.risk_score,
        at_risk=prediction.at_risk,
        threshold_score=prediction.threshold_score,
        scored_at=prediction.scored_at,
    )


def format_score(value: float) -> str:
    """Keep concise exact tenths, otherwise retain the supplied float's precision."""
    rounded = f"{value:.1f}"
    return rounded if float(rounded) == value else str(value)
