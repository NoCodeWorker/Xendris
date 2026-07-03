from phyng.exact_extract_review.exact_extracts import build_unresolved_exact_extract_pack
from phyng.exact_extract_review.schemas import ExactReviewedExtract
from phyng.source_pack_population.seed_pack import build_seed_extract_pack, build_seed_manifest


def test_seed_paraphrases_do_not_become_exact_extracts():
    manifest = build_seed_manifest()
    seed_pack = build_seed_extract_pack(manifest)
    exact_pack = build_unresolved_exact_extract_pack(manifest, seed_pack)

    assert exact_pack.extracts
    assert all(extract.exact_quote is None for extract in exact_pack.extracts)
    assert all(extract.validation_ready is False for extract in exact_pack.extracts)
    assert all(extract.review_status == "EXACT_EXTRACT_REQUIRES_LOCATION" for extract in exact_pack.extracts)


def test_no_fabricated_quote_or_range():
    extract = ExactReviewedExtract(
        exact_extract_id="EXACT-TEST",
        source_id="SRC",
        slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
        paraphrase_context="Seed paraphrase only.",
    )

    assert extract.exact_quote is None
    assert extract.benchmark_range_text is None
    assert extract.parameter_range_text is None
