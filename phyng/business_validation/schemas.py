"""
Phygn v1.9 — Business Validation: Schemas

Defines Pydantic models and Literals/Enums for business model validation gates,
WTP test protocols, channel validation levels, and unit economics checking.
"""

from __future__ import annotations

from typing import Literal, Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums and Literals
# ---------------------------------------------------------------------------

BusinessHypothesisType = Literal[
    "CUSTOMER",
    "PROBLEM",
    "URGENCY",
    "VALUE_PROPOSITION",
    "WILLINGNESS_TO_PAY",
    "CHANNEL",
    "CONVERSION",
    "RETENTION",
    "UNIT_ECONOMICS",
    "DIFFERENTIATION",
    "REGULATORY",
    "OPERATIONAL",
]

BusinessValidationStatus = Literal[
    "BUSINESS_IDEA_ALLOWED",
    "BUSINESS_HYPOTHESIS_SEED",
    "BUSINESS_TESTABLE",
    "BUSINESS_EVIDENCE_LIGHT",
    "BUSINESS_VALIDATED_LIMITED",
    "BUSINESS_BLOCKED_NO_CUSTOMER",
    "BUSINESS_BLOCKED_NO_PROBLEM",
    "BUSINESS_BLOCKED_NO_WTP",
    "BUSINESS_BLOCKED_NO_CHANNEL",
    "BUSINESS_BLOCKED_UNIT_ECONOMICS",
    "BUSINESS_BLOCKED_REGULATORY_RISK",
    "BUSINESS_BLOCKED_OVERCLAIM",
]

WillingnessToPayLevel = Literal[
    "WTP_0_OPINION",
    "WTP_1_INTEREST",
    "WTP_2_MEETING_ACCEPTED",
    "WTP_3_PROBLEM_CONFIRMED",
    "WTP_4_PRICE_ACCEPTED_VERBALLY",
    "WTP_5_PURCHASE_INTENT_WITH_DEADLINE",
    "WTP_6_DEPOSIT_OR_PREORDER",
    "WTP_7_PAID_PILOT",
    "WTP_8_REPEAT_PAYMENT",
]

ChannelValidationLevel = Literal[
    "CHANNEL_0_UNTESTED",
    "CHANNEL_1_REACHABLE",
    "CHANNEL_2_RESPONSES",
    "CHANNEL_3_QUALIFIED_CONVERSATIONS",
    "CHANNEL_4_OFFERS_SENT",
    "CHANNEL_5_PAYMENTS",
    "CHANNEL_6_REPEATABLE",
    "CHANNEL_7_SCALABLE",
]

UnitEconomicsStatus = Literal[
    "UNIT_ECONOMICS_UNKNOWN",
    "UNIT_ECONOMICS_NEGATIVE",
    "UNIT_ECONOMICS_FRAGILE",
    "UNIT_ECONOMICS_PLAUSIBLE",
    "UNIT_ECONOMICS_STRONG",
]

BusinessRiskStatus = Literal[
    "RISK_UNASSESSED",
    "RISK_LOW",
    "RISK_MEDIUM",
    "RISK_HIGH_REQUIRES_REVIEW",
    "RISK_BLOCKING",
]

BusinessPermissionLevel = Literal[
    "EXPLORE_ONLY",
    "INTERVIEW_ALLOWED",
    "TEST_OFFER_ALLOWED",
    "PAID_PILOT_ALLOWED",
    "LIMITED_LAUNCH_ALLOWED",
    "SCALE_BLOCKED",
    "SCALE_ALLOWED",
]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class BusinessIdeaInput(BaseModel):
    """Input payload representing a raw business idea or draft model."""
    idea_id: str
    raw_idea: str
    target_customer: str | None = None
    problem: str | None = None
    urgency: str | None = None
    current_alternative: str | None = None
    value_proposition: str | None = None
    wtp_assumption: str | None = None
    pricing: float | None = None
    channel: str | None = None
    cost_to_deliver: float | None = None
    cac: float | None = None
    gross_margin: float | None = None
    regulatory_risk: str | None = None
    kill_criteria: str | None = None


