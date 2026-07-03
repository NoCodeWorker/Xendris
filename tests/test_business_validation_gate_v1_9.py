"""
Tests v1.9 — Business Validation Gatekeeper
"""

import pytest
from phyng.business_validation.schemas import (
    BusinessHypothesisCanvas,
    WillingnessToPayTest,
    ChannelTest,
    UnitEconomicsProfile,
    BusinessRiskAssessment,
    KillCriteria,
)
from phyng.business_validation.gatekeeper import evaluate_business_validation_gate


def test_validated_limited_requires_wtp_and_channel():
    canvas = BusinessHypothesisCanvas(
        idea_id="I-001",
        business_idea="Deeptech claims audit",
        target_customer="VCs",
        problem="AI verification"
    )

    wtp = WillingnessToPayTest(
        offer="Audit",
        target_customer="VCs",
        price=1500.0,
        delivery_promise="audit report",
        time_window_days=14,
        outreach_count=30,
        qualified_conversations_count=8,
        success_threshold="2 pilots",
        failure_threshold="0 pilots",
        wtp_level="WTP_7_PAID_PILOT",
        payment_signals_received=2
    )

    channel = ChannelTest(
        channel="LinkedIn",
        target_segment="VC partners",
        message="audit hook",
        outreach_volume=30,
        payments_made=3,
        channel_level="CHANNEL_6_REPEATABLE"
    )

    economics = UnitEconomicsProfile(
        price=1500.0,
        cost_to_deliver=300.0,
        customer_acquisition_cost=500.0,
        economics_status="UNIT_ECONOMICS_STRONG"
    )

    risk = BusinessRiskAssessment(
        risks={"regulatory": "RISK_LOW"},
        risk_status="RISK_LOW"
    )

    kill = KillCriteria(
        kill_trigger="0 paid pilots",
        pivot_trigger="high CAC",
        justifies_next_test="1 pilot",
        justifies_investment="3 pilots",
        has_failure_threshold=True
    )

    res = evaluate_business_validation_gate(
        canvas=canvas,
        wtp_test=wtp,
        channel_test=channel,
        economics=economics,
        risk=risk,
        kill_criteria=kill
    )

    assert res.validation_status == "BUSINESS_VALIDATED_LIMITED"
    assert res.permission_level == "LIMITED_LAUNCH_ALLOWED"
    assert res.is_scale_allowed is True
