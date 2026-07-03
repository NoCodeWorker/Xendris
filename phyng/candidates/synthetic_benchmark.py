"""
Phygn v1.5 — Candidate vs Baseline Synthetic Benchmark

Computes V_base(t) vs V_candidate(t), delta, max_abs_delta,
detectability status, alpha_min estimate, failure conditions,
allowed/blocked claims.
"""

from __future__ import annotations

import math
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class CandidateSyntheticBenchmarkInput(BaseModel):
    benchmark_id: str
    candidate_id: str
    system_id: str
    m_kg: float
    L_value_m: float
    B: float
    QB: float
    gamma_env: float
    alpha: float
    t_grid: list[float]
    epsilon_exp: float | None = None
    y_true: list[float] | None = None
    error_metric: str = "MAE"
    benchmark_provenance: str = "SYNTHETIC"


class CandidateSyntheticBenchmarkResult(BaseModel):
    benchmark_id: str
    candidate_id: str
    v_base: list[float]
    v_candidate: list[float]
    delta: list[float]
    max_abs_delta: float
    detectability_status: str
    alpha_min_for_detectability: float | None = None
    synthetic_gain_status: str
    triggered_failure_conditions: list[str] = Field(default_factory=list)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------

def compute_v_base(gamma_env: float, t_grid: list[float]) -> list[float]:
    """V_base(t) = exp(-gamma_env * t)"""
    return [math.exp(-gamma_env * t) for t in t_grid]


def compute_v_candidate(gamma_env: float, delta_gamma_c: float, t_grid: list[float]) -> list[float]:
    """V_candidate(t) = exp(-(gamma_env + delta_gamma_c) * t)"""
    return [math.exp(-(gamma_env + delta_gamma_c) * t) for t in t_grid]


def compute_delta(v_candidate: list[float], v_base: list[float]) -> list[float]:
    """delta(t) = V_candidate(t) - V_base(t)"""
    return [vc - vb for vc, vb in zip(v_candidate, v_base)]


def compute_max_abs_delta(delta: list[float]) -> float:
    return max(abs(d) for d in delta) if delta else 0.0


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_synthetic_benchmark(inp: CandidateSyntheticBenchmarkInput) -> CandidateSyntheticBenchmarkResult:
    """
    Full synthetic benchmark for a candidate vs baseline.
    """
    from phyng.candidates.detectability import (
        classify_detectability,
        estimate_alpha_min_for_detectability,
    )
    from phyng.candidates.failure_report_v1_5 import evaluate_v1_5_failure_conditions

    delta_gamma_c = inp.alpha * inp.B

    v_base = compute_v_base(inp.gamma_env, inp.t_grid)
    v_candidate = compute_v_candidate(inp.gamma_env, delta_gamma_c, inp.t_grid)
    delta = compute_delta(v_candidate, v_base)
    max_abs_delta = compute_max_abs_delta(delta)

    detectability_status = classify_detectability(max_abs_delta, inp.epsilon_exp)

    alpha_min = estimate_alpha_min_for_detectability(
        inp.B, inp.gamma_env, inp.t_grid, inp.epsilon_exp
    )

    # Synthetic gain
    if inp.y_true is None:
        synthetic_gain_status = "NOT_COMPUTABLE_WITHOUT_Y_TRUE"
    else:
        synthetic_gain_status = "COMPUTABLE_WITH_Y_TRUE"

    # Failure conditions
    triggered_failures = evaluate_v1_5_failure_conditions(
        max_abs_delta=max_abs_delta,
        epsilon_exp=inp.epsilon_exp,
        y_true=inp.y_true,
        alpha_min=alpha_min,
        detectability_status=detectability_status,
    )

    # Allowed / blocked claims
    allowed_claims = [
        "The candidate was synthetically benchmarked.",
        f"The candidate is {detectability_status.lower()} under declared toy parameters.",
        "Physical claims remain blocked.",
    ]
    if alpha_min is not None:
        allowed_claims.append(
            f"The candidate requires alpha ≈ {alpha_min:.3e} for synthetic detectability."
        )

    blocked_claims = [
        "Phygn predicts decoherence.",
        "Frontera C is validated.",
        "Candidate has physical PredictiveGain.",
        "Synthetic delta proves physical effect.",
    ]

    return CandidateSyntheticBenchmarkResult(
        benchmark_id=inp.benchmark_id,
        candidate_id=inp.candidate_id,
        v_base=v_base,
        v_candidate=v_candidate,
        delta=delta,
        max_abs_delta=max_abs_delta,
        detectability_status=detectability_status,
        alpha_min_for_detectability=alpha_min,
        synthetic_gain_status=synthetic_gain_status,
        triggered_failure_conditions=triggered_failures,
        allowed_claims=allowed_claims,
        blocked_claims=blocked_claims,
    )
