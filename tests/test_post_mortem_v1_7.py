"""
Tests v1.7 — Prediction Accuracy: Post-Mortem
"""

import pytest
from phyng.prediction_accuracy.schemas import PredictionRecord, PredictionOutcome
from phyng.prediction_accuracy.post_mortem import generate_prediction_post_mortem


def test_post_mortem_generated():
    records = [
        PredictionRecord(
            prediction_id="PRED-PM-001",
            prediction_text="Visibility loss beats baseline",
            target_variable="decay",
            ladder_level="BENCHMARK_SUPPORTED",
            baseline_reference="exp(-0.05*t)",
        )
    ]
    outcomes = [
        PredictionOutcome(
            prediction_id="PRED-PM-001",
            resolved=True,
            actual_value=0.08,
            actual_direction="UP",
            success=True,
            benchmark_value=0.05,
            benchmark_success=True,
            notes="Decay was indeed faster.",
        )
    ]

    pm = generate_prediction_post_mortem("PRED-PM-001", records, outcomes)
    assert pm.prediction_id == "PRED-PM-001"
    assert pm.verdict == "CORRECT_BEATS_BASELINE"
    assert pm.baseline_beaten is True
    assert any("evidence" in e.lower() or "benchmark" in e.lower() for e in pm.evidence_that_mattered)
    assert len(pm.recommended_changes) > 0
