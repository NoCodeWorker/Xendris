from __future__ import annotations

from phyng.full_suite_logic_audit.claim_leakage_scanner import detects_claim_leakage


def test_claim_leakage_detects_predictive_gain_without_ytrue() -> None:
    issues = detects_claim_leakage("PredictiveGain exists for PHI_GRADIENT.")

    assert any(issue.category == "PREDICTIVE_GAIN_WITHOUT_YTRUE" for issue in issues)


def test_claim_leakage_detects_gradient_support_with_open_slot4_debt() -> None:
    issues = detects_claim_leakage("The gradient mechanism is supported while SLOT4 debt is open.")

    assert any(issue.category == "GRADIENT_SUPPORT_WITH_OPEN_SLOT4_DEBT" for issue in issues)


def test_blocked_claim_context_is_not_leakage() -> None:
    issues = detects_claim_leakage("Blocked claims: PredictiveGain exists for PHI_GRADIENT.")

    assert issues == []
