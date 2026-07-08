from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


COMPLETED = "COST_FRONTIER_COMPLETED_DIAGNOSTIC_ONLY"
PARTIAL = "COST_FRONTIER_PARTIAL_DIAGNOSTIC_ONLY"


class PreflightDecision(str, Enum):
    READY = "COST_FRONTIER_PREFLIGHT_READY"
    BLOCKED = "COST_FRONTIER_PREFLIGHT_BLOCKED"


@dataclass
class CostFrontierPreflight:
    can_execute: bool
    decision: str
    blockers: list[str] = field(default_factory=list)
    expected_attempts: int = 0
    task_count: int = 0
    dataset_hash: str = ""
    manifest_hash: str = ""
    budget_cap: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "can_execute": self.can_execute,
            "decision": self.decision,
            "blockers": self.blockers,
            "expected_attempts": self.expected_attempts,
            "task_count": self.task_count,
            "dataset_hash": self.dataset_hash,
            "manifest_hash": self.manifest_hash,
            "budget_cap": self.budget_cap,
        }


@dataclass
class CostFrontierComparison:
    comparison_name: str
    control_variant: str
    treatment_variant: str
    control_mean: float = 0.0
    treatment_mean: float = 0.0
    mean_delta: float = 0.0
    median_delta: float = 0.0
    wins: int = 0
    losses: int = 0
    ties: int = 0
    win_rate_excluding_ties: float = 0.0
    cost_a: float = 0.0
    cost_b: float = 0.0
    cost_delta: float = 0.0
    cost_ratio: float = 0.0
    cost_per_task_a: float = 0.0
    cost_per_task_b: float = 0.0
    cost_per_mean_score_point_a: float = 0.0
    cost_per_mean_score_point_b: float = 0.0
    cost_per_lift_point: float | None = None
    efficient_frontier_decision: str = "INCONCLUSIVE"

    def to_dict(self) -> dict[str, Any]:
        return {
            "comparison_name": self.comparison_name,
            "control_variant": self.control_variant,
            "treatment_variant": self.treatment_variant,
            "control_mean": round(self.control_mean, 6),
            "treatment_mean": round(self.treatment_mean, 6),
            "mean_delta": round(self.mean_delta, 6),
            "median_delta": round(self.median_delta, 6),
            "wins": self.wins,
            "losses": self.losses,
            "ties": self.ties,
            "win_rate_excluding_ties": round(self.win_rate_excluding_ties, 4),
            "cost_a": round(self.cost_a, 8),
            "cost_b": round(self.cost_b, 8),
            "cost_delta": round(self.cost_delta, 8),
            "cost_ratio": round(self.cost_ratio, 4),
            "cost_per_task_a": round(self.cost_per_task_a, 8),
            "cost_per_task_b": round(self.cost_per_task_b, 8),
            "cost_per_mean_score_point_a": round(self.cost_per_mean_score_point_a, 8),
            "cost_per_mean_score_point_b": round(self.cost_per_mean_score_point_b, 8),
            "cost_per_lift_point": round(self.cost_per_lift_point, 8) if self.cost_per_lift_point is not None else None,
            "efficient_frontier_decision": self.efficient_frontier_decision,
        }


EfficientFrontierDecision = str
