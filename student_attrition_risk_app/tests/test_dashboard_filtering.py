from test_dashboard import run_query


def test_filters_apply_to_validated_results_only():
    rows = [("case-a", 75, True, 60), ("case-b", 25, False, 60)]
    result = run_query(rows, outer_filter="WHERE row_kind='student' AND risk_score >= 70")
    assert [r["student_id"] for r in result] == ["case-a"]
    assert run_query(rows, outer_filter="WHERE row_kind='student' AND risk_score > 90") == []
