"""Tests for v4.6 candidate freeze review logic."""

from __future__ import annotations

import pytest
from phyng.candidate_decision.freeze_review import perform_freeze_review


def test_zero_ytrue_blocks_predictive_continuation() -> None:
    inputs = {
        "freeze_decision_v4_5": {
            "accepted_y_true_count": 0,
            "freeze_status": "FROZEN_NO_YTRUE_AVAILABLE",
            "decision_id": "FREEZE-v45-001"
        },
        "next_predictive_gain_inputs_v4_5": {
            "predictive_gain_status": "UNDEFINED_INSUFFICIENT_YTRUE"
        },
        "debt_slot4": {
            "status": "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"
        }
    }
    review = perform_freeze_review(inputs)
    assert review.accepted_y_true_count == 0
    assert review.freeze_status == "FROZEN_NO_YTRUE_AVAILABLE"
    assert review.review_status == "PHI_GRADIENT_FREEZE_REVIEW_COMPLETED"


def test_freeze_review_raises_on_sufficient_ytrue() -> None:
    inputs = {
        "freeze_decision_v4_5": {
            "accepted_y_true_count": 3,
            "freeze_status": "THRESHOLD_REACHED",
            "decision_id": "FREEZE-v45-001"
        },
        "next_predictive_gain_inputs_v4_5": {
            "predictive_gain_status": "VALID"
        },
        "debt_slot4": {
            "status": "RESOLVED"
        }
    }
    with pytest.raises(ValueError, match="Cannot perform freeze review: accepted y_true count is not below threshold."):
        perform_freeze_review(inputs)
