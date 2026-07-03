"""Phygn v3.1 PHI_GRADIENT reviewed local manifest campaign."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.reviewed_manifest.campaign_gate import run_phi_gradient_reviewed_manifest_gate
from phyng.reviewed_manifest.report import write_phi_gradient_reviewed_manifest_reports
from phyng.reviewed_manifest.schemas import (
    PhiGradientReviewedManifestCampaignResult,
    ReviewedSourceExtractPack,
    ReviewedSourceManifest,
)


def run_phi_gradient_reviewed_local_manifest_campaign(
    root: str | Path = ".",
    manifest: ReviewedSourceManifest | None = None,
    extract_pack: ReviewedSourceExtractPack | None = None,
) -> PhiGradientReviewedManifestCampaignResult:
    repo_root = Path(root)
    gate_result = run_phi_gradient_reviewed_manifest_gate(
        root=str(repo_root),
        manifest=manifest,
        extract_pack=extract_pack,
    )
    loop_input = CandidateLoopInput(
        loop_id="PHI-GRADIENT-REVIEWED-LOCAL-MANIFEST-v3_1",
        input_type="REVIEWED_LOCAL_MANIFEST_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        previous_status="PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING",
        result_status=gate_result.status,
        payload={
            "manifest_count": gate_result.manifest_validation.entry_count,
            "validated_extract_count": gate_result.validated_extract_count,
            "negative_source_count": len(gate_result.negative_source_ids),
            "missing_slots": gate_result.slot_coverage.missing_slots,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposal = CandidateUpdateProposal(
        proposal_id=f"PHI-GRADIENT-REVIEWED-LOCAL-MANIFEST-v3_1-{gate_result.status}",
        proposal_type="REVIEWED_MANIFEST_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        description="Reviewed local manifest gate executed; manifest entries require validated extracts before source pressure.",
        proposed_change={
            "status": gate_result.status,
            "validated_extract_count": gate_result.validated_extract_count,
            "benchmark_comparable_count": gate_result.benchmark_comparability.comparable_records,
        },
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=True,
        forbidden_actions=[
            "authorize physical claim",
            "validate Frontera C",
            "count manifest entry as evidence",
            "count benchmark candidate as benchmark support",
        ],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    result = PhiGradientReviewedManifestCampaignResult(
        campaign_id="PHI-GRADIENT-REVIEWED-LOCAL-MANIFEST-v3_1",
        status=gate_result.status,
        gate_result=gate_result,
        loop_input=loop_input,
        loop_result=loop_result,
        update_proposals=[proposal],
    )
    result.report_paths = write_phi_gradient_reviewed_manifest_reports(result, repo_root / "reports")
    return result
