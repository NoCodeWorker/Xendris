"""
Phygn v1.9 — Business Model Validation Campaign Orchestrator
"""

from __future__ import annotations

from pathlib import Path
from phyng.business_validation.schemas import (
    BusinessIdeaInput,
    WillingnessToPayTest,
    ChannelTest,
    UnitEconomicsProfile,
    BusinessRiskAssessment,
    KillCriteria,
)
from phyng.business_validation.decomposition import decompose_business_idea
from phyng.business_validation.gatekeeper import evaluate_business_validation_gate
from phyng.business_validation.post_mortem import create_business_post_mortem
from phyng.business_validation.report import write_business_validation_reports


def run_business_model_validation_campaign(
    reports_dir: str | Path = "reports",
) -> dict:
    """
    Run the full v1.9 business validation campaign demo.
    """
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)

    # 1. intake Business Idea
    idea_input = BusinessIdeaInput(
        idea_id="BUS-AI-AUDIT-001",
        raw_idea="Signphy AI Deeptech claim auditing service for early stage deeptech VCs.",
        target_customer="VCs investing in deeptech/AI startups",
        problem="Investors cannot verify deeptech claims before funding",
        urgency="high — diligence window is tight",
        current_alternative="Ad-hoc advisors or generalist consultants",
        value_proposition="Automated + deterministic physical validation reports",
        wtp_assumption="Paid pilots for technical due diligence report",
        pricing=1500.0,
        channel="LinkedIn outbound + investor events",
        cost_to_deliver=300.0,
        cac=500.0,
        gross_margin=0.8,
        regulatory_risk="No regulatory barriers, data NDA required",
        kill_criteria="0 paid pilots from 30 outreach attempts"
    )

    # Decompose into hypotheses
    canvas = decompose_business_idea(idea_input)

    # 2. Configure Test evidence
    # WTP test: 2 paid pilots achieved -> WTP_7
    wtp_test = WillingnessToPayTest(
        offer="Technical Claim Audit Report",
        target_customer=idea_input.target_customer or "VCs",
        price=1500.0,
        delivery_promise=" d+5 detailed audit",
        time_window_days=14,
        outreach_count=30,
        qualified_conversations_count=8,
        success_threshold="2 paid pilots",
        failure_threshold="0 paid pilots",
        wtp_level="WTP_7_PAID_PILOT",
        payment_signals_received=2,
        verbal_agreements=2
    )

    # Channel test: Outbound LinkedIn -> 3 payments converted -> CHANNEL_6
    channel_test = ChannelTest(
        channel="LinkedIn Outbound",
        target_segment="deeptech partner VCs",
        message="Technical audit for deeptech due diligence",
        outreach_volume=30,
        responses_received=10,
        qualified_leads=5,
        offers_sent=3,
        payments_made=3,
        cost=100.0,
        time_window_days=14,
        channel_level="CHANNEL_6_REPEATABLE"
    )

    # 3. Configure Economics, Risk and Kill Criteria
    economics = UnitEconomicsProfile(
        price=1500.0,
        gross_revenue_per_customer=1500.0,
        cost_to_deliver=300.0,
        gross_margin=0.8,
        customer_acquisition_cost=500.0,
        sales_cycle_length_days=14,
        economics_status="UNIT_ECONOMICS_STRONG"
    )

    risk = BusinessRiskAssessment(
        risks={
            "legal": "Client NDA compliance required",
            "regulatory": "No strict regulatory restrictions apply",
        },
        risk_status="RISK_LOW"
    )

    kill = KillCriteria(
        kill_trigger="0 paid pilots from 30 contacts",
        pivot_trigger="CAC exceeds gross margin after 3 channel tests",
        justifies_next_test="1 paid pilot from 15 contacts",
        justifies_investment="3+ paid pilots with margins > 70%",
        has_failure_threshold=True
    )

    # 4. Evaluate Validation Gate Verdict
    gate_result = evaluate_business_validation_gate(
        canvas=canvas,
        wtp_test=wtp_test,
        channel_test=channel_test,
        economics=economics,
        risk=risk,
        kill_criteria=kill,
    )

    # 5. Create mock Post-Mortem record
    post_mortem = create_business_post_mortem(
        hypothesis_id=canvas.hypotheses[2].hypothesis_id, # wtp hypothesis
        test_summary="LinkedIn outbound offering 1500 EUR paid pilots to VCs.",
        expected_result="At least 2 paid pilots signed in 14 days.",
        actual_result="2 paid pilots signed, total revenue 3000 EUR, CAC 500 EUR.",
        gate_decision="BUSINESS_VALIDATED_LIMITED",
        was_gate_too_strict=False,
        was_gate_too_loose=False,
        next_decision="LIMITED_LAUNCH_ALLOWED"
    )

    # 6. Generate Reports
    report_paths = write_business_validation_reports(
        reports_dir=reports_path,
        canvas=canvas,
        wtp_test=wtp_test,
        channel_test=channel_test,
        economics=economics,
        risk=risk,
        gate_result=gate_result,
        post_mortem=post_mortem,
    )

    return {
        "canvas": canvas,
        "wtp_test": wtp_test,
        "channel_test": channel_test,
        "economics": economics,
        "risk": risk,
        "gate_result": gate_result,
        "post_mortem": post_mortem,
        "report_paths": report_paths,
    }
