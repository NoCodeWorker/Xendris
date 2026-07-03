from phyng.source_pack_population.schemas import SeedSourceExtract, SeedSourceExtractPack, SeedSourceManifest, SeedSourceManifestEntry
from phyng.source_pack_validation.extract_validator import validate_source_pack_extracts, validated_extracts
from phyng.source_pack_validation.final_gate import build_final_gate
from phyng.source_pack_validation.slot_scoring import score_slot_coverage


def test_benchmark_requires_comparable_ranges():
    manifest = SeedSourceManifest(entries=[
        SeedSourceManifestEntry(source_id="SRC-BENCH", title="Bench", doi="10.1/bench", target_slots=["SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS"])
    ])
    incomplete = SeedSourceExtractPack(extracts=[
        SeedSourceExtract(
            extract_id="EXT-BENCH-BAD",
            source_id="SRC-BENCH",
            slot_id="SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS",
            extract_text_or_paraphrase="Benchmark candidate missing ranges.",
            exact_quote_available=True,
            benchmark_data_text="table mentioned",
            supported_components=["benchmark_dataset_or_table"],
            manual_review_required=False,
        )
    ])

    bad_validation = validate_source_pack_extracts(manifest, incomplete)[0]
    assert bad_validation.status == "EXTRACT_REJECTED_NOT_COMPARABLE"
    assert bad_validation.counts_as_real_support is False

    complete = SeedSourceExtractPack(extracts=[
        SeedSourceExtract(
            extract_id="EXT-BENCH-GOOD",
            source_id="SRC-BENCH",
            slot_id="SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS",
            extract_text_or_paraphrase="Comparable benchmark extract.",
            exact_quote_available=True,
            observable_text="visibility decay",
            parameter_constraint_text="m_kg, L_m, t_s ranges",
            benchmark_data_text="table: m_kg/L_m/t_s/V",
            supported_components=["benchmark_dataset_or_table"],
            limitations=["reviewed comparable range"],
            manual_review_required=False,
        )
    ])
    validations = validate_source_pack_extracts(manifest, complete)
    coverage = score_slot_coverage(manifest, complete, validations)
    gate = build_final_gate(manifest, complete, validations, validated_extracts(validations), coverage)

    assert gate.status == "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND"
    assert gate.benchmark_scoring.benchmark_comparable_count == 1
