"""Tests for v3.9 benchmark alignment."""

from __future__ import annotations

from phyng.source_pressure_decision.benchmark_alignment import assess_benchmark_alignment
from phyng.source_pressure_decision.pressure_classifier import classify_extract

from tests.test_source_pressure_loader_v3_9 import _extract


def test_no_benchmark_extracts() -> None:
    extracts = [
        _extract("VRX-001", "SRC-TEST", "abc", "SLOT_1_DECOHERENCE_BASELINE",
                 "DECOHERENCE_BASELINE", "BASELINE_CANDIDATE",
                 "The experiment reports thermal decoherence as the primary loss mechanism."),
    ]
    records = [classify_extract(ext, {}) for ext in extracts]

    alignment = assess_benchmark_alignment(records)

    assert alignment.benchmark_decision == "NO_BENCHMARK_EXTRACTS"
    assert len(alignment.benchmark_extracts) == 0


def test_benchmark_with_range_data() -> None:
    extracts = [
        _extract("VRX-001", "SRC-TEST", "abc", "SLOT_3_BENCHMARK_RANGES",
                 "BENCHMARK_RANGE", "BENCHMARK_CANDIDATE",
                 "The mass range of 500-2000 amu at temperatures below 1000 K and pressure of 1e-8 mbar defines the benchmark regime."),
        _extract("VRX-002", "SRC-TEST2", "def", "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE",
                 "VISIBILITY_COHERENCE_OBSERVABLE", "SUPPORT_CANDIDATE",
                 "Interference visibility was measured at 42 percent coherence loss."),
    ]
    records = [classify_extract(ext, {}) for ext in extracts]

    alignment = assess_benchmark_alignment(records)

    assert alignment.benchmark_decision != "NO_BENCHMARK_EXTRACTS"
    assert len(alignment.benchmark_extracts) >= 1
    assert any("Benchmark relevance does not validate physics." in lim for lim in alignment.limitations)
