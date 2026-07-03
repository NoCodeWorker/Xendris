"""Report writers for v2.7 phi search."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.synthetic_benchmark_design.schemas import PhiSearchCampaignResult


def write_phi_search_reports(result: PhiSearchCampaignResult, reports_dir: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_dir)
    execution_dir = root / "synthetic_benchmark_execution"
    campaigns_dir = root / "campaigns"
    execution_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "families": execution_dir / "phi_candidate_families_v2_7.md",
        "control_resistance": execution_dir / "phi_control_resistance_v2_7.md",
        "ranking": execution_dir / "phi_candidate_ranking_v2_7.md",
        "loop_feedback": execution_dir / "phi_search_loop_feedback_v2_7.md",
        "campaign": campaigns_dir / "LOG-BOUNDARY-NON-SATURATING-PHI-SEARCH-v2_7.md",
    }
    paths["families"].write_text(_canonical(_render_families(result), result), encoding="utf-8")
    paths["control_resistance"].write_text(_canonical(_render_control_resistance(result), result), encoding="utf-8")
    paths["ranking"].write_text(_canonical(_render_ranking(result), result), encoding="utf-8")
    paths["loop_feedback"].write_text(_canonical(_render_loop_feedback(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, result: PhiSearchCampaignResult, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="LOG_BOUNDARY Non-Saturating Phi Search v2.7",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="phi_search",
        reports_generated=reports_generated or [],
        discipline_note="A surviving phi earns pressure; a failing phi earns memory; neither earns truth.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_families(result: PhiSearchCampaignResult) -> str:
    lines = ["# Phi Candidate Families v2.7", ""]
    for evaluation in result.evaluations:
        candidate = evaluation.candidate
        lines.extend([
            f"## {candidate.family}",
            "",
            f"- Candidate Family: `{candidate.family}`",
            f"- Phi Formula: `{candidate.formula}`",
            f"- Parameters: `{candidate.parameters}`",
            f"- Boundedness Claim: {candidate.boundedness_claim}",
            f"- Dimensionless Inputs: `{', '.join(candidate.dimensionless_inputs)}`",
            f"- Known Risks: `{', '.join(candidate.known_risks)}`",
            f"- Control Expectations: `{', '.join(candidate.control_expectations)}`",
            "",
        ])
    return "\n".join(lines)


def _render_control_resistance(result: PhiSearchCampaignResult) -> str:
    lines = ["# Phi Control Resistance v2.7", ""]
    for evaluation in result.ranking.ranked_candidates:
        metrics = evaluation.metrics
        lines.extend([
            f"## {evaluation.candidate.family}",
            "",
            f"- Classification: `{evaluation.classification}`",
            f"- Synthetic Delta: `{metrics.candidate_delta}`",
            f"- Constant Control Delta: `{metrics.constant_phi_delta}`",
            f"- Mean Phi Delta: `{metrics.mean_phi_delta}`",
            f"- Remove-U Delta: `{metrics.remove_u_delta}`",
            f"- Remove-W Delta: `{metrics.remove_w_delta}`",
            f"- No-Log Delta: `{metrics.no_log_delta}`",
            f"- Saturation Ratio: `{metrics.saturation_ratio}`",
            f"- Control Gain: `{metrics.control_gain}`",
            f"- Coordinate Contribution: `{metrics.coordinate_contribution_score}`",
            f"- Threshold Robustness: `{metrics.threshold_robustness_score}`",
            f"- Alpha Sensitivity: `{metrics.alpha_sensitivity_score}`",
            f"- Warnings: `{', '.join(metrics.warnings)}`",
            "",
        ])
    return "\n".join(lines)


def _render_ranking(result: PhiSearchCampaignResult) -> str:
    return "\n".join([
        "# Phi Candidate Ranking v2.7",
        "",
        f"- status: `{result.ranking.status}`",
        f"- survivor_count: `{result.ranking.survivor_count}`",
        f"- best_candidate_family: `{result.ranking.best_candidate_family}`",
        f"- ranking_note: {result.ranking.ranking_note}",
        "",
        "## Ranking",
        "",
        *[
            f"- `{evaluation.candidate.family}`: score=`{evaluation.metrics.control_resistance_score}`, classification=`{evaluation.classification}`"
            for evaluation in result.ranking.ranked_candidates
        ],
        "",
        "## Blocked Uses",
        "",
        "- Physical claim authorization",
        "- Frontera C validation",
        "- Experimental confirmation",
    ]) + "\n"


def _render_loop_feedback(result: PhiSearchCampaignResult) -> str:
    feedback = result.loop_feedback
    return "\n".join([
        "# Phi Search Loop Feedback v2.7",
        "",
        f"- loop_event_id: `{feedback.loop_event_id}`",
        f"- result_status: `{feedback.result_status}`",
        "",
        "## Allowed Uses",
        "",
        *[f"- {item}" for item in feedback.allowed_updates],
        "",
        "## Blocked Uses",
        "",
        *[f"- {item}" for item in feedback.blocked_updates],
        "",
        "## Loop Feedback",
        "",
        *[f"- {item}" for item in feedback.next_actions],
    ]) + "\n"


def _render_campaign(result: PhiSearchCampaignResult) -> str:
    return "\n".join([
        "# Campaign Report - LOG-BOUNDARY-NON-SATURATING-PHI-SEARCH-v2_7",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- survivor_count: `{result.ranking.survivor_count}`",
        f"- best_candidate_family: `{result.ranking.best_candidate_family}`",
        "",
        "## Core Results",
        "",
        "- Phi candidate search completed under synthetic controls.",
        "- Ranking is synthetic-only and is not physical evidence.",
        "- Physical claims remain blocked.",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
