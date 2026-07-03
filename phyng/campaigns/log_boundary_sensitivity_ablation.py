"""Phygn v2.6 LOG_BOUNDARY sensitivity and ablation campaign."""

from __future__ import annotations

from pathlib import Path

from phyng.synthetic_benchmark_design.ablation_report import write_log_boundary_ablation_reports
from phyng.synthetic_benchmark_design.execution import execute_log_boundary_synthetic_benchmark
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.schemas import LogBoundarySensitivityAblationCampaignResult
from phyng.synthetic_benchmark_design.sensitivity import (
    generate_log_boundary_ablation_loop_feedback,
    run_log_boundary_sensitivity_ablation,
)


def run_log_boundary_sensitivity_ablation_campaign(
    root: str | Path = ".",
) -> LogBoundarySensitivityAblationCampaignResult:
    repo_root = Path(root)
    spec = create_log_boundary_candidate_spec()
    execution_result = execute_log_boundary_synthetic_benchmark(spec)
    ablation_result = run_log_boundary_sensitivity_ablation(execution_result)
    loop_feedback = generate_log_boundary_ablation_loop_feedback(ablation_result)
    result = LogBoundarySensitivityAblationCampaignResult(
        campaign_id="LOG-BOUNDARY-SENSITIVITY-ABLATION-v2_6",
        status=ablation_result.classification.status,
        candidate_spec=spec,
        execution_result=execution_result,
        ablation_result=ablation_result,
        loop_feedback=loop_feedback,
    )
    result.report_paths = write_log_boundary_ablation_reports(result, repo_root / "reports")
    return result
