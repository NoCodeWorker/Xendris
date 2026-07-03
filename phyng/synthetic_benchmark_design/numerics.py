"""Numerical functions for LOG_BOUNDARY synthetic execution."""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence

from phyng.synthetic_benchmark_design.schemas import BoundaryCoordinates, VisibilityCurveResult

HBAR = 1.054571817e-34
C = 299_792_458.0
G = 6.67430e-11


def compute_boundary_coordinates(m_kg: float, L_m: float) -> BoundaryCoordinates:
    if m_kg <= 0 or L_m <= 0:
        raise ValueError("m_kg and L_m must be positive finite values.")
    lambda_c = HBAR / (m_kg * C)
    r_g = G * m_kg / (C * C)
    q_ratio = lambda_c / L_m
    b_ratio = r_g / L_m
    q = math.log(q_ratio)
    b = math.log(b_ratio)
    u = (q + b) / 2.0
    w = (b - q) / 2.0
    coordinates = BoundaryCoordinates(
        m_kg=m_kg,
        L_m=L_m,
        lambda_C_m=lambda_c,
        r_g_m=r_g,
        Q=q_ratio,
        B=b_ratio,
        q=q,
        b=b,
        u=u,
        w=w,
    )
    _require_finite(coordinates.model_dump().values())
    return coordinates


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    exp_x = math.exp(x)
    return exp_x / (1.0 + exp_x)


def compute_phi_log(u: float, w: float, k: float, k2: float, u0: float, w0: float) -> float:
    value = sigmoid(k * (u - u0)) * math.tanh(k2 * (w - w0)) ** 2
    if not math.isfinite(value):
        raise ValueError("phi_log produced a non-finite value.")
    return min(1.0, max(0.0, value))


def compute_visibility_curves(
    t_grid: Sequence[float],
    Gamma_env: float,
    alpha: float,
    phi_log: float,
) -> VisibilityCurveResult:
    if not t_grid:
        raise ValueError("t_grid must not be empty.")
    if Gamma_env < 0 or alpha < 0 or phi_log < 0:
        raise ValueError("Gamma_env, alpha and phi_log must be non-negative.")

    delta_gamma = alpha * Gamma_env * phi_log
    V_base = [math.exp(-Gamma_env * t) for t in t_grid]
    V_log = [math.exp(-(Gamma_env + delta_gamma) * t) for t in t_grid]
    delta = [candidate - baseline for baseline, candidate in zip(V_base, V_log)]
    _require_finite([*V_base, *V_log, *delta, delta_gamma])
    if any(value < -1e-12 or value > 1.0 + 1e-12 for value in [*V_base, *V_log]):
        raise ValueError("Visibility values must remain in [0, 1].")
    return VisibilityCurveResult(
        t_grid=list(t_grid),
        V_base=V_base,
        V_log=V_log,
        delta=delta,
        Gamma_env=Gamma_env,
        DeltaGamma_log=delta_gamma,
        phi_log=phi_log,
    )


def compute_max_abs_delta(V_base: Sequence[float], V_log: Sequence[float]) -> float:
    if len(V_base) != len(V_log):
        raise ValueError("Visibility curves must have matching lengths.")
    if not V_base:
        raise ValueError("Visibility curves must not be empty.")
    value = max(abs(candidate - baseline) for baseline, candidate in zip(V_base, V_log))
    if not math.isfinite(value):
        raise ValueError("max_abs_delta produced a non-finite value.")
    return value


def _require_finite(values: Iterable[float]) -> None:
    for value in values:
        if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
            raise ValueError("Numerical result contains a non-finite value.")
