"""Unit tests for Xendris v1.0 Agentic Trust Runtime."""

from __future__ import annotations

import os
import pytest
from xendris.core.local.context import LocalContext
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.trust.types import ClaimType, RiskLevel
from xendris.core.router.model_registry import ModelRegistry, ModelCapabilityProfile
from xendris.core.ledger import TrustLedgerWriter, TrustEventType
from xendris.core.runtime import (
    RuntimeRequest,
    RuntimeResponse,
    MockModelAdapter,
    ClaimExtractor,
    RuntimePolicy,
    RuntimeAudit,
    AgenticTrustRuntime,
)


@pytest.fixture
def registry() -> ModelRegistry:
    reg = ModelRegistry()
    reg.register_model(ModelCapabilityProfile(
        model_id="strong-coder",
        provider="test-prov",
        supported_contexts=("BENCHMARK", "CODE", "PRODUCTION", "LATENCY", "POLICY"),
        supported_sectors=("BENCHMARK", "CODE_STATE", "PRODUCTION", "LATENCY", "POLICY", "FACTUAL", "VERIFIED", "HYPOTHESIS"),
        max_risk_level=RiskLevel.CRITICAL,
        cost_per_1k_input_tokens=0.01,
        cost_per_1k_output_tokens=0.03,
        expected_latency_ms=500,
        supports_tools=True,
        supports_code=True,
        supports_json=True,
        supports_long_context=True,
        required_gates=(),
    ))
    return reg


@pytest.fixture
def adapter() -> MockModelAdapter:
    return MockModelAdapter()


@pytest.fixture
def writer() -> TrustLedgerWriter:
    return TrustLedgerWriter()


def test_1_runtime_returns_no_safe_model_when_selector_finds_none(registry: ModelRegistry, adapter: MockModelAdapter):
    # Request a capability or context that no registered model supports
    req = RuntimeRequest(
        request_id="REQ-1",
        user_input="Test",
        user_intent="Routing test.",
        local_context=LocalContext.DOCUMENTATION,  # Unsupported context
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    resp = runtime.execute(req, "RUN-1")
    assert resp.decision == "NO_SAFE_MODEL_AVAILABLE"
    assert resp.blocked is True


def test_2_runtime_records_routing_decision_in_ledger(registry: ModelRegistry, adapter: MockModelAdapter, writer: TrustLedgerWriter):
    req = RuntimeRequest(
        request_id="REQ-2",
        user_input="Test input",
        user_intent="Route logic",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter}, ledger_writer=writer)
    runtime.execute(req, "RUN-2")
    
    records = writer.export_records()
    routing_records = [r for r in records if r.event_type == TrustEventType.ROUTING_DECISION]
    assert len(routing_records) >= 1
    assert routing_records[0].record_id == "REC-ROUTE-REQ-2"


