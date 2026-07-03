"""
Tests v1.6 — Risk-Weighted Gatekeeper

Tests:
    test_claim_mode_requires_source
    test_financial_action_requires_risk_fields
    test_automated_execution_blocks_without_full_authorization
    test_dream_mode_allows_idea
    test_financial_gate_intuition_always_logged
    test_financial_gate_all_fields_passes
"""

import pytest
from phyng.epistemic_modes.gatekeeper import evaluate_mode_gate, evaluate_financial_action_gate
from phyng.epistemic_modes.gatekeeper import FINANCIAL_ACTION_REQUIRED_FIELDS


def test_claim_mode_requires_source():
    """In CLAIM_MODE with no source, claim_permission must be CLAIM_BLOCKED."""
    result = evaluate_mode_gate(
        mode="CLAIM_MODE",
        risk_level="RISK_3_PUBLIC_CONTENT",
        has_source=False,
        has_benchmark=False,
    )
    assert result.claim_permission == "CLAIM_BLOCKED"


def test_dream_mode_allows_idea():
    """In DREAM_MODE, idea_permission must be IDEA_ALLOWED."""
    result = evaluate_mode_gate(
        mode="DREAM_MODE",
        risk_level="RISK_0_PRIVATE_THOUGHT",
        has_source=False,
        has_benchmark=False,
    )
    assert result.idea_permission == "IDEA_ALLOWED"


def test_dream_mode_blocks_claim_without_source():
    """Even in DREAM_MODE, claim is blocked without source."""
    result = evaluate_mode_gate(
        mode="DREAM_MODE",
        risk_level="RISK_0_PRIVATE_THOUGHT",
        has_source=False,
        has_benchmark=False,
    )
    assert result.claim_permission == "CLAIM_BLOCKED"


def test_automated_execution_blocks_without_full_authorization():
    """AUTOMATED_EXECUTION_MODE without source/benchmark must block execution."""
    result = evaluate_mode_gate(
        mode="AUTOMATED_EXECUTION_MODE",
        risk_level="RISK_7_AUTOMATED_EXECUTION",
        has_source=False,
        has_benchmark=False,
    )
    assert result.execution_permission == "EXECUTION_BLOCKED"


def test_financial_action_requires_risk_fields():
    """Financial gate with missing fields → ACTION_BLOCKED."""
    result = evaluate_financial_action_gate({"asset": "BTC"})  # missing 9 fields
    assert result.action_status == "ACTION_BLOCKED"
    assert len(result.missing_fields) > 0


def test_financial_gate_intuition_always_logged():
    """Even when action is blocked, intuition must be INTUITION_LOGGED."""
    result = evaluate_financial_action_gate({"asset": "ETH"})
    assert result.intuition_status == "INTUITION_LOGGED"


def test_financial_gate_all_fields_passes():
    """With all required fields, action gate passes (pending risk review)."""
    full_fields: dict[str, str | None] = {field: "value" for field in FINANCIAL_ACTION_REQUIRED_FIELDS}
    result = evaluate_financial_action_gate(full_fields)
    assert result.missing_fields == []
    assert result.action_status == "ACTION_REQUIRES_RISK_GATE"


def test_gate_result_distinguishes_five_permission_types():
    """ModeGateResult must have all 5 distinct permission fields."""
    result = evaluate_mode_gate("HYPOTHESIS_MODE", "RISK_2_INTERNAL_RESEARCH")
    assert hasattr(result, "idea_permission")
    assert hasattr(result, "hypothesis_permission")
    assert hasattr(result, "claim_permission")
    assert hasattr(result, "action_permission")
    assert hasattr(result, "execution_permission")


def test_mode_gate_has_allowed_and_blocked_uses():
    """ModeGateResult must have allowed_uses and blocked_uses."""
    result = evaluate_mode_gate("DREAM_MODE", "RISK_0_PRIVATE_THOUGHT")
    assert isinstance(result.allowed_uses, list)
    assert isinstance(result.blocked_uses, list)
