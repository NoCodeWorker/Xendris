"""Pivot decision module for v4.6 candidate freeze review."""

from __future__ import annotations

from typing import Any
from phyng.candidate_decision.schemas import PivotDecision, CandidateFamilySelectionRecord

def determine_pivot_decision(
    inputs: dict[str, Any],
    matrix_records: list[CandidateFamilySelectionRecord]
) -> PivotDecision:
    # Find the selected candidate family
    selected_family = None
    for record in matrix_records:
        if record.recommended_action == "SELECT_FOR_SOURCE_AND_YTRUE_SCREENING":
            selected_family = record.family_id
            break

    if selected_family:
        pivot_recommended = True
        next_phase = "v4.7 — Next Candidate Source/y_true Accessibility Screen"
        notes = [
            f"Selected {selected_family} as next candidate family based on non-synthetic selection criteria.",
            "PHI_GRADIENT remains archived as a method-only tool."
        ]
    else:
        pivot_recommended = False
        selected_family = None
        next_phase = "v4.7 — Research Program Pause / External Dataset Strategy"
        notes = [
            "No candidate family qualified for predictive pipeline under current selection rules."
        ]

    return PivotDecision(
        candidate_id="PHI_GRADIENT",
        decision_ref="PIVOT-DECISION-v4_6-001",
        freeze_review_status="PHI_GRADIENT_FREEZE_REVIEW_COMPLETED",
        pivot_recommended=pivot_recommended,
        next_candidate_family=selected_family,
        recommended_next_phase=next_phase,
        notes=notes,
    )
