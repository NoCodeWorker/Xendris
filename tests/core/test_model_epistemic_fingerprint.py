"""Unit tests for the Xendris Model Epistemic Fingerprint."""

from __future__ import annotations

import pytest
from xendris.core.boundary.contamination_guard import BoundaryDecision
from xendris.core.sectors.transition_engine import SectorTransitionDecision, SectorTransition
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.local.context import LocalContext
from xendris.core.representations.equivalence import RepresentationRelation
from xendris.core.representations.consistency_gate import RepresentationConsistencyDecision
from xendris.core.fingerprints.metrics import FingerprintMetric
from xendris.core.fingerprints.model_fingerprint import ModelIdentity, ModelEpistemicFingerprint
from xendris.core.fingerprints.aggregator import FingerprintAggregator
from xendris.core.fingerprints.profile import FingerprintProfile
from xendris.core.fingerprints.fingerprint_audit import FingerprintAudit
from xendris.core.trust.types import ClaimStatus, ClaimType, RiskLevel
from xendris.core.algebra.claim_object import ClaimObject


@pytest.fixture
def identity() -> ModelIdentity:
    return ModelIdentity(
        model_id="deepseek-coder",
        provider="deepseek",
        version="1.0",
        configuration={"temperature": 0.0},
        temperature=0.0,
        max_tokens=2048,
        run_context="TESTING",
    )


@pytest.fixture
def aggregator() -> FingerprintAggregator:
    return FingerprintAggregator(run_id="RUN-999", dataset_id="DATASET-888")


def test_1_empty_input_returns_limited_empty_fingerprint(identity: ModelIdentity, aggregator: FingerprintAggregator):
    fingerprint = aggregator.aggregate(identity, [])
    assert fingerprint.sample_count == 0
    assert fingerprint.metrics[FingerprintMetric.TOTAL_CLAIMS] == 0.0
    assert any("empty and limited" in limit for limit in fingerprint.limitations)


def test_2_total_claims_metric_is_counted_correctly(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
    ]
    fingerprint = aggregator.aggregate(identity, records)
    assert fingerprint.sample_count == 2
    assert fingerprint.metrics[FingerprintMetric.TOTAL_CLAIMS] == 2.0


def test_3_allow_rate_is_computed_correctly(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "ALLOW", "allowed": True},
        {"decision": "BLOCK", "allowed": False},
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
    ]
    fingerprint = aggregator.aggregate(identity, records)
    assert fingerprint.metrics[FingerprintMetric.ALLOW_RATE] == 0.75


def test_4_block_rate_is_computed_correctly(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "ALLOW", "allowed": True},
        {"decision": "BLOCK", "allowed": False},
    ]
    fingerprint = aggregator.aggregate(identity, records)
    assert fingerprint.metrics[FingerprintMetric.BLOCK_RATE] == 0.50


def test_5_human_review_rate_is_computed_correctly(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "HUMAN_REVIEW", "allowed": False},
        {"decision": "BLOCK", "allowed": False},
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
    ]
    fingerprint = aggregator.aggregate(identity, records)
    assert fingerprint.metrics[FingerprintMetric.HUMAN_REVIEW_RATE] == 0.20


def test_6_overgeneralization_rate_is_computed_correctly(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "BLOCK", "allowed": False, "reason": "OVERGENERALIZATION_DETECTED"},
        {"decision": "ALLOW", "allowed": True},
    ]
    fingerprint = aggregator.aggregate(identity, records)
    assert fingerprint.metrics[FingerprintMetric.OVERGENERALIZATION_RATE] == 0.50


def test_7_unsupported_claim_rate_is_computed_correctly(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "BLOCK", "allowed": False, "confidence": 0.4},
        {"decision": "ALLOW", "allowed": True, "confidence": 0.9},
    ]
    fingerprint = aggregator.aggregate(identity, records)
    assert fingerprint.metrics[FingerprintMetric.UNSUPPORTED_CLAIM_RATE] == 0.50


def test_8_evidence_mismatch_rate_is_computed_correctly(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "BLOCK", "allowed": False, "reason": "EVIDENCE_MISMATCH_DETECTED"},
        {"decision": "ALLOW", "allowed": True},
    ]
    fingerprint = aggregator.aggregate(identity, records)
    assert fingerprint.metrics[FingerprintMetric.EVIDENCE_MISMATCH_RATE] == 0.50


def test_9_normal_control_pass_rate_is_computed_correctly(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "ALLOW", "allowed": True, "claim_id": "control-01"},
        {"decision": "BLOCK", "allowed": False, "claim_id": "control-02"},
        {"decision": "ALLOW", "allowed": True, "claim_id": "other-01"},
    ]
    fingerprint = aggregator.aggregate(identity, records)
    assert fingerprint.metrics[FingerprintMetric.NORMAL_CONTROL_PASS_RATE] == 0.50


