"""Evaluate negative controls for v4.1 model comparison."""

from __future__ import annotations

from phyng.model_comparison.schemas import NegativeControlResult


def evaluate_negative_controls(control_plan: dict) -> list[NegativeControlResult]:
    """Evaluate controls in the plan. All results are inconclusive due to missing y_true."""
    results: list[NegativeControlResult] = []

    controls = control_plan.get("controls", [])
    for c in controls:
        ctype = c.get("control_type", "")
        cid = c.get("control_id", "")

        # Default inconclusive values due to lack of real observed y_true
        observed = "CONTROL_INCONCLUSIVE"
        status = "CONTROL_INCONCLUSIVE"
        reason = "Real-world observed y_true data is unavailable to evaluate the control."
        impact = "CONTROL_INCONCLUSIVE_NO_OBSERVED_DATA"

        if ctype == "NO_SLOT4_CONTROL":
            # NO_SLOT4_CONTROL is inconclusive without y_true
            impact = "CLAIM_BLOCKED_BY_SLOT4_DEBT"

        results.append(
            NegativeControlResult(
                control_id=cid,
                control_type=ctype,
                tested_models=["M_base", "M_candidate_debt_bounded", "M_negative_control_no_slot4"],
                expected_result_if_candidate_is_only_analogy=c.get("expected_result_if_PHIGRADIENT_is_only_analogy", ""),
                expected_result_if_candidate_has_signal=c.get("expected_result_if_candidate_has_signal", ""),
                observed_result=observed,
                survival_status=status,
                failure_reason=reason,
                claim_impact=impact,
            )
        )

    return results
