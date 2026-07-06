from xendris.core.trust import (
    AuditDecision,
    BenchmarkReadiness,
    ClaimStatus,
    ClaimType,
    Evidence,
    EvidenceType,
    QualityAction,
    QualityPriority,
    RiskLevel,
    TrustKernelEvaluator,
    bind_evidence_to_claim,
    build_quality_improvement_plan,
    make_claim,
    validate_quality_improvement_plan,
)
from xendris.core.response_contract import assess_response_contract


def test_verified_low_risk_audit_is_structurally_benchmark_ready():
    claim = make_claim(
        text="The response contract tests passed.",
        claim_type=ClaimType.CODE_STATE,
        confidence=0.96,
        status=ClaimStatus.VERIFIED,
    )
    evidence = Evidence(
        evidence_id="EV-TEST-RESPONSE-CONTRACT",
        evidence_type=EvidenceType.TEST_RESULT,
        source="pytest",
        content_hash="response-contract-tests-passed",
        excerpt="tests passed",
        confidence=0.96,
    )
    audit = TrustKernelEvaluator().evaluate(
        answer="The response contract tests passed.",
        claims=(claim,),
        evidence_bindings=(bind_evidence_to_claim(claim, (evidence,)),),
    )

    plan = build_quality_improvement_plan(audit)

    assert audit.decision == AuditDecision.APPROVED
    assert plan.action == QualityAction.ACCEPT
    assert plan.priority == QualityPriority.LOW
    assert plan.benchmark_readiness == BenchmarkReadiness.READY
    assert plan.quality_score >= 0.9
    assert "factual validation" in plan.suggested_next_steps[-1]
    assert plan.is_benchmark_ready() is True
    assert validate_quality_improvement_plan(plan, audit) is True


def test_unsupported_limited_audit_requires_limitations_before_benchmark_use():
    claim = make_claim(
        text="This answer may improve benchmark outcomes under these assumptions.",
        claim_type=ClaimType.UNSUPPORTED,
        confidence=0.45,
        status=ClaimStatus.UNSUPPORTED,
    )
    audit = TrustKernelEvaluator().evaluate(
        answer="This answer may improve benchmark outcomes under these assumptions.",
        claims=(claim,),
    )

    plan = build_quality_improvement_plan(audit)

    assert audit.decision == AuditDecision.APPROVED_WITH_LIMITATIONS
    assert plan.action == QualityAction.ADD_LIMITATIONS
    assert plan.priority == QualityPriority.MEDIUM
    assert plan.benchmark_readiness == BenchmarkReadiness.READY_WITH_LIMITATIONS
    assert plan.quality_score < audit.global_confidence
    assert plan.is_benchmark_ready() is True
    assert validate_quality_improvement_plan(plan, audit) is True


def test_high_confidence_unsupported_audit_is_not_benchmark_ready():
    claim = make_claim(
        text="Xendris will always raise every model benchmark considerably.",
        claim_type=ClaimType.UNSUPPORTED,
        confidence=0.91,
        status=ClaimStatus.UNSUPPORTED,
    )
    audit = TrustKernelEvaluator().evaluate(
        answer="Xendris will always raise every model benchmark considerably.",
        claims=(claim,),
    )

    plan = build_quality_improvement_plan(audit)

    assert audit.decision == AuditDecision.HUMAN_REVIEW_REQUIRED
    assert plan.action == QualityAction.REQUIRE_HUMAN_REVIEW
    assert plan.priority == QualityPriority.HIGH
    assert plan.benchmark_readiness == BenchmarkReadiness.NOT_READY
    assert plan.quality_score < 0.7
    assert plan.is_benchmark_ready() is False
    assert validate_quality_improvement_plan(plan, audit) is True


