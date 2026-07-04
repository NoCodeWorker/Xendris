"""Unit tests for the Xendris Representation Consistency Gate."""

from __future__ import annotations

import pytest
from xendris.core.local.context import LocalContext
from xendris.core.boundary.evidence_bridge import EvidenceBridge, EvidenceBridgeType
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.representations.representation import ClaimRepresentation
from xendris.core.representations.equivalence import RepresentationRelation
from xendris.core.representations.consistency_gate import RepresentationConsistencyGate
from xendris.core.representations.representation_audit import RepresentationAudit
from xendris.core.trust.types import ClaimType


@pytest.fixture
def gate() -> RepresentationConsistencyGate:
    return RepresentationConsistencyGate()


def test_1_equivalent_representations_are_allowed(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-01",
        content="Benchmark score was 0.985 with version 1.0.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.9,
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-01",
        content="Benchmark score was 0.985 with version 1.0.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    assert decision.decision == "ALLOW"
    assert decision.relation == RepresentationRelation.EQUIVALENT


def test_2_partially_equivalent_representations_allowed_with_limitations(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-02",
        content="Accuracy is high with version 1.0.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.9,
        limitations=("Scoped to dry-run data",),
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-02",
        content="Accuracy is high with version 1.0.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    assert decision.decision == "ALLOW_WITH_LIMITATIONS"
    assert decision.relation == RepresentationRelation.PARTIALLY_EQUIVALENT


def test_3_contradiction_between_test_passed_and_failed_requires_human_review(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-03",
        content="Unit tests pass cleanly.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="CODE",
        epistemic_sector="CODE_STATE",
        claim_type="FACTUAL",
        confidence=0.9,
        evidence_refs=("pytest-run-success",),
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-03",
        content="Unit tests fail with errors.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="CODE",
        epistemic_sector="CODE_STATE",
        claim_type="FACTUAL",
        confidence=0.95,
        evidence_refs=("pytest-run-fail",),
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    # Critical risk contradicts pass vs fail -> HUMAN_REVIEW
    assert decision.decision == "HUMAN_REVIEW"
    assert decision.relation == RepresentationRelation.CONTRADICTORY


def test_4_production_ready_vs_not_verified_is_blocked_or_human_review(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-04",
        content="System is production ready.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="PRODUCTION",
        epistemic_sector="PRODUCTION",
        claim_type="FACTUAL",
        confidence=0.9,
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-04",
        content="System is not verified.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    # High risk ready vs not verified contradiction -> BLOCK
    assert decision.decision == "BLOCK"
    assert decision.relation == RepresentationRelation.CONTRADICTORY


def test_5_benchmark_limited_claim_vs_universal_superiority_detects_overgeneralization(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-05",
        content="Xendris won benchmark.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.9,
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-05",
        content="Xendris claims universal superiority.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="PRODUCTION",
        epistemic_sector="PRODUCTION",
        claim_type="FACTUAL",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    assert decision.decision == "BLOCK"  # CRITICAL overgeneralization
    assert decision.relation == RepresentationRelation.OVERGENERALIZED


def test_6_dry_run_latency_vs_production_latency_detects_overgeneralization(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-06",
        content="Dry-run latency was 5ms.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="LATENCY",
        epistemic_sector="LATENCY",
        claim_type="CALCULATED",
        confidence=0.9,
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-06",
        content="Production latency was 5ms.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="PRODUCTION",
        epistemic_sector="PRODUCTION",
        claim_type="CALCULATED",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    assert decision.decision == "ALLOW_WITH_LIMITATIONS"  # Downgraded to scoped claim
    assert decision.relation == RepresentationRelation.OVERGENERALIZED


def test_7_latency_vs_accuracy_detects_invalid_proxy(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-07",
        content="Latency was 5ms.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="LATENCY",
        epistemic_sector="LATENCY",
        claim_type="CALCULATED",
        confidence=0.9,
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-07",
        content="Response accuracy is 100%.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    assert decision.decision == "BLOCK"  # CRITICAL proxy invalid
    assert decision.relation == RepresentationRelation.OVERGENERALIZED


def test_8_cost_vs_quality_detects_invalid_proxy(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-08",
        content="Cost was $0.01.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="COST",
        epistemic_sector="COST",
        claim_type="CALCULATED",
        confidence=0.9,
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-08",
        content="Quality is exceptionally high.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="POLICY",
        epistemic_sector="POLICY",
        claim_type="FACTUAL",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    assert decision.decision == "ALLOW_WITH_LIMITATIONS"  # High risk overgeneralization downgraded
    assert decision.relation == RepresentationRelation.OVERGENERALIZED


def test_9_disjoint_representations_do_not_force_consensus(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-09A",
        content="Standard code compiled.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="CODE",
        epistemic_sector="CODE_STATE",
        claim_type="FACTUAL",
        confidence=0.9,
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-09B",
        content="Different content entirely.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    assert decision.decision == "ALLOW_WITH_LIMITATIONS"
    assert decision.relation == RepresentationRelation.DISJOINT


def test_10_underspecified_benchmark_claim_allowed_with_limitations(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-10",
        content="Score was high, missing version.",
        source_model="",  # Missing model
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.9,
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-10",
        content="Score was high, version 1.0.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    assert decision.decision == "ALLOW_WITH_LIMITATIONS"
    assert decision.relation == RepresentationRelation.UNDERSPECIFIED


def test_11_evidence_mismatch_blocks_operational_promotion(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-11",
        content="Factual claim.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.9,
        evidence_refs=("run.json",),
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-11",
        content="Factual claim.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.95,
        evidence_refs=("run.log",),
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    assert decision.decision == "BLOCK"
    assert decision.relation == RepresentationRelation.EVIDENCE_MISMATCH


def test_12_cautious_representation_preferred_over_overstrong_claim(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-12",
        content="High quality.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.9,
        limitations=("Scoped explicitly to small dataset",),
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-12",
        content="High quality.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    assert decision.decision == "ALLOW_WITH_LIMITATIONS"
    assert decision.recommended_claim is not None
    assert decision.recommended_claim.representation_id == "REP-01"


def test_13_exploratory_representations_allowed_as_hypothesis(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-13",
        content="This may indicate a path forward.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="CODE",
        epistemic_sector="HYPOTHESIS",
        claim_type="INFERRED",
        confidence=0.9,
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-13",
        content="This may indicate a path forward.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="CODE",
        epistemic_sector="HYPOTHESIS",
        claim_type="INFERRED",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    assert decision.decision == "ALLOW_AS_HYPOTHESIS"
    assert "Exploratory speculative" in decision.limitations[0]


def test_14_representation_audit_is_deterministic(gate: RepresentationConsistencyGate):
    rep1 = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-14",
        content="Factual claim.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.9,
    )
    rep2 = ClaimRepresentation(
        representation_id="REP-02",
        claim_id="CLAIM-14",
        content="Factual claim.",
        source_model="deepseek-chat",
        source_provider="deepseek",
        source_context="BENCHMARK",
        epistemic_sector="BENCHMARK",
        claim_type="FACTUAL",
        confidence=0.95,
    )
    decision, comparisons = gate.check_consistency([rep1, rep2])
    audit = RepresentationAudit.create("AUDIT-1001", [rep1, rep2], decision)
    assert audit.audit_id == "AUDIT-1001"
    assert audit.final_decision == "ALLOW"
    assert audit.relation_summary == "EQUIVALENT"


def test_15_consistency_gate_composes_with_sector_transition_engine(gate: RepresentationConsistencyGate):
    # Single representation audited against sector transition engine
    rep = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-15",
        content="Dry-run latency was 5ms.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="LATENCY",
        epistemic_sector="LATENCY",
        claim_type="CALCULATED",
        confidence=0.9,
    )
    # Auditing transition from LATENCY sector to PRODUCTION sector -> should be blocked by sector engine
    decision, comparisons = gate.check_consistency(
        representations=[rep],
        target_sector=EpistemicSector.PRODUCTION,
        target_context=LocalContext.PRODUCTION,
    )
    assert decision.decision == "BLOCK"
    assert "DRY_RUN_LATENCY_TO_PRODUCTION_LATENCY_BLOCKED" in decision.reason


def test_16_consistency_gate_composes_with_contamination_guard(gate: RepresentationConsistencyGate):
    # Single representation audited against contamination guard boundary rules
    rep = ClaimRepresentation(
        representation_id="REP-01",
        claim_id="CLAIM-16",
        content="Latency response.",
        source_model="deepseek-coder",
        source_provider="deepseek",
        source_context="LATENCY",
        epistemic_sector="LATENCY",
        claim_type="CALCULATED",
        confidence=0.9,
    )
    # Auditing boundary rule of LATENCY to ACCURACY (requested target FACTUAL) -> should block
    decision, comparisons = gate.check_consistency(
        representations=[rep],
        target_sector=EpistemicSector.BENCHMARK,
        target_context=LocalContext.BENCHMARK,
        requested_claim_type=ClaimType.FACTUAL,
    )
    assert decision.decision == "BLOCK"
    assert "LATENCY_TO_ACCURACY_BLOCKED" in decision.reason
