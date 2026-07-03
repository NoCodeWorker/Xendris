from phyng.exact_extract_review.review_gate import run_phi_gradient_exact_extract_review_gate
from phyng.exact_extract_review.schemas import ExactReviewedExtract, ExactReviewedExtractPack
from phyng.source_pack_population.seed_pack import write_seed_pack


def test_missing_seed_files_blocks_review(tmp_path):
    result = run_phi_gradient_exact_extract_review_gate(str(tmp_path))

    assert result.status == "PHI_GRADIENT_EXACT_EXTRACT_REVIEW_BLOCKED"
    assert result.blocked_reason is not None


def test_exact_extracts_partial_status_when_some_ready(tmp_path):
    write_seed_pack(tmp_path)
    pack = ExactReviewedExtractPack(extracts=[
        ExactReviewedExtract(
            exact_extract_id="EXACT-READY",
            source_id="SRC-PHI-V32-002",
            slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
            location_type="PAGE",
            location_value="5",
            exact_quote="short exact quote",
            observable_text="visibility V",
            manual_review_required=False,
            review_status="EXACT_EXTRACT_REVIEWED",
        ),
        ExactReviewedExtract(
            exact_extract_id="EXACT-UNREADY",
            source_id="SRC-PHI-V32-010",
            slot_id="SLOT_4_GRADIENT_TRANSITION_OPERATORS",
            paraphrase_context="unresolved",
        ),
    ])

    result = run_phi_gradient_exact_extract_review_gate(str(tmp_path), exact_pack=pack)

    assert result.status == "PHI_GRADIENT_EXACT_EXTRACTS_PARTIAL"
    assert result.validation_ready_count == 1
    assert result.unresolved_extract_count == 1
