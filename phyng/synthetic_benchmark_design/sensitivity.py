"""Sensitivity metrics and classification for LOG_BOUNDARY ablation."""

from __future__ import annotations

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.synthetic_benchmark_design.ablation import run_log_boundary_ablation_suite
from phyng.synthetic_benchmark_design.schemas import (
    LogBoundaryAblationClassification,
    LogBoundaryAblationLoopFeedbackResult,
    LogBoundaryAblationResult,
    LogBoundaryExecutionResult,
    LogBoundarySensitivityMetrics,
)

EPS = 1e-12
CONTROL_GAIN_TOLERANCE = 0.01
COORDINATE_CONTRIBUTION_TOLERANCE = 1e-3


def run_log_boundary_sensitivity_ablation(execution: LogBoundaryExecutionResult) -> LogBoundaryAblationResult:
    controls = run_log_boundary_ablation_suite(execution)
    metrics = compute_log_boundary_sensitivity_metrics(execution, controls)
    classification = classify_log_boundary_ablation(metrics, execution)
    failure_conditions = list(execution.failure_conditions)
    if classification.status != "LOG_BOUNDARY_SURVIVES_ABLATION":
        failure_conditions.append(classification.status)
    return LogBoundaryAblationResult(
        candidate_id=execution.candidate_id,
        execution_result=execution,
        controls=controls,
        metrics=metrics,
        classification=classification,
        failure_conditions=_unique(failure_conditions),
    )


def compute_log_boundary_sensitivity_metrics(
    execution: LogBoundaryExecutionResult,
    controls,
) -> LogBoundarySensitivityMetrics:
    best = execution.sweep_result.best_point
    if best is None:
        return LogBoundarySensitivityMetrics(
            candidate_delta=0.0,
            constant_phi_delta=0.0,
            mean_phi_delta=0.0,
            remove_u_delta=0.0,
            remove_w_delta=0.0,
            no_log_coordinates_delta=0.0,
            alpha_1_delta=0.0,
            saturation_ratio=0.0,
            control_gain=0.0,
            coordinate_contribution_score=0.0,
            threshold_sensitivity_score=0.0,
            warnings=["WARN_ABLATION_BLOCKED"],
        )

    by_id = {control.control_id: control for control in controls}
    candidate_delta = best.max_abs_delta
    constant_delta = by_id["CONTROL_CONSTANT_PHI_ONE"].max_abs_delta
    remove_u_delta = by_id["CONTROL_REMOVE_U"].max_abs_delta
    remove_w_delta = by_id["CONTROL_REMOVE_W"].max_abs_delta
    no_log_delta = by_id["CONTROL_NO_LOG_COORDINATES"].max_abs_delta
    threshold_delta = by_id["CONTROL_RANDOM_U0_W0"].max_abs_delta
    control_gain = (candidate_delta - constant_delta) / max(constant_delta, EPS)
    coordinate_score = candidate_delta - max(remove_u_delta, remove_w_delta, no_log_delta)
    threshold_score = abs(candidate_delta - threshold_delta) / max(candidate_delta, EPS)
    warnings: list[str] = []
    if best.phi_log >= 0.99:
        warnings.append("WARN_PHI_SATURATION")
    if abs(control_gain) < CONTROL_GAIN_TOLERANCE:
        warnings.append("WARN_CONSTANT_CONTROL_MATCH")
    if coordinate_score <= COORDINATE_CONTRIBUTION_TOLERANCE:
        warnings.append("WARN_LOW_COORDINATE_CONTRIBUTION")
    if by_id["CONTROL_ALPHA_ONE"].max_abs_delta <= execution.sweep_result.epsilon_exp and candidate_delta > execution.sweep_result.epsilon_exp:
        warnings.append("WARN_ALPHA_DEPENDENCE")
    if threshold_score > 0.75:
        warnings.append("WARN_THRESHOLD_TUNING")

    return LogBoundarySensitivityMetrics(
        candidate_delta=candidate_delta,
        constant_phi_delta=constant_delta,
        mean_phi_delta=by_id["CONTROL_CONSTANT_PHI_MEAN"].max_abs_delta,
        remove_u_delta=remove_u_delta,
        remove_w_delta=remove_w_delta,
        no_log_coordinates_delta=no_log_delta,
        alpha_1_delta=by_id["CONTROL_ALPHA_ONE"].max_abs_delta,
        saturation_ratio=best.phi_log,
        control_gain=control_gain,
        coordinate_contribution_score=coordinate_score,
        threshold_sensitivity_score=threshold_score,
        warnings=warnings,
    )


