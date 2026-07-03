"""
Phygn v1.9 — Willingness-to-Pay test protocol evaluator

Distinguishes opinions/likes from paid commitment signals.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from phyng.business_validation.schemas import WillingnessToPayTest, WillingnessToPayLevel


class WTPGateResult(BaseModel):
    """Result of evaluating the willingness-to-pay signal."""
    wtp_level: WillingnessToPayLevel
    is_validated_limited: bool
    is_strong_signal: bool
    notes: list[str] = Field(default_factory=list)


def evaluate_willingness_to_pay(test: WillingnessToPayTest) -> WTPGateResult:
    """
    Classify the WTP level and check if the WTP gate is passed.

    Rules:
      - Opinions and likes are WTP_0_OPINION.
      - Verbal agreement is WTP_4.
      - Deposits/Preorders are WTP_6.
      - Paid pilots are WTP_7 (strongest B2B signal).
    """
    notes = []

    # Classify WTP Level
    if test.payment_signals_received >= 2:
        level: WillingnessToPayLevel = "WTP_7_PAID_PILOT"
        notes.append("Multiple paid commitments received. Excellent validation indicator.")
    elif test.payment_signals_received == 1:
        level = "WTP_6_DEPOSIT_OR_PREORDER"
        notes.append("Single deposit or preorder signal captured.")
    elif test.verbal_agreements > 0:
        level = "WTP_4_PRICE_ACCEPTED_VERBALLY"
        notes.append("Verbal interest only. Warning: opinions and verbal likes are not payment evidence.")
    elif test.qualified_conversations_count > 0:
        level = "WTP_3_PROBLEM_CONFIRMED"
        notes.append("Problem confirmed in conversations, but no pricing discussion occurred.")
    elif test.outreach_count > 0:
        level = "WTP_1_INTEREST"
        notes.append("Outreach conducted, only raw clicks/traffic. No direct purchase intent.")
    else:
        level = "WTP_0_OPINION"
        notes.append("WTP remains at raw opinion/praise level. Warning: likes do not equal demand.")

    is_validated = level in ("WTP_6_DEPOSIT_OR_PREORDER", "WTP_7_PAID_PILOT", "WTP_8_REPEAT_PAYMENT")
    is_strong = level in ("WTP_7_PAID_PILOT", "WTP_8_REPEAT_PAYMENT")

    return WTPGateResult(
        wtp_level=level,
        is_validated_limited=is_validated,
        is_strong_signal=is_strong,
        notes=notes
    )
