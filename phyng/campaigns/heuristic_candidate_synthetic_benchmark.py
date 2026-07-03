"""Phygn v2.3 heuristic candidate to synthetic benchmark campaign."""

from __future__ import annotations

from pathlib import Path

from phyng.synthetic_benchmark_design.log_boundary import (
    create_log_boundary_candidate_spec,
    design_synthetic_benchmark,
)
from phyng.synthetic_benchmark_design.report import write_synthetic_benchmark_design_reports
from phyng.synthetic_benchmark_design.schemas import HeuristicToBenchmarkCampaignResult


def run_heuristic_candidate_synthetic_benchmark_campaign(root: str | Path = ".") -> HeuristicToBenchmarkCampaignResult:
    repo_root = Path(root)
    spec = create_log_boundary_candidate_spec()
    design_result = design_synthetic_benchmark(spec)
    result = HeuristicToBenchmarkCampaignResult(
        campaign_id="HEURISTIC-CANDIDATE-SYNTHETIC-BENCHMARK-v2_3",
        status=design_result.status,
        candidate_spec=spec,
        design_result=design_result,
    )
    result.report_paths = write_synthetic_benchmark_design_reports(result, repo_root / "reports")
    return result
