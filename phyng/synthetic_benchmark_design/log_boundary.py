"""LOG_BOUNDARY candidate formalization and synthetic benchmark design."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.synthetic_benchmark_design.admissibility import check_log_boundary_admissibility
from phyng.synthetic_benchmark_design.detectability_protocol import build_detectability_protocol
from phyng.synthetic_benchmark_design.schemas import (
    LogBoundaryCandidateSpec,
    SyntheticBenchmarkDesign,
    SyntheticBenchmarkDesignResult,
)


def create_log_boundary_candidate_spec(
    candidate_id: str = "HEUR-PHY-003",
    observable: str = "visibility_decay",
) -> LogBoundaryCandidateSpec:
    return LogBoundaryCandidateSpec(
        candidate_id=candidate_id,
        observable=observable,
        baseline_equation="V_base(t)=exp(-Gamma_env*t)",
        candidate_equation="V_log(t)=exp(-(Gamma_env + DeltaGamma_log)*t)",
        delta_gamma_equation="DeltaGamma_log = alpha * Gamma_env * phi_log(q,b,u,w)",
        phi_function="phi_log = sigmoid(k * (u - u0)) * tanh(k2 * (w - w0))^2",
        dimensionless_variables=["q", "b", "u", "w", "alpha", "k", "k2", "u0", "w0"],
        parameters={
            "Gamma_env": 0.05,
            "alpha": 1.0,
            "k": 1.0,
            "k2": 1.0,
            "u0": -65.0,
            "w0": -20.0,
            "L_m": 1e-7,
        },
        parameter_ranges={
            "alpha": (0.0, 10.0),
            "k": (0.1, 5.0),
            "k2": (0.1, 5.0),
            "u0": (-90.0, -40.0),
            "w0": (-40.0, 5.0),
            "Gamma_env": (0.001, 1.0),
            "m_kg": (1e-20, 1e-14),
            "L_m": (1e-9, 1e-5),
        },
        t_grid=[i * 0.1 for i in range(101)],
        epsilon_exp=1e-6,
        scale_L_declared=True,
        scale_L_post_hoc=False,
        failure_conditions=[
            "FAIL_UNDETECTABLE_DELTA",
            "FAIL_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS",
            "FAIL_NO_SOURCE_SUPPORT",
            "FAIL_NO_BENCHMARK",
            "FAIL_NO_EXPERIMENTAL_DATA",
        ],
        canonical_status=normalize_status("HEURISTIC_TEST_DESIGN_READY", domain="heuristic_discovery"),
    )


def design_synthetic_benchmark(spec: LogBoundaryCandidateSpec) -> SyntheticBenchmarkDesignResult:
    admissibility = check_log_boundary_admissibility(spec)
    if not admissibility.is_admissible:
        return SyntheticBenchmarkDesignResult(
            candidate_id=spec.candidate_id,
            status="SYNTHETIC_BENCHMARK_BLOCKED",
            admissibility=admissibility,
            canonical_status=normalize_status("SYNTHETIC_BENCHMARK_BLOCKED", domain="synthetic_benchmark_design"),
            allowed_claims=["The candidate has been checked for formalization blockers."],
            blocked_claims=[
                "Synthetic benchmark execution",
                "Physical prediction",
                "Experimental validation",
            ],
            next_actions=["Resolve admissibility blockers before benchmark design."],
        )

    design = SyntheticBenchmarkDesign(
        candidate_id=spec.candidate_id,
        baseline_model=spec.baseline_equation,
        candidate_model=spec.candidate_equation,
        delta_metric="max_abs_delta = max_t |V_log(t) - V_base(t)|",
        t_grid=spec.t_grid,
        parameter_sweep_plan={
            "alpha_values": [0.1, 1.0, 3.0, 10.0],
            "k_values": [0.5, 1.0, 2.0, 5.0],
            "k2_values": [0.5, 1.0, 2.0, 5.0],
            "u0_values": [-90.0, -70.0, -50.0],
            "w0_values": [-40.0, -20.0, 0.0],
            "Gamma_env_values": [0.01, 0.05, 0.1],
        },
        epsilon_exp=spec.epsilon_exp,
        failure_conditions=spec.failure_conditions,
    )
    protocol = build_detectability_protocol(spec)
    return SyntheticBenchmarkDesignResult(
        candidate_id=spec.candidate_id,
        status="SYNTHETIC_BENCHMARK_DESIGNED",
        admissibility=admissibility,
        benchmark_design=design,
        detectability_protocol=protocol,
        canonical_status=normalize_status("SYNTHETIC_BENCHMARK_DESIGNED", domain="synthetic_benchmark_design"),
        allowed_claims=[
            "LOG_BOUNDARY has an explicit toy equation.",
            "LOG_BOUNDARY has declared parameter ranges.",
            "LOG_BOUNDARY has a synthetic benchmark design.",
            "LOG_BOUNDARY may proceed to synthetic execution.",
        ],
        blocked_claims=[
            "Physical prediction",
            "Experimental validation",
            "Source-backed claim",
            "Benchmark-supported claim without benchmark execution/data.",
        ],
        next_actions=[
            "Execute synthetic benchmark.",
            "Run parameter sweep.",
            "Compute max_abs_delta.",
            "Classify detectability.",
            "Search source support and benchmark data.",
        ],
    )
