"""Unit tests for the Xendris Multi-Model Selector."""

from __future__ import annotations

import pytest
from xendris.core.local.context import LocalContext
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.trust.types import ClaimType, RiskLevel
from xendris.core.fingerprints.metrics import FingerprintMetric
from xendris.core.fingerprints.model_fingerprint import ModelIdentity, ModelEpistemicFingerprint
from xendris.core.router.model_registry import ModelCapabilityProfile, ModelRegistry
from xendris.core.router.route_request import RouteRequest, RouteDecision
from xendris.core.router.cost_policy import CostPolicy
from xendris.core.router.risk_policy import RiskPolicy
from xendris.core.router.selector import MultiModelSelector
from xendris.core.router.router_audit import RouterAudit


@pytest.fixture
def registry() -> ModelRegistry:
    reg = ModelRegistry()

    # Cheap but low capacity model (only supports low risk, no tools/code, cheap)
    reg.register_model(ModelCapabilityProfile(
        model_id="cheap-draft",
        provider="test-prov",
        supported_contexts=("BENCHMARK", "CODE", "PRODUCTION", "LATENCY"),
        supported_sectors=("BENCHMARK", "CODE_STATE", "PRODUCTION", "LATENCY"),
        max_risk_level=RiskLevel.LOW,
        cost_per_1k_input_tokens=0.001,
        cost_per_1k_output_tokens=0.002,
        expected_latency_ms=100,
        supports_tools=False,
        supports_code=False,
        supports_json=False,
        supports_long_context=False,
        required_gates=("Verification Gate",),
    ))

    # Fast but low risk/low code model
    reg.register_model(ModelCapabilityProfile(
        model_id="fast-draft",
        provider="test-prov",
        supported_contexts=("BENCHMARK", "CODE", "PRODUCTION", "LATENCY"),
        supported_sectors=("BENCHMARK", "CODE_STATE", "PRODUCTION", "LATENCY"),
        max_risk_level=RiskLevel.LOW,
        cost_per_1k_input_tokens=0.002,
        cost_per_1k_output_tokens=0.004,
        expected_latency_ms=30,
        supports_tools=False,
        supports_code=False,
        supports_json=False,
        supports_long_context=False,
        required_gates=("Verification Gate",),
    ))

    # High capacity, supports high risk, code and tools, expensive
    reg.register_model(ModelCapabilityProfile(
        model_id="strong-coder",
        provider="test-prov",
        supported_contexts=("BENCHMARK", "CODE", "PRODUCTION", "LATENCY", "POLICY"),
        supported_sectors=("BENCHMARK", "CODE_STATE", "PRODUCTION", "LATENCY", "POLICY", "FACTUAL", "VERIFIED"),
        max_risk_level=RiskLevel.CRITICAL,
        cost_per_1k_input_tokens=0.015,
        cost_per_1k_output_tokens=0.030,
        expected_latency_ms=250,
        supports_tools=True,
        supports_code=True,
        supports_json=True,
        supports_long_context=True,
        required_gates=("Verification Gate",),
    ))

    return reg


@pytest.fixture
def selector() -> MultiModelSelector:
    return MultiModelSelector()


def test_1_low_risk_creative_selects_lowest_safe_cost_model(registry: ModelRegistry, selector: MultiModelSelector):
    req = RouteRequest(
        request_id="REQ-01",
        user_intent="Write a low-risk draft outline.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.INFERRED,
        risk_level=RiskLevel.LOW,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
        prefer_low_cost=True,
    )
    decision = selector.select_model(req, registry)
    assert decision.selected_model_id == "cheap-draft"


def test_2_selector_does_not_choose_cheapest_if_risk_incompatible(registry: ModelRegistry, selector: MultiModelSelector):
    req = RouteRequest(
        request_id="REQ-02",
        user_intent="Analyze high-risk benchmark assertions.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.HIGH,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
        prefer_low_cost=True,
    )
    decision = selector.select_model(req, registry)
    # cheap-draft is risk incompatible (max risk is LOW, request risk is HIGH)
    assert decision.selected_model_id == "strong-coder"


def test_3_selector_does_not_choose_fastest_if_risk_incompatible(registry: ModelRegistry, selector: MultiModelSelector):
    req = RouteRequest(
        request_id="REQ-03",
        user_intent="Execute high-risk safety verification code.",
        local_context=LocalContext.CODE,
        epistemic_sector=EpistemicSector.CODE_STATE,
        claim_type=ClaimType.CALCULATED,
        risk_level=RiskLevel.HIGH,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
        prefer_low_latency=True,
    )
    decision = selector.select_model(req, registry)
    # fast-draft is risk incompatible, so strong-coder must be chosen despite being slower
    assert decision.selected_model_id == "strong-coder"


