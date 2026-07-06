from xendris.core.trust import (
    AuditDecision,
    BenchmarkExclusionReason,
    BenchmarkGateDecision,
    BenchmarkReadiness,
    ClaimStatus,
    ClaimType,
    Evidence,
    EvidenceType,
    QualityAction,
    RiskLevel,
    TrustKernelEvaluator,
    bind_evidence_to_claim,
    build_quality_improvement_plan,
    gate_benchmark_output,
    make_claim,
)


def _approved_quality_plan():
    claim = make_claim(
        text="The deterministic trust tests passed.",
        claim_type=ClaimType.CODE_STATE,
        confidence=0.95,
        status=ClaimStatus.VERIFIED,
    )
    evidence = Evidence(
        evidence_id="EV-BENCH-GATE-001",
        evidence_type=EvidenceType.TEST_RESULT,
        source="pytest",
        content_hash="trust-tests-passed",
        excerpt="trust tests passed",
        confidence=0.95,
    )
    audit = TrustKernelEvaluator().evaluate(
        answer="The deterministic trust tests passed.",
        claims=(claim,),
        evidence_bindings=(bind_evidence_to_claim(claim, (evidence,)),),
    )
    return build_quality_improvement_plan(audit)


def test_benchmark_gate_includes_ready_output():
    plan = _approved_quality_plan()

    result = gate_benchmark_output(
        quality_plan=plan,
        response_text="The deterministic trust tests passed.",
    )

    assert result.decision == BenchmarkGateDecision.INCLUDE
    assert result.reason == BenchmarkExclusionReason.NONE
    assert result.include_in_scoring is True
    assert result.requires_limitation_note is False
    assert result.quality_score == plan.quality_score


def test_benchmark_gate_includes_limited_output_with_note():
    claim = make_claim(
        text="This answer may improve benchmark hygiene.",
        claim_type=ClaimType.UNSUPPORTED,
        confidence=0.45,
        status=ClaimStatus.UNSUPPORTED,
    )
    audit = TrustKernelEvaluator().evaluate(
        answer="This answer may improve benchmark hygiene.",
        claims=(claim,),
    )
    plan = build_quality_improvement_plan(audit)

    result = gate_benchmark_output(
        quality_plan=plan,
        response_text="This answer may improve benchmark hygiene.",
    )

    assert plan.benchmark_readiness == BenchmarkReadiness.READY_WITH_LIMITATIONS
    assert result.decision == BenchmarkGateDecision.INCLUDE_WITH_LIMITATIONS
    assert result.reason == BenchmarkExclusionReason.LIMITED_READINESS
    assert result.include_in_scoring is True
    assert result.requires_limitation_note is True


def test_benchmark_gate_excludes_runtime_error_even_when_plan_is_ready():
    result = gate_benchmark_output(
        quality_plan=_approved_quality_plan(),
        response_text="The deterministic trust tests passed.",
        runtime_metadata={"error": "provider unavailable"},
    )

    assert result.decision == BenchmarkGateDecision.EXCLUDE
    assert result.reason == BenchmarkExclusionReason.RUNTIME_ERROR
    assert result.include_in_scoring is False
    assert result.quality_score == 0.0


def test_benchmark_gate_excludes_timeout_before_scoring():
    result = gate_benchmark_output(
        quality_plan=_approved_quality_plan(),
        response_text="The deterministic trust tests passed.",
        runtime_metadata={"timeout": True},
    )

    assert result.decision == BenchmarkGateDecision.EXCLUDE
    assert result.reason == BenchmarkExclusionReason.TIMEOUT
    assert result.include_in_scoring is False
    assert result.requires_limitation_note is True


def test_benchmark_gate_excludes_fallback_text():
    result = gate_benchmark_output(
        quality_plan=_approved_quality_plan(),
        response_text="HTTP error fallback: provider did not respond.",
    )

    assert result.decision == BenchmarkGateDecision.EXCLUDE
    assert result.reason == BenchmarkExclusionReason.FALLBACK_RESPONSE
    assert result.include_in_scoring is False


def test_benchmark_gate_excludes_not_ready_quality_plan():
    claim = make_claim(
        text="Xendris will always improve every benchmark.",
        claim_type=ClaimType.UNSUPPORTED,
        confidence=0.9,
        status=ClaimStatus.UNSUPPORTED,
    )
    audit = TrustKernelEvaluator().evaluate(
        answer="Xendris will always improve every benchmark.",
        claims=(claim,),
    )
    plan = build_quality_improvement_plan(audit)

    result = gate_benchmark_output(
        quality_plan=plan,
        response_text="Xendris will always improve every benchmark.",
    )

    assert audit.decision == AuditDecision.HUMAN_REVIEW_REQUIRED
    assert audit.risk_level == RiskLevel.HIGH
    assert plan.action == QualityAction.REQUIRE_HUMAN_REVIEW
    assert result.decision == BenchmarkGateDecision.EXCLUDE
    assert result.reason == BenchmarkExclusionReason.HUMAN_REVIEW_REQUIRED
    assert result.include_in_scoring is False


def test_benchmark_gate_result_is_json_safe():
    result = gate_benchmark_output(
        quality_plan=_approved_quality_plan(),
        response_text="The deterministic trust tests passed.",
    )
    payload = result.to_dict()

    assert payload["decision"] == BenchmarkGateDecision.INCLUDE.value
    assert payload["reason"] == BenchmarkExclusionReason.NONE.value
    assert payload["include_in_scoring"] is True
