from phyng.source_pack_population.seed_pack import build_seed_extract_pack, build_seed_manifest
from phyng.source_pack_population.schemas import SeedSourceExtract, SeedSourceExtractPack, SeedSourceManifest, SeedSourceManifestEntry
from phyng.source_pack_validation.extract_validator import validate_source_pack_extracts


def test_seed_extracts_do_not_auto_validate_without_manual_review():
    manifest = build_seed_manifest()
    extract_pack = build_seed_extract_pack(manifest)

    results = validate_source_pack_extracts(manifest, extract_pack)

    assert results
    assert {result.status for result in results} == {"EXTRACT_REQUIRES_MANUAL_REVIEW"}
    assert all(result.counts_as_real_support is False for result in results)


def test_manual_review_required_blocks_support():
    manifest = SeedSourceManifest(entries=[
        SeedSourceManifestEntry(
            source_id="SRC-MANUAL",
            title="Manual source",
            doi="10.0000/manual",
            target_slots=["SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"],
        )
    ])
    pack = SeedSourceExtractPack(extracts=[
        SeedSourceExtract(
            extract_id="EXT-MANUAL",
            source_id="SRC-MANUAL",
            slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
            extract_text_or_paraphrase="Visibility observable candidate.",
            observable_text="V(t)",
            supported_components=["visibility_decay_observable"],
            manual_review_required=True,
            exact_quote_available=False,
        )
    ])

    result = validate_source_pack_extracts(manifest, pack)[0]

    assert result.status == "EXTRACT_REQUIRES_MANUAL_REVIEW"
    assert result.counts_as_real_support is False


def test_analogy_only_extract_is_rejected():
    manifest = SeedSourceManifest(entries=[
        SeedSourceManifestEntry(
            source_id="SRC-ANALOGY",
            title="Analogy source",
            doi="10.0000/analogy",
            target_slots=["SLOT_4_GRADIENT_TRANSITION_OPERATORS"],
        )
    ])
    pack = SeedSourceExtractPack(extracts=[
        SeedSourceExtract(
            extract_id="EXT-ANALOGY",
            source_id="SRC-ANALOGY",
            slot_id="SLOT_4_GRADIENT_TRANSITION_OPERATORS",
            extract_text_or_paraphrase="Boundary and gradient language with no component constraint.",
            manual_review_required=False,
            supported_components=[],
        )
    ])

    result = validate_source_pack_extracts(manifest, pack)[0]

    assert result.status == "EXTRACT_REJECTED_ANALOGY_ONLY"
    assert result.counts_as_real_support is False
