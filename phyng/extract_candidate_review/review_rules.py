"""Strict v3.8 review decision rules."""

from __future__ import annotations

from phyng.extract_candidate_review.garbage_filter import garbage_reason, short_preview
from phyng.extract_candidate_review.role_assignment import assign_component_role
from phyng.extract_candidate_review.schemas import (
    ManualReviewQueueItem,
    RawExtractionCandidate,
    RejectedExtractionCandidate,
    ReviewedCandidateMapEntry,
    ReviewedExtractionCandidate,
)


def review_candidate(candidate: RawExtractionCandidate) -> tuple[ReviewedExtractionCandidate | None, RejectedExtractionCandidate | None, ManualReviewQueueItem | None, ReviewedCandidateMapEntry]:
    reason = garbage_reason(candidate)
    role = assign_component_role(candidate)
    if reason:
        rejected = RejectedExtractionCandidate(
            candidate_id=candidate.candidate_id,
            source_id=candidate.source_id,
            reason=reason,
            original_candidate_type=candidate.candidate_type,
            short_text_preview=short_preview(candidate.extracted_text),
            review_status="REVIEWED_CANDIDATE_REJECTED_GARBAGE" if "length" not in reason else "REVIEWED_CANDIDATE_REJECTED_TOO_LONG",
        )
        return None, rejected, None, ReviewedCandidateMapEntry(
            candidate_id=candidate.candidate_id,
            source_id=candidate.source_id,
            review_decision=rejected.review_status,
            component_role="REJECTED_GARBAGE",
            output_record_id=None,
            notes=[reason],
        )
    if role == "REQUIRES_MANUAL_REVIEW":
        return _manual(candidate, role, "candidate role is uncertain")
    if not candidate.location_value or candidate.page_number is None:
        rejected = RejectedExtractionCandidate(
            candidate_id=candidate.candidate_id,
            source_id=candidate.source_id,
            reason="candidate lacks exact page or location",
            original_candidate_type=candidate.candidate_type,
            short_text_preview=short_preview(candidate.extracted_text),
            review_status="REVIEWED_CANDIDATE_REJECTED_NO_LOCATION",
        )
        return None, rejected, None, ReviewedCandidateMapEntry(
            candidate_id=candidate.candidate_id,
            source_id=candidate.source_id,
            review_decision=rejected.review_status,
            component_role=role,
            output_record_id=None,
            notes=["Exact location missing."],
        )
    if candidate.candidate_type == "EQUATION_CANDIDATE" and candidate.requires_manual_review:
        return _manual(candidate, role, "equation formatting is ambiguous and requires review")
    if candidate.requires_manual_review:
        return _manual(candidate, role, "candidate was extracted from PDF stream and requires review before validation")

    reviewed = ReviewedExtractionCandidate(
        candidate_id=candidate.candidate_id,
        source_id=candidate.source_id,
        sha256=candidate.sha256,
        page_number=candidate.page_number,
        location_type=candidate.location_type,
        location_value=candidate.location_value,
        candidate_type=candidate.candidate_type,
        extracted_text=candidate.extracted_text.strip(),
        component_role=role,
        review_status="REVIEWED_CANDIDATE_ACCEPTED_VALIDATION_READY",
        validation_ready=True,
        manual_review_required=False,
        limitations=["Validation-ready extract still requires v3.9 source-pressure validation."],
        notes=["Accepted by structural v3.8 review; this is not source support."],
    )
    return reviewed, None, None, ReviewedCandidateMapEntry(
        candidate_id=candidate.candidate_id,
        source_id=candidate.source_id,
        review_decision=reviewed.review_status,
        component_role=role,
        output_record_id=f"VRX-{candidate.candidate_id}",
        notes=reviewed.notes,
    )


def _manual(
    candidate: RawExtractionCandidate,
    role: str,
    reason: str,
) -> tuple[ReviewedExtractionCandidate, None, ManualReviewQueueItem, ReviewedCandidateMapEntry]:
    reviewed = ReviewedExtractionCandidate(
        candidate_id=candidate.candidate_id,
        source_id=candidate.source_id,
        sha256=candidate.sha256,
        page_number=candidate.page_number,
        location_type=candidate.location_type,
        location_value=candidate.location_value,
        candidate_type=candidate.candidate_type,
        extracted_text=candidate.extracted_text.strip(),
        component_role=role,
        review_status="REVIEWED_CANDIDATE_REQUIRES_MANUAL_REVIEW",
        validation_ready=False,
        manual_review_required=True,
        limitations=["Manual review unresolved."],
        notes=[reason],
    )
    item = ManualReviewQueueItem(
        candidate_id=candidate.candidate_id,
        source_id=candidate.source_id,
        page_number=candidate.page_number,
        candidate_type=candidate.candidate_type,
        text_preview=short_preview(candidate.extracted_text),
        reason=reason,
        priority="MEDIUM",
        suggested_action="Review the PDF page and confirm exact text, role, and location before v3.9.",
    )
    return reviewed, None, item, ReviewedCandidateMapEntry(
        candidate_id=candidate.candidate_id,
        source_id=candidate.source_id,
        review_decision=reviewed.review_status,
        component_role=role,
        output_record_id=None,
        notes=[reason],
    )
