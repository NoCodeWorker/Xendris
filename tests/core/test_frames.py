import pytest

from xendris.core.frames import (
    ActionabilityDecision,
    ActionabilityVerdict,
    EpistemicFrame,
    EvidenceRequirementVerdict,
    FrameShiftDecision,
    FrameShiftVerdict,
    PresentationBoundaryDecision,
    PresentationBoundaryVerdict,
    TruthGapAssessment,
    TruthGapSeverity,
    assess_interface_truth_gap,
    check_evidence_requirements,
    evaluate_actionability,
    evaluate_frame_shift,
    evaluate_presentation_boundary,
)


# ── ActionabilityGate ─────────────────────────────────────────────

class TestActionabilityGate:
    def test_explanatory_output_allows(self):
        verdict = evaluate_actionability(
            "This is a summary of recent findings.",
            frame_actionability="explanatory",
        )
        assert verdict.decision == ActionabilityDecision.ALLOW
        assert verdict.action_class == "explanatory"

    def test_actionable_output_with_sufficient_evidence(self):
        verdict = evaluate_actionability(
            "This approach likely reduces latency.",
            frame_actionability="actionable",
            evidence_score=0.7,
        )
        assert verdict.decision == ActionabilityDecision.ALLOW
        assert verdict.action_class == "actionable"

    def test_actionable_output_requires_more_evidence(self):
        verdict = evaluate_actionability(
            "This approach reduces latency.",
            frame_actionability="actionable",
            evidence_score=0.3,
        )
        assert verdict.decision == ActionabilityDecision.REQUIRE_MORE_EVIDENCE
        assert verdict.action_class == "actionable"

    def test_critical_output_blocks_without_evidence(self):
        verdict = evaluate_actionability(
            "This system guarantees safety.",
            frame_actionability="critical",
            evidence_score=0.2,
        )
        assert verdict.decision == ActionabilityDecision.BLOCK
        assert verdict.action_class == "critical"

    def test_critical_output_escalates_with_strong_evidence(self):
        verdict = evaluate_actionability(
            "This system guarantees safety.",
            frame_actionability="critical",
            evidence_score=0.9,
        )
        assert verdict.decision == ActionabilityDecision.ESCALATE_TO_HUMAN
        assert verdict.requires_human_review
        assert verdict.action_class == "critical"

    def test_detects_critical_from_safety_keywords(self):
        verdict = evaluate_actionability(
            "This system guarantees safety",
            has_safety_critical_terms=True,
        )
        assert verdict.action_class == "critical"

    def test_detects_actionable_from_recommendation_language(self):
        verdict = evaluate_actionability(
            "We recommend deploying this model.",
            has_recommendation_language=True,
        )
        assert verdict.action_class == "actionable"


# ── EvidenceRequirements ──────────────────────────────────────────

class TestEvidenceRequirements:
    def test_production_frame_requires_deployment_evidence(self):
        result = check_evidence_requirements(
            frame=EpistemicFrame.PRODUCTION,
            has_deployment_evidence=False,
        )
        assert not result.passed
        assert any(
            c.verdict == EvidenceRequirementVerdict.FAIL
            for c in result.checks
        )

    def test_benchmark_frame_requires_provider_and_dataset_scope(self):
        result = check_evidence_requirements(
            frame=EpistemicFrame.BENCHMARK,
            has_dataset_scope=True,
            has_provider_disclosure=True,
            has_cost_disclosure=True,
            has_latency_disclosure=True,
        )
        assert result.passed
        assert all(
            c.verdict == EvidenceRequirementVerdict.PASS
            for c in result.checks
        )

    def test_hypothesis_frame_allows_without_proof(self):
        result = check_evidence_requirements(
            frame=EpistemicFrame.HYPOTHESIS,
            is_hypothesis=True,
            has_limitation_statement=True,
        )
        assert result.passed

    def test_hypothesis_frame_fails_without_limitations(self):
        result = check_evidence_requirements(
            frame=EpistemicFrame.HYPOTHESIS,
            is_hypothesis=True,
            has_limitation_statement=False,
        )
        assert not result.passed

    def test_marketing_frame_bans_universal_language(self):
        result = check_evidence_requirements(
            frame=EpistemicFrame.MARKETING,
            has_universal_language=True,
        )
        assert not result.passed

    def test_safety_audit_frame_requires_limitations(self):
        result = check_evidence_requirements(
            frame=EpistemicFrame.SAFETY_AUDIT,
            has_limitation_statement=True,
            has_external_citation=True,
        )
        assert result.passed


