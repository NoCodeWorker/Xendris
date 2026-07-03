"""Campaign orchestration for PHI_GRADIENT exact extract review v3.4."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.exact_extract_review.report import write_exact_extract_review_reports
from phyng.exact_extract_review.review_gate import run_phi_gradient_exact_extract_review_gate
from phyng.exact_extract_review.schemas import ExactReviewedExtractPack, PhiGradientExactExtractReviewCampaignResult


def run_phi_gradient_exact_extract_review_campaign(
    root: str | Path = ".",
    exact_pack: ExactReviewedExtractPack | None = None,
) -> PhiGradientExactExtractReviewCampaignResult:
    repo_root = Path(root)
    gate = run_phi_gradient_exact_extract_review_gate(str(repo_root), exact_pack=exact_pack)
    loop_input = CandidateLoopInput(
        loop_id="PHI-GRADIENT-EXACT-EXTRACT-REVIEW-v3_4",
        input_type="EXACT_EXTRACT_REVIEW_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        previous_status="PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED",
        result_status=gate.status,
        payload={
            "manual_review_debt_before": gate.manual_review_debt_before,
            "manual_review_debt_after": gate.manual_review_debt_after,
            "validation_ready_count": gate.validation_ready_count,
            "exact_extract_count": gate.exact_extract_count,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposal = CandidateUpdateProposal(
        proposal_id=f"PHI-GRADIENT-EXACT-EXTRACT-REVIEW-v3_4-{gate.status}",
        proposal_type="EXACT_EXTRACT_REVIEW_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        description="Exact extract review executed; unresolved extracts remain outside source-pressure support.",
        proposed_change={
            "status": gate.status,
            "manual_review_debt_after": gate.manual_review_debt_after,
            "validation_ready_count": gate.validation_ready_count,
        },
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=True,
        forbidden_actions=["authorize physical claim", "count located quote as support", "count benchmark mention as benchmark data"],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    result = PhiGradientExactExtractReviewCampaignResult(
        campaign_id="PHI-GRADIENT-EXACT-EXTRACT-REVIEW-v3_4",
        status=gate.status,
        gate_result=gate,
        loop_input=loop_input,
        loop_result=loop_result,
        update_proposals=[proposal],
    )
    result.report_paths = write_exact_extract_review_reports(result, repo_root / "reports")
    return result
