"""Tests for v4.1 negative controls evaluation."""

from __future__ import annotations

from phyng.model_comparison.negative_controls import evaluate_negative_controls


def test_no_slot4_control_is_present_and_inconclusive() -> None:
    plan = {
        "controls": [
            {
                "control_id": "CTRL-001",
                "control_type": "NO_SLOT4_CONTROL",
                "expected_result_if_PHIGRADIENT_is_only_analogy": "baseline decay",
                "expected_result_if_candidate_has_signal": "active decay",
            }
        ]
    }

    results = evaluate_negative_controls(plan)

    assert len(results) == 1
    assert results[0].control_type == "NO_SLOT4_CONTROL"

    # All evaluations must be inconclusive without y_true
    assert results[0].survival_status == "CONTROL_INCONCLUSIVE"
    assert results[0].observed_result == "CONTROL_INCONCLUSIVE"
    assert results[0].claim_impact == "CLAIM_BLOCKED_BY_SLOT4_DEBT"
