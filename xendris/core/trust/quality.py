"""Deterministic quality planning for audited Xendris answers.

This module turns a structural trust audit into an operational improvement
plan. It does not call models, rewrite answers, optimize benchmark scores, or
validate factual truth. It only recommends conservative next actions that can
make a model answer safer, better calibrated, and more benchmark-ready.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from xendris.core.response_contract import ResponseContractAssessment

from .audit import ReasoningAudit
from .types import AuditDecision, RiskLevel


class QualityAction(str, Enum):
    """Deterministic action recommended after a trust audit."""

    ACCEPT = "ACCEPT"
    ADD_LIMITATIONS = "ADD_LIMITATIONS"
    ADD_EVIDENCE = "ADD_EVIDENCE"
    REQUIRE_HUMAN_REVIEW = "REQUIRE_HUMAN_REVIEW"
    BLOCK_OUTPUT = "BLOCK_OUTPUT"


class QualityPriority(str, Enum):
    """Priority level for the recommended quality action."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class BenchmarkReadiness(str, Enum):
    """Whether an answer is structurally ready for benchmark use."""

    READY = "READY"
    READY_WITH_LIMITATIONS = "READY_WITH_LIMITATIONS"
    NOT_READY = "NOT_READY"


class QualityDimension(str, Enum):
    """Quality dimensions affected by the plan."""

    EVIDENCE_SUPPORT = "EVIDENCE_SUPPORT"
    CONFIDENCE_CALIBRATION = "CONFIDENCE_CALIBRATION"
    DOMAIN_LIMITS = "DOMAIN_LIMITS"
    CONTRADICTION_CONTROL = "CONTRADICTION_CONTROL"
    HUMAN_REVIEW = "HUMAN_REVIEW"


@dataclass(frozen=True)
class QualityImprovementPlan:
    """A conservative plan for improving an audited answer.

    The plan is a control object for model orchestration and benchmark hygiene.
    It is not proof of answer quality and must not be interpreted as a factual
    validation signal.
    """

    action: QualityAction
    priority: QualityPriority
    benchmark_readiness: BenchmarkReadiness
    quality_score: float
    target_dimensions: tuple[QualityDimension, ...]
    rationale: str
    suggested_next_steps: tuple[str, ...]

    def is_benchmark_ready(self) -> bool:
        """Return whether the plan permits benchmark use without blocking.

        This is structural readiness only. It is not factual validation and
        does not imply that benchmark scores will improve.
        """

        return self.benchmark_readiness in {
            BenchmarkReadiness.READY,
            BenchmarkReadiness.READY_WITH_LIMITATIONS,
        }

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""

        return {
            "action": self.action.value,
            "priority": self.priority.value,
            "benchmark_readiness": self.benchmark_readiness.value,
            "quality_score": self.quality_score,
            "target_dimensions": [dimension.value for dimension in self.target_dimensions],
            "rationale": self.rationale,
            "suggested_next_steps": list(self.suggested_next_steps),
        }


def _clamp_score(score: float) -> float:
    return round(min(max(score, 0.0), 1.0), 6)


def _score_from_audit(
    audit: ReasoningAudit,
    penalty: float = 0.0,
    response_assessment: ResponseContractAssessment | None = None,
) -> float:
    unsupported_penalty = min(len(audit.unsupported_claims) * 0.12, 0.36)
    response_penalty = 0.0
    if response_assessment is not None and not response_assessment.is_conservative():
        response_penalty = 0.18
    return _clamp_score(audit.global_confidence - unsupported_penalty - penalty - response_penalty)