class BusinessHypothesis(BaseModel):
    """Decomposed single hypothesis from a business model."""
    hypothesis_id: str
    claim_text: str
    hypothesis_type: BusinessHypothesisType
    target_customer: str | None = None
    observable: str | None = None
    metric: str | None = None
    test_method: str | None = None
    success_threshold: str | None = None
    failure_threshold: str | None = None
    evidence_level: str = "NO_EVIDENCE"
    status: str = "UNTESTED"


class BusinessHypothesisCanvas(BaseModel):
    """The full canvased network of business hypotheses."""
    idea_id: str
    business_idea: str
    target_customer: str | None = None
    customer_segment: str | None = None
    problem: str | None = None
    problem_urgency: str | None = None
    current_alternative: str | None = None
    value_proposition: str | None = None
    pain_intensity: str | None = None
    willingness_to_pay_assumption: str | None = None
    pricing_assumption: str | None = None
    channel_assumption: str | None = None
    sales_cycle_assumption: str | None = None
    conversion_assumption: str | None = None
    retention_assumption: str | None = None
    gross_margin_assumption: str | None = None
    delivery_cost_assumption: str | None = None
    regulatory_risk: str | None = None
    operational_risk: str | None = None
    differentiation_claim: str | None = None
    kill_criteria: str | None = None
    next_test: str | None = None
    validation_status: BusinessValidationStatus = "BUSINESS_IDEA_ALLOWED"
    hypotheses: list[BusinessHypothesis] = Field(default_factory=list)


class WillingnessToPayTest(BaseModel):
    """Configuration and evidence of WTP test."""
    offer: str
    target_customer: str
    price: float
    delivery_promise: str
    time_window_days: int
    outreach_count: int
    qualified_conversations_count: int
    success_threshold: str
    failure_threshold: str
    wtp_level: WillingnessToPayLevel = "WTP_0_OPINION"
    payment_signals_received: int = 0
    verbal_agreements: int = 0


class ChannelTest(BaseModel):
    """Outreach channel experiment specification."""
    channel: str
    target_segment: str
    message: str
    outreach_volume: int
    responses_received: int = 0
    qualified_leads: int = 0
    offers_sent: int = 0
    payments_made: int = 0
    cost: float = 0.0
    time_window_days: int = 14
    channel_level: ChannelValidationLevel = "CHANNEL_0_UNTESTED"


class UnitEconomicsProfile(BaseModel):
    """Numeric unit economics model."""
    price: float | None = None
    gross_revenue_per_customer: float | None = None
    cost_to_deliver: float | None = None
    gross_margin: float | None = None
    customer_acquisition_cost: float | None = None
    sales_cycle_length_days: int | None = None
    refund_rate: float | None = None
    support_cost: float | None = None
    retention_rate: float | None = None
    repeat_purchase_rate: float | None = None
    payback_period_months: float | None = None
    contribution_margin: float | None = None
    economics_status: UnitEconomicsStatus = "UNIT_ECONOMICS_UNKNOWN"


class BusinessRiskAssessment(BaseModel):
    """Identified risks and overall safety classification."""
    risks: dict[str, str] = Field(default_factory=dict)
    risk_status: BusinessRiskStatus = "RISK_UNASSESSED"


class KillCriteria(BaseModel):
    """The defined criteria that triggers a kill or pivot decision."""
    kill_trigger: str
    pivot_trigger: str
    justifies_next_test: str
    justifies_investment: str
    has_failure_threshold: bool = False


class BusinessValidationGateResult(BaseModel):
    """Consolidated outcome of all validation sub-gates."""
    idea_id: str
    validation_status: BusinessValidationStatus
    permission_level: BusinessPermissionLevel
    wtp_level: WillingnessToPayLevel
    channel_level: ChannelValidationLevel
    unit_economics_status: UnitEconomicsStatus
    risk_status: BusinessRiskStatus
    kill_criteria_defined: bool
    is_scale_allowed: bool
    allowed_uses: list[str] = Field(default_factory=list)
    blocked_uses: list[str] = Field(default_factory=list)
    next_cheapest_test: str
    evaluation_notes: list[str] = Field(default_factory=list)


class BusinessPostMortem(BaseModel):
    """Retrospective analysis of a failed/finished business test."""
    post_mortem_id: str
    hypothesis_id: str
    test_summary: str
    expected_result: str
    actual_result: str
    gate_decision: str
    was_gate_too_strict: bool
    was_gate_too_loose: bool
    next_decision: str
