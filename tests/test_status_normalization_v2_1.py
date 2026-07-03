from phyng.business_validation.gatekeeper import evaluate_business_validation_gate
from phyng.business_validation.schemas import (
    BusinessHypothesisCanvas,
    BusinessRiskAssessment,
    ChannelTest,
    KillCriteria,
    UnitEconomicsProfile,
    WillingnessToPayTest,
)
from phyng.core.blocked_reasons import CanonicalBlockedReason
from phyng.core.compatibility import (
    get_blocked_reasons,
    get_canonical_permission,
    is_blocked,
    normalize_status,
    requires_human_review,
)
from phyng.core.permissions import CanonicalPermission


def test_unknown_status_requires_review():
    record = normalize_status("NEW_UNMAPPED_STATUS", domain="test_domain")

    assert record.domain_status == "NEW_UNMAPPED_STATUS"
    assert record.domain == "test_domain"
    assert record.canonical_permission == CanonicalPermission.REVIEW_REQUIRED
    assert CanonicalBlockedReason.HUMAN_REVIEW_REQUIRED in record.blocked_reasons
    assert requires_human_review("NEW_UNMAPPED_STATUS")
    assert is_blocked("NEW_UNMAPPED_STATUS")


def test_normalization_does_not_mutate_original_status():
    original_status = "BUSINESS_BLOCKED_NO_WTP"
    record = normalize_status(original_status)

    assert original_status == "BUSINESS_BLOCKED_NO_WTP"
    assert record.domain_status == original_status
    assert get_canonical_permission(original_status) == CanonicalPermission.SCALE_BLOCKED
    assert get_blocked_reasons(original_status) == [CanonicalBlockedReason.NO_PAYMENT_SIGNAL]


def test_existing_gate_result_status_remains_unchanged_after_normalization():
    canvas = BusinessHypothesisCanvas(
        idea_id="BUS-CANONICAL-PRESERVE",
        business_idea="Technical diligence service",
        target_customer="VCs",
        problem="Need claim verification",
    )
    wtp = WillingnessToPayTest(
        offer="Audit",
        target_customer="VCs",
        price=1500.0,
        delivery_promise="Five day report",
        time_window_days=14,
        outreach_count=30,
        qualified_conversations_count=0,
        success_threshold="2 paid pilots",
        failure_threshold="0 paid pilots",
        wtp_level="WTP_1_INTEREST",
    )
    channel = ChannelTest(
        channel="Outbound",
        target_segment="VCs",
        message="Technical audit",
        outreach_volume=30,
        responses_received=2,
    )
    economics = UnitEconomicsProfile(
        price=1500.0,
        cost_to_deliver=300.0,
        customer_acquisition_cost=500.0,
    )
    risk = BusinessRiskAssessment(risk_status="RISK_LOW")
    kill = KillCriteria(
        kill_trigger="0 paid pilots",
        pivot_trigger="CAC too high",
        justifies_next_test="1 paid pilot",
        justifies_investment="3 paid pilots",
        has_failure_threshold=True,
    )
    result = evaluate_business_validation_gate(canvas, wtp, channel, economics, risk, kill)
    before = result.validation_status

    normalized = normalize_status(before)
    after = result.validation_status

    assert before == "BUSINESS_BLOCKED_NO_WTP"
    assert after == before
    assert normalized.canonical_permission == CanonicalPermission.SCALE_BLOCKED
