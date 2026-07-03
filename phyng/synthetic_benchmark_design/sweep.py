"""Declared LOG_BOUNDARY parameter sweep."""

from __future__ import annotations

from itertools import product

from phyng.synthetic_benchmark_design.numerics import (
    compute_boundary_coordinates,
    compute_max_abs_delta,
    compute_phi_log,
    compute_visibility_curves,
)
from phyng.synthetic_benchmark_design.schemas import (
    LogBoundaryCandidateSpec,
    LogBoundarySweepPoint,
    LogBoundarySweepResult,
    ParameterReasonablenessResult,
)

DETECTABLE_STATUS = "LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA"
UNDETECTABLE_STATUS = "LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA"


def run_log_boundary_sweep(spec: LogBoundaryCandidateSpec) -> LogBoundarySweepResult:
    sweep_plan = _sweep_plan()
    t_grid = spec.t_grid or [i * 0.1 for i in range(101)]
    epsilon = spec.epsilon_exp
    coordinates = compute_boundary_coordinates(m_kg=1e-17, L_m=1e-7)
    points: list[LogBoundarySweepPoint] = []
    failures: list[str] = []

    for alpha, k, k2, u0, w0, gamma_env in product(
        sweep_plan["alpha_values"],
        sweep_plan["k_values"],
        sweep_plan["k2_values"],
        sweep_plan["u0_values"],
        sweep_plan["w0_values"],
        sweep_plan["Gamma_env_values"],
    ):
        phi = compute_phi_log(coordinates.u, coordinates.w, k=k, k2=k2, u0=u0, w0=w0)
        curves = compute_visibility_curves(t_grid, Gamma_env=gamma_env, alpha=alpha, phi_log=phi)
        max_abs_delta = compute_max_abs_delta(curves.V_base, curves.V_log)
        status = DETECTABLE_STATUS if max_abs_delta > epsilon else UNDETECTABLE_STATUS
        points.append(
            LogBoundarySweepPoint(
                alpha=alpha,
                k=k,
                k2=k2,
                u0=u0,
                w0=w0,
                Gamma_env=gamma_env,
                m_kg=coordinates.m_kg,
                L_m=coordinates.L_m,
                q=coordinates.q,
                b=coordinates.b,
                u=coordinates.u,
                w=coordinates.w,
                phi_log=phi,
                DeltaGamma_log=curves.DeltaGamma_log,
                max_abs_delta=max_abs_delta,
                detectability_status=status,
                parameter_reasonableness=classify_parameter_reasonableness(in_declared_sweep=True),
            )
        )

    if not points:
        failures.append("FAIL_EMPTY_SWEEP")

    best_point = max(points, key=lambda point: point.max_abs_delta) if points else None
    if best_point is None:
        failures.append("FAIL_NUMERICAL_INSTABILITY")
    elif best_point.max_abs_delta <= epsilon:
        failures.append("FAIL_UNDETECTABLE_DELTA")

    return LogBoundarySweepResult(
        candidate_id=spec.candidate_id,
        sweep_count=len(points),
        epsilon_exp=epsilon,
        best_point=best_point,
        points=points,
        failure_conditions=failures,
    )


def classify_parameter_reasonableness(
    *,
    in_declared_sweep: bool,
    post_hoc: bool = False,
    extreme: bool = False,
    unphysical: bool = False,
) -> ParameterReasonablenessResult:
    if unphysical:
        return ParameterReasonablenessResult(
            classification="PARAMETERS_UNJUSTIFIED_OR_UNPHYSICAL",
            is_unjustified_or_unphysical=True,
            notes=["Parameter choice lacks physical/source justification."],
        )
    if post_hoc:
        return ParameterReasonablenessResult(
            classification="PARAMETERS_POST_HOC",
            is_post_hoc=True,
            notes=["Parameter choice is outside the pre-declared sweep."],
        )
    if extreme:
        return ParameterReasonablenessResult(
            classification="PARAMETERS_EXTREME_TOY_RANGE",
            is_extreme_toy_range=True,
            notes=["Parameter choice is detectable only under extreme toy assumptions."],
        )
    if in_declared_sweep:
        return ParameterReasonablenessResult(
            classification="PARAMETERS_DECLARED_TOY_RANGE",
            is_declared_toy_range=True,
            notes=["Declared toy range; not source-backed physical calibration."],
        )
    return ParameterReasonablenessResult(
        classification="PARAMETERS_UNJUSTIFIED_OR_UNPHYSICAL",
        is_unjustified_or_unphysical=True,
    )


def _sweep_plan() -> dict[str, list[float]]:
    return {
        "alpha_values": [0.1, 1.0, 3.0, 10.0],
        "k_values": [0.5, 1.0, 2.0, 5.0],
        "k2_values": [0.5, 1.0, 2.0, 5.0],
        "u0_values": [-90.0, -70.0, -50.0],
        "w0_values": [-40.0, -20.0, 0.0],
        "Gamma_env_values": [0.01, 0.05, 0.1],
    }
