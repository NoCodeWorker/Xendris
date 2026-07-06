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


def _human_review_required_plan():
    claim = make_claim(
        text="This requires review.",
        claim_type=ClaimType.FACTUAL,
        confidence=0.95,
        status=ClaimStatus.VERIFIED,
    )
    # Factual claim without evidence requires human review
    audit = TrustKernelEvaluator().evaluate(
        answer="This requires review.",
        claims=(claim,),
    )
    return build_quality_improvement_plan(audit)


def test_unsupported_scoring_rule_excludes_from_scoring():
    plan = _approved_quality_plan()
    result = gate_benchmark_output(
        quality_plan=plan,
        response_text="Standard output.",
        runtime_metadata={"unsupported_scoring_rule": True},
    )
    assert result.decision == BenchmarkGateDecision.EXCLUDE
    assert result.reason == BenchmarkExclusionReason.UNSUPPORTED_SCORING_RULE
    assert result.include_in_scoring is False


def test_latency_below_threshold_does_not_imply_correctness():
    plan = _approved_quality_plan()
    result = gate_benchmark_output(
        quality_plan=plan,
        response_text="Standard output.",
        runtime_metadata={
            "latency_as_proxy": True,
            "latency_ms": 12.5,
            "policy_validated": False,
        },
    )
    assert result.decision == BenchmarkGateDecision.EXCLUDE
    assert result.reason == BenchmarkExclusionReason.LATENCY_PROXIED_WITHOUT_POLICY
    assert result.include_in_scoring is False

    # If policy is validated, it shouldn't exclude for this reason
    result_validated = gate_benchmark_output(
        quality_plan=plan,
        response_text="Standard output.",
        runtime_metadata={
            "latency_as_proxy": True,
            "latency_ms": 12.5,
            "policy_validated": True,
        },
    )
    assert result_validated.decision == BenchmarkGateDecision.INCLUDE
    assert result_validated.reason == BenchmarkExclusionReason.NONE


def test_user_provided_benchmark_rule_without_evidence_is_excluded():
    plan = _approved_quality_plan()
    result = gate_benchmark_output(
        quality_plan=plan,
        response_text="Standard output.",
        runtime_metadata={"user_rule_without_evidence": True},
    )
    assert result.decision == BenchmarkGateDecision.EXCLUDE
    assert result.reason == BenchmarkExclusionReason.USER_RULE_WITHOUT_EVIDENCE
    assert result.include_in_scoring is False


def test_human_review_is_not_used_when_deterministic_exclusion_is_possible():
    # Plan requires human review
    plan = _human_review_required_plan()
    assert plan.benchmark_readiness == BenchmarkReadiness.NOT_READY
    assert plan.action == QualityAction.REQUIRE_HUMAN_REVIEW

    # With timeout, excludes with TIMEOUT reason, not HUMAN_REVIEW_REQUIRED
    result_timeout = gate_benchmark_output(
        quality_plan=plan,
        response_text="Standard output.",
        runtime_metadata={"timeout": True},
    )
    assert result_timeout.decision == BenchmarkGateDecision.EXCLUDE
    assert result_timeout.reason == BenchmarkExclusionReason.TIMEOUT

    # With unsupported scoring rule, excludes with UNSUPPORTED_SCORING_RULE
    result_rule = gate_benchmark_output(
        quality_plan=plan,
        response_text="Standard output.",
        runtime_metadata={"unsupported_scoring_rule": True},
    )
    assert result_rule.decision == BenchmarkGateDecision.EXCLUDE
    assert result_rule.reason == BenchmarkExclusionReason.UNSUPPORTED_SCORING_RULE


def test_human_review_remains_available_for_genuine_unresolved_ambiguity():
    plan = _human_review_required_plan()

    # Genuine case 1: evidence conflict
    res1 = gate_benchmark_output(
        quality_plan=plan,
        response_text="Standard output.",
        runtime_metadata={"has_evidence_conflict": True},
    )
    assert res1.decision == BenchmarkGateDecision.EXCLUDE
    assert res1.reason == BenchmarkExclusionReason.HUMAN_REVIEW_REQUIRED

    # Genuine case 2: unresolved ambiguity
    res2 = gate_benchmark_output(
        quality_plan=plan,
        response_text="Standard output.",
        runtime_metadata={"has_unresolved_ambiguity": True},
    )
    assert res2.decision == BenchmarkGateDecision.EXCLUDE
    assert res2.reason == BenchmarkExclusionReason.HUMAN_REVIEW_REQUIRED

    # Genuine case 3: explicit policy review
    res3 = gate_benchmark_output(
        quality_plan=plan,
        response_text="Standard output.",
        runtime_metadata={"policy_requires_explicit_review": True},
    )
    assert res3.decision == BenchmarkGateDecision.EXCLUDE
    assert res3.reason == BenchmarkExclusionReason.HUMAN_REVIEW_REQUIRED

    # Genuine case 4: critical claims partial support
    res4 = gate_benchmark_output(
        quality_plan=plan,
        response_text="Standard output.",
        runtime_metadata={"critical_claims_partial_support": True},
    )
    assert res4.decision == BenchmarkGateDecision.EXCLUDE
    assert res4.reason == BenchmarkExclusionReason.HUMAN_REVIEW_REQUIRED

    # Non-genuine case: metadata is present but none of the review triggers are True
    res_nongenuine = gate_benchmark_output(
        quality_plan=plan,
        response_text="Standard output.",
        runtime_metadata={"latency_ms": 250.0},
    )
    assert res_nongenuine.decision == BenchmarkGateDecision.EXCLUDE
    assert res_nongenuine.reason == BenchmarkExclusionReason.TRUST_NOT_READY