def classify_log_boundary_ablation(
    metrics: LogBoundarySensitivityMetrics,
    execution: LogBoundaryExecutionResult | None = None,
) -> LogBoundaryAblationClassification:
    if execution is not None and execution.status == "LOG_BOUNDARY_EXECUTION_BLOCKED":
        return _classification("LOG_BOUNDARY_ABLATION_BLOCKED", "v2.5 execution was blocked.", metrics.warnings)
    if "WARN_PHI_SATURATION" in metrics.warnings and "WARN_CONSTANT_CONTROL_MATCH" in metrics.warnings:
        return _classification(
            "LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT",
            "Candidate delta matches the constant phi=1 control while phi_log is saturated.",
            metrics.warnings,
        )
    if abs(metrics.control_gain) < CONTROL_GAIN_TOLERANCE:
        return _classification("LOG_BOUNDARY_FAILS_CONSTANT_CONTROL", "Candidate does not beat constant phi control.", metrics.warnings)
    if "WARN_LOW_COORDINATE_CONTRIBUTION" in metrics.warnings:
        return _classification(
            "LOG_BOUNDARY_FAILS_COORDINATE_CONTRIBUTION",
            "Coordinate removal controls preserve the candidate signal.",
            metrics.warnings,
        )
    if "WARN_ALPHA_DEPENDENCE" in metrics.warnings:
        return _classification("LOG_BOUNDARY_SIGNAL_REQUIRES_ALPHA_EXTREME", "Detectability depends on high alpha.", metrics.warnings)
    if "WARN_THRESHOLD_TUNING" in metrics.warnings:
        return _classification(
            "LOG_BOUNDARY_SIGNAL_REQUIRES_THRESHOLD_TUNING",
            "Threshold changes strongly affect detectability.",
            metrics.warnings,
        )
    if metrics.candidate_delta > 0.0 and metrics.coordinate_contribution_score > COORDINATE_CONTRIBUTION_TOLERANCE:
        return _classification("LOG_BOUNDARY_SURVIVES_ABLATION", "Candidate differs from controls under declared toy ablation.", metrics.warnings)
    return _classification("LOG_BOUNDARY_SENSITIVITY_INCONCLUSIVE", "Ablation did not produce a decisive diagnostic.", metrics.warnings)


def generate_log_boundary_ablation_loop_feedback(
    ablation_result: LogBoundaryAblationResult,
) -> LogBoundaryAblationLoopFeedbackResult:
    loop_input = CandidateLoopInput(
        loop_id="LOG-BOUNDARY-ABLATION-v2_6",
        input_type="SYNTHETIC_ABLATION_RESULT",
        domain="physical_candidate",
        candidate_id=ablation_result.candidate_id,
        candidate_family=ablation_result.candidate_family,
        previous_status="LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA",
        result_status=ablation_result.classification.status,
        payload={
            "metrics": ablation_result.metrics.model_dump(),
            "failure_conditions": ablation_result.failure_conditions,
            "warnings": ablation_result.metrics.warnings,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposals = [_proposal_for_ablation(ablation_result)]
    allowed_updates, next_actions = _feedback_actions(ablation_result.classification.status)
    blocked_updates = [
        "physical claim authorization",
        "Frontera C validation",
        "experimental confirmation",
        "source requirement reduction",
        "benchmark requirement reduction",
        "canonical permission semantic change",
    ]
    return LogBoundaryAblationLoopFeedbackResult(
        loop_event_id=loop_result.audit_event_id,
        candidate_id=ablation_result.candidate_id,
        ablation_status=ablation_result.classification.status,
        canonical_status=ablation_result.classification.canonical_status,
        candidate_loop_input=loop_input,
        candidate_loop_result=loop_result,
        update_proposals=proposals,
        allowed_updates=allowed_updates,
        blocked_updates=blocked_updates,
        next_actions=next_actions,
        blocked_claims=ablation_result.classification.blocked_claims,
    )


def _classification(status: str, reason: str, warnings: list[str]) -> LogBoundaryAblationClassification:
    survival = status == "LOG_BOUNDARY_SURVIVES_ABLATION"
    allowed = ["Synthetic ablation result reporting"]
    if survival:
        allowed.extend(["Source-search prioritization", "Benchmark-pressure prioritization"])
    return LogBoundaryAblationClassification(
        status=status,
        canonical_status=normalize_status(status, domain="synthetic_benchmark_ablation"),
        reason=reason,
        allowed_claims=allowed,
        blocked_claims=[
            "LOG_BOUNDARY predicts physical decoherence.",
            "LOG_BOUNDARY validates Frontera C.",
            "Synthetic ablation proves a real-world effect.",
        ],
        next_actions=_feedback_actions(status)[1],
        warnings=warnings,
    )


def _proposal_for_ablation(ablation_result: LogBoundaryAblationResult) -> CandidateUpdateProposal:
    status = ablation_result.classification.status
    allowed_updates, next_actions = _feedback_actions(status)
    return CandidateUpdateProposal(
        proposal_id=f"LOG-BOUNDARY-ABLATION-v2_6-{status}",
        proposal_type="SYNTHETIC_ABLATION_FEEDBACK",
        candidate_id=ablation_result.candidate_id,
        candidate_family=ablation_result.candidate_family,
        description=ablation_result.classification.reason,
        proposed_change={"allowed_updates": allowed_updates, "next_actions": next_actions},
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=status != "LOG_BOUNDARY_SURVIVES_ABLATION",
        forbidden_actions=["authorize physical claim", "validate Frontera C", "relax source requirement"],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )


def _feedback_actions(status: str) -> tuple[list[str], list[str]]:
    if status == "LOG_BOUNDARY_SURVIVES_ABLATION":
        return (
            ["increase source-search priority", "increase benchmark-pressure priority"],
            ["schedule source support audit", "schedule benchmark data search", "keep physical claims blocked"],
        )
    if status == "LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT":
        return (
            ["block source-pressure upgrade"],
            ["down-rank current phi formulation", "create simpler control report", "search alternative non-saturating phi functions"],
        )
    if status == "LOG_BOUNDARY_FAILS_CONSTANT_CONTROL":
        return (["do not increase LOG_BOUNDARY priority"], ["record control failure", "compare next candidate family"])
    if status == "LOG_BOUNDARY_SIGNAL_REQUIRES_ALPHA_EXTREME":
        return (["block priority upgrade"], ["require alpha justification", "search source constraints on alpha"])
    if status == "LOG_BOUNDARY_SIGNAL_REQUIRES_THRESHOLD_TUNING":
        return (["block post-hoc threshold tuning"], ["require pre-registered thresholds", "rerun threshold robustness test"])
    return (["block automatic promotion"], ["review ablation diagnostics", "compare next candidate family"])


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result
