from phyng.real_source_ingestion.manifest import build_real_source_manifest, default_manifest_entries


def test_real_source_manifest_marks_fixtures_as_non_real_support():
    manifest = build_real_source_manifest(default_manifest_entries())

    assert "SRC-FIX-V2-8" in manifest.fixture_entries
    assert "RS-DOUBLE-OBS" in manifest.test_double_entries
    assert not manifest.actual_real_sources_ingested


def test_fixture_support_cannot_promote_real_source_status():
    manifest = build_real_source_manifest(default_manifest_entries())

    assert manifest.status == "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"
