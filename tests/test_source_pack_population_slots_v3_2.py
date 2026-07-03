from phyng.source_pack_population.seed_pack import write_seed_pack
from phyng.source_pack_population.validation import validate_seed_pack


def test_negative_source_candidates_present(tmp_path):
    manifest, extract_pack, _, _ = write_seed_pack(tmp_path)
    validation = validate_seed_pack(manifest, extract_pack)

    assert validation.negative_candidate_count >= 2
    assert any("SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES" in entry.target_slots for entry in manifest.entries)


def test_benchmark_candidate_sources_present(tmp_path):
    manifest, extract_pack, _, _ = write_seed_pack(tmp_path)
    validation = validate_seed_pack(manifest, extract_pack)

    assert validation.benchmark_candidate_count >= 3
    assert any("SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS" in entry.target_slots for entry in manifest.entries)
