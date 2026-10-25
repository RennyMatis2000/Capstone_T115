from fixture_repository import MockStudentRepository
from student_attrition_risk.briefing_pdf import create_briefing_pdf
from student_attrition_risk.models import (
    StudentRiskProfile,
    make_validated_briefing,
)


def test_create_briefing_pdf_returns_pdf_bytes():
    repository = MockStudentRepository()
    student_id = "synthetic-student-001"

    prediction = repository.predictions[student_id]

    profile = StudentRiskProfile(
        prediction=prediction,
        snapshot=repository.get_snapshot(student_id),
    )

    briefing = make_validated_briefing(
        student_id=student_id,
        prediction=prediction,
        text=(
            "**Risk Summary**\n"
            "- Classification: **At Risk**\n"
            "- Model-generated relative risk score: **78.5%**\n\n"
            "**Relevant Student Context**\n"
            "- Full-time student.\n\n"
            "**Recommended Advisor Actions**\n"
            "- Consider a supportive check-in.\n\n"
            "**Suggested Next Steps**\n"
            "- Review available support options."
        ),
        validator_id="test-validator",
        attempt_count=1,
    ).model_copy(update={"storage_confirmed": True})

    pdf = create_briefing_pdf(profile, briefing)

    assert isinstance(pdf, bytes)
    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1000
