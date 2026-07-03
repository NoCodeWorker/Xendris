"""Tests for v4.1 model prediction builder."""

from __future__ import annotations

from phyng.model_comparison.model_registry import get_registered_models
from phyng.model_comparison.prediction_builder import build_prediction_records


def test_prediction_records_mark_y_true_unavailable() -> None:
    models = get_registered_models()
    rows = [
        {
            "benchmark_id": "BM-001",
            "source_id": "SRC-TEST",
            "observable_type": "BASELINE",
            "allowed_model_comparison": True,
        }
    ]

    preds = build_prediction_records(models, rows)
    assert len(preds) == len(models) * len(rows)

    for p in preds:
        assert p.uses_real_y_true is False
        assert p.y_true_available is False
