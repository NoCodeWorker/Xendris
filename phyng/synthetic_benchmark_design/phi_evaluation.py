"""Control-resistance evaluation for non-saturating phi candidates."""

from __future__ import annotations

import math
from statistics import mean

from phyng.core.compatibility import normalize_status
from phyng.synthetic_benchmark_design.numerics import compute_max_abs_delta, compute_phi_log, compute_visibility_curves, sigmoid
from phyng.synthetic_benchmark_design.schemas import (
    LogBoundaryCandidateSpec,
    PhiCandidateEvaluationResult,
    PhiCandidateSpec,
    PhiControlResistanceMetrics,
)
from phyng.synthetic_benchmark_design.sweep import run_log_boundary_sweep

EPS = 1e-12
CONTROL_GAIN_TOLERANCE = 0.01
COORDINATE_THRESHOLD = 1e-3


def evaluate_phi_candidate(
    spec: LogBoundaryCandidateSpec,
    candidate: PhiCandidateSpec,
) -> PhiCandidateEvaluationResult:
    sweep = run_log_boundary_sweep(spec)
    try:
        phi_by_point = [_bounded_phi(_phi_value(candidate, point)) for point in sweep.points]
        if not phi_by_point:
            raise ValueError("empty phi evaluation")
        scored = [
            (
                _delta(point.Gamma_env, point.alpha, phi_value, spec.t_grid),
                point,
                phi_value,
            )
            for point, phi_value in zip(sweep.points, phi_by_point)
        ]
        candidate_delta, best_point, best_phi = max(scored, key=lambda item: item[0])
        mean_phi = mean(phi_by_point)
        constant_delta = _delta(best_point.Gamma_env, best_point.alpha, 1.0, spec.t_grid)
        mean_delta = _delta(best_point.Gamma_env, best_point.alpha, mean_phi, spec.t_grid)
        remove_u_phi = _bounded_phi(_phi_value(candidate, best_point, remove_u=True))
        remove_w_phi = _bounded_phi(_phi_value(candidate, best_point, remove_w=True))
        no_log_phi = mean_phi
        remove_u_delta = _delta(best_point.Gamma_env, best_point.alpha, remove_u_phi, spec.t_grid)
        remove_w_delta = _delta(best_point.Gamma_env, best_point.alpha, remove_w_phi, spec.t_grid)
        no_log_delta = _delta(best_point.Gamma_env, best_point.alpha, no_log_phi, spec.t_grid)
        alpha_1_delta = _delta(best_point.Gamma_env, 1.0, best_phi, spec.t_grid)
        threshold_phi = mean(
            _bounded_phi(_phi_value(candidate, best_point, u0=u0, w0=w0))
            for u0, w0 in [(-90.0, -40.0), (-70.0, -20.0), (-50.0, 0.0)]
        )
        threshold_delta = _delta(best_point.Gamma_env, best_point.alpha, threshold_phi, spec.t_grid)
        saturation_ratio = max(phi_by_point)
        control_gain = (candidate_delta - constant_delta) / max(constant_delta, EPS)
        coordinate_score = candidate_delta - max(remove_u_delta, remove_w_delta, no_log_delta)
        threshold_score = 1.0 - min(1.0, abs(candidate_delta - threshold_delta) / max(candidate_delta, EPS))
        alpha_score = min(1.0, alpha_1_delta / max(spec.epsilon_exp, candidate_delta))
        non_saturation_score = 1.0 - saturation_ratio
        numerical_score = 1.0
        warnings = _warnings(saturation_ratio, control_gain, coordinate_score, threshold_score)
        metrics = PhiControlResistanceMetrics(
            candidate_delta=candidate_delta,
            constant_phi_delta=constant_delta,
            mean_phi_delta=mean_delta,
            remove_u_delta=remove_u_delta,
            remove_w_delta=remove_w_delta,
            no_log_delta=no_log_delta,
            alpha_1_delta=alpha_1_delta,
            saturation_ratio=saturation_ratio,
            control_gain=control_gain,
            coordinate_contribution_score=coordinate_score,
            threshold_robustness_score=threshold_score,
            alpha_sensitivity_score=alpha_score,
            non_saturation_score=non_saturation_score,
            numerical_stability_score=numerical_score,
            control_resistance_score=_score(non_saturation_score, coordinate_score, threshold_score, alpha_score, numerical_score),
            warnings=warnings,
        )
        classification = classify_phi_candidate(metrics)
    except (OverflowError, ValueError):
        metrics = PhiControlResistanceMetrics(
            candidate_delta=0.0,
            constant_phi_delta=0.0,
            mean_phi_delta=0.0,
            remove_u_delta=0.0,
            remove_w_delta=0.0,
            no_log_delta=0.0,
            alpha_1_delta=0.0,
            saturation_ratio=1.0,
            control_gain=0.0,
            coordinate_contribution_score=0.0,
            threshold_robustness_score=0.0,
            alpha_sensitivity_score=0.0,
            non_saturation_score=0.0,
            numerical_stability_score=0.0,
            control_resistance_score=0.0,
            warnings=["WARN_NUMERICAL_INSTABILITY"],
        )
        classification = "PHI_CANDIDATE_NUMERICALLY_UNSTABLE"

    return PhiCandidateEvaluationResult(
        candidate=candidate,
        classification=classification,
        canonical_status=normalize_status(classification, domain="phi_search"),
        metrics=metrics,
        allowed_uses=_allowed_uses(classification),
        blocked_uses=["Physical claim authorization", "Frontera C validation", "Experimental confirmation"],
        blocked_claims=[
            "A surviving phi validates LOG_BOUNDARY.",
            "A non-saturating phi proves Frontera C.",
            "Synthetic control resistance proves a physical effect.",
        ],
        next_actions=_next_actions(classification),
    )


