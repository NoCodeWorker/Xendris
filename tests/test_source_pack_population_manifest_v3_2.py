from phyng.source_pack_population.seed_pack import write_seed_pack
from phyng.source_pack_population.validation import validate_seed_pack


def test_seed_manifest_exists(tmp_path):
    _, _, manifest_path, _ = write_seed_pack(tmp_path)

    assert (tmp_path / manifest_path).exists()


def test_seed_manifest_entries_have_traceable_identifiers(tmp_path):
    manifest, extract_pack, _, _ = write_seed_pack(tmp_path)
    validation = validate_seed_pack(manifest, extract_pack)

    assert validation.traceable_entry_count == validation.manifest_entry_count
    assert validation.errors == []


def test_seed_manifest_entries_target_valid_slots(tmp_path):
    manifest, extract_pack, _, _ = write_seed_pack(tmp_path)
    validation = validate_seed_pack(manifest, extract_pack)

    assert validation.valid_slot_entry_count == validation.manifest_entry_count


def test_seed_sources_are_not_validated_support(tmp_path):
    manifest, _, _, _ = write_seed_pack(tmp_path)

    assert {entry.evidence_status for entry in manifest.entries} == {"CANDIDATE_NOT_VALIDATED"}
    assert all(entry.review_status in {"REVIEWED_SOURCE_CANDIDATE", "REVIEWED_SOURCE_BENCHMARK_CANDIDATE", "REVIEWED_SOURCE_NEGATIVE_CANDIDATE"} for entry in manifest.entries)
