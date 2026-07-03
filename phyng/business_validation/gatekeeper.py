"""
Phygn v1.9 — Business Model Validation Gatekeeper

Integrates Willingness-to-Pay, acquisition channel, unit economics,
risk, and kill criteria sub-gates to output a consolidated permission level.
"""

from __future__ import annotations

from phyng.business_validation.schemas import (
    BusinessHypothesisCanvas,
    WillingnessToPayTest,
    ChannelTest,
    UnitEconomicsProfile,
    BusinessRiskAssessment,
    KillCriteria,
    BusinessValidationGateResult,
    BusinessValidationStatus,
    BusinessPermissionLevel,
)
from phyng.business_validation.wtp import evaluate_willingness_to_pay
from phyng.business_validation.channel import evaluate_channel_test
from phyng.business_validation.unit_economics import evaluate_unit_economics
from phyng.business_validation.risk import evaluate_business_risk
from phyng.business_validation.kill_criteria import evaluate_kill_criteria


def evaluate_business_validation_gate(
    canvas: BusinessHypothesisCanvas,
    wtp_test: WillingnessToPayTest | None,
    channel_test: ChannelTest | None,
    economics: UnitEconomicsProfile | None,
    risk: BusinessRiskAssessment | None,
    kill_criteria: KillCriteria | None,
) -> BusinessValidationGateResult:
    """
    Consolidate all business validation sub-gates to check feasibility and scale permission.
    """
    notes = []
    is_scale_allowed = True

    # 1. Run Sub-gates
    wtp_res = evaluate_willingness_to_pay(wtp_test) if wtp_test else None
    chan_res = evaluate_channel_test(channel_test) if channel_test else None
    econ_res = evaluate_unit_economics(economics) if economics else None
    risk_res = evaluate_business_risk(risk) if risk else None
    kill_res = evaluate_kill_criteria(kill_criteria) if kill_criteria else None

    # Retrieve WTP level & Channel level
    wtp_lvl = wtp_res.wtp_level if wtp_res else "WTP_0_OPINION"
    chan_lvl = chan_res.channel_level if chan_res else "CHANNEL_0_UNTESTED"
    econ_status = econ_res.economics_status if econ_res else "UNIT_ECONOMICS_UNKNOWN"
    risk_status = risk_res.risk_status if risk_res else "RISK_UNASSESSED"

    # 2. Check Blocking Rules for Scaling
    if not canvas.target_customer:
        is_scale_allowed = False
        notes.append("Scale blocked: Target customer is unknown.")
        status: BusinessValidationStatus = "BUSINESS_BLOCKED_NO_CUSTOMER"
        perm: BusinessPermissionLevel = "EXPLORE_ONLY"

    elif not canvas.problem:
        is_scale_allowed = False
        notes.append("Scale blocked: Problem is unknown.")
        status = "BUSINESS_BLOCKED_NO_PROBLEM"
        perm = "EXPLORE_ONLY"

    elif not wtp_test or wtp_lvl in ("WTP_0_OPINION", "WTP_1_INTEREST", "WTP_2_MEETING_ACCEPTED"):
        is_scale_allowed = False
        notes.append("Scale blocked: Insufficient willingness-to-pay evidence.")
        status = "BUSINESS_BLOCKED_NO_WTP"
        perm = "INTERVIEW_ALLOWED"

    elif not channel_test or chan_lvl == "CHANNEL_0_UNTESTED":
        is_scale_allowed = False
        notes.append("Scale blocked: Outbound channel remains untested.")
        status = "BUSINESS_BLOCKED_NO_CHANNEL"
        perm = "TEST_OFFER_ALLOWED"

    elif econ_status == "UNIT_ECONOMICS_NEGATIVE":
        is_scale_allowed = False
        notes.append("Scale blocked: Negative unit economics margin.")
        status = "BUSINESS_BLOCKED_UNIT_ECONOMICS"
        perm = "EXPLORE_ONLY"

    elif risk_status == "RISK_BLOCKING":
        is_scale_allowed = False
        notes.append("Scale blocked: Regulatory or compliance risk blocks operations.")
        status = "BUSINESS_BLOCKED_REGULATORY_RISK"
        perm = "SCALE_BLOCKED"

    elif not kill_res or not kill_res.is_valid:
        is_scale_allowed = False
        notes.append("Scale blocked: Kill criteria is invalid or missing failure thresholds.")
        status = "BUSINESS_TESTABLE"
        perm = "TEST_OFFER_ALLOWED"

    else:
        # Check validation level
        if wtp_res and chan_res and wtp_res.is_validated_limited and chan_res.is_validated_limited:
            if econ_res and econ_res.is_scale_allowed:
                status = "BUSINESS_VALIDATED_LIMITED"
                perm = "LIMITED_LAUNCH_ALLOWED"
                notes.append("Gate passed: Limited launch permitted under WTP and Channel validation.")
            else:
                is_scale_allowed = False
                status = "BUSINESS_EVIDENCE_LIGHT"
                perm = "PAID_PILOT_ALLOWED"
                notes.append("WTP & Channel show evidence, but Unit Economics restricts scaling.")
        else:
            is_scale_allowed = False
            status = "BUSINESS_TESTABLE"
            perm = "PAID_PILOT_ALLOWED"
            notes.append("Hypotheses are testable, but customer validation signals remain incomplete.")

    # Scale can only be SCALE_ALLOWED if is_scale_allowed is True and status is fully validated
    if is_scale_allowed and status == "BUSINESS_VALIDATED_LIMITED":
        perm = "LIMITED_LAUNCH_ALLOWED"
    elif not is_scale_allowed and perm not in ("EXPLORE_ONLY", "INTERVIEW_ALLOWED", "TEST_OFFER_ALLOWED", "PAID_PILOT_ALLOWED", "SCALE_BLOCKED"):
        perm = "SCALE_BLOCKED"

    # Define next cheapest test
    next_test = "Decompose business model"
    if status == "BUSINESS_BLOCKED_NO_CUSTOMER":
        next_test = "Identify target customer segment profile."
    elif status == "BUSINESS_BLOCKED_NO_PROBLEM":
        next_test = "Conduct customer discovery interviews to confirm pain."
    elif status == "BUSINESS_BLOCKED_NO_WTP":
        next_test = "Offer deposit preorder or B2B paid pilot proposal."
    elif status == "BUSINESS_BLOCKED_NO_CHANNEL":
        next_test = "Outreach to 30 prospects via cold email or LinkedIn."
    elif status == "BUSINESS_BLOCKED_UNIT_ECONOMICS":
        next_test = "Redesign pricing structure or decrease cost to deliver."
    elif status == "BUSINESS_BLOCKED_REGULATORY_RISK":
        next_test = "Resolve compliance constraints or pivot domain."
    elif not kill_res or not kill_res.is_valid:
        next_test = "Define clear failure thresholds and kill triggers."
    else:
        next_test = "Execute repeat cohort paid test."

    # Usage constraints
    allowed = ["Internal ideation", "Socratic refinement"]
    blocked = ["Public scale-out launch", "Capital expenditure allocation"]

    if perm in ("LIMITED_LAUNCH_ALLOWED", "SCALE_ALLOWED"):
        allowed.extend(["Limited product launch", "Channel marketing spend"])
        blocked.remove("Public scale-out launch")

    return BusinessValidationGateResult(
        idea_id=canvas.idea_id,
        validation_status=status,
        permission_level=perm,
        wtp_level=wtp_lvl,
        channel_level=chan_lvl,
        unit_economics_status=econ_status,
        risk_status=risk_status,
        kill_criteria_defined=(kill_res is not None and kill_res.is_valid),
        is_scale_allowed=is_scale_allowed,
        allowed_uses=allowed,
        blocked_uses=blocked,
        next_cheapest_test=next_test,
        evaluation_notes=notes
    )
