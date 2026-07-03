from pathlib import Path

from phyng.business_validation.gatekeeper import evaluate_business_validation_gate
from phyng.business_validation.schemas import (
    BusinessHypothesisCanvas,
    BusinessRiskAssessment,
    ChannelTest,
    KillCriteria,
    UnitEconomicsProfile,
    WillingnessToPayTest,
)
from phyng.campaigns.repository_orchestration_audit import (
    run_repository_orchestration_audit_campaign,
)


def test_campaign_report_generated(tmp_path):
    result = run_repository_orchestration_audit_campaign(Path("."))

    assert result.status == "COMPLETE_DISCOVERY_NO_BEHAVIOR_CHANGE"
    assert "campaign" in result.report_paths
    assert Path(result.report_paths["campaign"]).exists()
    assert Path(result.report_paths["structure"]).exists()
    campaign_text = Path(result.report_paths["campaign"]).read_text(encoding="utf-8")
    assert "repository_structure_audit_v2_0.md" in campaign_text


def test_audit_does_not_change_existing_gate_behavior():
    canvas = BusinessHypothesisCanvas(
        idea_id="BUS-AUDIT-STABILITY",
        business_idea="Technical diligence service",
        target_customer="VCs",
        problem="Need claim verification",
        willingness_to_pay_assumption="Paid pilot",
        channel_assumption="Outbound",
        kill_criteria="0 paid pilots",
    )
    wtp = WillingnessToPayTest(
        offer="Audit",
        target_customer="VCs",
        price=1500.0,
        delivery_promise="Five day report",
        time_window_days=14,
        outreach_count=30,
        qualified_conversations_count=8,
        success_threshold="2 paid pilots",
        failure_threshold="0 paid pilots",
        wtp_level="WTP_7_PAID_PILOT",
        payment_signals_received=2,
    )
    channel = ChannelTest(
        channel="Outbound",
        target_segment="VCs",
        message="Technical audit",
        outreach_volume=30,
        responses_received=10,
        qualified_leads=5,
        offers_sent=3,
        payments_made=2,
        channel_level="CHANNEL_6_REPEATABLE",
    )
    economics = UnitEconomicsProfile(
        price=1500.0,
        cost_to_deliver=300.0,
        customer_acquisition_cost=500.0,
        economics_status="UNIT_ECONOMICS_STRONG",
    )
    risk = BusinessRiskAssessment(risk_status="RISK_LOW")
    kill = KillCriteria(
        kill_trigger="0 paid pilots",
        pivot_trigger="CAC too high",
        justifies_next_test="1 paid pilot",
        justifies_investment="3 paid pilots",
        has_failure_threshold=True,
    )

    before = evaluate_business_validation_gate(canvas, wtp, channel, economics, risk, kill)
    run_repository_orchestration_audit_campaign(Path("."))
    after = evaluate_business_validation_gate(canvas, wtp, channel, economics, risk, kill)

    assert before.model_dump() == after.model_dump()
