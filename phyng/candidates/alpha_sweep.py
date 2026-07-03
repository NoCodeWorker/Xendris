"""
Phygn v1.5 — Alpha Sweep for Candidate vs Baseline

Runs candidate benchmark across a range of alpha values to identify
the alpha scale required for synthetic detectability.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from phyng.candidates.detectability import (
    classify_detectability,
    classify_alpha_reasonableness,
    estimate_alpha_min_for_detectability,
)


# Default alpha sweep values per spec
DEFAULT_ALPHA_VALUES: list[float] = [1e0, 1e10, 1e20, 1e30, 1e35, 1e38, 1e40]


@dataclass
class AlphaSweepRow:
    alpha: float
    delta_gamma_c: float
    max_abs_delta: float
    detectability_status: str
    alpha_reasonableness_status: str
    triggered_failures: list[str] = field(default_factory=list)


def run_alpha_sweep(
    B: float,
    gamma_env: float,
    t_grid: list[float],
    epsilon_exp: float | None,
    alpha_values: list[float] | None = None,
) -> list[AlphaSweepRow]:
    """
    Run benchmark across multiple alpha values.

    Returns one AlphaSweepRow per alpha value containing:
        alpha, delta_gamma_c, max_abs_delta,
        detectability_status, alpha_reasonableness_status, triggered_failures
    """
    if alpha_values is None:
        alpha_values = DEFAULT_ALPHA_VALUES

    rows: list[AlphaSweepRow] = []

    for alpha in alpha_values:
        delta_gamma_c = alpha * B

        # Compute V_base and V_candidate
        v_base = [math.exp(-gamma_env * t) for t in t_grid]
        v_candidate = [math.exp(-(gamma_env + delta_gamma_c) * t) for t in t_grid]

        delta = [vc - vb for vc, vb in zip(v_candidate, v_base)]
        max_abs_delta = max(abs(d) for d in delta) if delta else 0.0

        detectability_status = classify_detectability(max_abs_delta, epsilon_exp)
        alpha_reasonableness_status = classify_alpha_reasonableness(alpha)

        # Collect triggered failures for this alpha
        triggered_failures: list[str] = []
        if detectability_status == "UNDETECTABLE_SYNTHETIC_DELTA":
            triggered_failures.append("FAIL_UNDETECTABLE_DELTA")
        if alpha_reasonableness_status == "ALPHA_UNPHYSICAL_OR_UNCONSTRAINED":
            triggered_failures.append("REQUIRES_UNPHYSICAL_ALPHA")

        rows.append(
            AlphaSweepRow(
                alpha=alpha,
                delta_gamma_c=delta_gamma_c,
                max_abs_delta=max_abs_delta,
                detectability_status=detectability_status,
                alpha_reasonableness_status=alpha_reasonableness_status,
                triggered_failures=triggered_failures,
            )
        )

    return rows


def find_first_detectable_alpha(rows: list[AlphaSweepRow]) -> float | None:
    """Return the smallest alpha in the sweep that achieves DETECTABLE_SYNTHETIC_DELTA."""
    for row in rows:
        if row.detectability_status == "DETECTABLE_SYNTHETIC_DELTA":
            return row.alpha
    return None