# ── PresentationBoundary ──────────────────────────────────────────

class TestPresentationBoundary:
    def test_clear_boundary_no_conflation(self):
        verdict = evaluate_presentation_boundary(
            "This table shows the benchmark results."
        )
        assert verdict.decision == PresentationBoundaryDecision.CLEAR_BOUNDARY

    def test_boundary_violation_detected(self):
        verdict = evaluate_presentation_boundary(
            "This demo is proof the system works."
        )
        assert verdict.decision == PresentationBoundaryDecision.BOUNDARY_VIOLATION
        assert len(verdict.violations) > 0

    def test_unclear_when_assertion_dominates(self):
        verdict = evaluate_presentation_boundary(
            "This proves the method is superior. It confirms our hypothesis. "
            "The results demonstrate conclusively that we are right."
        )
        assert verdict.decision == PresentationBoundaryDecision.UNCLEAR


# ── InterfaceTruthGap ─────────────────────────────────────────────

class TestInterfaceTruthGap:
    def test_no_gap_when_evidence_matches_confidence(self):
        result = assess_interface_truth_gap(
            "The results suggest the hypothesis may be correct.",
            evidence_score=0.8,
        )
        assert result.severity == TruthGapSeverity.NONE
        assert result.gap_score < 0.1

    def test_critical_gap_when_confidence_far_exceeds_evidence(self):
        result = assess_interface_truth_gap(
            "This is guaranteed to work. It is absolutely certain and proven without doubt.",
            evidence_score=0.1,
        )
        assert result.severity == TruthGapSeverity.CRITICAL
        assert result.gap_score >= 0.7

    def test_high_gap_detected(self):
        result = assess_interface_truth_gap(
            "This is undoubtedly the best solution. It is certainly proven and guaranteed.",
            evidence_score=0.35,
        )
        assert result.severity == TruthGapSeverity.HIGH
        assert 0.5 <= result.gap_score < 0.7

    def test_medium_gap_detected(self):
        result = assess_interface_truth_gap(
            "This definitely proves the approach works.",
            evidence_score=0.65,
        )
        assert result.severity == TruthGapSeverity.MEDIUM
        assert 0.3 <= result.gap_score < 0.5


# ── FrameShiftGuard ───────────────────────────────────────────────

class TestFrameShiftGuard:
    def test_allow_from_none_to_any_frame(self):
        verdict = evaluate_frame_shift(None, EpistemicFrame.BENCHMARK)
        assert verdict.decision == FrameShiftDecision.ALLOW

    def test_allow_same_frame(self):
        verdict = evaluate_frame_shift(EpistemicFrame.BENCHMARK, EpistemicFrame.BENCHMARK)
        assert verdict.decision == FrameShiftDecision.ALLOW

    def test_allow_downshift_reduces_actionability(self):
        verdict = evaluate_frame_shift(EpistemicFrame.PRODUCTION, EpistemicFrame.HYPOTHESIS)
        assert verdict.decision == FrameShiftDecision.ALLOW

    def test_require_bridge_for_upshift(self):
        verdict = evaluate_frame_shift(EpistemicFrame.HYPOTHESIS, EpistemicFrame.BENCHMARK)
        assert verdict.decision == FrameShiftDecision.REQUIRE_EVIDENCE_BRIDGE
        assert len(verdict.bridge_requirements) > 0

    def test_block_large_upshift_without_evidence(self):
        verdict = evaluate_frame_shift(EpistemicFrame.HYPOTHESIS, EpistemicFrame.PRODUCTION)
        assert verdict.decision == FrameShiftDecision.BLOCK
        assert len(verdict.bridge_requirements) > 0

    def test_allow_large_upshift_with_strong_bridge(self):
        verdict = evaluate_frame_shift(
            EpistemicFrame.HYPOTHESIS,
            EpistemicFrame.PRODUCTION,
            has_evidence_bridge=True,
            bridge_type="deployment_logs",
        )
        assert verdict.decision == FrameShiftDecision.ALLOW_WITH_WARNING
