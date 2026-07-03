"""Validation for reviewed local manifests."""

from __future__ import annotations

from phyng.reviewed_manifest.schemas import ReviewedSourceManifest, ReviewedSourceManifestValidationResult
from phyng.source_pressure.slots import build_phi_gradient_source_slots


VALID_SLOTS = {slot.slot_id for slot in build_phi_gradient_source_slots()}


def validate_reviewed_manifest(manifest: ReviewedSourceManifest) -> ReviewedSourceManifestValidationResult:
    if not manifest.entries:
        return ReviewedSourceManifestValidationResult(
            status="REVIEWED_MANIFEST_EMPTY",
            manifest_id=manifest.manifest_id,
            warnings=["Reviewed manifest is empty; no source pressure can be claimed."],
        )

    accepted: list[str] = []
    rejected: list[str] = []
    fixtures: list[str] = []
    test_doubles: list[str] = []
    warnings: list[str] = []
    errors: list[str] = []
    traceable = 0

    for entry in manifest.entries:
        if entry.is_fixture:
            fixtures.append(entry.source_id)
        if entry.is_test_double:
            test_doubles.append(entry.source_id)
        if _has_traceable_identifier(entry):
            traceable += 1
        else:
            rejected.append(entry.source_id)
            errors.append(f"{entry.source_id}: MANIFEST_ENTRY_REJECTED_NO_TRACEABLE_IDENTIFIER")
            continue
        if not set(entry.target_slots).intersection(VALID_SLOTS):
            rejected.append(entry.source_id)
            errors.append(f"{entry.source_id}: MANIFEST_ENTRY_REJECTED_NO_TARGET_SLOT")
            continue
        if entry.is_fixture or entry.is_test_double:
            warnings.append(f"{entry.source_id}: MANIFEST_ENTRY_NON_EVIDENTIAL_TEST_OBJECT")
            continue
        if entry.review_status == "REVIEWED_SOURCE_REQUIRES_MANUAL_REVIEW":
            warnings.append(f"{entry.source_id}: REVIEWED_SOURCE_REQUIRES_MANUAL_REVIEW")
        accepted.append(entry.source_id)

    status = _status_for(manifest, accepted, rejected, fixtures, test_doubles, warnings)
    return ReviewedSourceManifestValidationResult(
        status=status,
        manifest_id=manifest.manifest_id,
        entry_count=len(manifest.entries),
        traceable_entry_count=traceable,
        accepted_entry_ids=accepted,
        rejected_entry_ids=rejected,
        fixture_entry_ids=fixtures,
        test_double_entry_ids=test_doubles,
        warnings=warnings,
        errors=errors,
    )


def _has_traceable_identifier(entry) -> bool:
    return bool(entry.doi or entry.arxiv_id or entry.url or entry.local_path)


def _status_for(
    manifest: ReviewedSourceManifest,
    accepted: list[str],
    rejected: list[str],
    fixtures: list[str],
    test_doubles: list[str],
    warnings: list[str],
) -> str:
    if rejected:
        return "REVIEWED_MANIFEST_CONTAINS_UNTRACEABLE_ENTRIES"
    if manifest.entries and len(fixtures) + len(test_doubles) == len(manifest.entries):
        return "REVIEWED_MANIFEST_CONTAINS_ONLY_FIXTURES"
    if warnings and not accepted:
        return "REVIEWED_MANIFEST_REQUIRES_MANUAL_REVIEW"
    if warnings:
        return "REVIEWED_MANIFEST_REQUIRES_MANUAL_REVIEW"
    return "REVIEWED_MANIFEST_VALID"