def classify_phi_candidate(metrics: PhiControlResistanceMetrics) -> str:
    if metrics.numerical_stability_score <= 0.0:
        return "PHI_CANDIDATE_NUMERICALLY_UNSTABLE"
    if metrics.saturation_ratio >= 0.99:
        return "PHI_CANDIDATE_SATURATES"
    if abs(metrics.control_gain) < CONTROL_GAIN_TOLERANCE and metrics.coordinate_contribution_score <= COORDINATE_THRESHOLD:
        return "PHI_CANDIDATE_FAILS_CONSTANT_CONTROL"
    if metrics.coordinate_contribution_score <= COORDINATE_THRESHOLD:
        return "PHI_CANDIDATE_FAILS_COORDINATE_CONTRIBUTION"
    if metrics.threshold_robustness_score < 0.25:
        return "PHI_CANDIDATE_REQUIRES_THRESHOLD_TUNING"
    return "PHI_CANDIDATE_SURVIVES_CONTROLS"


def _phi_value(candidate: PhiCandidateSpec, point, *, remove_u: bool = False, remove_w: bool = False, u0: float | None = None, w0: float | None = None) -> float:
    u = 0.0 if remove_u else point.u
    w = 0.0 if remove_w else point.w
    center_u = point.u0 if u0 is None else u0
    center_w = point.w0 if w0 is None else w0
    raw = compute_phi_log(point.u, point.w, point.k, point.k2, point.u0, point.w0)
    if candidate.family == "PHI_CENTERED":
        return abs(raw - 0.6191750426941809)
    if candidate.family == "PHI_GRADIENT":
        s = sigmoid(point.k * (u - center_u))
        du = abs(point.k * s * (1.0 - s))
        tw = math.tanh(point.k2 * (w - center_w))
        dw = abs(2.0 * point.k2 * tw * (1.0 - tw * tw))
        return min(1.0, (du + dw) / 3.0)
    if candidate.family == "PHI_BANDPASS":
        sigma_u = candidate.parameters.get("sigma_u", 20.0)
        sigma_w = candidate.parameters.get("sigma_w", 20.0)
        return math.exp(-(((u - center_u) ** 2) / (sigma_u * sigma_u) + ((w - center_w) ** 2) / (sigma_w * sigma_w)))
    if candidate.family == "PHI_CURVATURE":
        s = sigmoid(point.k * (u - center_u))
        curvature_u = abs(point.k * point.k * s * (1.0 - s) * (1.0 - 2.0 * s))
        tw = math.tanh(point.k2 * (w - center_w))
        curvature_w = abs(2.0 * point.k2 * point.k2 * (1.0 - tw * tw) * (1.0 - 3.0 * tw * tw))
        return min(1.0, (curvature_u + curvature_w) / 3.0)
    if candidate.family == "PHI_RELATIVE_BOUNDARY":
        return abs(u - w) / (1.0 + abs(u) + abs(w))
    if candidate.family == "PHI_NON_SATURATING_RATIO":
        u_part = math.log1p(abs(u - center_u))
        w_part = math.log1p(abs(w - center_w))
        return u_part / (1.0 + u_part + w_part)
    if candidate.family == "PHI_COORDINATE_CONTRAST":
        z_u = (u + 63.992270844348376) / 10.0
        z_w = (w + 21.50095375174356) / 10.0
        return abs(z_u - z_w) / (1.0 + abs(z_u) + abs(z_w))
    if candidate.family == "PHI_LOCALIZED_WINDOW":
        sigma_u = candidate.parameters.get("sigma_u", 10.0)
        sigma_w = candidate.parameters.get("sigma_w", 10.0)
        return _sech((u - center_u) / sigma_u) ** 2 * _sech((w - center_w) / sigma_w) ** 2
    raise ValueError(f"Unknown phi candidate family: {candidate.family}")


