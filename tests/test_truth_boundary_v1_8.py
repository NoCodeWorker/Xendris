"""
Tests v1.8 — Truth Boundary status evaluator
"""

import pytest
from phyng.copilot.truth_boundary import evaluate_truth_boundary


def test_lack_of_evidence_is_outside_claim_not_falsehood():
    # Public claim mode but no verified sources -> OUTSIDE_CLAIM_BOUNDARY
    res = evaluate_truth_boundary(
        ladder_level="HYPOTHESIS_SEED",
        mode="CLAIM_MODE",
        risk_level="RISK_3_PUBLIC_CONTENT",
        has_sources=False,
    )
    assert res.status == "OUTSIDE_CLAIM_BOUNDARY"
    assert res.is_valid is False


def test_overclaim_crosses_overclaim_boundary():
    # Overclaim is active -> CROSSED_OVERCLAIM_BOUNDARY
    res = evaluate_truth_boundary(
        ladder_level="HYPOTHESIS_SEED",
        mode="CLAIM_MODE",
        risk_level="RISK_3_PUBLIC_CONTENT",
        has_overclaim=True,
    )
    assert res.status == "CROSSED_OVERCLAIM_BOUNDARY"
    assert res.is_valid is False


def test_contradiction_crosses_falsehood_boundary():
    # Contradiction is active -> CROSSED_FALSEHOOD_BOUNDARY
    res = evaluate_truth_boundary(
        ladder_level="HYPOTHESIS_SEED",
        mode="CLAIM_MODE",
        risk_level="RISK_3_PUBLIC_CONTENT",
        has_contradiction=True,
    )
    assert res.status == "CROSSED_FALSEHOOD_BOUNDARY"
    assert res.is_valid is False


def test_action_without_authorization_blocked():
    # Requesting action without appropriate ladder level / benchmark -> OUTSIDE_ACTION_BOUNDARY
    res = evaluate_truth_boundary(
        ladder_level="HYPOTHESIS_SEED",
        mode="FINANCIAL_ACTION_MODE",
        risk_level="RISK_5_FINANCIAL_RECOMMENDATION",
        requests_action=True,
        has_benchmark=False,
    )
    assert res.status == "OUTSIDE_ACTION_BOUNDARY"
    assert res.is_valid is False


def test_execution_without_authorization_blocked():
    # Requesting execution without execution-allowed rung / benchmark -> OUTSIDE_EXECUTION_BOUNDARY
    res = evaluate_truth_boundary(
        ladder_level="OPERATIONALLY_ACTIONABLE",
        mode="AUTOMATED_EXECUTION_MODE",
        risk_level="RISK_7_AUTOMATED_EXECUTION",
        requests_execution=True,
        has_benchmark=False,
    )
    assert res.status == "OUTSIDE_EXECUTION_BOUNDARY"
    assert res.is_valid is False