def test_contradicted_audit_blocks_benchmark_use():
    claim = make_claim(
        text="The result is both passed and failed.",
        claim_type=ClaimType.CODE_STATE,
        confidence=0.9,
        status=ClaimStatus.CONTRADICTED,
    )
    audit = TrustKernelEvaluator().evaluate(
        answer="The result is both passed and failed.",
        claims=(claim,),
    )

    plan = build_quality_improvement_plan(audit)

    assert audit.risk_level == RiskLevel.HIGH
    assert plan.action == QualityAction.BLOCK_OUTPUT
    assert plan.priority == QualityPriority.CRITICAL
    assert plan.benchmark_readiness == BenchmarkReadiness.NOT_READY
    assert plan.quality_score <= 0.3
    assert plan.is_benchmark_ready() is False
    assert validate_quality_improvement_plan(plan, audit) is True


def test_quality_plan_exports_json_safe_shape():
    audit = TrustKernelEvaluator().evaluate(
        answer="No claims were declared.",
        claims=(),
    )

    plan = build_quality_improvement_plan(audit)
    payload = plan.to_dict()

    assert payload["action"] == QualityAction.REQUIRE_HUMAN_REVIEW.value
    assert payload["benchmark_readiness"] == BenchmarkReadiness.NOT_READY.value
    assert isinstance(payload["target_dimensions"], list)
    assert isinstance(payload["suggested_next_steps"], list)


def test_response_contract_overclaim_downgrades_otherwise_approved_audit():
    claim = make_claim(
        text="The calculation follows from the supplied equation.",
        claim_type=ClaimType.CALCULATED,
        confidence=0.92,
        status=ClaimStatus.VERIFIED,
    )
    evidence = Evidence(
        evidence_id="EV-CALC-001",
        evidence_type=EvidenceType.DERIVED_PROOF,
        source="local derivation",
        content_hash="derived-proof-001",
        excerpt="calculation checked",
        confidence=0.92,
    )
    audit = TrustKernelEvaluator().evaluate(
        answer="The calculation is exactly universal and guaranteed.",
        claims=(claim,),
        evidence_bindings=(bind_evidence_to_claim(claim, (evidence,)),),
    )
    response_assessment = assess_response_contract(
        "The calculation is exactly universal and guaranteed."
    )

    plan = build_quality_improvement_plan(audit, response_assessment)

    assert audit.decision == AuditDecision.APPROVED
    assert response_assessment.is_conservative() is False
    assert plan.action == QualityAction.ADD_LIMITATIONS
    assert plan.benchmark_readiness == BenchmarkReadiness.READY_WITH_LIMITATIONS
    assert plan.quality_score < audit.global_confidence
    assert validate_quality_improvement_plan(plan, audit) is True


def test_quality_plan_contract_rejects_impossible_acceptance():
    claim = make_claim(
        text="The result is contradicted.",
        claim_type=ClaimType.FACTUAL,
        confidence=0.9,
        status=ClaimStatus.CONTRADICTED,
    )
    audit = TrustKernelEvaluator().evaluate(
        answer="The result is contradicted.",
        claims=(claim,),
    )
    impossible_plan = build_quality_improvement_plan(audit)
    object.__setattr__(impossible_plan, "action", QualityAction.ACCEPT)
    object.__setattr__(impossible_plan, "priority", QualityPriority.LOW)
    object.__setattr__(
        impossible_plan,
        "benchmark_readiness",
        BenchmarkReadiness.READY,
    )

    assert validate_quality_improvement_plan(impossible_plan) is True
    assert validate_quality_improvement_plan(impossible_plan, audit) is False


def test_quality_plan_contract_rejects_not_ready_low_priority():
    claim = make_claim(
        text="Human review is required.",
        claim_type=ClaimType.UNSUPPORTED,
        confidence=0.91,
        status=ClaimStatus.UNSUPPORTED,
    )
    audit = TrustKernelEvaluator().evaluate(
        answer="Human review is required.",
        claims=(claim,),
    )
    plan = build_quality_improvement_plan(audit)
    object.__setattr__(plan, "priority", QualityPriority.LOW)

    assert validate_quality_improvement_plan(plan) is False
