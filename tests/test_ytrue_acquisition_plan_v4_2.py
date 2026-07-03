"""Tests for v4.2 y_true acquisition plan."""

from __future__ import annotations

from phyng.observable_dataset.normalization import normalize_benchmark_rows
from phyng.observable_dataset.ytrue_acquisition import build_acquisition_plan


def test_no_y_true_available_without_numeric_observed_values() -> None:
    rows = [
        {
            "benchmark_id": "BM-001",
            "source_id": "SRC-1",
            "extract_id": "VRX-1",
            "observable_type": "BASELINE",
            "observable_text": "thermal emission rate",
        }
    ]

    targets = normalize_benchmark_rows(rows)
    plan = build_acquisition_plan(targets)

    assert len(plan) == 1
    assert plan[0].y_true_status != "Y_TRUE_AVAILABLE"
    # It must be manual extraction or other acquirable status
    assert plan[0].y_true_status == "Y_TRUE_ACQUIRABLE_MANUAL_EXTRACTION"
