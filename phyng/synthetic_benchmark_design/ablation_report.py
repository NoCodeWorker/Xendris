"""Report writers for LOG_BOUNDARY sensitivity and ablation v2.6."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.synthetic_benchmark_design.schemas import LogBoundarySensitivityAblationCampaignResult


def write_log_boundary_ablation_reports(
    result: LogBoundarySensitivityAblationCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    execution_dir = root / "synthetic_benchmark_execution"
    campaigns_dir = root / "campaigns"
    execution_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "controls": execution_dir / "log_boundary_ablation_controls_v2_6.md",
        "metrics": execution_dir / "log_boundary_sensitivity_metrics_v2_6.md",
        "classification": execution_dir / "log_boundary_ablation_classification_v2_6.md",
        "loop_feedback": execution_dir / "log_boundary_ablation_loop_feedback_v2_6.md",
        "campaign": campaigns_dir / "LOG-BOUNDARY-SENSITIVITY-ABLATION-v2_6.md",
    }
    paths["controls"].write_text(_canonical(_render_controls(result), result), encoding="utf-8")
    paths["metrics"].write_text(_canonical(_render_metrics(result), result), encoding="utf-8")
    paths["classification"].write_text(_canonical(_render_classification(result), result), encoding="utf-8")
    paths["loop_feedback"].write_text(_canonical(_render_loop_feedback(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: LogBoundarySensitivityAblationCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    contract = build_report_contract(
        title="LOG_BOUNDARY Sensitivity Ablation v2.6",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="synthetic_benchmark_ablation",
        failure_conditions=result.ablation_result.failure_conditions,
        reports_generated=reports_generated or [],
        discipline_note="Ablation may change synthetic priority; it may not authorize physical truth.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_controls(result: LogBoundarySensitivityAblationCampaignResult) -> str:
    return "\n".join([
        "# LOG_BOUNDARY Ablation Controls v2.6",
        "",
        "## Controls Summary",
        "",
        *[
            f"- `{control.control_id}`: delta=`{control.max_abs_delta}`, phi=`{control.phi_value}`, status=`{control.detectability_status}`"
            for control in result.ablation_result.controls
        ],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in result.ablation_result.classification.blocked_claims],
    ]) + "\n"


def _render_metrics(result: LogBoundarySensitivityAblationCampaignResult) -> str:
    metrics = result.ablation_result.metrics
    return "\n".join([
        "# LOG_BOUNDARY Sensitivity Metrics v2.6",
        "",
        f"- candidate_delta: `{metrics.candidate_delta}`",
        f"- constant_phi_delta: `{metrics.constant_phi_delta}`",
        f"- mean_phi_delta: `{metrics.mean_phi_delta}`",
        f"- remove_u_delta: `{metrics.remove_u_delta}`",
        f"- remove_w_delta: `{metrics.remove_w_delta}`",
        f"- no_log_coordinates_delta: `{metrics.no_log_coordinates_delta}`",
        f"- alpha_1_delta: `{metrics.alpha_1_delta}`",
        f"- saturation_ratio: `{metrics.saturation_ratio}`",
        f"- control_gain: `{metrics.control_gain}`",
        f"- coordinate_contribution_score: `{metrics.coordinate_contribution_score}`",
        f"- threshold_sensitivity_score: `{metrics.threshold_sensitivity_score}`",
        "",
        "## Warnings",
        "",
        *[f"- `{warning}`" for warning in metrics.warnings],
    ]) + "\n"


def _render_classification(result: LogBoundarySensitivityAblationCampaignResult) -> str:
    classification = result.ablation_result.classification
    return "\n".join([
        "# LOG_BOUNDARY Ablation Classification v2.6",
        "",
        f"- ablation_status: `{classification.status}`",
        f"- reason: {classification.reason}",
        "",
        "## Allowed Claims",
        "",
        *[f"- {claim}" for claim in classification.allowed_claims],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in classification.blocked_claims],
        "",
        "## Next Actions",
        "",
        *[f"- {action}" for action in classification.next_actions],
    ]) + "\n"


def _render_loop_feedback(result: LogBoundarySensitivityAblationCampaignResult) -> str:
    feedback = result.loop_feedback
    return "\n".join([
        "# LOG_BOUNDARY Ablation Loop Feedback v2.6",
        "",
        f"- loop_event_id: `{feedback.loop_event_id}`",
        f"- ablation_status: `{feedback.ablation_status}`",
        "",
        "## Allowed Updates",
        "",
        *[f"- {item}" for item in feedback.allowed_updates],
        "",
        "## Blocked Updates",
        "",
        *[f"- {item}" for item in feedback.blocked_updates],
        "",
        "## Next Actions",
        "",
        *[f"- {item}" for item in feedback.next_actions],
    ]) + "\n"


def _render_campaign(result: LogBoundarySensitivityAblationCampaignResult) -> str:
    return "\n".join([
        "# Campaign Report - LOG-BOUNDARY-SENSITIVITY-ABLATION-v2_6",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- candidate_id: `{result.candidate_spec.candidate_id}`",
        f"- candidate_family: `{result.candidate_spec.candidate_family}`",
        "",
        "## Core Results",
        "",
        f"- Ablation classification: `{result.status}`",
        f"- Warnings: `{', '.join(result.ablation_result.metrics.warnings)}`",
        "- Physical claims remain blocked.",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
