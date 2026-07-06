"""Marginal certainty gain and token avoidance tracking for council decisions."""
from __future__ import annotations

from decimal import Decimal


class CouncilMetrics:
    """Tracks marginal certainty gain and tokens avoided by local guards."""

    def __init__(self) -> None:
        self.total_council_calls = 0
        self.total_tokens_used = 0
        self.total_cost = Decimal("0.00")
        self.total_tokens_avoided = 0
        self.total_cost_saved = Decimal("0.00")
        self.council_decisions: list[dict] = []

    def record_decision(
        self,
        requires_council: bool,
        tokens_used: int = 0,
        cost: Decimal = Decimal("0.00"),
        tokens_avoided: int = 0,
        cost_saved: Decimal = Decimal("0.00"),
        verdict: str = "",
    ) -> None:
        if requires_council:
            self.total_council_calls += 1
            self.total_tokens_used += tokens_used
            self.total_cost += cost
        self.total_tokens_avoided += tokens_avoided
        self.total_cost_saved += cost_saved
        self.council_decisions.append({
            "requires_council": requires_council,
            "tokens_used": tokens_used,
            "cost": str(cost),
            "tokens_avoided": tokens_avoided,
            "cost_saved": str(cost_saved),
            "verdict": verdict,
        })

    @property
    def marginal_certainty_gain_per_token(self) -> Decimal:
        if self.total_tokens_used == 0:
            return Decimal("0.00")
        return (Decimal("0.05") * Decimal(str(self.total_council_calls))) / Decimal(str(self.total_tokens_used))

    @property
    def tokens_avoided_by_local_guards(self) -> int:
        return self.total_tokens_avoided

    @property
    def cost_saved_vs_always_council(self) -> Decimal:
        return self.total_cost_saved

    def summary(self) -> dict:
        return {
            "total_council_calls": self.total_council_calls,
            "total_tokens_used": self.total_tokens_used,
            "total_cost": str(self.total_cost),
            "total_tokens_avoided": self.total_tokens_avoided,
            "total_cost_saved": str(self.total_cost_saved),
            "marginal_certainty_gain_per_token": str(self.marginal_certainty_gain_per_token),
            "tokens_avoided_by_local_guards": self.tokens_avoided_by_local_guards,
            "cost_saved_vs_always_council": str(self.cost_saved_vs_always_council),
        }
