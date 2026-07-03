"""Tests for v4.1 model scoring."""

from __future__ import annotations

from phyng.model_comparison.model_registry import get_registered_models
from phyng.model_comparison.scoring import compute_comparison_scores


def test_predictive_gain_undefined_without_y_true() -> None:
    models = get_registered_models()
    rows = [{"benchmark_id": "BM-001"}]

    scores = compute_comparison_scores(models, rows)

    assert len(scores) == len(models)
    for s in scores:
        assert s.predictive_gain is None
        assert s.predictive_gain_status == "UNDEFINED_NO_REAL_Y_TRUE"