def _delta(gamma_env: float, alpha: float, phi_value: float, t_grid: list[float]) -> float:
    curves = compute_visibility_curves(t_grid, Gamma_env=gamma_env, alpha=alpha, phi_log=phi_value)
    return compute_max_abs_delta(curves.V_base, curves.V_log)


def _bounded_phi(value: float) -> float:
    if not math.isfinite(value):
        raise ValueError("phi candidate produced a non-finite value")
    return max(0.0, min(1.0, value))


def _warnings(saturation_ratio: float, control_gain: float, coordinate_score: float, threshold_score: float) -> list[str]:
    warnings: list[str] = []
    if saturation_ratio >= 0.99:
        warnings.append("WARN_PHI_SATURATION")
    if abs(control_gain) < CONTROL_GAIN_TOLERANCE:
        warnings.append("WARN_CONSTANT_CONTROL_MATCH")
    if coordinate_score <= COORDINATE_THRESHOLD:
        warnings.append("WARN_LOW_COORDINATE_CONTRIBUTION")
    if threshold_score < 0.25:
        warnings.append("WARN_THRESHOLD_TUNING")
    return warnings


def _score(non_saturation: float, coordinate_score: float, threshold_score: float, alpha_score: float, numerical_score: float) -> float:
    coordinate_normalized = max(0.0, min(1.0, coordinate_score))
    return (
        0.30 * non_saturation
        + 0.25 * coordinate_normalized
        + 0.20 * threshold_score
        + 0.15 * alpha_score
        + 0.10 * numerical_score
    )


def _allowed_uses(classification: str) -> list[str]:
    if classification == "PHI_CANDIDATE_SURVIVES_CONTROLS":
        return ["Synthetic control-resistance report", "Source-search prioritization", "Benchmark-pressure prioritization"]
    return ["Synthetic failure memory", "Alternative phi search"]


def _next_actions(classification: str) -> list[str]:
    if classification == "PHI_CANDIDATE_SURVIVES_CONTROLS":
        return ["schedule source-support audit", "schedule benchmark-data search", "keep physical claims blocked"]
    if classification == "PHI_CANDIDATE_SATURATES":
        return ["reject or down-rank formulation", "add saturation warning", "search non-saturating alternatives"]
    if classification == "PHI_CANDIDATE_FAILS_CONSTANT_CONTROL":
        return ["reject formulation", "record control failure", "do not increase source pressure"]
    return ["retain result as synthetic diagnostic", "compare next phi family"]


def _sech(value: float) -> float:
    return 1.0 / math.cosh(value)
