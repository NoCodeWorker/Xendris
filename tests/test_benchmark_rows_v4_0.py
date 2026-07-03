"""Tests for v4.0 benchmark rows."""

from __future__ import annotations

from phyng.benchmark_construction.benchmark_rows import build_benchmark_rows


def test_benchmark_row_blocks_gradient_claim() -> None:
    records = [
        {
            "extract_id": "VRX-001",
            "assigned_slot": "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE",
            "pressure_class": "SUPPORTS_OBSERVABLE_ONLY",
            "exact_text": "measured visibility range",
        }
    ]
    rows = build_benchmark_rows(records)
    assert len(rows) == 1
    assert rows[0].gradient_claim_allowed is False


def test_benchmark_row_allows_model_comparison_only_with_observable() -> None:
    records = [
        {
            "extract_id": "VRX-001",
            "assigned_slot": "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE",
            "pressure_class": "SUPPORTS_OBSERVABLE_ONLY",
            "exact_text": "measured visibility range",
        },
        {
            "extract_id": "VRX-002",
            "assigned_slot": "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS",
            "pressure_class": "LIMITS_COMPONENT",
            "exact_text": "environmental noise dominates",
        },
    ]

    rows = build_benchmark_rows(records)
    assert len(rows) == 2

    row_slot2 = next(r for r in rows if r.extract_id == "VRX-001")
    row_slot6 = next(r for r in rows if r.extract_id == "VRX-002")

    # Observable/regime slot allows model comparison
    assert row_slot2.allowed_model_comparison is True

    # Limitation slot does not allow model comparison directly
    assert row_slot6.allowed_model_comparison is False
