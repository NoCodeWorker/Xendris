"""Tests for v4.6 candidate selection matrix."""

from __future__ import annotations

from phyng.candidate_decision.next_candidate_matrix import evaluate_selection_matrix


def test_next_candidate_not_selected_by_synthetic_score_alone() -> None:
    inputs = {}
    matrix = evaluate_selection_matrix(inputs)
    
    # B_SUPPRESSED has the highest synthetic score (0.55) but should not be selected
    b_suppressed = [r for r in matrix if r.family_id == "B_SUPPRESSED"][0]
    assert b_suppressed.synthetic_survivability_score == 0.55
    assert b_suppressed.recommended_action == "ARCHIVE"

    # PHI_CURVATURE should be selected despite having a lower synthetic score (0.4668)
    phi_curvature = [r for r in matrix if r.family_id == "PHI_CURVATURE"][0]
    assert phi_curvature.synthetic_survivability_score == 0.4668
    assert phi_curvature.recommended_action == "SELECT_FOR_SOURCE_AND_YTRUE_SCREENING"
    assert phi_curvature.y_true_accessibility in ("HIGH", "MEDIUM")
    assert phi_curvature.experimental_feasibility in ("HIGH", "MEDIUM")
