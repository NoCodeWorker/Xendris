"""
Tests v1.9 — Unit Economics, Risk & Kill Criteria Gates
"""

import pytest
from phyng.business_validation.schemas import (
    UnitEconomicsProfile,
    BusinessRiskAssessment,
    KillCriteria,
)
from phyng.business_validation.unit_economics import evaluate_unit_economics
from phyng.business_validation.risk import evaluate_business_risk
from phyng.business_validation.kill_criteria import evaluate_kill_criteria


def test_negative_unit_economics_blocks_scale():
    # Delivery cost (500) exceeds price (400) -> negative margin
    profile = UnitEconomicsProfile(
        price=400.0,
        cost_to_deliver=500.0,
    )
    res = evaluate_unit_economics(profile)
    assert res.economics_status == "UNIT_ECONOMICS_NEGATIVE"
    assert res.is_scale_allowed is False


def test_missing_kill_criteria_blocks_scale():
    # KillCriteria is None
    res = evaluate_kill_criteria(None)
    assert res.is_valid is False

    # KillCriteria has has_failure_threshold = False
    crit = KillCriteria(
        kill_trigger="0 paid pilots",
        pivot_trigger="high CAC",
        justifies_next_test="1 pilot",
        justifies_investment="3 pilots",
        has_failure_threshold=False
    )
    res_crit = evaluate_kill_criteria(crit)
    assert res_crit.is_valid is False


def test_blocking_risk_blocks_scale():
    # Assessed risks contains RISK_BLOCKING
    assessment = BusinessRiskAssessment(
        risks={"regulatory": "RISK_BLOCKING"},
        risk_status="RISK_UNASSESSED"
    )
    res = evaluate_business_risk(assessment)
    assert res.risk_status == "RISK_BLOCKING"
    assert res.is_blocking is True
