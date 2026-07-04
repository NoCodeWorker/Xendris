"""RoutingPolicy container combining risk and cost policies."""

from __future__ import annotations

from xendris.core.router.cost_policy import CostPolicy
from xendris.core.router.risk_policy import RiskPolicy


class RoutingPolicy:
    """epistemic router policy that orchestrates cost and risk evaluation."""

    def __init__(self, cost_policy: CostPolicy | None = None, risk_policy: RiskPolicy | None = None) -> None:
        self.cost_policy = cost_policy or CostPolicy()
        self.risk_policy = risk_policy or RiskPolicy()
