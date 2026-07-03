"""
Tests v1.6 — Dream-to-Claim Ladder

Tests:
    test_dream_mode_allows_intuition
    test_dream_mode_blocks_public_claim
    test_hypothesis_seed_allowed_not_claim
    test_claim_mode_requires_source
    test_ladder_advances_with_evidence
    test_ladder_dream_has_zero_index
"""

import pytest
from phyng.epistemic_modes.ladder import (
    classify_ladder_level,
    LADDER_ORDER,
    LADDER_INDEX,
    get_ladder_level_name,
)


def test_dream_mode_allows_intuition():
    """With no evidence, result is DREAM level and idea is allowed."""
    result = classify_ladder_level("Maybe X causes Y.", "dream", [])
    assert result.idea_allowed is True
    assert result.ladder_level == "DREAM"
    assert result.level_index == 0


def test_dream_mode_blocks_public_claim():
    """With no evidence, claim and action are not allowed."""
    result = classify_ladder_level("Maybe X causes Y.", "publish", [])
    assert result.claim_allowed is False
    assert result.action_allowed is False
    assert result.execution_allowed is False


def test_hypothesis_seed_allowed_not_claim():
    """With seed-level evidence, hypothesis_seed status is returned but claim is blocked."""
    evidence = ["candidate_phenomenon", "domain", "uncertainty_acknowledged"]
    result = classify_ladder_level("Frontera C modulates decoherence.", "explore", evidence)
    assert result.idea_allowed is True
    assert result.claim_allowed is False
    assert result.status == "HYPOTHESIS_SEED"


def test_testable_hypothesis_requires_all_fields():
    """TESTABLE_HYPOTHESIS needs all 6 required fields."""
    # Missing some fields → stays at lower level
    evidence = ["candidate_phenomenon", "domain", "uncertainty_acknowledged", "variables"]
    result = classify_ladder_level("test", "test", evidence)
    assert result.ladder_level in ("DREAM", "HYPOTHESIS_SEED", "FORMALIZING_HYPOTHESIS")
    assert result.claim_allowed is False


def test_ladder_advances_with_evidence():
    """Adding more evidence progressively advances the ladder."""
    r1 = classify_ladder_level("test", "explore", [])
    r2 = classify_ladder_level("test", "explore", ["candidate_phenomenon", "domain", "uncertainty_acknowledged"])
    assert r2.level_index >= r1.level_index


def test_ladder_dream_has_zero_index():
    assert LADDER_INDEX["DREAM"] == 0


def test_ladder_order_has_9_levels():
    assert len(LADDER_ORDER) == 9


def test_ladder_execution_level_allows_execution():
    """AUTOMATED_EXECUTION_ALLOWED should allow execution."""
    all_evidence = [
        "candidate_phenomenon", "domain", "uncertainty_acknowledged",
        "variables", "possible_observable", "rough_mechanism", "scope_boundary",
        "observable", "baseline", "candidate_model", "failure_condition",
        "metric", "detectability_threshold",
        "synthetic_benchmark", "delta_computation", "toy_failure_conditions",
        "source_audit", "claim_source_links", "source_support",
        "y_true", "baseline_comparison", "uncertainty",
        "risk_assessment", "scope_limits", "failure_protocol", "monitoring",
        "strong_evidence", "risk_engine", "logging", "rollback",
        "kill_switch", "compliance_review",
    ]
    result = classify_ladder_level("test", "execute", all_evidence)
    assert result.ladder_level == "AUTOMATED_EXECUTION_ALLOWED"
    assert result.execution_allowed is True


def test_get_ladder_level_name():
    assert get_ladder_level_name(0) == "DREAM"
    assert get_ladder_level_name(8) == "AUTOMATED_EXECUTION_ALLOWED"
    assert get_ladder_level_name(4) == "SYNTHETIC_SUPPORT"
