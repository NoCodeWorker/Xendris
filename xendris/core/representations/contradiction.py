"""Heuristic logic for detecting contradictions and relations between representations."""

from __future__ import annotations

from xendris.core.representations.representation import ClaimRepresentation
from xendris.core.representations.equivalence import RepresentationRelation, RepresentationComparison
from xendris.core.trust.types import RiskLevel


def compare_representations(
    left: ClaimRepresentation,
    right: ClaimRepresentation,
) -> RepresentationComparison:
    """Compare two claim representations using deterministic heuristics."""
    left_content = left.content.lower()
    right_content = right.content.lower()
    
    # 1. Disjoint Relation
    if left.claim_id != right.claim_id:
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.DISJOINT,
            reason="DISJOINT_DIFFERENT_CLAIM_ID",
            shared_claim_id="",
        )

    # Helper: Check terms presence
    def has_conflict(term_a: str, term_b: str) -> bool:
        return (term_a in left_content and term_b in right_content) or (
            term_b in left_content and term_a in right_content
        )

    # 2. Overgeneralization Relation
    # Latency to Accuracy proxy violation
    if has_conflict("latency", "accuracy") or has_conflict("ms", "accuracy") or has_conflict("response time", "correct"):
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.OVERGENERALIZED,
            reason="LATENCY_TO_ACCURACY_OVERGENERALIZATION",
            shared_claim_id=left.claim_id,
            conflict_terms=("latency", "accuracy"),
            risk_level=RiskLevel.CRITICAL,
        )

    # Cost to Quality proxy violation
    if has_conflict("cost", "quality") or has_conflict("price", "quality") or has_conflict("$", "quality"):
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.OVERGENERALIZED,
            reason="COST_TO_QUALITY_OVERGENERALIZATION",
            shared_claim_id=left.claim_id,
            conflict_terms=("cost", "quality"),
            risk_level=RiskLevel.HIGH,
        )

    # Dry-run to Production
    is_dry = "dry-run" in left_content or "dry_run" in left.metadata or "dry-run" in right_content or "dry_run" in right.metadata
    is_prod = "production" in left_content or "production" in right_content or left.source_context == "PRODUCTION" or right.source_context == "PRODUCTION"
    if is_dry and is_prod:
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.OVERGENERALIZED,
            reason="DRY_RUN_TO_PRODUCTION_OVERGENERALIZATION",
            shared_claim_id=left.claim_id,
            conflict_terms=("dry-run", "production"),
            risk_level=RiskLevel.HIGH,
        )

    # Benchmark to Universal Superiority
    is_bench = "benchmark" in left_content or "benchmark" in right_content or left.source_context == "BENCHMARK" or right.source_context == "BENCHMARK"
    is_universal = "universal" in left_content or "universal" in right_content or "superior" in left_content or "superior" in right_content
    if is_bench and is_universal:
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.OVERGENERALIZED,
            reason="BENCHMARK_TO_UNIVERSAL_SUPERIORITY_OVERGENERALIZATION",
            shared_claim_id=left.claim_id,
            conflict_terms=("benchmark", "universal"),
            risk_level=RiskLevel.CRITICAL,
        )

    # Normal Controls to Universal Safety
    is_control = "control" in left_content or "control" in right_content or "control" in left.claim_id.lower() or "control" in right.claim_id.lower()
    is_safety = "universal safety" in left_content or "universal safety" in right_content or "completely safe" in left_content or "completely safe" in right_content
    if is_control and is_safety:
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.OVERGENERALIZED,
            reason="NORMAL_CONTROL_TO_UNIVERSAL_SAFETY_OVERGENERALIZATION",
            shared_claim_id=left.claim_id,
            conflict_terms=("control", "universal safety"),
            risk_level=RiskLevel.HIGH,
        )

    # 3. Contradiction Relation
    # Pass vs Fail
    if has_conflict("pass", "fail") or has_conflict("success", "fail") or has_conflict("green", "red") or has_conflict("succeed", "error"):
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.CONTRADICTORY,
            reason="PASS_FAIL_CONTRADICTION",
            shared_claim_id=left.claim_id,
            conflict_terms=("pass", "fail"),
            risk_level=RiskLevel.CRITICAL,
        )

    # Production Ready vs Not Verified
    if has_conflict("ready", "not verified") or has_conflict("production", "not verified") or has_conflict("production ready", "unverified"):
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.CONTRADICTORY,
            reason="PRODUCTION_READY_VS_UNVERIFIED_CONTRADICTION",
            shared_claim_id=left.claim_id,
            conflict_terms=("ready", "not verified"),
            risk_level=RiskLevel.HIGH,
        )

    # Universal vs Limited Benchmark
    if has_conflict("universal superiority", "limited to dataset") or has_conflict("superior", "limited benchmark"):
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.CONTRADICTORY,
            reason="UNIVERSAL_VS_LIMITED_CONTRADICTION",
            shared_claim_id=left.claim_id,
            conflict_terms=("universal", "limited"),
            risk_level=RiskLevel.HIGH,
        )

    # Evidence Conflicts
    left_ev = set(left.evidence_refs)
    right_ev = set(right.evidence_refs)
    left_has_fail = any("fail" in ev.lower() or "error" in ev.lower() for ev in left_ev)
    right_has_fail = any("fail" in ev.lower() or "error" in ev.lower() for ev in right_ev)
    left_has_pass = any("pass" in ev.lower() or "success" in ev.lower() for ev in left_ev)
    right_has_pass = any("pass" in ev.lower() or "success" in ev.lower() for ev in right_ev)
    if (left_has_fail and right_has_pass) or (left_has_pass and right_has_fail):
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.CONTRADICTORY,
            reason="EVIDENCE_REFS_CONTRADICTION",
            shared_claim_id=left.claim_id,
            risk_level=RiskLevel.CRITICAL,
        )

    # 4. Evidence Mismatch
    # E.g. Json benchmark vs Log file
    left_has_json = any(ev.endswith(".json") for ev in left_ev)
    right_has_json = any(ev.endswith(".json") for ev in right_ev)
    left_has_log = any(ev.endswith(".log") for ev in left_ev)
    right_has_log = any(ev.endswith(".log") for ev in right_ev)
    if (left_has_json and right_has_log) or (left_has_log and right_has_json):
        # Allow if target requires compatible, but mismatch if they are disjoint evidence types
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.EVIDENCE_MISMATCH,
            reason="INCOMPATIBLE_EVIDENCE_TYPES_MISMATCH",
            shared_claim_id=left.claim_id,
            risk_level=RiskLevel.MEDIUM,
        )

    # 5. Underspecified Relation
    # Lack of version/config/model
    left_under = not left.source_model or not left.source_provider or not left.source_context
    right_under = not right.source_model or not right.source_provider or not right.source_context
    if left_under or right_under:
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.UNDERSPECIFIED,
            reason="MISSING_VERSION_OR_MODEL_SPECIFICATION",
            shared_claim_id=left.claim_id,
            risk_level=RiskLevel.LOW,
        )

    # 6. Partially Equivalent Relation
    # Different limitations or scope
    if left.limitations != right.limitations or left.source_context != right.source_context:
        return RepresentationComparison(
            left_representation_id=left.representation_id,
            right_representation_id=right.representation_id,
            relation=RepresentationRelation.PARTIALLY_EQUIVALENT,
            reason="DIFFERENT_LIMITATIONS_OR_CONTEXT_SCOPE",
            shared_claim_id=left.claim_id,
            limitations=tuple(set(left.limitations) | set(right.limitations)),
            risk_level=RiskLevel.LOW,
        )

    # 7. Equivalent Relation
    return RepresentationComparison(
        left_representation_id=left.representation_id,
        right_representation_id=right.representation_id,
        relation=RepresentationRelation.EQUIVALENT,
        reason="IDENTICAL_CORE_PROPERTIES_AND_LIMITATIONS",
        shared_claim_id=left.claim_id,
    )
