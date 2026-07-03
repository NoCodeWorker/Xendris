"""Control failure review rules for LOG_BOUNDARY."""

from __future__ import annotations

from phyng.frontera_c_disposition.loader import REQUIRED_INPUTS
from phyng.frontera_c_disposition.schemas import ControlFailureInputs, ControlFailureReview


def build_control_failure_review(inputs: ControlFailureInputs) -> ControlFailureReview:
    decision = inputs.next_gate_decision or inputs.control_decision
    previous_status = decision.get("final_status", "UNKNOWN")
    metrics = {item.get("model_id"): item for item in inputs.error_metrics.get("metrics", [])}
    loo = {item.get("model_id"): item for item in inputs.loo_results.get("loo_results", [])}
    supporting = [
        {
            "control": "CONTROL_MONOTONIC_INTERPOLATION",
            "rmse": metrics.get("CONTROL_MONOTONIC_INTERPOLATION", {}).get("rmse"),
            "interpretation": "Generic monotonic interpolation matched the four training y_true records exactly.",
        },
        {
            "control": "CONTROL_LINEAR_POWER",
            "loo_rmse": loo.get("CONTROL_LINEAR_POWER", {}).get("loo_rmse"),
            "candidate_loo_rmse": loo.get("M_C_LOG_BOUNDARY", {}).get("loo_rmse"),
            "interpretation": "Linear leave-one-out error was lower than M_C_LOG_BOUNDARY.",
        },
    ]
    return ControlFailureReview(
        candidate_family="LOG_BOUNDARY",
        previous_status=previous_status,
        positive_smoke_test_ref=str(REQUIRED_INPUTS["predictive_gain_smoke_test"]),
        negative_control_ref=str(REQUIRED_INPUTS["next_gate_decision"]),
        failure_summary=decision.get("exact_blocker")
        or "LOG_BOUNDARY positive smoke-test gain failed negative controls.",
        primary_failure_reason="GAIN_EXPLAINED_BY_SIMPLE_CONTROL",
        supporting_control_results=supporting,
        can_proceed_to_c_structure_ablation=False,
        can_support_frontera_c_validation=False,
        notes=[
            "Do not rescue LOG_BOUNDARY with C-structure ablation.",
            "Control failure blocks validation use.",
            "No PredictiveGain was recomputed in v5.6.",
        ],
    )
