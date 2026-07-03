"""Tests for v4.6 candidate final claim permissions."""

from __future__ import annotations

from phyng.candidate_decision.claim_permissions import establish_claim_permissions


def test_final_claim_permissions_block_predictive_gain() -> None:
    inputs = {}
    permissions = establish_claim_permissions(inputs, "FREEZE-v45-001")
    assert permissions.predictive_gain_permission == "BLOCKED_NO_YTRUE"
    assert "PHI_GRADIENT has PredictiveGain." in permissions.blocked_claims


def test_final_claim_permissions_block_physical_claim() -> None:
    inputs = {}
    permissions = establish_claim_permissions(inputs, "FREEZE-v45-001")
    assert permissions.physical_claim_permission == "BLOCKED"
    assert permissions.gradient_mechanism_claim_permission == "BLOCKED_BY_SLOT4_DEBT"
    assert "PHI_GRADIENT is a source-backed physical mechanism." in permissions.blocked_claims
    assert "PHI_GRADIENT was evaluated as a benchmark candidate." in permissions.allowed_claims
