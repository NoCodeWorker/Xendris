"""
Tests v1.6 — Hypothesis Incubation

Tests:
    test_incubation_returns_next_steps
    test_incubation_allows_private_recording
    test_incubation_blocks_publication_claim
    test_incubation_result_has_required_fields
    test_incubation_seed_forbidden_claims_propagate
"""

import pytest
from typing import cast
from phyng.epistemic_modes.schemas import HypothesisSeed, LadderLevel
from phyng.epistemic_modes.incubation import incubate_hypothesis


def make_seed(level="HYPOTHESIS_SEED", observable=None):
    return HypothesisSeed(
        seed_id="TEST-SEED-001",
        title="Test hypothesis",
        intuition="Maybe X causes Y.",
        domain="physics",
        possible_observable=observable,
        current_level=cast(LadderLevel, level),
        risk_level="RISK_1_INTERNAL_NOTE",
        known_unknowns=["unknown coupling constant"],
        next_formalization_steps=["Define observable."],
        forbidden_claims=["This is validated."],
    )


def test_incubation_returns_next_steps():
    """IncubationResult must include non-empty next_formalization_steps."""
    seed = make_seed()
    result = incubate_hypothesis(seed)
    assert isinstance(result.next_formalization_steps, list)
    assert len(result.next_formalization_steps) > 0


def test_incubation_allows_private_recording():
    """Incubation must allow recording intuition."""
    seed = make_seed()
    result = incubate_hypothesis(seed)
    assert any("intuition" in a.lower() or "record" in a.lower() for a in result.allowed_use)


def test_incubation_blocks_publication_claim():
    """Incubation must block publication claim."""
    seed = make_seed()
    result = incubate_hypothesis(seed)
    assert any("publication" in b.lower() or "claim" in b.lower() for b in result.blocked_use)


def test_incubation_result_has_required_fields():
    """All required fields must be present."""
    seed = make_seed()
    result = incubate_hypothesis(seed)
    assert result.seed_id == "TEST-SEED-001"
    assert isinstance(result.current_level, str)
    assert isinstance(result.incubation_status, str)
    assert isinstance(result.allowed_use, list)
    assert isinstance(result.blocked_use, list)
    assert isinstance(result.required_evidence_for_next_level, list)
    assert isinstance(result.friction_level, str)


def test_incubation_seed_forbidden_claims_propagate():
    """Forbidden claims from the seed must appear in blocked_use."""
    seed = make_seed()
    result = incubate_hypothesis(seed)
    assert "This is validated." in result.blocked_use


def test_incubation_dream_level_has_needs_observable():
    """DREAM-level seed without observable → NEEDS_OBSERVABLE status."""
    seed = make_seed(level="DREAM", observable=None)
    result = incubate_hypothesis(seed)
    assert result.incubation_status == "NEEDS_OBSERVABLE"


def test_incubation_with_observable_advances_status():
    """Seed with observable defined should not return NEEDS_OBSERVABLE."""
    seed = make_seed(level="HYPOTHESIS_SEED", observable="visibility_loss")
    result = incubate_hypothesis(seed)
    assert result.incubation_status != "NEEDS_OBSERVABLE"


def test_incubation_blocks_financial_action():
    """Financial action must always be blocked during incubation."""
    seed = make_seed()
    result = incubate_hypothesis(seed)
    assert any("financial" in b.lower() or "action" in b.lower() for b in result.blocked_use)
