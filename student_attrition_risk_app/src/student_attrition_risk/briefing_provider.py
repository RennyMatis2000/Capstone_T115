"""Managed generation adapter and explicit unconfigured-generation failure."""

from typing import Any

from .config import ConfigurationError
from .models import BriefingGenerationContext, DraftBriefing, StudentRiskProfile


def _prompt(profile: StudentRiskProfile) -> str:
    return (
        "Write a concise, neutral, supportive briefing for a human reviewer "
        "about this operator-supplied record. "
        "Use only the supplied structured values. State that the risk is a model-generated signal, "
        "make no historical claims, and do not infer health, disability, finances, family circumstances, "
        "motivation, behaviour, or personal causes. Do not claim raw values caused the prediction. "
        "Suggest a non-punitive, human-reviewed check-in.\n\n"
        f"PROFILE JSON: {profile.model_dump_json()}"
    )


def _extract_response_text(content: Any) -> str:
    """Extract final text from string or structured GPT OSS output."""

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text_parts: list[str] = []

        for part in content:
            if isinstance(part, dict):
                if part.get("type") != "text":
                    continue
                text = part.get("text")
            else:
                if getattr(part, "type", None) != "text":
                    continue
                text = getattr(part, "text", None)

            if isinstance(text, str):
                text_parts.append(text)

        return "\n".join(text_parts).strip()

    return ""


class StubGenerationProvider:
    """Feature-001 (US-08) placeholder for the ``GenerationProvider`` seam.

    The concrete generative integration (the OpenAI API) is owned by **US-13**. Until then,
    the default behaviour is to raise ``ConfigurationError`` so an unconfigured backend fails
    fast and explicitly — never a template briefing masquerading as success (FR-014, FR-020).

    Tests pass ``draft=`` to return a fixed ``DraftBriefing`` or ``raises=`` to raise a chosen
    error, exercising the orchestration without any external service.
    """

    def __init__(
        self,
        draft: DraftBriefing | None = None,
        raises: BaseException | None = None,
    ) -> None:
        self._draft = draft
        self._raises = raises

    def generate(self, context: BriefingGenerationContext) -> DraftBriefing:
        if self._raises is not None:
            raise self._raises
        if self._draft is not None:
            return self._draft
        raise ConfigurationError("Briefing generation is not configured")


class DatabricksGenerationProvider:
    """Current provider used by the end-to-end briefing workflow."""

    def __init__(self, model_name: str) -> None:
        if not model_name:
            raise ConfigurationError("DATABRICKS_MODEL_NAME is required.")

        self.model_name = model_name

    def generate(
        self,
        context: BriefingGenerationContext,
    ) -> DraftBriefing:
        from databricks.sdk import WorkspaceClient
        from databricks.sdk.service.serving import (
            ChatMessage,
            ChatMessageRole,
        )

        response: Any = WorkspaceClient().serving_endpoints.query(
            name=self.model_name,
            messages=[
                ChatMessage(
                    role=ChatMessageRole.USER,
                    content=context.composed_prompt,
                )
            ],
            temperature=0.2,
            max_tokens=1600,
        )

        choices = getattr(response, "choices", None) or []

        if not choices:
            raise RuntimeError("Managed model returned no choices.")

        message = getattr(choices[0], "message", None)

        if message is None:
            raise RuntimeError("Managed model returned no response message.")

        content = getattr(message, "content", None)
        text = _extract_response_text(content)

        if not text:
            raise RuntimeError("Managed model returned no briefing text.")

        return DraftBriefing(
            student_id=(context.student_id),
            text=text,
        )
