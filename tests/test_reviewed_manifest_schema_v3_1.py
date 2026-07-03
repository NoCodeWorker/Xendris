from phyng.reviewed_manifest.manifest_loader import load_or_create_reviewed_manifest_inputs
from phyng.reviewed_manifest.schemas import ReviewedSourceManifestEntry


def test_empty_manifest_creates_template_without_claiming_support(tmp_path):
    manifest, extract_pack, manifest_created, extract_created = load_or_create_reviewed_manifest_inputs(tmp_path)

    assert manifest_created is True
    assert extract_created is True
    assert manifest.entries == []
    assert extract_pack.extracts == []
    assert (tmp_path / "data/real_sources/phi_gradient_reviewed_manifest_v3_1.json").exists()
    assert (tmp_path / "data/real_sources/extracts/phi_gradient_extract_pack_v3_1.json").exists()


def test_fixture_entry_cannot_count_as_real_support():
    entry = ReviewedSourceManifestEntry(
        source_id="SRC-FIX-001",
        title="Fixture",
        local_path="fixtures/source.md",
        target_slots=["SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"],
        is_fixture=True,
    )

    assert entry.is_fixture is True
