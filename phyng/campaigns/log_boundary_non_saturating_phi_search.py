"""Phygn v2.7 LOG_BOUNDARY non-saturating phi search campaign."""

from __future__ import annotations

from pathlib import Path

from phyng.synthetic_benchmark_design.log_boundary import create_log_boundary_candidate_spec
from phyng.synthetic_benchmark_design.phi_report import write_phi_search_reports
from phyng.synthetic_benchmark_design.phi_search import generate_phi_search_loop_feedback, run_phi_candidate_search
from phyng.synthetic_benchmark_design.schemas import PhiSearchCampaignResult


def run_log_boundary_non_saturating_phi_search_campaign(root: str | Path = ".") -> PhiSearchCampaignResult:
    repo_root = Path(root)
    spec = create_log_boundary_candidate_spec()
    evaluations, ranking = run_phi_candidate_search(spec)
    loop_feedback = generate_phi_search_loop_feedback(ranking)
    result = PhiSearchCampaignResult(
        campaign_id="LOG-BOUNDARY-NON-SATURATING-PHI-SEARCH-v2_7",
        status=ranking.status,
        candidate_spec=spec,
        evaluations=evaluations,
        ranking=ranking,
        loop_feedback=loop_feedback,
    )
    result.report_paths = write_phi_search_reports(result, repo_root / "reports")
    return result
