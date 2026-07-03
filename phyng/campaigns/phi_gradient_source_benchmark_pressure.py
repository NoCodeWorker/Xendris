"""Phygn v2.8 PHI_GRADIENT source and benchmark pressure campaign."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.source_pressure.benchmark_pressure import assess_benchmark_pressure
from phyng.source_pressure.phi_gradient_audit import default_benchmark_fixtures, default_source_fixtures, run_phi_gradient_source_pressure_audit
from phyng.source_pressure.report import write_phi_gradient_source_pressure_reports
from phyng.source_pressure.schemas import BenchmarkPressureRecord, PhiGradientSourceBenchmarkCampaignResult, SourceCandidate


def run_phi_gradient_source_benchmark_pressure_campaign(
    root: str | Path = ".",
    sources: list[SourceCandidate] | None = None,
    benchmarks: list[BenchmarkPressureRecord] | None = None,
) -> PhiGradientSourceBenchmarkCampaignResult:
    repo_root = Path(root)
    source_result = run_phi_gradient_source_pressure_audit(sources if sources is not None else default_source_fixtures())
    benchmark_results = [assess_benchmark_pressure(record) for record in (benchmarks if benchmarks is not None else default_benchmark_fixtures())]
    status = _campaign_status(source_result.status, benchmark_results)
    loop_input = CandidateLoopInput(
        loop_id="PHI-GRADIENT-SOURCE-BENCHMARK-v2_8",
        input_type="SOURCE_BENCHMARK_PRESSURE_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        previous_status="PHI_CANDIDATE_SURVIVES_CONTROLS",
        result_status=status,
        payload={"source_status": source_result.status, "benchmark_statuses": [item.status for item in benchmark_results]},
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposal = CandidateUpdateProposal(
        proposal_id=f"PHI-GRADIENT-SOURCE-BENCHMARK-v2_8-{status}",
        proposal_type="SOURCE_BENCHMARK_PRESSURE_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        description="PHI_GRADIENT received fixture-based source and benchmark pressure; physical claims remain blocked.",
        proposed_change={"status": status, "real_literature_acquisition_required": True},
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=status != "PHI_GRADIENT_BENCHMARK_DATA_FOUND",
        forbidden_actions=["authorize physical claim", "validate Frontera C", "relax source requirement"],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    result = PhiGradientSourceBenchmarkCampaignResult(
        campaign_id="PHI-GRADIENT-SOURCE-BENCHMARK-PRESSURE-v2_8",
        status=status,
        source_result=source_result,
        benchmark_results=benchmark_results,
        loop_input=loop_input,
        loop_result=loop_result,
        update_proposals=[proposal],
    )
    result.report_paths = write_phi_gradient_source_pressure_reports(result, repo_root / "reports")
    return result


def _campaign_status(source_status: str, benchmark_results) -> str:
    if source_status == "PHI_GRADIENT_CONTRADICTED_BY_SOURCE":
        return source_status
    if any(result.status == "BENCHMARK_SUPPORTS_CANDIDATE_LIMITED" for result in benchmark_results):
        return "PHI_GRADIENT_BENCHMARK_DATA_FOUND"
    return source_status
