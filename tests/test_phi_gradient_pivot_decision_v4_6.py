"""Tests for v4.6 candidate pivot decision."""

from __future__ import annotations

from phyng.candidate_decision.pivot_decision import determine_pivot_decision
from phyng.candidate_decision.next_candidate_matrix import evaluate_selection_matrix


def test_pivot_decision_recommends_curvature() -> None:
    inputs = {}
    matrix = evaluate_selection_matrix(inputs)
    pivot = determine_pivot_decision(inputs, matrix)
    
    assert pivot.pivot_recommended is True
    assert pivot.next_candidate_family == "PHI_CURVATURE"
    assert "v4.7" in pivot.recommended_next_phase
    assert pivot.freeze_review_status == "PHI_GRADIENT_FREEZE_REVIEW_COMPLETED"
