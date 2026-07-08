"""Deterministic budget guard for provider smoke runs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BudgetDecision(str, Enum):
    WITHIN_BUDGET = "WITHIN_BUDGET"
    WOULD_EXCEED_BUDGET = "WOULD_EXCEED_BUDGET"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    UNKNOWN_COST_ALLOWED_WITH_WARNING = "UNKNOWN_COST_ALLOWED_WITH_WARNING"
    BLOCKED = "BLOCKED"


@dataclass
class BudgetGuard:
    budget_cap_usd: float
    total_estimated_cost_usd: float = 0.0

    def check_before_task(self, projected_cost_usd: float | None) -> BudgetDecision:
        if self.total_estimated_cost_usd >= self.budget_cap_usd:
            return BudgetDecision.BUDGET_EXHAUSTED
        if projected_cost_usd is None:
            return BudgetDecision.UNKNOWN_COST_ALLOWED_WITH_WARNING
        if self.total_estimated_cost_usd + projected_cost_usd > self.budget_cap_usd:
            return BudgetDecision.WOULD_EXCEED_BUDGET
        return BudgetDecision.WITHIN_BUDGET

    def record_cost(self, cost_usd: float | None) -> None:
        if cost_usd is not None:
            self.total_estimated_cost_usd += cost_usd
