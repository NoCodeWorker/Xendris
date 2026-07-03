"""Tests for v3.9 pressure classifier."""

from __future__ import annotations

from phyng.source_pressure_decision.pressure_classifier import classify_extract

from tests.test_source_pressure_loader_v3_9 import _extract


def test_extract_classified_as_baseline_only() -> None:
    ext = _extract("VRX-001", "SRC-TEST", "abc123", "SLOT_1_DECOHERENCE_BASELINE",
                   "DECOHERENCE_BASELINE", "BASELINE_CANDIDATE",
                   "The experiment reports thermal decoherence as the primary loss of coherence mechanism.")
    record = classify_extract(ext, {"hashes": []})

    assert record.pressure_class == "SUPPORTS_BASELINE_ONLY"
    assert record.can_support_claim is True
    assert record.can_contradict_claim is False


def test_extract_classified_as_observable_only() -> None:
    ext = _extract("VRX-002", "SRC-TEST", "abc123", "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE",
                   "VISIBILITY_COHERENCE_OBSERVABLE", "SUPPORT_CANDIDATE",
                   "Interference visibility was measured at 42 percent loss under environmental decoherence conditions.")
    record = classify_extract(ext, {"hashes": []})

    assert record.pressure_class == "SUPPORTS_OBSERVABLE_ONLY"
    assert record.can_support_claim is True


def test_extract_classified_as_benchmark_alignment() -> None:
    ext = _extract("VRX-003", "SRC-TEST", "abc123", "SLOT_3_BENCHMARK_RANGES",
                   "BENCHMARK_RANGE", "BENCHMARK_CANDIDATE",
                   "The mass range of 500-2000 amu at temperatures below 1000 K defines the benchmark regime.")
    record = classify_extract(ext, {"hashes": []})

    assert record.pressure_class == "SUPPORTS_BENCHMARK_ALIGNMENT"


def test_extract_classified_as_parameter_constraint() -> None:
    ext = _extract("VRX-004", "SRC-TEST", "abc123", "SLOT_5_PARAMETER_CONSTRAINTS",
                   "PARAMETER_CONSTRAINT", "PARAMETER_CONSTRAINT_CANDIDATE",
                   "CSL collapse model bounds constrain lambda to less than 1e-8 and r_c hypothesis testing.")
    record = classify_extract(ext, {"hashes": []})

    assert record.pressure_class == "SUPPORTS_PARAMETER_CONSTRAINT"


def test_analogy_only_extract_does_not_grant_support() -> None:
    ext = _extract("VRX-005", "SRC-TEST", "abc123", "SLOT_3_BENCHMARK_RANGES",
                   "ANALOGY_ONLY", "ANALOGY_ONLY",
                   "General decoherence context that does not directly support PHI_GRADIENT.")
    record = classify_extract(ext, {"hashes": []})

    assert record.pressure_class == "ANALOGY_ONLY"
    assert record.can_support_claim is False
    assert record.can_contradict_claim is False


def test_negative_or_limitation_extract_can_dominate_support() -> None:
    ext = _extract("VRX-006", "SRC-TEST", "abc123", "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS",
                   "NEGATIVE_CONSTRAINT_LIMITATION", "CONTRADICTION_CANDIDATE",
                   "Environmental noise dominates over any candidate gradient effect making it incompatible with the observed regime.")
    record = classify_extract(ext, {"hashes": []})

    assert record.pressure_class == "CONTRADICTS_COMPONENT"
    assert record.can_contradict_claim is True
    assert record.pressure_score < 0
