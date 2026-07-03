"""
Tests v1.6 — Friction Gradient

Tests:
    test_low_risk_low_friction
    test_high_risk_high_friction
    test_automated_execution_is_blocked
    test_friction_scales_monotonically
    test_dream_mode_no_block
"""

import pytest
from typing import cast
from phyng.epistemic_modes.schemas import RiskLevel
from phyng.epistemic_modes.friction import (
    evaluate_friction,
    get_friction_for_risk,
    RISK_TO_DEFAULT_FRICTION,
    FRICTION_INDEX,
)


def test_low_risk_low_friction():
    """RISK_0 with DREAM_MODE → FRICTION_0_FREE, not blocked."""
    result = evaluate_friction("RISK_0_PRIVATE_THOUGHT", "DREAM_MODE")
    assert result.friction_level == "FRICTION_0_FREE"
    assert result.is_blocked is False
    assert result.requires_human_approval is False


def test_high_risk_high_friction():
    """RISK_7 with AUTOMATED_EXECUTION_MODE → fully blocked."""
    result = evaluate_friction("RISK_7_AUTOMATED_EXECUTION", "AUTOMATED_EXECUTION_MODE")
    assert result.friction_level == "FRICTION_8_BLOCK_UNLESS_FULLY_AUTHORIZED"
    assert result.is_blocked is True
    assert result.requires_human_approval is True


def test_automated_execution_is_blocked():
    """AUTOMATED_EXECUTION_MODE always carries friction 8 (block) due to mode floor."""
    result = evaluate_friction("RISK_0_PRIVATE_THOUGHT", "AUTOMATED_EXECUTION_MODE")
    assert result.is_blocked is True


def test_financial_action_high_friction():
    """FINANCIAL_ACTION_MODE with RISK_5 → at least FRICTION_6 (risk engine required)."""
    result = evaluate_friction("RISK_5_FINANCIAL_RECOMMENDATION", "FINANCIAL_ACTION_MODE")
    # FRICTION_6 = REQUIRE_RISK_ENGINE; human approval starts at FRICTION_7
    assert result.friction_level in ("FRICTION_6_REQUIRE_RISK_ENGINE", "FRICTION_7_REQUIRE_HUMAN_APPROVAL")

def test_real_world_action_requires_human_approval():
    """RISK_6 with FINANCIAL_ACTION_MODE → FRICTION_7 → requires human approval."""
    result = evaluate_friction("RISK_6_REAL_WORLD_ACTION", "FINANCIAL_ACTION_MODE")
    assert result.requires_human_approval is True


def test_friction_scales_monotonically():
    """Higher risk levels should have equal or higher friction index."""
    risk_levels = list(RISK_TO_DEFAULT_FRICTION.keys())
    indices = [FRICTION_INDEX[RISK_TO_DEFAULT_FRICTION[r]] for r in risk_levels]
    for i in range(1, len(indices)):
        assert indices[i] >= indices[i - 1]


def test_dream_mode_no_block():
    """DREAM_MODE with any reasonable risk should not be blocked unless execution mode."""
    for risk in ["RISK_0_PRIVATE_THOUGHT", "RISK_1_INTERNAL_NOTE", "RISK_2_INTERNAL_RESEARCH"]:
        result = evaluate_friction(cast(RiskLevel, risk), "DREAM_MODE")
        assert result.is_blocked is False


def test_friction_decision_has_gate_notes():
    """FrictionDecision always includes gate_notes."""
    result = evaluate_friction("RISK_3_PUBLIC_CONTENT", "CLAIM_MODE")
    assert isinstance(result.gate_notes, list)
    assert len(result.gate_notes) > 0


def test_get_friction_for_risk_convenience():
    assert get_friction_for_risk("RISK_0_PRIVATE_THOUGHT") == "FRICTION_0_FREE"
    assert get_friction_for_risk("RISK_7_AUTOMATED_EXECUTION") == "FRICTION_8_BLOCK_UNLESS_FULLY_AUTHORIZED"
