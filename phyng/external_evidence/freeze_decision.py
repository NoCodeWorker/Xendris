"""Freeze decision logic for v4.5."""

from __future__ import annotations

from phyng.external_evidence.schemas import CandidateFreezeDecision, AssembledYTrueDatasetv45


def evaluate_freeze_decision(
    assembled: AssembledYTrueDatasetv45,
) -> CandidateFreezeDecision:
    total_y_true = assembled.total_y_true_count
    threshold = assembled.minimum_viable_y_true_count

    allowed_future_work = [
        "new experiment design",
        "public dataset discovery",
        "source acquisition",
        "manual extraction with new locations",
        "SLOT_4 resolution",
        "candidate redesign",
        "kill/pivot analysis",
    ]
    blocked_future_work = [
        "PredictiveGain claim",
        "validation claim",
        "physical claim",
        "gradient mechanism claim",
        "new benchmark-only score inflation",
    ]

    if total_y_true >= threshold:
        return CandidateFreezeDecision(
            decision_id="FREEZE-DECISION-v4_5-001",
            accepted_y_true_count=total_y_true,
            minimum_viable_y_true_count=threshold,
            ready_for_predictive_gain=True,
            freeze_status="NOT_FROZEN_THRESHOLD_REACHED",
            freeze_reason=None,
            allowed_future_work=allowed_future_work,
            blocked_future_work=blocked_future_work,
            required_to_unfreeze=[],
            recommended_next_phase="v4.6 — PredictiveGain Smoke Test & Error Comparison",
        )
    else:
        # Check if any unresolved acquisition paths exist. Since there are no local supplementary or external datasets,
        # we freeze due to no y_true available.
        return CandidateFreezeDecision(
            decision_id="FREEZE-DECISION-v4_5-001",
            accepted_y_true_count=total_y_true,
            minimum_viable_y_true_count=threshold,
            ready_for_predictive_gain=False,
            freeze_status="FROZEN_NO_YTRUE_AVAILABLE",
            freeze_reason="No observed y_true records could be validated from Table Review, Supplementary Search, or Public Dataset Search.",
            allowed_future_work=allowed_future_work,
            blocked_future_work=blocked_future_work,
            required_to_unfreeze=[
                "Acquire at least 3 validated observed y_true records from physical literature.",
                "Verify location and numeric outcomes for visibility and decoherence rate observables.",
            ],
            recommended_next_phase="v4.6 — Candidate Freeze Review & Experiment Design Decision",
        )