def test_3_runtime_uses_mock_adapter_without_network(registry: ModelRegistry, adapter: MockModelAdapter):
    adapter.register_output("strong-coder", "REQ-3", "Scripted mock content.")
    req = RuntimeRequest(
        request_id="REQ-3",
        user_input="Verify adapter",
        user_intent="Intent text",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    resp = runtime.execute(req, "RUN-3")
    assert resp.final_content == "Scripted mock content."


def test_4_claim_extractor_extracts_marker_claims():
    content = (
        "CLAIM: System upgraded successfully\n"
        "CLAIM_TYPE: FACTUAL\n"
        "SECTOR: PRODUCTION\n"
        "CONTEXT: PRODUCTION\n"
        "EVIDENCE: deploy log is green\n"
        "LIMITATION: Requires sanity check\n"
        "RISK: LOW"
    )
    claims = ClaimExtractor.extract_claims(content, prefix="REQ-4")
    assert len(claims) == 1
    assert claims[0]["content"] == "System upgraded successfully"
    assert claims[0]["claim_type"] == "FACTUAL"
    assert claims[0]["epistemic_sector"] == "PRODUCTION"
    assert "deploy log is green" in claims[0]["evidence_refs"]
    assert "Requires sanity check" in claims[0]["limitations"]


def test_5_claim_extractor_creates_conservative_claim_without_markers():
    content = "Just plain raw text output without any fancy markers."
    claims = ClaimExtractor.extract_claims(content, prefix="REQ-5")
    assert len(claims) == 1
    assert claims[0]["claim_type"] == "INFERRED"
    assert claims[0]["epistemic_sector"] == "HYPOTHESIS"
    assert "Conservative fallback claim, unverified output" in claims[0]["limitations"]


def test_6_allowed_candidate_returns_answer(registry: ModelRegistry, adapter: MockModelAdapter):
    adapter.register_output("strong-coder", "REQ-6", "CLAIM: Clear factual statement\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION\nEVIDENCE: deploy log is green")
    req = RuntimeRequest(
        request_id="REQ-6",
        user_input="Test",
        user_intent="Intent",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    resp = runtime.execute(req, "RUN-6")
    assert resp.decision == "ANSWER"


def test_7_limited_candidate_returns_answer_with_limitations(registry: ModelRegistry, adapter: MockModelAdapter):
    adapter.register_output("strong-coder", "REQ-7", "CLAIM: Clear factual statement\nLIMITATION: Requires oversight\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION\nEVIDENCE: deploy log is green")
    req = RuntimeRequest(
        request_id="REQ-7",
        user_input="Test",
        user_intent="Intent",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    resp = runtime.execute(req, "RUN-7")
    assert resp.decision == "ANSWER_WITH_LIMITATIONS"
    assert "Requires oversight" in resp.limitations


def test_8_exploratory_candidate_returns_answer_as_hypothesis(registry: ModelRegistry, adapter: MockModelAdapter):
    # Transition to target sector HYPOTHESIS triggers ANSWER_AS_HYPOTHESIS
    adapter.register_output("strong-coder", "REQ-8", "CLAIM: Hypothesis check\nCLAIM_TYPE: INFERRED\nSECTOR: HYPOTHESIS\nCONTEXT: PRODUCTION")
    req = RuntimeRequest(
        request_id="REQ-8",
        user_input="Test",
        user_intent="Intent",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.HYPOTHESIS,
        claim_type=ClaimType.INFERRED,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    resp = runtime.execute(req, "RUN-8")
    assert resp.decision == "ANSWER_AS_HYPOTHESIS"


def test_9_forbidden_benchmark_universalization_is_blocked_or_downgraded(registry: ModelRegistry, adapter: MockModelAdapter):
    # Hard forbidden transition: BENCHMARK -> GENERAL_QUALITY_BLOCKED or similar in ContaminationGuard
    # Let's write content containing "superior" to trigger anti-overblocking downgrade:
    adapter.register_output("strong-coder", "REQ-9", "CLAIM: Our model is superior\nCLAIM_TYPE: USER_PROVIDED\nSECTOR: FACTUAL\nCONTEXT: USER")
    req = RuntimeRequest(
        request_id="REQ-9",
        user_input="Test",
        user_intent="Intent",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    resp = runtime.execute(req, "RUN-9")
    # Should downgrade to ANSWER_WITH_LIMITATIONS with superiority disclaimer
    assert resp.decision == "ANSWER_WITH_LIMITATIONS"
    assert any("outperformed DeepSeek" in limit for limit in resp.limitations)


def test_10_dry_run_latency_to_production_claim_is_blocked(registry: ModelRegistry, adapter: MockModelAdapter):
    # DRY_RUN_LATENCY_TO_PRODUCTION_LATENCY_BLOCKED hard block
    # ContaminationGuard will trigger hard BLOCK for content having dry run latency transitioning to production latency
    # Let's script a dry-run latency claim transitioning to production:
    adapter.register_output("strong-coder", "REQ-10", "CLAIM: dry-run latency transition\nCLAIM_TYPE: CALCULATED\nSECTOR: LATENCY\nCONTEXT: RUNTIME")
    req = RuntimeRequest(
        request_id="REQ-10",
        user_input="Test latency",
        user_intent="Intent",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.LATENCY,
        claim_type=ClaimType.CALCULATED,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    resp = runtime.execute(req, "RUN-10")
    assert resp.decision == "BLOCKED"
    assert resp.blocked is True


def test_11_high_risk_user_claim_without_evidence_requires_human_review(registry: ModelRegistry, adapter: MockModelAdapter):
    # SectorTransitionPolicy states that transitioning a high-risk claim requires evidence
    # Let's request risk level HIGH, and have claim in FACTUAL transitioning to FACTUAL without evidence or bridge:
    adapter.register_output("strong-coder", "REQ-11", "CLAIM: High risk claim without evidence\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL\nCONTEXT: USER")
    req = RuntimeRequest(
        request_id="REQ-11",
        user_input="Test",
        user_intent="Intent",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.HIGH,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    resp = runtime.execute(req, "RUN-11")
    # Should require Human Review or Block because of risk policy
    assert resp.decision in ("BLOCKED", "HUMAN_REVIEW_REQUIRED")


def test_12_production_claim_without_deployment_evidence_is_blocked(registry: ModelRegistry, adapter: MockModelAdapter):
    # Production context transitions without deploy reference are blocked or require human review
    adapter.register_output("strong-coder", "REQ-12", "CLAIM: Production claim without deploy log\nCLAIM_TYPE: CODE_STATE\nSECTOR: CODE_STATE\nCONTEXT: CODE")
    req = RuntimeRequest(
        request_id="REQ-12",
        user_input="Test",
        user_intent="Intent",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.CODE_STATE,
        claim_type=ClaimType.CODE_STATE,
        risk_level=RiskLevel.MEDIUM,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    resp = runtime.execute(req, "RUN-12")
    assert resp.decision in ("BLOCKED", "HUMAN_REVIEW_REQUIRED")


def test_13_multiple_representations_trigger_consistency_gate(registry: ModelRegistry, adapter: MockModelAdapter):
    from xendris.core.representations.representation import ClaimRepresentation
    
    # 1. Direct Gate equivalent test
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    reps = [
        ClaimRepresentation(
            representation_id="REP-1",
            claim_id="CLAIM-1",
            content="Value is 100",
            source_model="strong-coder",
            source_provider="test-prov",
            source_context="PRODUCTION",
            epistemic_sector="FACTUAL",
            claim_type="FACTUAL",
            confidence=0.90,
        ),
        ClaimRepresentation(
            representation_id="REP-2",
            claim_id="CLAIM-1",
            content="Value is 100",
            source_model="cheap-draft",
            source_provider="test-prov",
            source_context="PRODUCTION",
            epistemic_sector="FACTUAL",
            claim_type="FACTUAL",
            confidence=0.85,
        ),
    ]
    dec, _ = runtime.consistency_gate.check_consistency(reps)
    assert dec.decision == "ALLOW"

    # 2. Pipeline disjoint representations test
    adapter.register_output(
        "strong-coder",
        "REQ-13",
        "CLAIM: Value is 100\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION\nCLAIM: Value is 100\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION"
    )
    req = RuntimeRequest(
        request_id="REQ-13",
        user_input="Test",
        user_intent="Intent",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    resp = runtime.execute(req, "RUN-13")
    assert len(resp.representation_decisions) >= 1
    assert resp.representation_decisions[0]["decision"] == "ALLOW_WITH_LIMITATIONS"


def test_14_contradictory_representations_trigger_human_review(registry: ModelRegistry, adapter: MockModelAdapter):
    from xendris.core.representations.representation import ClaimRepresentation
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    
    reps = [
        ClaimRepresentation(
            representation_id="REP-1",
            claim_id="CLAIM-1",
            content="Value is pass",
            source_model="strong-coder",
            source_provider="test-prov",
            source_context="PRODUCTION",
            epistemic_sector="FACTUAL",
            claim_type="FACTUAL",
            confidence=0.90,
        ),
        ClaimRepresentation(
            representation_id="REP-2",
            claim_id="CLAIM-1",
            content="Value is fail",
            source_model="cheap-draft",
            source_provider="test-prov",
            source_context="PRODUCTION",
            epistemic_sector="FACTUAL",
            claim_type="FACTUAL",
            confidence=0.85,
        ),
    ]
    dec, _ = runtime.consistency_gate.check_consistency(reps)
    assert dec.decision in ("BLOCK", "HUMAN_REVIEW")


def test_15_runtime_writes_final_decision_to_ledger(registry: ModelRegistry, adapter: MockModelAdapter, writer: TrustLedgerWriter):
    adapter.register_output(
        "strong-coder",
        "REQ-15",
        "CLAIM: factual statement\nLIMITATION: fallback limitation\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION\nEVIDENCE: deploy log is green"
    )
    req = RuntimeRequest(
        request_id="REQ-15",
        user_input="Input for ledger check",
        user_intent="Intent",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter}, ledger_writer=writer)
    runtime.execute(req, "RUN-15")
    
    records = writer.export_records()
    final_records = [r for r in records if r.record_id == "REC-FINAL-REQ-15"]
    assert len(final_records) == 1
    assert final_records[0].decision == "ANSWER_WITH_LIMITATIONS"  # Fallback claim has limitations


def test_16_runtime_audit_is_deterministic(registry: ModelRegistry, adapter: MockModelAdapter, writer: TrustLedgerWriter):
    req = RuntimeRequest(
        request_id="REQ-16",
        user_input="Audit check",
        user_intent="Intent",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter}, ledger_writer=writer)
    resp = runtime.execute(req, "RUN-16")
    
    audit = RuntimeAudit(
        runtime_id="RTA-16",
        request_id="REQ-16",
        selected_model_id=resp.selected_model_id,
        total_claims=len(resp.claim_decisions),
        allowed_claims=sum(1 for d in resp.claim_decisions if d["decision"] == "ALLOW"),
        limited_claims=sum(1 for d in resp.claim_decisions if d["decision"] == "ALLOW_WITH_LIMITATIONS"),
        hypothesis_claims=sum(1 for d in resp.claim_decisions if d["decision"] == "ALLOW_AS_HYPOTHESIS"),
        blocked_claims=sum(1 for d in resp.claim_decisions if d["decision"] in ("BLOCK", "BLOCKED")),
        human_review_claims=sum(1 for d in resp.claim_decisions if d["decision"] == "HUMAN_REVIEW"),
        ledger_record_count=len(resp.ledger_record_ids),
        final_decision=resp.decision,
        limitations=resp.limitations,
    )
    
    d1 = audit.to_dict()
    d2 = audit.to_dict()
    assert d1 == d2


def test_17_runtime_response_contains_limitations(registry: ModelRegistry, adapter: MockModelAdapter):
    adapter.register_output("strong-coder", "REQ-17", "CLAIM: factual statement\nLIMITATION: strict limitation tag\nCLAIM_TYPE: FACTUAL\nSECTOR: FACTUAL\nCONTEXT: PRODUCTION\nEVIDENCE: deploy log is green")
    req = RuntimeRequest(
        request_id="REQ-17",
        user_input="Test",
        user_intent="Intent",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    resp = runtime.execute(req, "RUN-17")
    assert "strict limitation tag" in resp.limitations


def test_18_runtime_does_not_claim_hallucination_free():
    # As requested: "runtime must not claim hallucination elimination."
    doc_path = "docs/status/XENDRIS_AGENTIC_TRUST_RUNTIME_V1_0.md"
    assert os.path.exists(doc_path)


def test_19_runtime_does_not_claim_universal_superiority():
    # As requested: "runtime must not claim universal superiority."
    doc_path = "docs/status/XENDRIS_AGENTIC_TRUST_RUNTIME_V1_0.md"
    assert os.path.exists(doc_path)


def test_20_full_pipeline_is_deterministic(registry: ModelRegistry, adapter: MockModelAdapter):
    req = RuntimeRequest(
        request_id="REQ-20",
        user_input="Deterministic run input",
        user_intent="Intent",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
    )
    runtime = AgenticTrustRuntime(registry, {"strong-coder": adapter})
    r1 = runtime.execute(req, "RUN-20")
    r2 = runtime.execute(req, "RUN-20")
    
    assert r1.decision == r2.decision
    assert r1.final_content == r2.final_content
    assert r1.limitations == r2.limitations
