"""
Tests v1.7 — Prediction Accuracy: Filter Lift
"""

import pytest
from phyng.prediction_accuracy.schemas import PredictionRecord, PredictionOutcome
from phyng.prediction_accuracy.ledger import evaluate_filter_lift


def test_filter_lift_insufficient_outcomes():
    # Need at least 5 resolved outcomes
    records = [
        PredictionRecord(prediction_id="P1", prediction_text="t1", target_variable="v", ladder_level="DREAM")
    ]
    outcomes = [
        PredictionOutcome(prediction_id="P1", resolved=True, success=True)
    ]
    report = evaluate_filter_lift(records, outcomes)
    assert report.filter_status == "INSUFFICIENT_OUTCOMES"


def test_filter_lift_detects_no_predictive_lift():
    # 6 resolved outcomes, passed predictions are less accurate than baseline (0.50)
    records = [
        PredictionRecord(prediction_id="P1", prediction_text="t1", target_variable="v", ladder_level="BENCHMARK_SUPPORTED"),
        PredictionRecord(prediction_id="P2", prediction_text="t2", target_variable="v", ladder_level="BENCHMARK_SUPPORTED"),
        PredictionRecord(prediction_id="P3", prediction_text="t3", target_variable="v", ladder_level="BENCHMARK_SUPPORTED"),
        PredictionRecord(prediction_id="P4", prediction_text="t4", target_variable="v", ladder_level="DREAM"),
        PredictionRecord(prediction_id="P5", prediction_text="t5", target_variable="v", ladder_level="DREAM"),
        PredictionRecord(prediction_id="P6", prediction_text="t6", target_variable="v", ladder_level="DREAM"),
    ]
    # Passed: 1 success, 2 failures -> 33%
    # Low level: 2 success, 1 failure -> 66%
    outcomes = [
        PredictionOutcome(prediction_id="P1", resolved=True, success=True),
        PredictionOutcome(prediction_id="P2", resolved=True, success=False),
        PredictionOutcome(prediction_id="P3", resolved=True, success=False),
        PredictionOutcome(prediction_id="P4", resolved=True, success=True),
        PredictionOutcome(prediction_id="P5", resolved=True, success=True),
        PredictionOutcome(prediction_id="P6", resolved=True, success=False),
    ]

    report = evaluate_filter_lift(records, outcomes, base_rate=0.5)
    assert report.filter_status in ("FILTER_NOT_PREDICTIVELY_USEFUL_YET", "LADDER_NOT_PREDICTIVELY_ORDERED")
