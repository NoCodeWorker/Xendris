"""Phygn v3.0 PHI_GRADIENT real source acquisition campaign."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.real_source_acquisition.campaign_gate import run_phi_gradient_real_source_acquisition
from phyng.real_source_acquisition.report import write_phi_gradient_real_source_acquisition_reports
from phyng.real_source_acquisition.schemas import (
    PhiGradientRealSourceAcquisitionCampaignResult,
    SourceAcquisitionBackend,
)
from phyng.real_source_ingestion.schemas import RealSourceExtract


def run_phi_gradient_real_source_acquisition_campaign(
    root: str | Path = ".",
    backend: SourceAcquisitionBackend | None = None,
    extracts_by_source_id: dict[str, RealSourceExtract] | None = None,
) -> PhiGradientRealSourceAcquisitionCampaignResult:
    repo_root = Path(root)
    acquisition_result = run_phi_gradient_real_source_acquisition(
        backend=backend,
        extracts_by_source_id=extracts_by_source_id,
    )
    loop_input = CandidateLoopInput(
        loop_id="PHI-GRADIENT-REAL-SOURCE-ACQUISITION-v3_0",
        input_type="REAL_SOURCE_ACQUISITION_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        previous_status="PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE",
        result_status=acquisition_result.status,
        payload={
            "backend_status": acquisition_result.backend_status,
            "actual_real_sources_acquired": acquisition_result.actual_real_sources_acquired,
            "actual_real_extracts_validated": acquisition_result.actual_real_extracts_validated,
            "missing_slots": acquisition_result.slot_coverage.missing_slots,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposal = CandidateUpdateProposal(
        proposal_id=f"PHI-GRADIENT-REAL-SOURCE-ACQUISITION-v3_0-{acquisition_result.status}",
        proposal_type="REAL_SOURCE_ACQUISITION_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        description="Real-source acquisition boundary executed; candidates and query plans do not count as support.",
        proposed_change={
            "status": acquisition_result.status,
            "backend_status": acquisition_result.backend_status,
            "actual_real_sources_acquired": acquisition_result.actual_real_sources_acquired,
        },
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=True,
        forbidden_actions=[
            "authorize physical claim",
            "validate Frontera C",
            "count query plan as evidence",
            "count candidates as source support",
        ],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    result = PhiGradientRealSourceAcquisitionCampaignResult(
        campaign_id="PHI-GRADIENT-REAL-SOURCE-ACQUISITION-v3_0",
        status=acquisition_result.status,
        acquisition_result=acquisition_result,
        loop_input=loop_input,
        loop_result=loop_result,
        update_proposals=[proposal],
    )
    result.report_paths = write_phi_gradient_real_source_acquisition_reports(result, repo_root / "reports")
    return result
