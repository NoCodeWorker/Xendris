"""Execution and reporting for LOG_BOUNDARY synthetic benchmark v2.5."""

from __future__ import annotations

from pathlib import Path

from phyng.core.compatibility import normalize_status
from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.synthetic_benchmark_design.schemas import (
    LogBoundaryCandidateSpec,
    LogBoundaryExecutionResult,
    LogBoundarySweepResult,
    LogBoundarySyntheticExecutionCampaignResult,
)
from phyng.synthetic_benchmark_design.sweep import run_log_boundary_sweep


def execute_log_boundary_synthetic_benchmark(spec: LogBoundaryCandidateSpec) -> LogBoundaryExecutionResult:
    try:
        sweep = run_log_boundary_sweep(spec)
    except (OverflowError, ValueError) as exc:
        failure_conditions = ["FAIL_EMPTY_SWEEP", "FAIL_NUMERICAL_INSTABILITY"]
        empty_sweep = LogBoundarySweepResult(
            candidate_id=spec.candidate_id,
            sweep_count=0,
            epsilon_exp=spec.epsilon_exp,
            best_point=None,
            points=[],
            failure_conditions=failure_conditions,
        )
        return LogBoundaryExecutionResult(
            candidate_id=spec.candidate_id,
            status="LOG_BOUNDARY_EXECUTION_BLOCKED",
            sweep_result=empty_sweep,
            canonical_status=normalize_status("LOG_BOUNDARY_EXECUTION_BLOCKED", domain="synthetic_benchmark_execution"),
            blocked_claims=_always_blocked_claims(),
            failure_conditions=failure_conditions,
            next_actions=[f"Review numerical inputs before rerunning the sweep; error type: {type(exc).__name__}."],
        )

    status = classify_execution_status(sweep)
    failure_conditions = list(sweep.failure_conditions)
    _extend_unique(failure_conditions, ["FAIL_NO_SOURCE_SUPPORT", "FAIL_NO_BENCHMARK", "FAIL_NO_EXPERIMENTAL_DATA"])

    if status == "LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA":
        allowed_claims = [
            "LOG_BOUNDARY produced a detectable synthetic delta under declared toy parameters.",
            "LOG_BOUNDARY may proceed to source/benchmark pressure.",
            "Candidate priority may be updated.",
        ]
        next_actions = [
            "increase source-search priority",
            "increase benchmark-pressure priority",
            "schedule source support audit",
            "schedule benchmark data search",
            "keep physical claims blocked",
        ]
    elif status == "LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA":
        allowed_claims = [
            "LOG_BOUNDARY did not produce a detectable synthetic delta under declared toy parameters.",
            "LOG_BOUNDARY can be down-ranked as a synthetic negative result.",
        ]
        next_actions = ["down-rank LOG_BOUNDARY", "record synthetic negative result", "select next heuristic family"]
    else:
        allowed_claims = ["LOG_BOUNDARY synthetic execution produced a gated result requiring review."]
        next_actions = ["require parameter justification", "block priority elevation unless source-backed"]

    return LogBoundaryExecutionResult(
        candidate_id=spec.candidate_id,
        status=status,
        sweep_result=sweep,
        canonical_status=normalize_status(status, domain="synthetic_benchmark_execution"),
        allowed_claims=allowed_claims,
        blocked_claims=_always_blocked_claims(),
        failure_conditions=failure_conditions,
        next_actions=next_actions,
    )


def classify_execution_status(sweep: LogBoundarySweepResult) -> str:
    if sweep.best_point is None:
        return "LOG_BOUNDARY_EXECUTION_BLOCKED"
    reasonableness = sweep.best_point.parameter_reasonableness
    if sweep.best_point.max_abs_delta <= sweep.epsilon_exp:
        return "LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA"
    if reasonableness.is_post_hoc:
        return "LOG_BOUNDARY_DETECTABLE_ONLY_WITH_POST_HOC_TUNING"
    if reasonableness.is_extreme_toy_range or reasonableness.is_unjustified_or_unphysical:
        return "LOG_BOUNDARY_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS"
    return "LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA"


