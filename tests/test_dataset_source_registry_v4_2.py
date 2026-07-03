"""Tests for v4.2 dataset source registry."""

from __future__ import annotations

from phyng.observable_dataset.dataset_registry import build_dataset_source_registry
from phyng.observable_dataset.normalization import normalize_benchmark_rows


def test_dataset_source_registry_created() -> None:
    rows = [
        {
            "benchmark_id": "BM-001",
            "source_id": "SRC-UNIQUE-1",
            "extract_id": "VRX-1",
            "observable_type": "BASELINE",
            "observable_text": "thermal decay rate",
        },
        {
            "benchmark_id": "BM-002",
            "source_id": "SRC-UNIQUE-1",
            "extract_id": "VRX-2",
            "observable_type": "OBSERVABLE",
            "observable_text": "measured visibility fringe contrast",
        },
    ]

    targets = normalize_benchmark_rows(rows)
    registry = build_dataset_source_registry(targets)

    # Should group same source_id into 1 registry record
    assert len(registry) == 1
    assert registry[0].related_source_id == "SRC-UNIQUE-1"
    assert "DECOHERENCE_RATE" in registry[0].expected_observables
    assert "VISIBILITY" in registry[0].expected_observables