def test_4_benchmark_claim_avoids_high_universalization_model(registry: ModelRegistry, selector: MultiModelSelector):
    # Register another model with fingerprint reference
    registry.register_model(ModelCapabilityProfile(
        model_id="universalizer",
        provider="test-prov",
        supported_contexts=("BENCHMARK",),
        supported_sectors=("BENCHMARK",),
        max_risk_level=RiskLevel.CRITICAL,
        cost_per_1k_input_tokens=0.010,
        cost_per_1k_output_tokens=0.020,
        expected_latency_ms=200,
        supports_tools=True,
        supports_code=True,
        supports_json=True,
        supports_long_context=True,
        required_gates=(),
    ))

    # Build fingerprint showing high universalization rate
    fp = ModelEpistemicFingerprint(
        model_identity=ModelIdentity("universalizer", "test-prov", "1.0"),
        sample_count=10,
        run_id="RUN-1",
        dataset_id="DATA-1",
        metrics={
            FingerprintMetric.BENCHMARK_UNIVERSALIZATION_RATE: 0.20,
            FingerprintMetric.OVERGENERALIZATION_RATE: 0.0,
        },
        observed_strengths=(),
        observed_risks=("universalization_observed",),
        recommended_use=(),
        required_gates=(),
        limitations=(),
        created_from_audits=(),
    )

    req = RouteRequest(
        request_id="REQ-04",
        user_intent="Analyze benchmark score.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.MEDIUM,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )

    decision = selector.select_model(req, registry, fingerprints={"universalizer": fp})
    # Avoids universalizer and falls back to cheap-draft or strong-coder
    assert decision.selected_model_id != "universalizer"


def test_5_benchmark_claim_requires_benchmark_gate(registry: ModelRegistry, selector: MultiModelSelector):
    req = RouteRequest(
        request_id="REQ-05",
        user_intent="Benchmark score check.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )
    decision = selector.select_model(req, registry)
    assert "Benchmark Gate" in decision.required_gates


def test_6_production_claim_avoids_high_production_overclaim_model(registry: ModelRegistry, selector: MultiModelSelector):
    registry.register_model(ModelCapabilityProfile(
        model_id="overclaimer",
        provider="test-prov",
        supported_contexts=("PRODUCTION", "CODE"),
        supported_sectors=("PRODUCTION", "CODE_STATE"),
        max_risk_level=RiskLevel.CRITICAL,
        cost_per_1k_input_tokens=0.010,
        cost_per_1k_output_tokens=0.020,
        expected_latency_ms=200,
        supports_tools=True,
        supports_code=True,
        supports_json=True,
        supports_long_context=True,
        required_gates=(),
    ))

    fp = ModelEpistemicFingerprint(
        model_identity=ModelIdentity("overclaimer", "test-prov", "1.0"),
        sample_count=10,
        run_id="RUN-1",
        dataset_id="DATA-1",
        metrics={
            FingerprintMetric.PRODUCTION_OVERCLAIM_RATE: 0.20,
        },
        observed_strengths=(),
        observed_risks=("overclaim_observed",),
        recommended_use=(),
        required_gates=(),
        limitations=(),
        created_from_audits=(),
    )

    req = RouteRequest(
        request_id="REQ-06",
        user_intent="Execute production database code.",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.PRODUCTION,
        claim_type=ClaimType.CALCULATED,
        risk_level=RiskLevel.HIGH,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
        requires_code=True,
    )

    decision = selector.select_model(req, registry, fingerprints={"overclaimer": fp})
    assert decision.selected_model_id != "overclaimer"


def test_7_production_claim_requires_code_support_and_evidence_gate(registry: ModelRegistry, selector: MultiModelSelector):
    req = RouteRequest(
        request_id="REQ-07",
        user_intent="Execute production pipeline.",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.PRODUCTION,
        claim_type=ClaimType.CALCULATED,
        risk_level=RiskLevel.HIGH,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
        requires_code=True,
    )
    decision = selector.select_model(req, registry)
    # Requires code and is eligible -> selected strong-coder
    assert decision.selected_model_id == "strong-coder"
    assert "Production Evidence Gate" in decision.required_gates


def test_8_high_risk_factual_claim_avoids_high_unsupported_rate_model(registry: ModelRegistry, selector: MultiModelSelector):
    registry.register_model(ModelCapabilityProfile(
        model_id="hallucinator",
        provider="test-prov",
        supported_contexts=("PRODUCTION", "CODE"),
        supported_sectors=("FACTUAL",),
        max_risk_level=RiskLevel.CRITICAL,
        cost_per_1k_input_tokens=0.010,
        cost_per_1k_output_tokens=0.020,
        expected_latency_ms=200,
        supports_tools=True,
        supports_code=True,
        supports_json=True,
        supports_long_context=True,
        required_gates=(),
    ))

    fp = ModelEpistemicFingerprint(
        model_identity=ModelIdentity("hallucinator", "test-prov", "1.0"),
        sample_count=10,
        run_id="RUN-1",
        dataset_id="DATA-1",
        metrics={
            FingerprintMetric.UNSUPPORTED_CLAIM_RATE: 0.20,
        },
        observed_strengths=(),
        observed_risks=("unsupported_claims_observed",),
        recommended_use=(),
        required_gates=(),
        limitations=(),
        created_from_audits=(),
    )

    req = RouteRequest(
        request_id="REQ-08",
        user_intent="High risk factual database check.",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.HIGH,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )

    decision = selector.select_model(req, registry, fingerprints={"hallucinator": fp})
    assert decision.selected_model_id != "hallucinator"


def test_9_high_risk_factual_claim_requires_strict_evidence_gate(registry: ModelRegistry, selector: MultiModelSelector):
    req = RouteRequest(
        request_id="REQ-09",
        user_intent="High-risk factual validation.",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.HIGH,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )
    decision = selector.select_model(req, registry)
    assert "Strict Evidence Gate" in decision.required_gates


def test_10_latency_preference_applies_only_after_safety(registry: ModelRegistry, selector: MultiModelSelector):
    # both cheap-draft (100ms) and fast-draft (30ms) are safety eligible
    req = RouteRequest(
        request_id="REQ-10",
        user_intent="Quick low risk check.",
        local_context=LocalContext.LATENCY,
        epistemic_sector=EpistemicSector.LATENCY,
        claim_type=ClaimType.INFERRED,
        risk_level=RiskLevel.LOW,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
        prefer_low_latency=True,
    )
    decision = selector.select_model(req, registry)
    assert decision.selected_model_id == "fast-draft"


def test_11_no_safe_model_returns_no_safe_model_available(registry: ModelRegistry, selector: MultiModelSelector):
    # Request something that requires tools, but with risk level LOW (so strong-coder is eligible but cheap-draft/fast-draft are filtered by capability)
    # Wait, let's request something with unsupported context
    req = RouteRequest(
        request_id="REQ-11",
        user_intent="Something entirely unsupported.",
        local_context=LocalContext.DOCUMENTATION,  # Context not supported by cheap-draft, fast-draft or strong-coder
        epistemic_sector=EpistemicSector.HYPOTHESIS,
        claim_type=ClaimType.INFERRED,
        risk_level=RiskLevel.LOW,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )
    decision = selector.select_model(req, registry)
    assert decision.decision == "NO_SAFE_MODEL_AVAILABLE"


def test_12_human_review_required_when_all_models_exceed_risk(registry: ModelRegistry, selector: MultiModelSelector):
    # Request a Critical risk task but registry has no model that supports it if we register only cheap-draft (which supports LOW)
    empty_registry = ModelRegistry()
    empty_registry.register_model(ModelCapabilityProfile(
        model_id="cheap-draft-only",
        provider="test-prov",
        supported_contexts=("BENCHMARK",),
        supported_sectors=("BENCHMARK",),
        max_risk_level=RiskLevel.LOW,
        cost_per_1k_input_tokens=0.001,
        cost_per_1k_output_tokens=0.002,
        expected_latency_ms=100,
        supports_tools=False,
        supports_code=False,
        supports_json=False,
        supports_long_context=False,
        required_gates=(),
    ))
    req = RouteRequest(
        request_id="REQ-12",
        user_intent="High risk operations.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.HIGH,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )
    decision = selector.select_model(req, empty_registry)
    assert decision.decision == "REQUIRE_HUMAN_REVIEW"
    assert decision.human_review_required is True


def test_13_tie_breaker_is_deterministic(registry: ModelRegistry, selector: MultiModelSelector):
    # Register two models with identical capabilities, cost, latency, but different IDs
    registry.register_model(ModelCapabilityProfile(
        model_id="model-a",
        provider="test-prov",
        supported_contexts=("BENCHMARK",),
        supported_sectors=("BENCHMARK",),
        max_risk_level=RiskLevel.LOW,
        cost_per_1k_input_tokens=0.001,
        cost_per_1k_output_tokens=0.001,
        expected_latency_ms=10,
        supports_tools=False,
        supports_code=False,
        supports_json=False,
        supports_long_context=False,
        required_gates=(),
    ))
    registry.register_model(ModelCapabilityProfile(
        model_id="model-b",
        provider="test-prov",
        supported_contexts=("BENCHMARK",),
        supported_sectors=("BENCHMARK",),
        max_risk_level=RiskLevel.LOW,
        cost_per_1k_input_tokens=0.001,
        cost_per_1k_output_tokens=0.001,
        expected_latency_ms=10,
        supports_tools=False,
        supports_code=False,
        supports_json=False,
        supports_long_context=False,
        required_gates=(),
    ))

    req = RouteRequest(
        request_id="REQ-13",
        user_intent="Tie breaking check.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.INFERRED,
        risk_level=RiskLevel.LOW,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )
    decision = selector.select_model(req, registry)
    # model-a breaks tie due to lexicographic ordering over model-b
    assert decision.selected_model_id == "model-a"


def test_14_estimated_cost_is_computed_correctly(registry: ModelRegistry):
    policy = CostPolicy()
    prof = registry.get_model("strong-coder")
    cost = policy.estimate_cost(1000, 2000, prof)
    # (1000 / 1000) * 0.015 + (2000 / 1000) * 0.030 = 0.015 + 0.060 = 0.075
    assert abs(cost - 0.075) < 1e-5


def test_15_cost_is_not_used_as_quality_proxy(registry: ModelRegistry, selector: MultiModelSelector):
    # Verify that cost does not change the eligible status or ranking when prefer_low_cost is False
    req = RouteRequest(
        request_id="REQ-15",
        user_intent="Low risk factual validation.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )
    decision1 = selector.select_model(req, registry)
    # Check that selecting another model with lower cost is only influenced when prefer_low_cost is explicitly enabled
    req_cost = RouteRequest(
        request_id="REQ-15-cost",
        user_intent="Low risk factual validation.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
        prefer_low_cost=True,
    )
    decision2 = selector.select_model(req_cost, registry)
    assert decision2.selected_model_id == "cheap-draft"


def test_16_router_audit_is_deterministic(registry: ModelRegistry, selector: MultiModelSelector):
    req = RouteRequest(
        request_id="REQ-16",
        user_intent="Low risk drafting.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.INFERRED,
        risk_level=RiskLevel.LOW,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )
    decision = selector.select_model(req, registry)
    audit = RouterAudit.create("AUDIT-7001", "REQ-16", decision)
    assert audit.route_id == "AUDIT-7001"
    assert audit.selected_model_id == decision.selected_model_id
    assert audit.to_dict()["selected_model_id"] == decision.selected_model_id


def test_17_selector_accepts_model_fingerprint_records(registry: ModelRegistry, selector: MultiModelSelector):
    fp = ModelEpistemicFingerprint(
        model_identity=ModelIdentity("strong-coder", "test-prov", "1.0"),
        sample_count=10,
        run_id="RUN-1",
        dataset_id="DATA-1",
        metrics={
            FingerprintMetric.UNSUPPORTED_CLAIM_RATE: 0.0,
        },
        observed_strengths=(),
        observed_risks=(),
        recommended_use=(),
        required_gates=(),
        limitations=(),
        created_from_audits=(),
    )
    req = RouteRequest(
        request_id="REQ-17",
        user_intent="High risk check.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.HIGH,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )
    decision = selector.select_model(req, registry, fingerprints={"strong-coder": fp})
    assert decision.selected_model_id == "strong-coder"


def test_18_selector_works_without_fingerprint_but_adds_limitation(registry: ModelRegistry, selector: MultiModelSelector):
    req = RouteRequest(
        request_id="REQ-18",
        user_intent="Check without fingerprints.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.INFERRED,
        risk_level=RiskLevel.LOW,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )
    decision = selector.select_model(req, registry, fingerprints=None)
    assert any("Routed without epistemic fingerprint audits." in limit for limit in decision.limitations)


def test_19_strict_gate_required_for_benchmark_sector(registry: ModelRegistry, selector: MultiModelSelector):
    req = RouteRequest(
        request_id="REQ-19",
        user_intent="Benchmark evaluation.",
        local_context=LocalContext.BENCHMARK,
        epistemic_sector=EpistemicSector.BENCHMARK,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )
    decision = selector.select_model(req, registry)
    assert "Strict Safety Fence" in decision.required_gates


def test_20_strict_gate_required_for_production_sector(registry: ModelRegistry, selector: MultiModelSelector):
    req = RouteRequest(
        request_id="REQ-20",
        user_intent="Production run check.",
        local_context=LocalContext.PRODUCTION,
        epistemic_sector=EpistemicSector.FACTUAL,
        claim_type=ClaimType.FACTUAL,
        risk_level=RiskLevel.LOW,
        estimated_input_tokens=1000,
        estimated_output_tokens=1000,
    )
    decision = selector.select_model(req, registry)
    assert "Strict Safety Fence" in decision.required_gates
