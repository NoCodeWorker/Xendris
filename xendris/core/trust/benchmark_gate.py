"""Benchmark-readiness gate for audited model outputs.

The gate protects evaluation suites from scoring outputs that are structurally
unsafe, review-blocked, or produced by degraded runtime paths such as fallbacks
after API errors. It does not compute benchmark metrics, improve scores, or
claim model superiority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .quality import BenchmarkReadiness, QualityImprovementPlan


class BenchmarkGateDecision(str, Enum):
    """Decision for whether a model output may enter benchmark scoring."""
    INCLUDE = "INCLUDE"
    INCLUDE_WITH_LIMITATIONS = "INCLUDE_WITH_LIMITATIONS"
    EXCLUDE = "EXCLUDE"


class BenchmarkExclusionReason(str, Enum):
    """Reason an output is excluded or limited for benchmark use."""
    NONE = "NONE"
    TRUST_NOT_READY = "TRUST_NOT_READY"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    TIMEOUT = "TIMEOUT"
    FALLBACK_RESPONSE = "FALLBACK_RESPONSE"
    LIMITED_READINESS = "LIMITED_READINESS"
    UNSUPPORTED_SCORING_RULE = "UNSUPPORTED_SCORING_RULE"
    UNSUPPORTED_CLAIM_PREMISE = "UNSUPPORTED_CLAIM_PREMISE"
    LATENCY_PROXIED_WITHOUT_POLICY = "LATENCY_PROXIED_WITHOUT_POLICY"
    USER_RULE_WITHOUT_EVIDENCE = "USER_RULE_WITHOUT_EVIDENCE"
    EVIDENCE_CONFLICT = "EVIDENCE_CONFLICT"
    PARTIAL_SUPPORT = "PARTIAL_SUPPORT"
    CONTRADICTED_EVIDENCE = "CONTRADICTED_EVIDENCE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    CLAIM_OVERREACH = "CLAIM_OVERREACH"
    NEEDS_SOURCE_VALIDATION = "NEEDS_SOURCE_VALIDATION"
    AMBIGUITY_NOT_RESOLVABLE = "AMBIGUITY_NOT_RESOLVABLE"
    PRODUCTION_READINESS_NOT_ESTABLISHED = "PRODUCTION_READINESS_NOT_ESTABLISHED"
    SECURITY_NOT_VALIDATED = "SECURITY_NOT_VALIDATED"
    TEST_COVERAGE_INSUFFICIENT = "TEST_COVERAGE_INSUFFICIENT"
    PERFORMANCE_NOT_MEASURED = "PERFORMANCE_NOT_MEASURED"
    RUNTIME_ENVIRONMENT_MISMATCH = "RUNTIME_ENVIRONMENT_MISMATCH"
    COMPILATION_NOT_CORRECTNESS = "COMPILATION_NOT_CORRECTNESS"
    TEST_PASS_NOT_PRODUCTION_READY = "TEST_PASS_NOT_PRODUCTION_READY"
    BENCHMARK_NOT_REAL_WORLD_PERFORMANCE = "BENCHMARK_NOT_REAL_WORLD_PERFORMANCE"


@dataclass(frozen=True)
class BenchmarkGateResult:
    """A deterministic benchmark-readiness decision.

    This result is an evaluation hygiene object. It is not a benchmark score,
    not a performance claim, and not a factual validation signal.
    """
    decision: BenchmarkGateDecision
    reason: BenchmarkExclusionReason
    include_in_scoring: bool
    requires_limitation_note: bool
    quality_score: float
    notes: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""
        return {
            "decision": self.decision.value,
            "reason": self.reason.value,
            "include_in_scoring": self.include_in_scoring,
            "requires_limitation_note": self.requires_limitation_note,
            "quality_score": self.quality_score,
            "notes": self.notes,
        }


def _has_runtime_error(metadata: Mapping[str, object] | None) -> bool:
    if not metadata:
        return False
    return bool(metadata.get("error"))


def _has_timeout(metadata: Mapping[str, object] | None) -> bool:
    if not metadata:
        return False
    return bool(metadata.get("timeout"))


def _has_unsupported_scoring_rule(metadata: Mapping[str, object] | None) -> bool:
    if not metadata:
        return False
    return bool(
        metadata.get("unsupported_scoring_rule")
        or metadata.get("has_unsupported_scoring_rule")
        or metadata.get("citation_as_proxy")
    )


def _has_unsupported_claim_premise(metadata: Mapping[str, object] | None) -> bool:
    if not metadata:
        return False
    return bool(
        metadata.get("unsupported_claim_premise")
        or metadata.get("has_unsupported_claim_premise")
    )


def _uses_latency_as_correctness_proxy(metadata: Mapping[str, object] | None) -> bool:
    if not metadata:
        return False
    latency_as_proxy = metadata.get("latency_as_proxy")
    policy_validated = metadata.get("policy_validated") or metadata.get(
        "benchmark_policy_validated"
    )
    return bool(latency_as_proxy and not policy_validated)


def _has_user_rule_without_evidence(metadata: Mapping[str, object] | None) -> bool:
    if not metadata:
        return False
    return bool(
        metadata.get("user_provided_rule_without_evidence")
        or metadata.get("user_rule_without_evidence")
    )


def _specific_reason_from_metadata(
    metadata: Mapping[str, object] | None,
) -> BenchmarkExclusionReason | None:
    if not metadata:
        return None
    reason = metadata.get("specific_exclusion_reason") or metadata.get("trust_reason")
    if not reason:
        return None
    try:
        return BenchmarkExclusionReason(str(reason))
    except ValueError:
        return None


def _is_genuine_human_review_case(metadata: Mapping[str, object] | None) -> bool:
    if not metadata:
        return True
    has_flags = any(
        flag in metadata
        for flag in (
            "has_evidence_conflict",
            "has_unresolved_ambiguity",
            "policy_requires_explicit_review",
            "critical_claims_partial_support",
        )
    )
    if not has_flags:
        return False
    return bool(
        metadata.get("has_evidence_conflict")
        or metadata.get("has_unresolved_ambiguity")
        or metadata.get("policy_requires_explicit_review")
        or metadata.get("critical_claims_partial_support")
    )


def _looks_like_fallback(response_text: str) -> bool:
    normalized = " ".join(response_text.lower().split())
    fallback_markers = (
        "fallback",
        "http error fallback",
        "urlerror fallback",
        "generic error fallback",
    )
    return any(marker in normalized for marker in fallback_markers)


def gate_benchmark_output(
    *,
    quality_plan: QualityImprovementPlan,
    response_text: str,
    runtime_metadata: Mapping[str, object] | None = None,
) -> BenchmarkGateResult:
    """Decide whether a model output may enter benchmark scoring.

    Runtime degradation takes precedence over trust readiness: a fallback or
    timeout is excluded even if the text superficially looks safe.
    """
    if _has_timeout(runtime_metadata):
        return BenchmarkGateResult(
            decision=BenchmarkGateDecision.EXCLUDE,
            reason=BenchmarkExclusionReason.TIMEOUT,
            include_in_scoring=False,
            requires_limitation_note=True,
            quality_score=0.0,
            notes="Output came from a timeout path and must not be benchmark-scored.",
        )

    if _has_runtime_error(runtime_metadata):
        return BenchmarkGateResult(
            decision=BenchmarkGateDecision.EXCLUDE,
            reason=BenchmarkExclusionReason.RUNTIME_ERROR,
            include_in_scoring=False,
            requires_limitation_note=True,
            quality_score=0.0,
            notes="Output came from an error path and must not be benchmark-scored.",
        )

    if _has_unsupported_scoring_rule(runtime_metadata):
        specific_reason = _specific_reason_from_metadata(runtime_metadata)
        return BenchmarkGateResult(
            decision=BenchmarkGateDecision.EXCLUDE,
            reason=specific_reason or BenchmarkExclusionReason.UNSUPPORTED_SCORING_RULE,
            include_in_scoring=False,
            requires_limitation_note=True,
            quality_score=0.0,
            notes="Unsupported scoring rules must not enter benchmark scoring.",
        )

    if _has_unsupported_claim_premise(runtime_metadata):
        specific_reason = _specific_reason_from_metadata(runtime_metadata)
        return BenchmarkGateResult(
            decision=BenchmarkGateDecision.EXCLUDE,
            reason=specific_reason or BenchmarkExclusionReason.UNSUPPORTED_CLAIM_PREMISE,
            include_in_scoring=False,
            requires_limitation_note=True,
            quality_score=0.0,
            notes="Unsupported claim premises must not enter benchmark scoring.",
        )

    if _uses_latency_as_correctness_proxy(runtime_metadata):
        return BenchmarkGateResult(
            decision=BenchmarkGateDecision.EXCLUDE,
            reason=BenchmarkExclusionReason.LATENCY_PROXIED_WITHOUT_POLICY,
            include_in_scoring=False,
            requires_limitation_note=True,
            quality_score=0.0,
            notes="Latency cannot be used as a correctness proxy without policy validation.",
        )

    if _has_user_rule_without_evidence(runtime_metadata):
        specific_reason = _specific_reason_from_metadata(runtime_metadata)
        return BenchmarkGateResult(
            decision=BenchmarkGateDecision.EXCLUDE,
            reason=specific_reason or BenchmarkExclusionReason.USER_RULE_WITHOUT_EVIDENCE,
            include_in_scoring=False,
            requires_limitation_note=True,
            quality_score=0.0,
            notes="User-provided scoring rules require evidence before scoring.",
        )

    if _looks_like_fallback(response_text):
        return BenchmarkGateResult(
            decision=BenchmarkGateDecision.EXCLUDE,
            reason=BenchmarkExclusionReason.FALLBACK_RESPONSE,
            include_in_scoring=False,
            requires_limitation_note=True,
            quality_score=0.0,
            notes="Fallback output must be excluded from benchmark scoring.",
        )

    if quality_plan.benchmark_readiness == BenchmarkReadiness.NOT_READY:
        is_review = "review" in quality_plan.action.value.lower()
        if is_review and _is_genuine_human_review_case(runtime_metadata):
            reason = BenchmarkExclusionReason.HUMAN_REVIEW_REQUIRED
        else:
            reason = BenchmarkExclusionReason.TRUST_NOT_READY
        return BenchmarkGateResult(
            decision=BenchmarkGateDecision.EXCLUDE,
            reason=reason,
            include_in_scoring=False,
            requires_limitation_note=True,
            quality_score=quality_plan.quality_score,
            notes="Trust quality plan marks this output as not benchmark-ready.",
        )

    if quality_plan.benchmark_readiness == BenchmarkReadiness.READY_WITH_LIMITATIONS:
        return BenchmarkGateResult(
            decision=BenchmarkGateDecision.INCLUDE_WITH_LIMITATIONS,
            reason=BenchmarkExclusionReason.LIMITED_READINESS,
            include_in_scoring=True,
            requires_limitation_note=True,
            quality_score=quality_plan.quality_score,
            notes="Output may be scored only with explicit limitations.",
        )

    return BenchmarkGateResult(
        decision=BenchmarkGateDecision.INCLUDE,
        reason=BenchmarkExclusionReason.NONE,
        include_in_scoring=True,
        requires_limitation_note=False,
        quality_score=quality_plan.quality_score,
        notes="Output is structurally ready for benchmark scoring.",
    )
