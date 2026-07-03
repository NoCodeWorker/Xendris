from phyng.reviewed_manifest.campaign_gate import run_phi_gradient_reviewed_manifest_gate
from phyng.reviewed_manifest.extract_validation_bridge import validate_reviewed_extract_pack
from phyng.reviewed_manifest.schemas import (
    ReviewedSourceExtract,
    ReviewedSourceExtractPack,
    ReviewedSourceManifest,
    ReviewedSourceManifestEntry,
)


def _manifest() -> ReviewedSourceManifest:
    return ReviewedSourceManifest(entries=[
        ReviewedSourceManifestEntry(
            source_id="SRC-OBS",
            title="Observable source",
            doi="10.0000/obs",
            target_slots=["SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"],
            review_status="REVIEWED_SOURCE_HIGH_PRIORITY",
        ),
        ReviewedSourceManifestEntry(
            source_id="SRC-COMP",
            title="Component source",
            doi="10.0000/comp",
            target_slots=["SLOT_4_GRADIENT_TRANSITION_OPERATORS"],
            review_status="REVIEWED_SOURCE_HIGH_PRIORITY",
        ),
        ReviewedSourceManifestEntry(
            source_id="SRC-BENCH",
            title="Benchmark source",
            doi="10.0000/bench",
            target_slots=["SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS"],
            review_status="REVIEWED_SOURCE_BENCHMARK_CANDIDATE",
        ),
        ReviewedSourceManifestEntry(
            source_id="SRC-NEG",
            title="Negative source",
            doi="10.0000/neg",
            target_slots=["SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES"],
            review_status="REVIEWED_SOURCE_NEGATIVE_CANDIDATE",
        ),
    ])


def test_extract_source_must_exist_in_manifest():
    pack = ReviewedSourceExtractPack(extracts=[
        ReviewedSourceExtract(
            extract_id="EXT-MISSING-SOURCE",
            source_id="SRC-MISSING",
            slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
            extract_text_or_paraphrase="Visibility text.",
            observable_text="V(t)",
            supported_components=["visibility_decay_observable"],
        )
    ])

    result = validate_reviewed_extract_pack(_manifest(), pack)

    assert result[0].status == "EXTRACT_REJECTED_SOURCE_NOT_IN_MANIFEST"
    assert result[0].counts_as_real_support is False


def test_analogy_extract_is_rejected():
    pack = ReviewedSourceExtractPack(extracts=[
        ReviewedSourceExtract(
            extract_id="EXT-ANALOGY",
            source_id="SRC-COMP",
            slot_id="SLOT_4_GRADIENT_TRANSITION_OPERATORS",
            extract_text_or_paraphrase="The paper uses boundary gradient language metaphorically.",
        )
    ])

    result = validate_reviewed_extract_pack(_manifest(), pack)

    assert result[0].status == "EXTRACT_REJECTED_ANALOGY_ONLY"
    assert result[0].counts_as_real_support is False


def test_observable_and_component_extracts_allow_source_backed_limited():
    pack = ReviewedSourceExtractPack(extracts=[
        ReviewedSourceExtract(
            extract_id="EXT-OBS",
            source_id="SRC-OBS",
            slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
            extract_text_or_paraphrase="Defines visibility decay.",
            observable_text="V(t)",
            supported_components=["visibility_decay_observable"],
        ),
        ReviewedSourceExtract(
            extract_id="EXT-COMP",
            source_id="SRC-COMP",
            slot_id="SLOT_4_GRADIENT_TRANSITION_OPERATORS",
            extract_text_or_paraphrase="Defines a gradient transition contribution.",
            equation_text="rate += |d phi / du|",
            supported_components=["gradient_transition_operator"],
        ),
    ])

    result = run_phi_gradient_reviewed_manifest_gate(manifest=_manifest(), extract_pack=pack)

    assert result.status == "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED"
    assert result.validated_extract_count == 2


def test_benchmark_extract_requires_comparability():
    pack = ReviewedSourceExtractPack(extracts=[
        ReviewedSourceExtract(
            extract_id="EXT-BENCH-BAD",
            source_id="SRC-BENCH",
            slot_id="SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS",
            extract_text_or_paraphrase="Mentions benchmark data without comparable ranges.",
            benchmark_data_text="table exists",
            supported_components=["benchmark_dataset_or_table"],
        )
    ])

    result = validate_reviewed_extract_pack(_manifest(), pack)

    assert result[0].status == "EXTRACT_REJECTED_NOT_COMPARABLE"
    assert result[0].counts_as_real_support is False


def test_negative_extract_blocks_upgrade():
    pack = ReviewedSourceExtractPack(extracts=[
        ReviewedSourceExtract(
            extract_id="EXT-NEG",
            source_id="SRC-NEG",
            slot_id="SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES",
            extract_text_or_paraphrase="Excludes the candidate mechanism.",
            contradicted_components=["gradient_transition_operator"],
        )
    ])

    result = run_phi_gradient_reviewed_manifest_gate(manifest=_manifest(), extract_pack=pack)

    assert result.status == "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED"
    assert result.negative_source_ids == ["SRC-NEG"]
