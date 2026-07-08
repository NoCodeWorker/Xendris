"""Types for v0.9.0 runtime paired lift."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RuntimeAuditDecision(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_LIMITATIONS = "ALLOW_WITH_LIMITATIONS"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    BLOCK = "BLOCK"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"


@dataclass
class RuntimeAuditResult:
    decision: RuntimeAuditDecision
    score: float
    reasons: list[str]
    blocked_claims: list[str] = field(default_factory=list)
    repair_reasons: list[str] = field(default_factory=list)
    component_scores: dict[str, float] = field(default_factory=dict)
    is_repairable: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "score": self.score,
            "reasons": self.reasons,
            "blocked_claims": self.blocked_claims,
            "repair_reasons": self.repair_reasons,
            "component_scores": dict(self.component_scores),
            "is_repairable": self.is_repairable,
        }


@dataclass
class RuntimeTrace:
    task_id: str
    provider_name: str
    variant_name: str
    initial_response: str
    initial_audit: RuntimeAuditResult
    audit_decision: RuntimeAuditDecision
    repair_attempted: bool
    repair_response: str | None
    repair_audit: RuntimeAuditResult | None
    final_response: str
    final_audit: RuntimeAuditResult | None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    estimated_cost_usd: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "provider_name": self.provider_name,
            "variant_name": self.variant_name,
            "initial_response": self.initial_response,
            "initial_audit": self.initial_audit.to_dict(),
            "audit_decision": self.audit_decision.value,
            "repair_attempted": self.repair_attempted,
            "repair_response": self.repair_response,
            "repair_audit": self.repair_audit.to_dict() if self.repair_audit else None,
            "final_response": self.final_response,
            "final_audit": self.final_audit.to_dict() if self.final_audit else None,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "estimated_cost_usd": self.estimated_cost_usd,
        }


@dataclass
class RuntimeScoredRecord:
    variant_name: str
    provider_name: str
    model_name: str
    task_id: str
    task_family: str
    score_total: float
    score_components: dict[str, float]
    verified_success: bool
    estimated_cost_usd: float | None = None
    normalized_response_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "variant_name": self.variant_name,
            "provider_name": self.provider_name,
            "model_name": self.model_name,
            "task_id": self.task_id,
            "task_family": self.task_family,
            "score_total": self.score_total,
            "score_components": dict(self.score_components),
            "verified_success": self.verified_success,
            "estimated_cost_usd": self.estimated_cost_usd,
        }


@dataclass
class RuntimeVariantAggregate:
    variant_name: str
    provider_name: str
    task_count: int
    mean_score: float
    component_means: dict[str, float]
    min_score: float
    max_score: float
    verified_count: int
    total_cost_usd: float
    cost_per_mean_score_point: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "variant_name": self.variant_name,
            "provider_name": self.provider_name,
            "task_count": self.task_count,
            "mean_score": self.mean_score,
            "component_means": dict(self.component_means),
            "min_score": self.min_score,
            "max_score": self.max_score,
            "verified_count": self.verified_count,
            "total_cost_usd": self.total_cost_usd,
            "cost_per_mean_score_point": self.cost_per_mean_score_point,
        }


AUDIT_COMPONENTS = [
    "response_present",
    "follows_task_format",
    "preserves_api_contract_claim",
    "task_completion_signal",
    "no_false_success_claim",
    "mentions_limitations_when_needed",
    "deterministic_structure",
    "no_runtime_error",
    "security_clean",
    "no_secret_exposure",
    "minimal_unnecessary_verbosity",
    "actionable_answer",
]
