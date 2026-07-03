"""
Phygn v1.9 — Business claim decomposition

Extracts BusinessIdeaInput parameters into structured hypotheses
conforming to the BusinessHypothesisCanvas without inventing evidence.
"""

from __future__ import annotations

import uuid
from phyng.business_validation.schemas import (
    BusinessIdeaInput,
    BusinessHypothesisCanvas,
    BusinessHypothesis,
    BusinessValidationStatus,
)


def decompose_business_idea(idea_input: BusinessIdeaInput) -> BusinessHypothesisCanvas:
    """
    Decompose a raw business idea into a Hypothesis Canvas.

    Fills fields or leaves them marked as None/explicitly unknown.
    Populates list of decomposed BusinessHypothesis items.
    """
    canvas = BusinessHypothesisCanvas(
        idea_id=idea_input.idea_id,
        business_idea=idea_input.raw_idea,
        target_customer=idea_input.target_customer,
        customer_segment=idea_input.target_customer,  # segment matches customer segment
        problem=idea_input.problem,
        problem_urgency=idea_input.urgency,
        current_alternative=idea_input.current_alternative,
        value_proposition=idea_input.value_proposition,
        willingness_to_pay_assumption=idea_input.wtp_assumption,
        pricing_assumption=f"{idea_input.pricing} EUR" if idea_input.pricing else None,
        channel_assumption=idea_input.channel,
        gross_margin_assumption=f"{idea_input.gross_margin * 100}%" if idea_input.gross_margin else None,
        delivery_cost_assumption=f"{idea_input.cost_to_deliver} EUR" if idea_input.cost_to_deliver else None,
        regulatory_risk=idea_input.regulatory_risk,
        kill_criteria=idea_input.kill_criteria,
    )

    hypotheses = []

    # 1. Customer segment hypothesis
    hypotheses.append(
        BusinessHypothesis(
            hypothesis_id=f"H-CUST-{uuid.uuid4().hex[:4].upper()}",
            claim_text=f"Target customer segments are: {idea_input.target_customer or 'UNKNOWN'}",
            hypothesis_type="CUSTOMER",
            target_customer=idea_input.target_customer,
            observable="identifiable customer profile responding to initial messaging",
            metric="qualified responses",
            test_method="outbound outreach to 30 profiles",
            success_threshold="5+ qualified leads",
            failure_threshold="0 qualified leads",
            status="UNTESTED" if idea_input.target_customer else "UNKNOWN"
        )
    )

    # 2. Problem hypothesis
    hypotheses.append(
        BusinessHypothesis(
            hypothesis_id=f"H-PROB-{uuid.uuid4().hex[:4].upper()}",
            claim_text=f"Primary customer pain is: {idea_input.problem or 'UNKNOWN'}",
            hypothesis_type="PROBLEM",
            target_customer=idea_input.target_customer,
            observable="verbal/written confirmation of the problem during interviews",
            metric="problem urgency rating (1-5)",
            test_method="socratic customer discovery interviews",
            success_threshold="80% rate pain >= 4/5",
            failure_threshold="majority rate pain < 3/5",
            status="UNTESTED" if idea_input.problem else "UNKNOWN"
        )
    )

    # 3. Willingness-to-pay hypothesis
    hypotheses.append(
        BusinessHypothesis(
            hypothesis_id=f"H-WTP-{uuid.uuid4().hex[:4].upper()}",
            claim_text=f"Willingness to pay: {idea_input.wtp_assumption or 'UNKNOWN'} at price: {idea_input.pricing or 'UNKNOWN'}",
            hypothesis_type="WILLINGNESS_TO_PAY",
            target_customer=idea_input.target_customer,
            observable="real payment commitments (deposits, preorders, paid pilots)",
            metric="conversion rate",
            test_method="paid pilot test offer",
            success_threshold="10% target sign-ups or deposits",
            failure_threshold="0 payment signals after conversations",
            status="UNTESTED" if idea_input.wtp_assumption else "UNKNOWN"
        )
    )

    # 4. Channel hypothesis
    hypotheses.append(
        BusinessHypothesis(
            hypothesis_id=f"H-CHAN-{uuid.uuid4().hex[:4].upper()}",
            claim_text=f"Channel strategy: {idea_input.channel or 'UNKNOWN'}",
            hypothesis_type="CHANNEL",
            target_customer=idea_input.target_customer,
            observable="acquisition response and click-through metrics",
            metric="response rate",
            test_method="outreach campaign",
            success_threshold="15% click or response rate",
            failure_threshold="<2% response rate",
            status="UNTESTED" if idea_input.channel else "UNKNOWN"
        )
    )

    canvas.hypotheses = hypotheses

    # Recalculate status based on completeness
    if not idea_input.target_customer:
        canvas.validation_status = "BUSINESS_BLOCKED_NO_CUSTOMER"
    elif not idea_input.problem:
        canvas.validation_status = "BUSINESS_BLOCKED_NO_PROBLEM"
    elif not idea_input.wtp_assumption:
        canvas.validation_status = "BUSINESS_BLOCKED_NO_WTP"
    elif not idea_input.channel:
        canvas.validation_status = "BUSINESS_BLOCKED_NO_CHANNEL"
    else:
        canvas.validation_status = "BUSINESS_HYPOTHESIS_SEED"

    return canvas
