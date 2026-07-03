"""Tests for v4.2 measurement readiness matrix and quality control rules."""

from __future__ import annotations

from phyng.observable_dataset.normalization import normalize_benchmark_rows
from phyng.observable_dataset.quality_control import get_quality_control_rules
from phyng.observable_dataset.readiness import evaluate_readiness


def test_measurement_readiness_matrix_created() -> None:
    rows = [
        {
            "benchmark_id": "BM-001",
            "source_id": "SRC-1",
            "extract_id": "VRX-1",
            "observable_type": "BASELINE",
            "observable_text": "thermal decay rate",
        }
    ]

    targets = normalize_benchmark_rows(rows)
    matrix = evaluate_readiness(targets)

    assert len(matrix) == 11
    # Check that DECOHERENCE_RATE is not blocked
    decoher = next(m for m in matrix if m.observable_class == "DECOHERENCE_RATE")
    assert decoher.target_count == 1
    assert decoher.readiness_status == "MANUAL_EXTRACTION_REQUIRED"


def test_quality_control_requires_hash_traceability() -> None:
    qc = get_quality_control_rules()
    assert "source hash traceability required" in qc.rules
    assert "unit normalization required" in qc.rules


def test_slot4_debt_remains_open_blocking() -> None:
    rows = [
        {
            "benchmark_id": "BM-001",
            "source_id": "SRC-1",
            "extract_id": "VRX-1",
            "observable_type": "BASELINE",
            "observable_text": "thermal decay rate",
        }
    ]
    targets = normalize_benchmark_rows(rows)
    assert len(targets) == 1
    assert targets[0].slot4_debt_status == "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"
