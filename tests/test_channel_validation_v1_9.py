"""
Tests v1.9 — Channel acquisition validation gate
"""

import pytest
from phyng.business_validation.schemas import ChannelTest
from phyng.business_validation.channel import evaluate_channel_test


def test_channel_traffic_without_response_is_weak():
    # Outreach logged, but no responses or conversions -> CHANNEL_1
    test = ChannelTest(
        channel="LinkedIn Outbound",
        target_segment="VC partners",
        message="Diligence audit",
        outreach_volume=30,
        responses_received=0
    )
    res = evaluate_channel_test(test)
    assert res.channel_level == "CHANNEL_1_REACHABLE"
    assert res.is_repeatable is False
    assert any("weak" in n.lower() for n in res.notes)