def build_quality_improvement_plan(
    audit: ReasoningAudit,
    response_assessment: ResponseContractAssessment | None = None,
) -> QualityImprovementPlan:
    """Build a deterministic improvement plan from a trust audit.

    Rules are deliberately conservative:

    - blocked or critical audits are not benchmark-ready;
    - high-risk audits require human review or additional evidence;
    - limitation-bearing audits are usable only with explicit caveats;
    - low-risk approved audits are structurally ready, not factually proven.
    """

    if audit.decision == AuditDecision.BLOCKED or audit.risk_level == RiskLevel.CRITICAL:
        return QualityImprovementPlan(
            action=QualityAction.BLOCK_OUTPUT,
            priority=QualityPriority.CRITICAL,
            benchmark_readiness=BenchmarkReadiness.NOT_READY,
            quality_score=_score_from_audit(
                audit,
                penalty=0.6,
                response_assessment=response_assessment,
            ),
            target_dimensions=(
                QualityDimension.CONTRADICTION_CONTROL,
                QualityDimension.HUMAN_REVIEW,
            ),
            rationale="The audit is blocked or critical and must not enter benchmark scoring.",
            suggested_next_steps=(
                "Remove or rewrite contradicted statements.",
                "Re-run the trust audit after contradiction resolution.",
            ),
        )

    if audit.decision == AuditDecision.HUMAN_REVIEW_REQUIRED:
        return QualityImprovementPlan(
            action=QualityAction.REQUIRE_HUMAN_REVIEW,
            priority=QualityPriority.HIGH,
            benchmark_readiness=BenchmarkReadiness.NOT_READY,
            quality_score=_score_from_audit(
                audit,
                penalty=0.3,
                response_assessment=response_assessment,
            ),
            target_dimensions=(
                QualityDimension.EVIDENCE_SUPPORT,
                QualityDimension.CONFIDENCE_CALIBRATION,
                QualityDimension.HUMAN_REVIEW,
            ),
            rationale="The audit requires human review before benchmark use.",
            suggested_next_steps=(
                "Attach stronger evidence to unsupported high-impact statements.",
                "Lower confidence or mark limits before re-evaluation.",
            ),
        )

    if response_assessment is not None and not response_assessment.is_conservative():
        return QualityImprovementPlan(
            action=QualityAction.ADD_LIMITATIONS,
            priority=QualityPriority.MEDIUM,
            benchmark_readiness=BenchmarkReadiness.READY_WITH_LIMITATIONS,
            quality_score=_score_from_audit(
                audit,
                penalty=0.12,
                response_assessment=response_assessment,
            ),
            target_dimensions=(
                QualityDimension.DOMAIN_LIMITS,
                QualityDimension.CONFIDENCE_CALIBRATION,
            ),
            rationale=(
                "The trust audit passed, but the response contract detected "
                "non-conservative wording or missing limits."
            ),
            suggested_next_steps=(
                "Add explicit uncertainty markers and domain limits.",
                "Remove absolute wording before benchmark use.",
            ),
        )

    if audit.unsupported_claims or audit.decision == AuditDecision.APPROVED_WITH_LIMITATIONS:
        return QualityImprovementPlan(
            action=QualityAction.ADD_LIMITATIONS,
            priority=QualityPriority.MEDIUM,
            benchmark_readiness=BenchmarkReadiness.READY_WITH_LIMITATIONS,
            quality_score=_score_from_audit(
                audit,
                penalty=0.1,
                response_assessment=response_assessment,
            ),
            target_dimensions=(
                QualityDimension.DOMAIN_LIMITS,
                QualityDimension.EVIDENCE_SUPPORT,
                QualityDimension.CONFIDENCE_CALIBRATION,
            ),
            rationale="The answer can be used only with explicit limitations.",
            suggested_next_steps=(
                "State assumptions and domain limits in the answer.",
                "Add evidence bindings for unsupported statements when available.",
            ),
        )

    return QualityImprovementPlan(
        action=QualityAction.ACCEPT,
        priority=QualityPriority.LOW,
        benchmark_readiness=BenchmarkReadiness.READY,
        quality_score=_score_from_audit(audit, response_assessment=response_assessment),
        target_dimensions=(),
        rationale="The answer is structurally acceptable for benchmark use.",
        suggested_next_steps=(
            "Preserve evidence references and confidence calibration.",
            "Do not treat structural readiness as factual validation.",
        ),
    )


def validate_quality_improvement_plan(
    plan: QualityImprovementPlan,
    audit: ReasoningAudit | None = None,
) -> bool:
    """Validate structural coherence of a quality improvement plan.

    The validation is intentionally conservative and deterministic. It checks
    whether a plan is internally coherent and, when an audit is supplied,
    whether the plan respects blocking audit decisions. It does not validate
    factual truth, score benchmarks, or prove answer quality.
    """

    if not 0.0 <= plan.quality_score <= 1.0:
        return False
    if not plan.rationale.strip():
        return False
    if not plan.suggested_next_steps:
        return False

    if plan.action == QualityAction.ACCEPT:
        if plan.priority != QualityPriority.LOW:
            return False
        if plan.benchmark_readiness != BenchmarkReadiness.READY:
            return False

    if plan.action == QualityAction.BLOCK_OUTPUT:
        if plan.priority != QualityPriority.CRITICAL:
            return False
        if plan.benchmark_readiness != BenchmarkReadiness.NOT_READY:
            return False

    if plan.action == QualityAction.REQUIRE_HUMAN_REVIEW:
        if plan.priority not in {QualityPriority.HIGH, QualityPriority.CRITICAL}:
            return False
        if plan.benchmark_readiness != BenchmarkReadiness.NOT_READY:
            return False

    if plan.benchmark_readiness == BenchmarkReadiness.NOT_READY:
        if plan.priority not in {QualityPriority.HIGH, QualityPriority.CRITICAL}:
            return False

    if audit is None:
        return True

    if audit.decision == AuditDecision.BLOCKED or audit.risk_level == RiskLevel.CRITICAL:
        return (
            plan.action == QualityAction.BLOCK_OUTPUT
            and plan.benchmark_readiness == BenchmarkReadiness.NOT_READY
        )

    if audit.decision == AuditDecision.HUMAN_REVIEW_REQUIRED:
        return (
            plan.action == QualityAction.REQUIRE_HUMAN_REVIEW
            and plan.benchmark_readiness == BenchmarkReadiness.NOT_READY
        )

    return True
