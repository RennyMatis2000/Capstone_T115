"""Independently invented, offline-only verification records. Never used by runtime."""

from student_attrition_risk.models import ApprovedModelFeatureValues, StudentPrediction, StudentSnapshot
from student_attrition_risk.student_repository import STUDENT_ID_LENGTH


class MockStudentRepository:
    """Clearly synthetic repository for local demos and unit tests."""

    def __init__(self) -> None:
        self.predictions = {
            "synthetic-student-001": StudentPrediction(
                student_id="synthetic-student-001",
                risk_score=78.5,
                at_risk=True,
                threshold_score=50.0,
                model_reference="mock-run-001",
                scored_at="2026-01-15T10:00:00Z",
            ),
            "synthetic-student-002": StudentPrediction(
                student_id="synthetic-student-002",
                risk_score=18.0,
                at_risk=False,
                threshold_score=50.0,
                model_reference="mock-run-002",
                scored_at="2026-01-15T10:00:00Z",
            ),
            # Flagged at risk; tests seed the briefing store with an existing validated
            # briefing for this hash to exercise the return-existing and regenerate paths.
            "synthetic-student-003": StudentPrediction(
                student_id="synthetic-student-003",
                risk_score=64.0,
                at_risk=True,
                threshold_score=50.0,
                model_reference="mock-run-003",
                scored_at="2026-01-15T10:00:00Z",
            ),
        }

    def get_prediction(self, student_id: str) -> StudentPrediction | None:
        return self.predictions.get(student_id)

    def find_predictions_by_student_id(self, student_id: str) -> list[StudentPrediction]:
        matches = [p for h, p in self.predictions.items() if h[:STUDENT_ID_LENGTH] == student_id]
        return matches[:2]

    def get_snapshot(self, student_id):
        if student_id not in self.predictions:
            return None
        return StudentSnapshot(attributes={"support_channel": "email", "meeting_requested": True})

    def get_model_features(self, student_id):
        snapshot = self.get_snapshot(student_id)
        return ApprovedModelFeatureValues(values=snapshot.attributes) if snapshot else None

    def get_predictions(self):
        return list(self.predictions.values())

    def get_high_risk_students(self, limit: int) -> list[StudentPrediction]:
        return sorted(
            [prediction for prediction in self.predictions.values() if prediction.at_risk],
            key=lambda prediction: prediction.risk_score,
            reverse=True,
        )[:limit]

    def health_check(self) -> bool:
        return True


MODEL_FEATURE_COLUMNS = ("support_channel", "meeting_requested")
