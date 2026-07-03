"""
Tests v1.7 — Prediction Accuracy: Ledger
"""

import pytest
from phyng.prediction_accuracy.schemas import PredictionRecord, PredictionOutcome
from phyng.prediction_accuracy.ledger import record_prediction, resolve_prediction


def test_prediction_record_and_resolution():
    ledger: list[PredictionRecord] = []
    outcomes: list[PredictionOutcome] = []

    # Record
    r = PredictionRecord(
        prediction_text="Bitcoin reaches 100k",
        target_variable="BTC-USD",
        predicted_value=100000.0,
        ladder_level="HYPOTHESIS_SEED",
    )
    record_prediction(r, ledger)
    assert len(ledger) == 1
    assert ledger[0].prediction_id == r.prediction_id

    # Resolve
    resolve_prediction(
        prediction_id=r.prediction_id,
        ledger=ledger,
        outcomes=outcomes,
        actual_value=105000.0,
        actual_direction="UP",
        success=True,
        benchmark_value=98000.0,
        notes="Succeeded and beat baseline",
    )

    assert len(outcomes) == 1
    assert outcomes[0].prediction_id == r.prediction_id
    assert outcomes[0].resolved is True
    assert outcomes[0].success is True
    assert outcomes[0].error_value == 5000.0
    assert outcomes[0].benchmark_success is True
