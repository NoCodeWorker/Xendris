"""Aggregate benchmark diagnostics for gated model outputs.

This module summarizes benchmark gate results into a deterministic readiness
decision for a whole evaluation run. It does not compute benchmark metrics,
call models, compare providers, or claim performance improvement.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from collections.abc import Sequence

from .benchmark_gate import (
    BenchmarkExclusionReason,
    BenchmarkGateDecision,
    BenchmarkGateResult,
)


class BenchmarkSuiteReadiness(str, Enum):
    """Readiness of a gated benchmark run."""

    EXCELLENT = "EXCELLENT"
    USABLE_WITH_LIMITATIONS = "USABLE_WITH_LIMITATIONS"
    NEEDS_REMEDIATION = "NEEDS_REMEDIATION"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class BenchmarkSuiteDiagnostics:
    """Deterministic summary of gated benchmark outputs.

    This object is benchmark hygiene metadata. It is not a benchmark score,
    not a provider comparison, and not a claim that a model improved.
    """

    total_outputs: int
    included_outputs: int
    limited_outputs: int
    excluded_outputs: int
    inclusion_rate: float
    average_quality_score: float
    readiness: BenchmarkSuiteReadiness
    improvement_actions: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.total_outputs < 0:
            raise ValueError("total_outputs must not be negative")
        if self.included_outputs < 0:
            raise ValueError("included_outputs must not be negative")
        if self.limited_outputs < 0:
            raise ValueError("limited_outputs must not be negative")
        if self.excluded_outputs < 0:
            raise ValueError("excluded_outputs must not be negative")
        if not 0.0 <= self.inclusion_rate <= 1.0:
            raise ValueError("inclusion_rate must be between 0.0 and 1.0")
        if not 0.0 <= self.average_quality_score <= 1.0:
            raise ValueError("average_quality_score must be between 0.0 and 1.0")
        object.__setattr__(self, "improvement_actions", tuple(self.improvement_actions))

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""

        return {
            "total_outputs": self.total_outputs,
            "included_outputs": self.included_outputs,
            "limited_outputs": self.limited_outputs,
            "excluded_outputs": self.excluded_outputs,
            "inclusion_rate": self.inclusion_rate,
            "average_quality_score": self.average_quality_score,
            "readiness": self.readiness.value,
            "improvement_actions": list(self.improvement_actions),
        }


def _round_score(value: float) -> float:
    return round(min(max(value, 0.0), 1.0), 6)


def _has_degraded_runtime(results: Sequence[BenchmarkGateResult]) -> bool:
    degraded_reasons = {
        BenchmarkExclusionReason.RUNTIME_ERROR,
        BenchmarkExclusionReason.TIMEOUT,
        BenchmarkExclusionReason.FALLBACK_RESPONSE,
    }
    return any(result.reason in degraded_reasons for result in results)


def _build_actions(
    *,
    results: Sequence[BenchmarkGateResult],
    readiness: BenchmarkSuiteReadiness,
) -> tuple[str, ...]:
    actions: list[str] = []
    if not results:
        return ("Add gated outputs before interpreting benchmark readiness.",)

    if _has_degraded_runtime(results):
        actions.append("Remove timeout, runtime-error, and fallback outputs before scoring.")

    if any(result.reason == BenchmarkExclusionReason.HUMAN_REVIEW_REQUIRED for result in results):
        actions.append("Resolve human-review-required outputs before benchmark scoring.")

    if any(result.reason == BenchmarkExclusionReason.TRUST_NOT_READY for result in results):
        actions.append("Improve evidence support or claim status for trust-not-ready outputs.")

    if any(result.reason == BenchmarkExclusionReason.LIMITED_READINESS for result in results):
        actions.append("Attach limitation notes to outputs included with limitations.")

    if readiness == BenchmarkSuiteReadiness.EXCELLENT:
        actions.append("Preserve trust gates and evidence bindings for reproducibility.")

    if not actions:
        actions.append("Review low-quality included outputs before publishing benchmark results.")

    return tuple(actions)


def diagnose_benchmark_suite(
    gate_results: Sequence[BenchmarkGateResult],
) -> BenchmarkSuiteDiagnostics:
    """Summarize a benchmark run from deterministic gate results."""

    results = tuple(gate_results)
    total_outputs = len(results)
    if total_outputs == 0:
        return BenchmarkSuiteDiagnostics(
            total_outputs=0,
            included_outputs=0,
            limited_outputs=0,
            excluded_outputs=0,
            inclusion_rate=0.0,
            average_quality_score=0.0,
            readiness=BenchmarkSuiteReadiness.BLOCKED,
            improvement_actions=("Add gated outputs before interpreting benchmark readiness.",),
        )

    included_outputs = sum(1 for result in results if result.include_in_scoring)
    limited_outputs = sum(
        1
        for result in results
        if result.decision == BenchmarkGateDecision.INCLUDE_WITH_LIMITATIONS
    )
    excluded_outputs = total_outputs - included_outputs
    inclusion_rate = _round_score(included_outputs / total_outputs)
    average_quality_score = _round_score(
        sum(result.quality_score for result in results) / total_outputs
    )

    if included_outputs == 0:
        readiness = BenchmarkSuiteReadiness.BLOCKED
    elif excluded_outputs > 0 or _has_degraded_runtime(results):
        readiness = BenchmarkSuiteReadiness.NEEDS_REMEDIATION
    elif limited_outputs > 0:
        readiness = BenchmarkSuiteReadiness.USABLE_WITH_LIMITATIONS
    elif average_quality_score >= 0.85:
        readiness = BenchmarkSuiteReadiness.EXCELLENT
    else:
        readiness = BenchmarkSuiteReadiness.USABLE_WITH_LIMITATIONS

    return BenchmarkSuiteDiagnostics(
        total_outputs=total_outputs,
        included_outputs=included_outputs,
        limited_outputs=limited_outputs,
        excluded_outputs=excluded_outputs,
        inclusion_rate=inclusion_rate,
        average_quality_score=average_quality_score,
        readiness=readiness,
        improvement_actions=_build_actions(results=results, readiness=readiness),
    )
