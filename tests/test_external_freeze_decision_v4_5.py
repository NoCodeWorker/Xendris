"""Tests for candidate freeze decision rules."""

from __future__ import annotations

from phyng.external_evidence.schemas import AssembledYTrueDatasetv45
from phyng.external_evidence.freeze_decision import evaluate_freeze_decision


def test_insufficient_ytrue_freezes_candidate() -> None:
    assembled = AssembledYTrueDatasetv45(
        dataset_id="DS-1",
        created_at="2026-07-01",
        previous_dataset_ref=None,
        external_evidence_ref=None,
        previous_y_true_count=0,
        new_y_true_count=0,
        total_y_true_count=1,  # Under threshold
        records=[],
        ready_for_predictive_gain=False,
        predictive_gain_status="UNDEFINED_INSUFFICIENT_YTRUE",
        minimum_viable_y_true_count=3,
        matched_prediction_count=1,
        slot4_debt_status="OPEN_BLOCKING_FOR_GRADIENT_CLAIMS",
        physical_claim_permission="BLOCKED",
        notes=[],
    )

    decision = evaluate_freeze_decision(assembled)
    assert decision.freeze_status == "FROZEN_NO_YTRUE_AVAILABLE"
    assert decision.ready_for_predictive_gain is False
    assert "kill/pivot analysis" in decision.allowed_future_work
    assert "gradient mechanism claim" in decision.blocked_future_work
