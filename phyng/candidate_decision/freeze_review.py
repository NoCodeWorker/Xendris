"""Freeze review module for v4.6 candidate freeze review."""

from __future__ import annotations

from typing import Any
from phyng.candidate_decision.schemas import CandidateFreezeReview

def perform_freeze_review(inputs: dict[str, Any]) -> CandidateFreezeReview:
    freeze_dec = inputs["freeze_decision_v4_5"]
    pred_inputs = inputs["next_predictive_gain_inputs_v4_5"]
    debt_slot4 = inputs["debt_slot4"]

    accepted_y_true = freeze_dec.get("accepted_y_true_count", 0)
    freeze_status = freeze_dec.get("freeze_status", "FROZEN_NO_YTRUE_AVAILABLE")
    predictive_gain_status = pred_inputs.get("predictive_gain_status", "UNDEFINED_INSUFFICIENT_YTRUE")
    slot4_debt_status = debt_slot4.get("status", "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS")

    notes = [
        f"Freeze decision ID: {freeze_dec.get('decision_id')}",
        f"Reason for freeze: {freeze_dec.get('freeze_reason')}",
    ]

    # Validate conditions from freeze decision
    if accepted_y_true >= 3:
        raise ValueError("Cannot perform freeze review: accepted y_true count is not below threshold.")

    return CandidateFreezeReview(
        candidate_id="PHI_GRADIENT",
        freeze_decision_ref=freeze_dec.get("decision_id", "UNKNOWN"),
        freeze_status=freeze_status,
        accepted_y_true_count=accepted_y_true,
        predictive_gain_status=predictive_gain_status,
        slot4_debt_status=slot4_debt_status,
        review_status="PHI_GRADIENT_FREEZE_REVIEW_COMPLETED",
        notes=notes,
    )
