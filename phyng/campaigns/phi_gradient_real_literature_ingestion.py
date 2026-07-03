"""Phygn v2.9 PHI_GRADIENT real literature ingestion campaign."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.real_source_ingestion.benchmark_ingestion import default_benchmark_doubles
from phyng.real_source_ingestion.extract_validation import default_extract_doubles
from phyng.real_source_ingestion.manifest import build_real_source_manifest, default_manifest_entries
from phyng.real_source_ingestion.phi_gradient_real_source_gate import run_phi_gradient_real_source_gate
from phyng.real_source_ingestion.report import write_phi_gradient_real_source_reports
from phyng.real_source_ingestion.schemas import (
    PhiGradientRealLiteratureCampaignResult,
    RealBenchmarkRecord,
    RealSourceExtract,
    RealSourceManifestEntry,
)


def run_phi_gradient_real_literature_ingestion_campaign(
    root: str | Path = ".",
    manifest_entries: list[RealSourceManifestEntry] | None = None,
    extracts: list[RealSourceExtract] | None = None,
    benchmarks: list[RealBenchmarkRecord] | None = None,
) -> PhiGradientRealLiteratureCampaignResult:
    repo_root = Path(root)
    manifest = build_real_source_manifest(manifest_entries if manifest_entries is not None else default_manifest_entries())
    gate_result = run_phi_gradient_real_source_gate(
        manifest,
        extracts if extracts is not None else default_extract_doubles(),
        benchmarks if benchmarks is not None else default_benchmark_doubles(),
    )
    loop_input = CandidateLoopInput(
        loop_id="PHI-GRADIENT-REAL-LITERATURE-v2_9",
        input_type="REAL_SOURCE_INGESTION_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        previous_status="PHI_GRADIENT_BENCHMARK_DATA_FOUND_FIXTURE_ONLY",
        result_status=gate_result.status,
        payload={
            "actual_real_sources_ingested": gate_result.actual_real_sources_ingested,
            "missing_requirements": gate_result.missing_requirements,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposal = CandidateUpdateProposal(
        proposal_id=f"PHI-GRADIENT-REAL-LITERATURE-v2_9-{gate_result.status}",
        proposal_type="REAL_SOURCE_INGESTION_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        description="Real-source ingestion gate executed; test doubles do not count as real support.",
        proposed_change={"status": gate_result.status, "actual_real_sources_ingested": gate_result.actual_real_sources_ingested},
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=True,
        forbidden_actions=["authorize physical claim", "validate Frontera C", "count test doubles as real literature"],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    result = PhiGradientRealLiteratureCampaignResult(
        campaign_id="PHI-GRADIENT-REAL-LITERATURE-INGESTION-v2_9",
        status=gate_result.status,
        gate_result=gate_result,
        loop_input=loop_input,
        loop_result=loop_result,
        update_proposals=[proposal],
    )
    result.report_paths = write_phi_gradient_real_source_reports(result, repo_root / "reports")
    return result
