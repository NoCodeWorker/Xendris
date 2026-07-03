"""Tests for v4.2 observable normalization."""

from __future__ import annotations

from phyng.observable_dataset.normalization import normalize_benchmark_rows


def test_normalized_targets_keep_predictive_gain_blocked() -> None:
    rows = [
        {
            "benchmark_id": "BM-001",
            "source_id": "SRC-1",
            "extract_id": "VRX-1",
            "observable_type": "BASELINE",
            "observable_text": "decay constant rate",
        }
    ]
    targets = normalize_benchmark_rows(rows)
    assert len(targets) == 1
    assert targets[0].predictive_gain_allowed is False
    assert targets[0].y_true_required is True


def test_visibility_maps_to_dimensionless_float() -> None:
    rows = [
        {
            "benchmark_id": "BM-002",
            "source_id": "SRC-1",
            "extract_id": "VRX-2",
            "observable_type": "OBSERVABLE",
            "observable_text": "fringe visibility contrast is observed",
        }
    ]
    targets = normalize_benchmark_rows(rows)
    assert len(targets) == 1
    t = targets[0]
    assert t.observable_class == "VISIBILITY"
    assert t.normalized_variable_name == "visibility"
    assert t.unit == "dimensionless"
    assert t.expected_dtype == "float"


def test_parameter_bounds_not_treated_as_y_true() -> None:
    rows = [
        {
            "benchmark_id": "BM-003",
            "source_id": "SRC-1",
            "extract_id": "VRX-3",
            "observable_type": "PARAMETER_CONSTRAINT",
            "observable_text": "parameter bounds lambda collapse",
        }
    ]
    targets = normalize_benchmark_rows(rows)
    assert len(targets) == 1
    t = targets[0]
    assert t.observable_class == "PARAMETER_BOUND"
    assert t.y_true_status == "Y_TRUE_NOT_OBSERVABLE_FROM_CURRENT_SOURCE"


def test_limitation_flags_not_treated_as_y_true() -> None:
    rows = [
        {
            "benchmark_id": "BM-004",
            "source_id": "SRC-1",
            "extract_id": "VRX-4",
            "observable_type": "NEGATIVE_LIMITATION",
            "observable_text": "environmental noise background limits detection",
        }
    ]
    targets = normalize_benchmark_rows(rows)
    assert len(targets) == 1
    t = targets[0]
    assert t.observable_class == "LIMITATION_FLAG"
    assert t.y_true_status == "Y_TRUE_NOT_OBSERVABLE_FROM_CURRENT_SOURCE"
