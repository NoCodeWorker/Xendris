from phyng.reviewed_manifest.manifest_validation import validate_reviewed_manifest
from phyng.reviewed_manifest.schemas import ReviewedSourceManifest, ReviewedSourceManifestEntry


def test_manifest_entry_requires_traceable_identifier():
    manifest = ReviewedSourceManifest(entries=[
        ReviewedSourceManifestEntry(
            source_id="SRC-NO-ID",
            title="No identifier",
            target_slots=["SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"],
        )
    ])

    result = validate_reviewed_manifest(manifest)

    assert result.status == "REVIEWED_MANIFEST_CONTAINS_UNTRACEABLE_ENTRIES"
    assert "SRC-NO-ID" in result.rejected_entry_ids
    assert "MANIFEST_ENTRY_REJECTED_NO_TRACEABLE_IDENTIFIER" in result.errors[0]


def test_manifest_entry_requires_valid_slot():
    manifest = ReviewedSourceManifest(entries=[
        ReviewedSourceManifestEntry(
            source_id="SRC-BAD-SLOT",
            title="Bad slot",
            doi="10.0000/bad-slot",
            target_slots=["SLOT_UNKNOWN"],
        )
    ])

    result = validate_reviewed_manifest(manifest)

    assert "SRC-BAD-SLOT" in result.rejected_entry_ids
    assert "MANIFEST_ENTRY_REJECTED_NO_TARGET_SLOT" in result.errors[0]


def test_fixture_entry_cannot_count_as_real_support_in_validation():
    manifest = ReviewedSourceManifest(entries=[
        ReviewedSourceManifestEntry(
            source_id="SRC-FIX-VALIDATION",
            title="Fixture validation",
            local_path="fixtures/source.md",
            target_slots=["SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"],
            is_fixture=True,
        )
    ])

    result = validate_reviewed_manifest(manifest)

    assert result.status == "REVIEWED_MANIFEST_CONTAINS_ONLY_FIXTURES"
    assert "SRC-FIX-VALIDATION" in result.fixture_entry_ids
