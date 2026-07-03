"""Phygn v2.5 LOG_BOUNDARY synthetic execution campaign."""

from __future__ import annotations

from pathlib import Path

from phyng.synthetic_benchmark_design.execution import (
    execute_log_boundary_synthetic_benchmark,
    write_log_boundary_execution_reports,
)
from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.loop_feedback import generate_log_boundary_loop_feedback
from phyng.synthetic_benchmark_design.schemas import LogBoundarySyntheticExecutionCampaignResult


def run_log_boundary_synthetic_execution_campaign(
    root: str | Path = ".",
) -> LogBoundarySyntheticExecutionCampaignResult:
    repo_root = Path(root)
    spec = create_log_boundary_candidate_spec()
    execution_result = execute_log_boundary_synthetic_benchmark(spec)
    loop_feedback = generate_log_boundary_loop_feedback(execution_result)
    result = LogBoundarySyntheticExecutionCampaignResult(
        campaign_id="LOG-BOUNDARY-SYNTHETIC-EXECUTION-v2_5",
        status=execution_result.status,
        candidate_spec=spec,
        execution_result=execution_result,
        loop_feedback=loop_feedback,
    )
    result.report_paths = write_log_boundary_execution_reports(result, repo_root / "reports")
    return result
