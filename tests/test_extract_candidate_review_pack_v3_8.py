from __future__ import annotations

from phyng.extract_candidate_review.schemas import ManualReviewQueueItem, RejectedExtractionCandidate, ReviewedExtractionCandidate
from phyng.extract_candidate_review.validation_ready_pack import build_validation_ready_pack


def test_validation_ready_pack_does_not_grant_support() -> None:
    reviewed = ReviewedExtractionCandidate(
        candidate_id="CAND-1",
        source_id="SRC-TEST",
        sha256="abc123",
        page_number=1,
        location_type="PAGE_TEXT",
        location_value="page=1",
        candidate_type="QUOTE_CANDIDATE",
        extracted_text="Visibility decoherence was measured.",
        component_role="VISIBILITY_DECAY_OBSERVABLE",
        review_status="REVIEWED_CANDIDATE_ACCEPTED_VALIDATION_READY",
        validation_ready=True,
        manual_review_required=False,
        limitations=["Validation-ready extract still requires v3.9 source-pressure validation."],
    )
    pack = build_validation_ready_pack(
        [reviewed],
        [],
        [],
        {"hashes": [{"source_id": "SRC-TEST", "local_path": "data/real_sources/pdfs/source.pdf"}]},
        "PHI_GRADIENT_EXTRACT_REVIEW_READY_FOR_VALIDATION",
    )

    assert pack.validation_ready_count == 1
    assert pack.extracts[0].next_gate_required == "v3.9 validation-ready extract gate"
    assert "not support" in pack.notes[0]
