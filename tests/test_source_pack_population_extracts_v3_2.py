from phyng.source_pack_population.seed_pack import write_seed_pack
from phyng.source_pack_population.validation import validate_seed_pack


def test_seed_extract_pack_exists(tmp_path):
    _, _, _, extract_path = write_seed_pack(tmp_path)

    assert (tmp_path / extract_path).exists()


def test_seed_extracts_require_manual_review(tmp_path):
    manifest, extract_pack, _, _ = write_seed_pack(tmp_path)
    validation = validate_seed_pack(manifest, extract_pack)

    assert validation.manual_review_extract_count == validation.extract_count
    assert {extract.initial_validation_status for extract in extract_pack.extracts} == {"EXTRACT_CANDIDATE_REQUIRES_REVIEW"}
    assert all(extract.manual_review_required for extract in extract_pack.extracts)
