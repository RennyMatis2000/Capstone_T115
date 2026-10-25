"""Current portfolio traceability, without republishing excluded worklogs."""

from pathlib import Path


def test_current_feature_has_requirements_and_acceptance_mapping():
    feature = Path(__file__).resolve().parents[2] / "specs/007-public-portfolio"
    spec = (feature / "spec.md").read_text(encoding="utf-8")
    acceptance = (feature / "acceptance.md").read_text(encoding="utf-8")
    tasks = (feature / "tasks.md").read_text(encoding="utf-8")
    for i in range(1, 16):
        assert f"FR-{i:03}" in spec
        assert f"FR-{i:03}" in acceptance or f",{i:03}" in acceptance
    for i in range(1, 25):
        assert f"T{i:03}" in tasks