def test_10_usefulness_preservation_rate_is_computed_correctly(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "ALLOW", "allowed": True, "reason": "USEFULNESS_PRESERVED"},
        {"decision": "ALLOW", "allowed": True},
    ]
    fingerprint = aggregator.aggregate(identity, records)
    assert fingerprint.metrics[FingerprintMetric.USEFULNESS_PRESERVATION_RATE] == 0.50


def test_11_observed_risk_generated_from_overgeneralization_threshold(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "BLOCK", "allowed": False, "reason": "OVERGENERALIZATION_DETECTED"},
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
        {"decision": "ALLOW", "allowed": True},
    ]  # 1/10 = 0.10 overgeneralization rate -> threshold met
    fingerprint = aggregator.aggregate(identity, records)
    assert "overgeneralization_observed" in fingerprint.observed_risks


def test_12_observed_strength_generated_from_normal_control_threshold(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "ALLOW", "allowed": True, "claim_id": "control-01"},
        {"decision": "ALLOW", "allowed": True, "claim_id": "safety-01"},
    ]  # 100% control pass rate -> strengths met
    fingerprint = aggregator.aggregate(identity, records)
    assert "normal_controls_preserved" in fingerprint.observed_strengths


def test_13_fingerprint_does_not_claim_universal_superiority(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [{"decision": "ALLOW", "allowed": True}]
    fingerprint = aggregator.aggregate(identity, records)
    
    # Verify forbidden words are absent
    forbidden = ["Best model", "Universally superior", "Safe for all use cases", "Hallucination-free"]
    
    # Check all strengths, risks, recommendations, and limitations
    all_text = " ".join(
        list(fingerprint.observed_strengths)
        + list(fingerprint.observed_risks)
        + list(fingerprint.recommended_use)
        + list(fingerprint.limitations)
    )
    for word in forbidden:
        assert word.lower() not in all_text.lower()


def test_14_profile_recommendations_are_scoped(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [
        {"decision": "BLOCK", "allowed": False, "reason": "OVERGENERALIZATION_DETECTED"},
        {"decision": "ALLOW", "allowed": True},
    ]
    fingerprint = aggregator.aggregate(identity, records)
    profile = FingerprintProfile.from_fingerprint(fingerprint)
    
    # Verify recommended use is scoped
    assert "Suitable for low-risk drafting" in profile.recommended_use[0]


def test_15_fingerprint_audit_is_deterministic(identity: ModelIdentity, aggregator: FingerprintAggregator):
    records = [{"decision": "ALLOW", "allowed": True}]
    fingerprint1 = aggregator.aggregate(identity, records)
    fingerprint2 = aggregator.aggregate(identity, records)
    
    audit1 = FingerprintAudit.create("AUDIT-01", fingerprint1)
    audit2 = FingerprintAudit.create("AUDIT-01", fingerprint2)
    
    assert audit1.metrics_hash == audit2.metrics_hash
    assert audit1.to_dict() == audit2.to_dict()


def test_16_aggregator_accepts_representation_consistency_records(identity: ModelIdentity, aggregator: FingerprintAggregator):
    rec = RepresentationConsistencyDecision(
        decision="ALLOW_WITH_LIMITATIONS",
        relation=RepresentationRelation.PARTIALLY_EQUIVALENT,
        allowed=True,
        reason="PARTIALLY_EQUIVALENT_REPRESENTATIONS_ALLOWED",
    )
    fingerprint = aggregator.aggregate(identity, [rec])
    assert fingerprint.sample_count == 1
    assert fingerprint.metrics[FingerprintMetric.ALLOW_WITH_LIMITATIONS_RATE] == 1.0


def test_17_aggregator_accepts_sector_transition_records(identity: ModelIdentity, aggregator: FingerprintAggregator):
    claim_obj = ClaimObject(
        claim_id="CLAIM-101",
        content="Test content",
        claim_type=ClaimType.FACTUAL,
        claim_status=ClaimStatus.VERIFIED,
        risk_level=RiskLevel.MEDIUM,
        context=LocalContext.BENCHMARK,
    )
    rec = SectorTransitionDecision(
        decision="ALLOW",
        allowed=True,
        source_sector=EpistemicSector.BENCHMARK,
        target_sector=EpistemicSector.FACTUAL,
        reason="SECTOR_TRANSITION_SUCCESSFUL",
    )
    fingerprint = aggregator.aggregate(identity, [rec])
    assert fingerprint.sample_count == 1
    assert fingerprint.metrics[FingerprintMetric.ALLOW_RATE] == 1.0


def test_18_aggregator_accepts_contamination_guard_records(identity: ModelIdentity, aggregator: FingerprintAggregator):
    rec = BoundaryDecision(
        decision="BLOCK",
        reason="LATENCY_TO_ACCURACY_BLOCKED",
        source_context=LocalContext.LATENCY,
        target_context=LocalContext.BENCHMARK,
        allowed=False,
    )
    fingerprint = aggregator.aggregate(identity, [rec])
    assert fingerprint.sample_count == 1
    assert fingerprint.metrics[FingerprintMetric.BLOCK_RATE] == 1.0
