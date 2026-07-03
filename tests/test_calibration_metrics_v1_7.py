"""
Tests v1.7 — Prediction Accuracy: Calibration & Metrics
"""

import pytest
import math
from phyng.prediction_accuracy.schemas import PredictionRecord, PredictionOutcome
from phyng.prediction_accuracy.metrics import compute_prediction_metrics
from phyng.prediction_accuracy.calibration import (
    compute_brier_score,
    compute_expected_calibration_error,
    evaluate_calibration,
)


def test_hit_rate_computation():
    records = [
        PredictionRecord(prediction_id="P1", prediction_text="t1", target_variable="v1"),
        PredictionRecord(prediction_id="P2", prediction_text="t2", target_variable="v2"),
        PredictionRecord(prediction_id="P3", prediction_text="t3", target_variable="v3"),
    ]
    outcomes = [
        PredictionOutcome(prediction_id="P1", resolved=True, success=True),
        PredictionOutcome(prediction_id="P2", resolved=True, success=False),
        PredictionOutcome(prediction_id="P3", resolved=True, success=True),
    ]

    metrics = compute_prediction_metrics(records, outcomes, base_rate=0.5)
    assert metrics.n_resolved == 3
    assert metrics.n_correct == 2
    assert metrics.n_incorrect == 1
    assert metrics.hit_rate == pytest.approx(2 / 3)
    assert metrics.accuracy_lift == pytest.approx(2 / 3 - 0.5)


def test_brier_score_computation():
    # 3 predictions with probabilities, outcomes: Correct (1), Incorrect (0), Correct (1)
    probs = [0.90, 0.10, 0.80]
    outcomes_binary = [1, 0, 1]

    # Brier Score = ((0.9-1)^2 + (0.1-0)^2 + (0.8-1)^2) / 3
    #              = (0.01 + 0.01 + 0.04) / 3 = 0.06 / 3 = 0.02
    score = compute_brier_score(probs, outcomes_binary)
    assert score == pytest.approx(0.02)


def test_expected_calibration_error():
    probs = [0.90, 0.10, 0.80, 0.30, 0.40]
    outcomes_binary = [1, 0, 1, 0, 0]
    ece = compute_expected_calibration_error(probs, outcomes_binary, n_bins=5)
    assert 0.0 <= ece <= 1.0


def test_evaluate_calibration_insufficient():
    # Less than 5 resolved predictions with probability
    records = [PredictionRecord(prediction_id="P1", prediction_text="t", target_variable="v", predicted_probability=0.9)]
    outcomes = [PredictionOutcome(prediction_id="P1", resolved=True, success=True)]
    report = evaluate_calibration(records, outcomes)
    assert report.calibration_status == "INSUFFICIENT_DATA"


def test_evaluate_calibration_well_calibrated():
    records = [
        PredictionRecord(prediction_id="P1", prediction_text="t1", target_variable="v", predicted_probability=0.90),
        PredictionRecord(prediction_id="P2", prediction_text="t2", target_variable="v", predicted_probability=0.10),
        PredictionRecord(prediction_id="P3", prediction_text="t3", target_variable="v", predicted_probability=0.80),
        PredictionRecord(prediction_id="P4", prediction_text="t4", target_variable="v", predicted_probability=0.20),
        PredictionRecord(prediction_id="P5", prediction_text="t5", target_variable="v", predicted_probability=0.50),
    ]
    outcomes = [
        PredictionOutcome(prediction_id="P1", resolved=True, success=True),
        PredictionOutcome(prediction_id="P2", resolved=True, success=False),
        PredictionOutcome(prediction_id="P3", resolved=True, success=True),
        PredictionOutcome(prediction_id="P4", resolved=True, success=False),
        PredictionOutcome(prediction_id="P5", resolved=True, success=True),
    ]
    report = evaluate_calibration(records, outcomes)
    assert report.n_predictions_with_probability == 5
    assert report.calibration_status in ("WELL_CALIBRATED", "OVERCONFIDENT_GATE", "UNDERCONFIDENT_GATE")
