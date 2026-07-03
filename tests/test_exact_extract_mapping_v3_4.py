from phyng.exact_extract_review.equation_observable_map import build_equation_observable_map
from phyng.exact_extract_review.parameter_range_map import build_parameter_range_map
from phyng.exact_extract_review.schemas import ExactReviewedExtract, ExactReviewedExtractPack


def test_equation_observable_map_requires_exact_extract():
    pack = ExactReviewedExtractPack(extracts=[
        ExactReviewedExtract(
            exact_extract_id="EXACT-EQ",
            source_id="SRC-1",
            slot_id="SLOT_4_GRADIENT_TRANSITION_OPERATORS",
            location_type="EQUATION_NUMBER",
            location_value="Eq. 4",
            equation_text="rate += |d phi / du|",
            manual_review_required=False,
        ),
        ExactReviewedExtract(
            exact_extract_id="EXACT-UNREADY",
            source_id="SRC-1",
            slot_id="SLOT_4_GRADIENT_TRANSITION_OPERATORS",
            equation_text="unlocated equation",
            manual_review_required=False,
        ),
    ])

    result = build_equation_observable_map(pack, {"SRC-1"})

    assert len(result.entries) == 1
    assert result.entries[0].exact_extract_id == "EXACT-EQ"
    assert result.entries[0].model_role == "GRADIENT_COMPONENT"


def test_parameter_range_map_requires_exact_values():
    pack = ExactReviewedExtractPack(extracts=[
        ExactReviewedExtract(
            exact_extract_id="EXACT-RANGE",
            source_id="SRC-1",
            slot_id="SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS",
            location_type="TABLE",
            location_value="Table 1",
            benchmark_range_text="mass range; length range; time range; visibility measure; environment limitations",
            manual_review_required=False,
        ),
        ExactReviewedExtract(
            exact_extract_id="EXACT-NO-RANGE",
            source_id="SRC-1",
            slot_id="SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS",
            location_type="PAGE",
            location_value="8",
            exact_quote="benchmark discussion",
            manual_review_required=False,
        ),
    ])

    result = build_parameter_range_map(pack, {"SRC-1"})

    assert len(result.entries) == 1
    assert result.entries[0].comparability_status == "COMPARABLE_RANGE_READY"
