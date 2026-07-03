from phyng.reviewed_manifest.campaign_gate import run_phi_gradient_reviewed_manifest_gate
from phyng.reviewed_manifest.schemas import (
    ReviewedSourceExtract,
    ReviewedSourceExtractPack,
    ReviewedSourceManifest,
    ReviewedSourceManifestEntry,
)


def test_missing_extract_keeps_source_pressure_inconclusive():
    manifest = ReviewedSourceManifest(entries=[
        ReviewedSourceManifestEntry(
            source_id="SRC-ONLY-MANIFEST",
            title="Manifest only",
            doi="10.0000/manifest-only",
            target_slots=["SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"],
            review_status="REVIEWED_SOURCE_CANDIDATE",
        )
    ])

    result = run_phi_gradient_reviewed_manifest_gate(
        manifest=manifest,
        extract_pack=ReviewedSourceExtractPack(extracts=[]),
    )

    assert result.status == "PHI_GRADIENT_REVIEWED_MANIFEST_LOADED"
    assert result.validated_extract_count == 0
    assert "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT" in result.slot_coverage.missing_slots


def test_valid_benchmark_extract_reaches_benchmark_status():
    manifest = ReviewedSourceManifest(entries=[
        ReviewedSourceManifestEntry(
            source_id="SRC-BENCH-GOOD",
            title="Good benchmark",
            doi="10.0000/bench-good",
            target_slots=["SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS"],
            review_status="REVIEWED_SOURCE_BENCHMARK_CANDIDATE",
        )
    ])
    pack = ReviewedSourceExtractPack(extracts=[
        ReviewedSourceExtract(
            extract_id="EXT-BENCH-GOOD",
            source_id="SRC-BENCH-GOOD",
            slot_id="SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS",
            extract_text_or_paraphrase="Provides comparable visibility benchmark ranges.",
            observable_text="visibility decay",
            parameter_constraint_text="m_kg, L_m, t_s ranges",
            benchmark_data_text="table: m_kg/L_m/t_s/V",
            supported_components=["benchmark_dataset_or_table"],
            limitations=["reviewed extract pack test case"],
        )
    ])

    result = run_phi_gradient_reviewed_manifest_gate(manifest=manifest, extract_pack=pack)

    assert result.status == "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND"
    assert result.benchmark_comparability.comparable_records == 1
