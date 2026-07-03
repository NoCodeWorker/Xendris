"""Tests for v3.9 slot pressure summary."""

from __future__ import annotations

from phyng.source_pressure_decision.pressure_classifier import classify_extract
from phyng.source_pressure_decision.slot_pressure import compute_slot_pressure

from tests.test_source_pressure_loader_v3_9 import _extract


def test_no_slot4_extract_blocks_gradient_component_support() -> None:
    """If no SLOT_4 extract exists, the slot summary should show SLOT_NO_VALID_EXTRACTS for SLOT_4."""
    extracts = [
        _extract("VRX-001", "SRC-TEST", "abc", "SLOT_1_DECOHERENCE_BASELINE",
                 "DECOHERENCE_BASELINE", "BASELINE_CANDIDATE",
                 "The experiment reports thermal decoherence as the primary loss mechanism."),
    ]
    records = [classify_extract(ext, {}) for ext in extracts]

    summaries = compute_slot_pressure(records)

    slot4 = next(s for s in summaries if s.slot_id == "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS")
    assert slot4.pressure_status == "SLOT_NO_VALID_EXTRACTS"
    assert slot4.extract_count == 0


def test_slot_with_support_extracts() -> None:
    extracts = [
        _extract("VRX-001", "SRC-TEST", "abc", "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE",
                 "VISIBILITY_COHERENCE_OBSERVABLE", "SUPPORT_CANDIDATE",
                 "Interference visibility was measured at 42 percent loss under environmental decoherence conditions."),
    ]
    records = [classify_extract(ext, {}) for ext in extracts]

    summaries = compute_slot_pressure(records)

    slot2 = next(s for s in summaries if s.slot_id == "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE")
    assert slot2.pressure_status == "SLOT_SOURCE_BACKED_LIMITED"
    assert slot2.support_count == 1


def test_benchmark_relevant_does_not_validate_physics() -> None:
    """Benchmark relevance in slot summary does not validate physics."""
    extracts = [
        _extract("VRX-001", "SRC-TEST", "abc", "SLOT_3_BENCHMARK_RANGES",
                 "BENCHMARK_RANGE", "BENCHMARK_CANDIDATE",
                 "The mass range of 500-2000 amu at temperatures below 1000 K defines the benchmark regime."),
    ]
    records = [classify_extract(ext, {}) for ext in extracts]

    summaries = compute_slot_pressure(records)

    slot3 = next(s for s in summaries if s.slot_id == "SLOT_3_BENCHMARK_RANGES")
    assert slot3.pressure_status in ("SLOT_SOURCE_BACKED_LIMITED", "SLOT_BENCHMARK_RELEVANT")
    # The slot summary structure never grants physical validation
    assert "validate" not in slot3.summary.lower()
