"""Campaign orchestration for PHI_GRADIENT extract candidate review v3.8."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.extract_candidate_review.deduplication import split_unique_candidates
from phyng.extract_candidate_review.garbage_filter import short_preview
from phyng.extract_candidate_review.loader import load_v3_7_review_inputs
from phyng.extract_candidate_review.manual_review_queue import build_pedernales_manual_review_item
from phyng.extract_candidate_review.report import write_extract_candidate_review_reports
from phyng.extract_candidate_review.review_rules import review_candidate
from phyng.extract_candidate_review.schemas import (
    ManualReviewQueueItem,
    PhiGradientExtractCandidateReviewCampaignResult,
    PhiGradientExtractCandidateReviewGateResult,
    RejectedExtractionCandidate,
    ReviewedCandidateMapEntry,
    ReviewedExtractionCandidate,
)
from phyng.extract_candidate_review.validation_ready_pack import build_validation_ready_pack, write_v3_8_outputs


def run_phi_gradient_extract_candidate_review_campaign(root: str | Path = ".") -> PhiGradientExtractCandidateReviewCampaignResult:
    repo_root = Path(root)
    candidates, extraction_manifest, source_hashes, blocked_reason = load_v3_7_review_inputs(repo_root)
    reviewed: list[ReviewedExtractionCandidate] = []
    rejected: list[RejectedExtractionCandidate] = []
    manual_queue: list[ManualReviewQueueItem] = []
    map_entries: list[ReviewedCandidateMapEntry] = []

    if blocked_reason is None:
        unique_candidates, duplicates = split_unique_candidates(candidates)
        for duplicate in duplicates:
            rejected.append(
                RejectedExtractionCandidate(
                    candidate_id=duplicate.candidate_id,
                    source_id=duplicate.source_id,
                    reason="duplicate candidate",
                    original_candidate_type=duplicate.candidate_type,
                    short_text_preview=short_preview(duplicate.extracted_text),
                    review_status="REVIEWED_CANDIDATE_REJECTED_DUPLICATE",
                )
            )
            map_entries.append(
                ReviewedCandidateMapEntry(
                    candidate_id=duplicate.candidate_id,
                    source_id=duplicate.source_id,
                    review_decision="REVIEWED_CANDIDATE_REJECTED_DUPLICATE",
                    component_role="REJECTED_GARBAGE",
                    notes=["Duplicate candidate by source, page, type and normalized text."],
                )
            )
        for candidate in unique_candidates:
            reviewed_item, rejected_item, queue_item, map_entry = review_candidate(candidate)
            if reviewed_item is not None:
                reviewed.append(reviewed_item)
            if rejected_item is not None:
                rejected.append(rejected_item)
            if queue_item is not None:
                manual_queue.append(queue_item)
            map_entries.append(map_entry)
        pedernales_item = build_pedernales_manual_review_item(extraction_manifest)
        if pedernales_item is not None:
            manual_queue.append(pedernales_item)
            map_entries.append(
                ReviewedCandidateMapEntry(
                    candidate_id=pedernales_item.candidate_id,
                    source_id=pedernales_item.source_id,
                    review_decision="REVIEWED_CANDIDATE_REQUIRES_MANUAL_REVIEW",
                    component_role="GRADIENT_COMPONENT",
                    output_record_id=None,
                    notes=[pedernales_item.reason],
                )
            )
    status = _status(blocked_reason, reviewed, rejected, manual_queue)
    blocked_claims = _blocked_claims()
    pack = build_validation_ready_pack(reviewed, rejected, manual_queue, source_hashes, status)
    output_paths = write_v3_8_outputs(repo_root, pack, rejected, manual_queue, map_entries, blocked_claims, status)
    role_counts = _role_counts(reviewed, map_entries)
    gate = PhiGradientExtractCandidateReviewGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="extract_candidate_review"),
        input_candidate_count=len(candidates),
        validation_ready_count=pack.validation_ready_count,
        rejected_count=len(rejected),
        manual_review_count=len(manual_queue),
        component_role_counts=role_counts,
        pedernales_blocked=any(item.candidate_id == "MANUAL-PEDERNALES-SLOT-4-GRADIENT-COMPONENT" for item in manual_queue),
        reviewed_candidates=reviewed,
        validation_ready_pack=pack,
        rejected_candidates=rejected,
        manual_review_queue=manual_queue,
        reviewed_candidate_map=map_entries,
        output_paths=output_paths,
        allowed_claims=_allowed_claims(status),
        blocked_claims=blocked_claims,
        next_actions=_next_actions(status),
    )
    loop_input = CandidateLoopInput(
        loop_id="PHI-GRADIENT-EXTRACT-CANDIDATE-REVIEW-v3_8",
        input_type="EXTRACT_CANDIDATE_REVIEW_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        previous_status="PHI_GRADIENT_PDF_EXTRACTION_PARTIAL",
        result_status=status,
        payload={
            "input_candidate_count": gate.input_candidate_count,
            "validation_ready_count": gate.validation_ready_count,
            "rejected_count": gate.rejected_count,
            "manual_review_count": gate.manual_review_count,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposal = CandidateUpdateProposal(
        proposal_id=f"PHI-GRADIENT-EXTRACT-CANDIDATE-REVIEW-v3_8-{status}",
        proposal_type="EXTRACT_CANDIDATE_REVIEW_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        description="Extraction candidates reviewed into validation-ready, rejected, and manual-review buckets without granting support.",
        proposed_change={
            "status": status,
            "validation_ready_count": gate.validation_ready_count,
            "manual_review_count": gate.manual_review_count,
        },
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=True,
        forbidden_actions=["authorize physical claim", "treat validation-ready extract as support", "treat benchmark candidate as benchmark support"],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    result = PhiGradientExtractCandidateReviewCampaignResult(
        campaign_id="PHI-GRADIENT-EXTRACT-CANDIDATE-REVIEW-v3_8",
        status=status,
        gate_result=gate,
        loop_input=loop_input,
        loop_result=loop_result,
        update_proposals=[proposal],
    )
    result.report_paths = write_extract_candidate_review_reports(result, repo_root / "reports")
    return result


def _status(
    blocked_reason: str | None,
    reviewed: list[ReviewedExtractionCandidate],
    rejected: list[RejectedExtractionCandidate],
    manual_queue: list[ManualReviewQueueItem],
) -> str:
    if blocked_reason:
        return blocked_reason
    validation_ready_count = sum(1 for item in reviewed if item.validation_ready)
    if validation_ready_count and manual_queue:
        return "PHI_GRADIENT_EXTRACT_REVIEW_PARTIAL"
    if validation_ready_count:
        return "PHI_GRADIENT_EXTRACT_REVIEW_READY_FOR_VALIDATION"
    if manual_queue:
        return "PHI_GRADIENT_EXTRACT_REVIEW_MANUAL_REVIEW_REQUIRED"
    if rejected:
        return "PHI_GRADIENT_EXTRACT_REVIEW_NO_VALIDATION_READY_EXTRACTS"
    return "PHI_GRADIENT_EXTRACT_REVIEW_COMPLETED"


def _role_counts(reviewed: list[ReviewedExtractionCandidate], entries: list[ReviewedCandidateMapEntry]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in reviewed:
        counts[item.component_role] = counts.get(item.component_role, 0) + 1
    for item in entries:
        if item.component_role in {"REJECTED_GARBAGE", "GRADIENT_COMPONENT"} and item.output_record_id is None:
            counts[item.component_role] = counts.get(item.component_role, 0) + 1
    return counts


def _allowed_claims(status: str) -> list[str]:
    return [
        "Extraction candidates were reviewed.",
        "A validation-ready extract pack was assembled.",
        "Some candidates were rejected or queued for manual review.",
    ]


def _blocked_claims() -> list[str]:
    return [
        "Reviewed candidate validates PHI_GRADIENT.",
        "Validation-ready extract equals source support.",
        "Equation candidate proves physical component.",
        "Benchmark candidate proves benchmark support.",
        "PHI_GRADIENT is physically validated.",
        "Frontera C is validated.",
    ]


def _next_actions(status: str) -> list[str]:
    if status in {"PHI_GRADIENT_EXTRACT_REVIEW_READY_FOR_VALIDATION", "PHI_GRADIENT_EXTRACT_REVIEW_PARTIAL"}:
        return ["Run v3.9 validation-ready extract gate without treating the pack as support."]
    if status == "PHI_GRADIENT_EXTRACT_REVIEW_MANUAL_REVIEW_REQUIRED":
        return ["Resolve manual-review queue, especially Pedernales SLOT_4, before source-pressure decisions."]
    if status == "PHI_GRADIENT_EXTRACT_REVIEW_BLOCKED_MISSING_CANDIDATES":
        return ["Regenerate v3.7 candidate artifacts before v3.8 review."]
    return ["Review rejected candidates and rerun v3.7/v3.8 if extraction quality improves."]
