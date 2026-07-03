"""Admissibility checks for LOG_BOUNDARY benchmark design."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.synthetic_benchmark_design.schemas import (
    EquationAdmissibilityResult,
    LogBoundaryCandidateSpec,
)


REQUIRED_DIMENSIONLESS = {"q", "b", "u", "w", "alpha", "k", "k2", "u0", "w0"}
REQUIRED_RANGES = {"alpha", "k", "k2", "u0", "w0", "Gamma_env", "m_kg", "L_m"}


def check_log_boundary_admissibility(spec: LogBoundaryCandidateSpec) -> EquationAdmissibilityResult:
    blocked: list[str] = []
    passed: list[str] = []
    warnings: list[str] = []

    if spec.observable:
        passed.append("observable_exists")
    else:
        blocked.append("FAIL_NO_OBSERVABLE")

    if spec.baseline_equation:
        passed.append("baseline_equation_exists")
    else:
        blocked.append("FAIL_NO_EXPLICIT_EQUATION")

    if spec.candidate_equation and spec.delta_gamma_equation:
        passed.append("candidate_equation_exists")
    else:
        blocked.append("FAIL_NO_EXPLICIT_EQUATION")

    declared = set(spec.dimensionless_variables)
    if REQUIRED_DIMENSIONLESS.issubset(declared):
        passed.append("dimensionless_variables_declared")
    else:
        blocked.append("FAIL_DIMENSIONAL_INCONSISTENCY")

    if "log(" not in spec.phi_function.lower() and "log(" not in spec.delta_gamma_equation.lower():
        passed.append("no_dimensionful_log_detected")
    else:
        warnings.append("log use detected; arguments must be proven dimensionless before execution.")

    if "Gamma_env" in spec.delta_gamma_equation and "alpha" in spec.delta_gamma_equation and "phi_log" in spec.delta_gamma_equation:
        passed.append("delta_gamma_log_has_rate_units_by_construction")
    else:
        blocked.append("FAIL_DIMENSIONAL_INCONSISTENCY")

    if spec.failure_conditions:
        passed.append("failure_conditions_exist")
    else:
        blocked.append("FAIL_NO_FAILURE_CONDITION")

    if REQUIRED_RANGES.issubset(set(spec.parameter_ranges)):
        passed.append("parameter_ranges_declared")
    else:
        blocked.append("FAIL_UNBOUNDED_PARAMETERS")

    if spec.scale_L_declared and not spec.scale_L_post_hoc:
        passed.append("scale_L_declared_not_post_hoc")
    else:
        blocked.append("FAIL_AD_HOC_SCALE")

    status = "SYNTHETIC_BENCHMARK_DESIGNED" if not blocked else "SYNTHETIC_BENCHMARK_BLOCKED"
    return EquationAdmissibilityResult(
        candidate_id=spec.candidate_id,
        is_admissible=not blocked,
        blocked_reasons=blocked,
        checks_passed=passed,
        warnings=warnings,
        canonical_status=normalize_status(status, domain="synthetic_benchmark_design"),
    )
