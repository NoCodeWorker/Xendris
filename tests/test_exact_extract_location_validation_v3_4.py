from phyng.exact_extract_review.location_validation import validate_exact_extract_locations
from phyng.exact_extract_review.schemas import ExactReviewedExtract, ExactReviewedExtractPack


def test_exact_extract_requires_location():
    pack = ExactReviewedExtractPack(extracts=[
        ExactReviewedExtract(
            exact_extract_id="EXACT-NO-LOC",
            source_id="SRC-1",
            slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
            exact_quote="short exact quote",
            manual_review_required=False,
        )
    ])

    result = validate_exact_extract_locations(pack, {"SRC-1"})[0]

    assert result.validation_ready is False
    assert "known_location_type" in result.missing_requirements
    assert "location_value" in result.missing_requirements


def test_exact_extract_requires_exact_content():
    pack = ExactReviewedExtractPack(extracts=[
        ExactReviewedExtract(
            exact_extract_id="EXACT-NO-CONTENT",
            source_id="SRC-1",
            slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
            location_type="PAGE",
            location_value="12",
            manual_review_required=False,
        )
    ])

    result = validate_exact_extract_locations(pack, {"SRC-1"})[0]

    assert result.validation_ready is False
    assert "exact_content_field" in result.missing_requirements


def test_validation_ready_requires_manual_review_false():
    pack = ExactReviewedExtractPack(extracts=[
        ExactReviewedExtract(
            exact_extract_id="EXACT-MANUAL",
            source_id="SRC-1",
            slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
            location_type="PAGE",
            location_value="12",
            exact_quote="short exact quote",
            manual_review_required=True,
        )
    ])

    result = validate_exact_extract_locations(pack, {"SRC-1"})[0]

    assert result.validation_ready is False
    assert "manual_review_required_false" in result.missing_requirements
