"""
Phygn v1.9 — Business Hypothesis Canvas Questions

Generates the next best business question based on the missing components of the canvas.
"""

from __future__ import annotations

import uuid
from phyng.business_validation.schemas import BusinessHypothesisCanvas
from phyng.copilot.schemas import NextBestQuestion


def generate_next_best_business_question(canvas: BusinessHypothesisCanvas) -> NextBestQuestion:
    """
    Generate exactly one socratic question focusing on the missing field with the highest leverage.

    Priority:
    1. target customer
    2. painful problem
    3. current alternative
    4. willingness to pay
    5. price
    6. channel
    7. unit economics
    8. risks
    9. kill criteria
    """
    # 1. Target Customer
    if not canvas.target_customer:
        return NextBestQuestion(
            question_id=f"QB-{uuid.uuid4().hex[:8].upper()}",
            question_type="CLARIFY_TERM",
            question_text="Who exactly is the target customer segment experiencing this pain?",
            why_needed="No customer Segment defined. We cannot test business assumptions without a specific audience.",
            answer_options=["B2B Startups", "Venture Funds / Investors", "Individual Consumers (B2C)", "Enterprise Innovation Labs"],
            free_text_allowed=True,
            updates_fields=["target_customer"],
            blocks_until_answered=["target_customer"]
        )

    # 2. Painful Problem
    if not canvas.problem:
        return NextBestQuestion(
            question_id=f"QB-{uuid.uuid4().hex[:8].upper()}",
            question_type="DEFINE_VARIABLE",
            question_text="What painful situation or core problem does this customer segment experience today?",
            why_needed="No defined problem. A business validates when it solves a real, urgent customer pain.",
            answer_options=[],
            free_text_allowed=True,
            updates_fields=["problem"],
            blocks_until_answered=["problem"]
        )

    # 3. Current Alternative
    if not canvas.current_alternative:
        return NextBestQuestion(
            question_id=f"QB-{uuid.uuid4().hex[:8].upper()}",
            question_type="CHOOSE_BASELINE",
            question_text="What current alternative or workaround does the customer use today to solve this problem?",
            why_needed="We need a baseline alternative to measure our relative value proposition.",
            answer_options=["Manual worksheets", "Consulting services", "Doing nothing / accepting risk", "In-house custom code"],
            free_text_allowed=True,
            updates_fields=["current_alternative"],
            blocks_until_answered=["current_alternative"]
        )

    # 4. Willingness to Pay
    if not canvas.willingness_to_pay_assumption:
        return NextBestQuestion(
            question_id=f"QB-{uuid.uuid4().hex[:8].upper()}",
            question_type="SELECT_PROXY",
            question_text="What willingness-to-pay metric or offer can you test with customers?",
            why_needed="We must identify the transaction token (deposit, preorder, paid pilot) that shows real demand.",
            answer_options=["Paid pilot letter of intent", "Deposit/preorder payment", "Standard verbal commitment"],
            free_text_allowed=True,
            updates_fields=["willingness_to_pay_assumption"],
            blocks_until_answered=["willingness_to_pay_assumption"]
        )

    # 5. Price
    if not canvas.pricing_assumption:
        return NextBestQuestion(
            question_id=f"QB-{uuid.uuid4().hex[:8].upper()}",
            question_type="DEFINE_TIME_HORIZON",
            question_text="What is the exact target pricing or subscription price for this validation test?",
            why_needed="Vague pricing blocks financial validation. We must test a specific price point.",
            answer_options=["99 EUR/month", "499 EUR/month", "1,500 EUR one-time pilot", "5,000 EUR annual contract"],
            free_text_allowed=True,
            updates_fields=["pricing_assumption"],
            blocks_until_answered=["pricing_assumption"]
        )

    # 6. Channel
    if not canvas.channel_assumption:
        return NextBestQuestion(
            question_id=f"QB-{uuid.uuid4().hex[:8].upper()}",
            question_type="CONFIRM_SCOPE",
            question_text="Which acquisition channel will you use to reach 20 qualified prospects this week?",
            why_needed="Without a reachable channel, customer acquisition costs cannot be measured.",
            answer_options=["Cold outbound email", "LinkedIn sales navigator", "Direct referrals / warm intro", "Community networking"],
            free_text_allowed=True,
            updates_fields=["channel_assumption"],
            blocks_until_answered=["channel_assumption"]
        )

    # 7. Unit Economics
    if not canvas.gross_margin_assumption or not canvas.delivery_cost_assumption:
        return NextBestQuestion(
            question_id=f"QB-{uuid.uuid4().hex[:8].upper()}",
            question_type="CHOOSE_METRIC",
            question_text="How much does it cost you to deliver one successful customer outcome?",
            why_needed="Without delivery cost and gross margin estimates, the unit economics status remains fragile.",
            answer_options=[],
            free_text_allowed=True,
            updates_fields=["delivery_cost_assumption", "gross_margin_assumption"],
            blocks_until_answered=["gross_margin_assumption"]
        )

    # 8. Risks
    if not canvas.regulatory_risk:
        return NextBestQuestion(
            question_id=f"QB-{uuid.uuid4().hex[:8].upper()}",
            question_type="ASSESS_RISK",
            question_text="What regulatory, legal, or compliance risks apply to this business model?",
            why_needed="Risk unassessed. We must identify regulatory roadblocks early.",
            answer_options=["GDPR / Data Privacy compliance", "Technical claim overclaim risk", "Financial regulatory compliance", "No significant regulatory risks"],
            free_text_allowed=True,
            updates_fields=["regulatory_risk"],
            blocks_until_answered=["regulatory_risk"]
        )

    # 9. Kill Criteria
    if not canvas.kill_criteria:
        return NextBestQuestion(
            question_id=f"QB-{uuid.uuid4().hex[:8].upper()}",
            question_type="DEFINE_FAILURE_CONDITION",
            question_text="What concrete failure result or threshold will kill this hypothesis?",
            why_needed="No kill criteria defined. Rigor requires a failure threshold to stop burning money.",
            answer_options=["0 payment signals from 30 contacts", "CAC exceeds price after 3 attempts", "Fewer than 2 paid pilots in 14 days"],
            free_text_allowed=True,
            updates_fields=["kill_criteria"],
            blocks_until_answered=["kill_criteria"]
        )

    # Default
    return NextBestQuestion(
        question_id=f"QB-{uuid.uuid4().hex[:8].upper()}",
        question_type="CONFIRM_SCOPE",
        question_text="All business canvas hypotheses formulated. Ready to initiate customer validation tests?",
        why_needed="Confirms transition from design to test protocol execution.",
        answer_options=["Yes, start outbound test", "No, revise pricing"],
        free_text_allowed=False,
        updates_fields=[],
        blocks_until_answered=[]
    )
