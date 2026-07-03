"""
Phygn v1.9 — Channel test protocol evaluator

Flags vanity metrics like raw traffic without qualified response.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from phyng.business_validation.schemas import ChannelTest, ChannelValidationLevel


class ChannelGateResult(BaseModel):
    """Result of evaluating acquisition channel experiments."""
    channel_level: ChannelValidationLevel
    is_repeatable: bool
    is_validated_limited: bool
    notes: list[str] = Field(default_factory=list)


def evaluate_channel_test(test: ChannelTest) -> ChannelGateResult:
    """
    Classify the channel validation level based on results.

    Rules:
      - Traffic without responses is weak (CHANNEL_1).
      - qualified leads -> CHANNEL_3.
      - repeatable acquisition -> CHANNEL_6.
    """
    notes = []

    # 1. Payments made
    if test.payments_made >= 3:
        level: ChannelValidationLevel = "CHANNEL_6_REPEATABLE"
        notes.append("Channel is repeatable: multiple paid customers acquired through this route.")
    elif test.payments_made > 0:
        level = "CHANNEL_5_PAYMENTS"
        notes.append("Channel has produced payments, but repeatability is not yet proven.")
    elif test.offers_sent > 0:
        level = "CHANNEL_4_OFFERS_SENT"
        notes.append("Offers sent, but no conversion/payment received. Offers without payment do not validate WTP.")
    elif test.qualified_leads > 0:
        level = "CHANNEL_3_QUALIFIED_CONVERSATIONS"
        notes.append("Meetings accepted and qualified conversations held. Warning: meetings without offers are weak.")
    elif test.responses_received > 0:
        level = "CHANNEL_2_RESPONSES"
        notes.append("Received responses, but none are qualified leads.")
    elif test.outreach_volume > 0:
        level = "CHANNEL_1_REACHABLE"
        notes.append("Outreach volume logged. Warning: traffic without qualified response is weak.")
    else:
        level = "CHANNEL_0_UNTESTED"
        notes.append("Channel is untested.")

    is_repeatable = level in ("CHANNEL_6_REPEATABLE", "CHANNEL_7_SCALABLE")
    is_validated = level in ("CHANNEL_3_QUALIFIED_CONVERSATIONS", "CHANNEL_4_OFFERS_SENT", "CHANNEL_5_PAYMENTS", "CHANNEL_6_REPEATABLE", "CHANNEL_7_SCALABLE")

    return ChannelGateResult(
        channel_level=level,
        is_repeatable=is_repeatable,
        is_validated_limited=is_validated,
        notes=notes
    )
