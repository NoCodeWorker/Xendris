"""Tests for v4.1 claim permission updates."""

from __future__ import annotations

from phyng.model_comparison.claim_permission import build_claim_permission_update


def test_claim_permission_blocks_physical_claims() -> None:
    update = build_claim_permission_update()
    assert update.physical_claim_permission == "BLOCKED"
    assert "PHI_GRADIENT is validated." in update.blocked_claims
    assert "Frontera C is validated." in update.blocked_claims


def test_gradient_claim_blocked_by_slot4_debt() -> None:
    update = build_claim_permission_update()
    assert update.gradient_mechanism_claim_permission == "BLOCKED_BY_SLOT4_DEBT"
    assert "Gradient mechanism is supported." in update.blocked_claims
    assert update.benchmark_claim_permission == "BENCHMARK_COMPARISON_PERFORMED_LIMITED"
