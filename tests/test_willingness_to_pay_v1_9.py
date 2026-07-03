"""
Tests v1.9 — Willingness-to-Pay validation gate
"""

import pytest
from phyng.business_validation.schemas import WillingnessToPayTest
from phyng.business_validation.wtp import evaluate_willingness_to_pay


def test_wtp_opinion_not_payment_signal():
    # Only outreach count, level is WTP_1_INTEREST (verbal agreements is 0, payments is 0)
    test = WillingnessToPayTest(
        offer="Technical report",
        target_customer="VCs",
        price=1500.0,
        delivery_promise=" d+5 audit",
        time_window_days=14,
        outreach_count=30,
        qualified_conversations_count=0,
        success_threshold="2 paid pilots",
        failure_threshold="0 pilots",
    )
    res = evaluate_willingness_to_pay(test)
    assert res.wtp_level == "WTP_1_INTEREST"
    assert res.is_validated_limited is False


def test_paid_pilot_upgrades_wtp():
    # Paid commitment signal received -> WTP_7 or WTP_6
    test = WillingnessToPayTest(
        offer="Technical report",
        target_customer="VCs",
        price=1500.0,
        delivery_promise=" d+5 audit",
        time_window_days=14,
        outreach_count=30,
        qualified_conversations_count=8,
        success_threshold="2 paid pilots",
        failure_threshold="0 pilots",
        payment_signals_received=2
    )
    res = evaluate_willingness_to_pay(test)
    assert res.wtp_level == "WTP_7_PAID_PILOT"
    assert res.is_validated_limited is True
    assert res.is_strong_signal is True
