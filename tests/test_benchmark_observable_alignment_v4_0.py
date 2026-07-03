"""Tests for v4.0 benchmark observable alignment."""

from __future__ import annotations

from phyng.benchmark_construction.observable_alignment import align_observables


def test_observable_alignment_uses_survived_slots_only() -> None:
    records = [
        {
            "extract_id": "VRX-001",
            "assigned_slot": "SLOT_1_DECOHERENCE_BASELINE",
            "pressure_class": "SUPPORTS_BASELINE_ONLY",
            "exact_text": "thermal emission baseline",
        },
        {
            "extract_id": "VRX-002",
            "assigned_slot": "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS",
            "pressure_class": "SUPPORTS_GRADIENT_COMPONENT",
            "exact_text": "gradient dynamics",
        },
        {
            "extract_id": "VRX-003",
            "assigned_slot": "SLOT_3_BENCHMARK_RANGES",
            "pressure_class": "ANALOGY_ONLY",
            "exact_text": "analogy context",
        },
    ]

    alignments = align_observables(records)

    # Should only keep SLOT_1 extract since SLOT_4 is skipped, and ANALOGY_ONLY is skipped.
    assert len(alignments) == 1
    assert alignments[0].extract_id == "VRX-001"
    assert alignments[0].observable == "Decoherence rate / baseline loss"
    assert alignments[0].alignment_status == "OBSERVABLE_ALIGNED_FOR_BENCHMARK"
