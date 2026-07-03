"""Detectability and failure protocol for LOG_BOUNDARY synthetic design."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.synthetic_benchmark_design.schemas import DetectabilityProtocolSpec, LogBoundaryCandidateSpec


def build_detectability_protocol(spec: LogBoundaryCandidateSpec) -> DetectabilityProtocolSpec:
    return DetectabilityProtocolSpec(
        candidate_id=spec.candidate_id,
        baseline_equation=spec.baseline_equation,
        candidate_equation=spec.candidate_equation,
        delta_equation="delta(t) = V_log(t) - V_base(t)",
        detectability_metric="max_abs_delta = max_t |delta(t)|",
        epsilon_exp=spec.epsilon_exp,
        alpha_sweep=[0.1, 1.0, 3.0, 10.0],
        k_sweep=[0.5, 1.0, 2.0, 5.0],
        u0_sweep=[-90.0, -70.0, -50.0],
        w0_sweep=[-40.0, -20.0, 0.0],
        detectability_classification_rule=(
            "DETECTABLE_SYNTHETIC_DELTA if max_abs_delta > epsilon_exp; "
            "otherwise UNDETECTABLE_SYNTHETIC_DELTA"
        ),
        failure_classification_rules=[
            "FAIL_NO_EXPLICIT_EQUATION",
            "FAIL_DIMENSIONAL_INCONSISTENCY",
            "FAIL_NO_OBSERVABLE",
            "FAIL_NO_FAILURE_CONDITION",
            "FAIL_AD_HOC_SCALE",
            "FAIL_UNDETECTABLE_DELTA",
            "FAIL_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS",
            "FAIL_NO_SOURCE_SUPPORT",
            "FAIL_NO_BENCHMARK",
            "FAIL_NO_EXPERIMENTAL_DATA",
        ],
        canonical_status=normalize_status("SYNTHETIC_BENCHMARK_DESIGNED", domain="synthetic_benchmark_design"),
    )
