"""Tests for v3.9 decision engine."""

from __future__ import annotations

from phyng.source_pressure_decision.benchmark_alignment import assess_benchmark_alignment
from phyng.source_pressure_decision.contradiction_map import build_contradiction_map
from phyng.source_pressure_decision.decision_engine import compute_decision
from phyng.source_pressure_decision.pressure_classifier import classify_extract
from phyng.source_pressure_decision.slot_pressure import compute_slot_pressure

from tests.test_source_pressure_loader_v3_9 import _extract


def _run_decision(extracts: list[dict]):
    records = [classify_extract(ext, {}) for ext in extracts]
    slots = compute_slot_pressure(records)
    benchmark = assess_benchmark_alignment(records)
    contradiction = build_contradiction_map(records)
    return compute_decision(records, slots, benchmark, contradiction)


def test_no_slot4_extract_blocks_gradient_component_support() -> None:
    """Critical rule: No SLOT_4 → gradient_component_support = false."""
    extracts = [
        _extract("VRX-001", "SRC-TEST", "abc", "SLOT_1_DECOHERENCE_BASELINE",
                 "DECOHERENCE_BASELINE", "BASELINE_CANDIDATE",
                 "The experiment reports thermal decoherence as the primary loss of coherence mechanism."),
        _extract("VRX-002", "SRC-TEST2", "def", "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE",
                 "VISIBILITY_COHERENCE_OBSERVABLE", "SUPPORT_CANDIDATE",
                 "Interference visibility was measured at 42 percent loss under environmental decoherence conditions."),
    ]
    decision = _run_decision(extracts)

    assert decision.gradient_component_support is False
    assert "The current extract pack does not support the gradient-component mechanism." in decision.allowed_claims


def test_decision_engine_allows_contradiction() -> None:
    """A contradiction extract must be able to dominate support."""
    extracts = [
        _extract("VRX-001", "SRC-TEST", "abc", "SLOT_1_DECOHERENCE_BASELINE",
                 "DECOHERENCE_BASELINE", "BASELINE_CANDIDATE",
                 "The experiment reports thermal decoherence as the primary loss mechanism."),
        _extract("VRX-002", "SRC-NEGATIVE", "neg", "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS",
                 "NEGATIVE_CONSTRAINT_LIMITATION", "CONTRADICTION_CANDIDATE",
                 "Environmental noise dominates over any candidate gradient effect making it incompatible with the observed regime."),
    ]
    decision = _run_decision(extracts)

    assert "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED" in decision.global_decisions


def test_analogy_only_extract_does_not_grant_support() -> None:
    extracts = [
        _extract("VRX-001", "SRC-TEST", "abc", "SLOT_3_BENCHMARK_RANGES",
                 "ANALOGY_ONLY", "ANALOGY_ONLY",
                 "General decoherence context that does not directly support PHI_GRADIENT."),
    ]
    decision = _run_decision(extracts)

    assert "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED" not in decision.global_decisions
    assert decision.gradient_component_support is False


def test_physical_claims_remain_blocked() -> None:
    extracts = [
        _extract("VRX-001", "SRC-TEST", "abc", "SLOT_1_DECOHERENCE_BASELINE",
                 "DECOHERENCE_BASELINE", "BASELINE_CANDIDATE",
                 "The experiment reports thermal decoherence as the primary loss mechanism."),
    ]
    decision = _run_decision(extracts)

    assert decision.physical_claim_permission == "BLOCKED"
    assert "PHI_GRADIENT is physically validated." in decision.blocked_claims
    assert "Frontera C is validated." in decision.blocked_claims
    assert "Source pressure validates PHI_GRADIENT." in decision.blocked_claims


def test_with_slot4_support_enables_gradient_component() -> None:
    extracts = [
        _extract("VRX-001", "SRC-TEST", "abc", "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS",
                 "GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS", "SUPPORT_CANDIDATE",
                 "The gradient of the motional Hamiltonian governs spin-motion coupling in the transition effective dynamics regime."),
    ]
    decision = _run_decision(extracts)

    assert decision.gradient_component_support is True
