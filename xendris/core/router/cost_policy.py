"""Deterministic CostPolicy implementation for estimating request cost."""

from __future__ import annotations

from xendris.core.router.model_registry import ModelCapabilityProfile


class CostPolicy:
    """Estimates routing costs deterministically without using cost as quality proxy."""

    def estimate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        profile: ModelCapabilityProfile,
    ) -> float:
        """Calculate estimated cost for a given capability profile."""
        input_cost = (input_tokens / 1000.0) * profile.cost_per_1k_input_tokens
        output_cost = (output_tokens / 1000.0) * profile.cost_per_1k_output_tokens
        return input_cost + output_cost

    def get_cost_band(self, estimated_cost: float) -> str:
        """Return cost band description based on deterministic thresholds."""
        if estimated_cost < 0.01:
            return "LOW"
        elif estimated_cost < 0.05:
            return "MEDIUM"
        else:
            return "HIGH"