def write_log_boundary_execution_reports(
    result: LogBoundarySyntheticExecutionCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    execution_dir = root / "synthetic_benchmark_execution"
    campaigns_dir = root / "campaigns"
    execution_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "sweep": execution_dir / "log_boundary_numerical_sweep_v2_5.md",
        "detectability": execution_dir / "log_boundary_detectability_v2_5.md",
        "failure_conditions": execution_dir / "log_boundary_failure_conditions_v2_5.md",
        "loop_feedback": execution_dir / "log_boundary_loop_feedback_v2_5.md",
        "campaign": campaigns_dir / "LOG-BOUNDARY-SYNTHETIC-EXECUTION-v2_5.md",
    }
    paths["sweep"].write_text(_canonical(_render_sweep(result), result), encoding="utf-8")
    paths["detectability"].write_text(_canonical(_render_detectability(result), result), encoding="utf-8")
    paths["failure_conditions"].write_text(_canonical(_render_failure_conditions(result), result), encoding="utf-8")
    paths["loop_feedback"].write_text(_canonical(_render_loop_feedback(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: LogBoundarySyntheticExecutionCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    contract = build_report_contract(
        title="LOG_BOUNDARY Synthetic Execution v2.5",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="synthetic_benchmark_execution",
        failure_conditions=result.execution_result.failure_conditions,
        reports_generated=reports_generated or [],
        discipline_note="Synthetic signal may update search priority; it may not authorize physical truth.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_sweep(result: LogBoundarySyntheticExecutionCampaignResult) -> str:
    sweep = result.execution_result.sweep_result
    best = sweep.best_point
    lines = [
        "# LOG_BOUNDARY Numerical Sweep v2.5",
        "",
        f"- candidate_id: `{sweep.candidate_id}`",
        f"- candidate_family: `{sweep.candidate_family}`",
        f"- parameter_grid_size: `{sweep.sweep_count}`",
        f"- epsilon_exp: `{sweep.epsilon_exp}`",
    ]
    if best:
        lines.extend([
            f"- best_max_abs_delta: `{best.max_abs_delta}`",
            f"- best_status: `{best.detectability_status}`",
            "",
            "## Best Parameter Record",
            "",
            f"- alpha: `{best.alpha}`",
            f"- k: `{best.k}`",
            f"- k2: `{best.k2}`",
            f"- u0: `{best.u0}`",
            f"- w0: `{best.w0}`",
            f"- Gamma_env: `{best.Gamma_env}`",
            f"- m_kg: `{best.m_kg}`",
            f"- L_m: `{best.L_m}`",
            f"- q: `{best.q}`",
            f"- b: `{best.b}`",
            f"- u: `{best.u}`",
            f"- w: `{best.w}`",
            f"- phi_log: `{best.phi_log}`",
            f"- DeltaGamma_log: `{best.DeltaGamma_log}`",
        ])
    return "\n".join(lines) + "\n"


def _render_detectability(result: LogBoundarySyntheticExecutionCampaignResult) -> str:
    return "\n".join([
        "# LOG_BOUNDARY Detectability v2.5",
        "",
        f"- detectability_status: `{result.status}`",
        f"- parameter_reasonableness: `{_parameter_classification(result)}`",
        "",
        "## Allowed Claims",
        "",
        *[f"- {claim}" for claim in result.execution_result.allowed_claims],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in result.execution_result.blocked_claims],
    ]) + "\n"


def _render_failure_conditions(result: LogBoundarySyntheticExecutionCampaignResult) -> str:
    return "\n".join([
        "# LOG_BOUNDARY Failure Conditions v2.5",
        "",
        *[f"- `{failure}`" for failure in result.execution_result.failure_conditions],
        "",
        "## Blocked Physical Claims",
        "",
        *[f"- {claim}" for claim in result.execution_result.blocked_claims],
    ]) + "\n"


def _render_loop_feedback(result: LogBoundarySyntheticExecutionCampaignResult) -> str:
    feedback = result.loop_feedback
    return "\n".join([
        "# LOG_BOUNDARY Loop Feedback v2.5",
        "",
        f"- loop_event_id: `{feedback.loop_event_id}`",
        f"- candidate_id: `{feedback.candidate_id}`",
        f"- result_status: `{feedback.result_status}`",
        f"- canonical_status: `{feedback.canonical_status.domain_status}`",
        f"- shadow_mode_required: `{feedback.shadow_mode_required}`",
        f"- human_review_required: `{feedback.human_review_required}`",
        "",
        "## Update Proposals",
        "",
        *[f"- `{proposal.proposal_type}`: {proposal.description}" for proposal in feedback.update_proposals],
        "",
        "## Blocked Updates",
        "",
        *[f"- {item}" for item in feedback.blocked_updates],
        "",
        "## Next Actions",
        "",
        *[f"- {item}" for item in feedback.next_actions],
    ]) + "\n"


def _render_campaign(result: LogBoundarySyntheticExecutionCampaignResult) -> str:
    return "\n".join([
        "# Campaign Report - LOG-BOUNDARY-SYNTHETIC-EXECUTION-v2_5",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- candidate_id: `{result.candidate_spec.candidate_id}`",
        f"- candidate_family: `{result.candidate_spec.candidate_family}`",
        f"- sweep_count: `{result.execution_result.sweep_result.sweep_count}`",
        "",
        "## Core Results",
        "",
        "- LOG_BOUNDARY synthetic benchmark was executed under declared toy parameters.",
        "- Detectability remains synthetic-only.",
        "- Physical claims remain blocked.",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"


def _parameter_classification(result: LogBoundarySyntheticExecutionCampaignResult) -> str:
    best = result.execution_result.sweep_result.best_point
    if best is None:
        return "None"
    return best.parameter_reasonableness.classification


def _always_blocked_claims() -> list[str]:
    return [
        "LOG_BOUNDARY predicts physical decoherence.",
        "LOG_BOUNDARY validates Frontera C.",
        "Synthetic delta proves a physical effect.",
        "Toy parameter sweep establishes real-world detectability.",
    ]


def _extend_unique(target: list[str], values: list[str]) -> None:
    for value in values:
        if value not in target:
            target.append(value)
