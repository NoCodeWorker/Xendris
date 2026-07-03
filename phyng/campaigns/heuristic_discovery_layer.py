"""Phygn v2.2 heuristic discovery campaign runner."""

from __future__ import annotations

from pathlib import Path

from phyng.heuristic_discovery.pipeline import run_heuristic_to_testable_pipeline
from phyng.heuristic_discovery.report import write_heuristic_discovery_reports
from phyng.heuristic_discovery.schemas import HeuristicDiscoveryCampaignResult


def run_heuristic_discovery_layer_campaign(root: str | Path = ".") -> HeuristicDiscoveryCampaignResult:
    repo_root = Path(root)
    pipeline_result = run_heuristic_to_testable_pipeline(
        raw_problem="Find testable physical signatures near boundary regimes without overclaiming truth.",
        domain="physical_candidate",
    )
    result = HeuristicDiscoveryCampaignResult(
        campaign_id="HEURISTIC-DISCOVERY-LAYER-v2_2",
        status="HEURISTIC_TEST_DESIGN_READY",
        pipeline_result=pipeline_result,
    )
    result.report_paths = write_heuristic_discovery_reports(result, repo_root / "reports")
    return result
