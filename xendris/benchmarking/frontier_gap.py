"""Cheap-to-frontier gap analysis for Xendris benchmarks.

The calculations in this module are purely analytical. They do not call model
providers and do not imply universal model superiority.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Literal


SystemRole = Literal[
    "cheap_base",
    "cheap_xendris",
    "frontier_base",
    "frontier_xendris_optional",
]

EPSILON = 1e-12


@dataclass(frozen=True)
class FrontierGapSystemResult:
    """Aggregated benchmark result for one system in a frontier-gap comparison."""

    system_name: str
    model_name: str
    provider: str
    role: SystemRole
    average_score: float
    total_cost_usd: float
    average_latency_ms: float
    scoring_allowed_count: int
    exclusion_rate: float
    human_review_rate: float
    cost_per_valid_answer: float | None

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation."""
        return asdict(self)


@dataclass(frozen=True)
class FrontierGapComparison:
    """Computed cheap-to-frontier gap comparison."""

    cheap_base: FrontierGapSystemResult
    cheap_xendris: FrontierGapSystemResult
    frontier_base: FrontierGapSystemResult
    frontier_xendris_optional: FrontierGapSystemResult | None
    absolute_delta_cheap_to_xendris: float
    absolute_gap_cheap_to_frontier: float
    gap_closed_ratio: float | None
    gap_closed_percent: float | None
    cost_multiplier_xendris_vs_cheap: float | None
    cost_multiplier_frontier_vs_cheap: float | None
    cost_per_gap_point_xendris: float | None
    cost_per_gap_point_frontier: float | None
    latency_overhead_xendris: float
    latency_overhead_frontier: float
    interpretation: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation."""
        payload = asdict(self)
        payload["cheap_base"] = self.cheap_base.to_dict()
        payload["cheap_xendris"] = self.cheap_xendris.to_dict()
        payload["frontier_base"] = self.frontier_base.to_dict()
        payload["frontier_xendris_optional"] = (
            self.frontier_xendris_optional.to_dict()
            if self.frontier_xendris_optional is not None
            else None
        )
        return payload


def compute_frontier_gap(
    cheap_base: FrontierGapSystemResult,
    cheap_xendris: FrontierGapSystemResult,
    frontier_base: FrontierGapSystemResult,
    frontier_xendris_optional: FrontierGapSystemResult | None = None,
) -> FrontierGapComparison:
    """Compute how much of a measured cheap-to-frontier benchmark gap closes.

    The result is benchmark-local. It must not be interpreted as universal model
    superiority or broad production readiness.
    """
    _validate_role(cheap_base, "cheap_base")
    _validate_role(cheap_xendris, "cheap_xendris")
    _validate_role(frontier_base, "frontier_base")
    if frontier_xendris_optional is not None:
        _validate_role(frontier_xendris_optional, "frontier_xendris_optional")

    absolute_delta = cheap_xendris.average_score - cheap_base.average_score
    absolute_gap = frontier_base.average_score - cheap_base.average_score

    if absolute_gap <= 0:
        gap_closed_ratio = None
        gap_closed_percent = None
    else:
        gap_closed_ratio = absolute_delta / absolute_gap
        gap_closed_percent = gap_closed_ratio * 100.0

    cost_multiplier_xendris = _safe_ratio(
        cheap_xendris.total_cost_usd,
        cheap_base.total_cost_usd,
    )
    cost_multiplier_frontier = _safe_ratio(
        frontier_base.total_cost_usd,
        cheap_base.total_cost_usd,
    )

    cost_per_gap_point_xendris = _cost_per_gap_point(
        cheap_xendris.total_cost_usd - cheap_base.total_cost_usd,
        absolute_delta,
    )
    cost_per_gap_point_frontier = _cost_per_gap_point(
        frontier_base.total_cost_usd - cheap_base.total_cost_usd,
        absolute_gap,
    )

    latency_overhead_xendris = cheap_xendris.average_latency_ms - cheap_base.average_latency_ms
    latency_overhead_frontier = frontier_base.average_latency_ms - cheap_base.average_latency_ms

    return FrontierGapComparison(
        cheap_base=cheap_base,
        cheap_xendris=cheap_xendris,
        frontier_base=frontier_base,
        frontier_xendris_optional=frontier_xendris_optional,
        absolute_delta_cheap_to_xendris=round(absolute_delta, 8),
        absolute_gap_cheap_to_frontier=round(absolute_gap, 8),
        gap_closed_ratio=_round_optional(gap_closed_ratio),
        gap_closed_percent=_round_optional(gap_closed_percent),
        cost_multiplier_xendris_vs_cheap=_round_optional(cost_multiplier_xendris),
        cost_multiplier_frontier_vs_cheap=_round_optional(cost_multiplier_frontier),
        cost_per_gap_point_xendris=_round_optional(cost_per_gap_point_xendris),
        cost_per_gap_point_frontier=_round_optional(cost_per_gap_point_frontier),
        latency_overhead_xendris=round(latency_overhead_xendris, 8),
        latency_overhead_frontier=round(latency_overhead_frontier, 8),
        interpretation=_build_interpretation(gap_closed_percent, absolute_gap),
    )


def write_frontier_gap_summary_json(
    comparison: FrontierGapComparison,
    path: str | Path,
) -> None:
    """Write a frontier-gap comparison as JSON."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(comparison.to_dict(), handle, ensure_ascii=False, indent=2, sort_keys=True)


def _validate_role(system: FrontierGapSystemResult, expected_role: SystemRole) -> None:
    if system.role != expected_role:
        raise ValueError(
            f"{system.system_name} has role {system.role!r}; expected {expected_role!r}"
        )


def _safe_ratio(numerator: float, denominator: float) -> float | None:
    if abs(denominator) <= EPSILON:
        return None
    return numerator / denominator


def _cost_per_gap_point(cost_delta: float, score_delta: float) -> float | None:
    denominator = max(abs(score_delta), EPSILON)
    if denominator <= EPSILON:
        return None
    return cost_delta / denominator


def _round_optional(value: float | None) -> float | None:
    return round(value, 8) if value is not None else None


def _build_interpretation(gap_closed_percent: float | None, absolute_gap: float) -> str:
    if gap_closed_percent is None or absolute_gap <= 0:
        return (
            "Gap not applicable: the measured frontier baseline does not exceed "
            "the measured cheap baseline on this benchmark. No universal "
            "superiority claim is supported."
        )
    if gap_closed_percent > 100.0:
        return (
            "Frontier exceeded on this benchmark only: the cheap Xendris variant "
            "scored above the measured frontier baseline in this dataset. This "
            "does not imply universal superiority or generalization."
        )
    return (
        "Benchmark-local gap estimate: the cheap Xendris variant closes "
        f"{gap_closed_percent:.2f}% of the measured cheap-to-frontier gap under "
        "this dataset and configuration. This does not imply universal "
        "superiority."
    )
