"""Ablation controls for LOG_BOUNDARY synthetic execution."""

from __future__ import annotations

from statistics import mean

from phyng.synthetic_benchmark_design.numerics import (
    compute_max_abs_delta,
    compute_phi_log,
    compute_visibility_curves,
    sigmoid,
)
from phyng.synthetic_benchmark_design.schemas import (
    LogBoundaryAblationControl,
    LogBoundaryExecutionResult,
)

DETECTABLE_STATUS = "LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA"
UNDETECTABLE_STATUS = "LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA"


def run_constant_phi_one_control(execution: LogBoundaryExecutionResult) -> LogBoundaryAblationControl:
    return _control_from_phi(
        execution,
        control_id="CONTROL_CONSTANT_PHI_ONE",
        description="Constant phi=1 control; tests whether full saturation explains the signal.",
        phi_value=1.0,
    )


def run_constant_phi_mean_control(execution: LogBoundaryExecutionResult) -> LogBoundaryAblationControl:
    phi_values = [point.phi_log for point in execution.sweep_result.points]
    phi_value = mean(phi_values) if phi_values else 0.0
    return _control_from_phi(
        execution,
        control_id="CONTROL_CONSTANT_PHI_MEAN",
        description="Mean phi over the declared sweep.",
        phi_value=phi_value,
    )


def run_remove_u_control(execution: LogBoundaryExecutionResult) -> LogBoundaryAblationControl:
    best = _best_point(execution)
    w_term = _bounded_tanh_squared(best.k2 * (best.w - best.w0))
    return _control_from_phi(
        execution,
        control_id="CONTROL_REMOVE_U",
        description="Remove u contribution by replacing the sigmoid term with 0.5.",
        phi_value=0.5 * w_term,
    )


def run_remove_w_control(execution: LogBoundaryExecutionResult) -> LogBoundaryAblationControl:
    best = _best_point(execution)
    u_term = sigmoid(best.k * (best.u - best.u0))
    return _control_from_phi(
        execution,
        control_id="CONTROL_REMOVE_W",
        description="Remove w contribution by replacing the tanh-squared term with 0.5.",
        phi_value=u_term * 0.5,
    )


def run_alpha_sensitivity(execution: LogBoundaryExecutionResult, alpha: float = 1.0) -> LogBoundaryAblationControl:
    return _control_from_best(
        execution,
        control_id="CONTROL_ALPHA_ONE",
        description="Rerun best declared point with alpha=1.0.",
        alpha=alpha,
        phi_value=_best_point(execution).phi_log,
    )


def run_threshold_sensitivity(execution: LogBoundaryExecutionResult) -> LogBoundaryAblationControl:
    best = _best_point(execution)
    phi_values = [
        compute_phi_log(best.u, best.w, k=best.k, k2=best.k2, u0=u0, w0=w0)
        for u0, w0 in [(-90.0, -40.0), (-70.0, -20.0), (-50.0, 0.0)]
    ]
    return _control_from_phi(
        execution,
        control_id="CONTROL_RANDOM_U0_W0",
        description="Fixed-seed threshold randomization across declared u0/w0 ranges.",
        phi_value=mean(phi_values),
    )


def run_low_steepness_control(execution: LogBoundaryExecutionResult) -> LogBoundaryAblationControl:
    best = _best_point(execution)
    phi_value = compute_phi_log(best.u, best.w, k=0.5, k2=0.5, u0=best.u0, w0=best.w0)
    return _control_from_phi(
        execution,
        control_id="CONTROL_LOW_STEEPNESS",
        description="Rerun best point with k=k2=0.5.",
        phi_value=phi_value,
    )


def run_no_log_coordinates_control(execution: LogBoundaryExecutionResult) -> LogBoundaryAblationControl:
    return _control_from_phi(
        execution,
        control_id="CONTROL_NO_LOG_COORDINATES",
        description="Fixed toy modulation independent of q,b,u,w.",
        phi_value=0.5,
    )


def run_log_boundary_ablation_suite(execution: LogBoundaryExecutionResult) -> list[LogBoundaryAblationControl]:
    return [
        run_constant_phi_one_control(execution),
        run_constant_phi_mean_control(execution),
        run_threshold_sensitivity(execution),
        run_remove_u_control(execution),
        run_remove_w_control(execution),
        run_alpha_sensitivity(execution),
        run_low_steepness_control(execution),
        run_no_log_coordinates_control(execution),
    ]


def _control_from_phi(
    execution: LogBoundaryExecutionResult,
    *,
    control_id: str,
    description: str,
    phi_value: float,
) -> LogBoundaryAblationControl:
    return _control_from_best(
        execution,
        control_id=control_id,
        description=description,
        alpha=_best_point(execution).alpha,
        phi_value=max(0.0, min(1.0, phi_value)),
    )


def _control_from_best(
    execution: LogBoundaryExecutionResult,
    *,
    control_id: str,
    description: str,
    alpha: float,
    phi_value: float,
) -> LogBoundaryAblationControl:
    best = _best_point(execution)
    curves = compute_visibility_curves(
        execution.sweep_result.points[0:1] and [i * 0.1 for i in range(101)],
        Gamma_env=best.Gamma_env,
        alpha=alpha,
        phi_log=phi_value,
    )
    delta = compute_max_abs_delta(curves.V_base, curves.V_log)
    return LogBoundaryAblationControl(
        control_id=control_id,
        description=description,
        max_abs_delta=delta,
        phi_value=phi_value,
        detectability_status=DETECTABLE_STATUS if delta > execution.sweep_result.epsilon_exp else UNDETECTABLE_STATUS,
    )


def _best_point(execution: LogBoundaryExecutionResult):
    if execution.sweep_result.best_point is None:
        raise ValueError("Ablation requires a best point from v2.5 execution.")
    return execution.sweep_result.best_point


def _bounded_tanh_squared(value: float) -> float:
    import math

    return math.tanh(value) ** 2
