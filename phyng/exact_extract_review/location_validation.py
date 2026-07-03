"""Location and exact-content validation for reviewed extracts."""

from __future__ import annotations

from phyng.exact_extract_review.schemas import ExactExtractLocationValidationResult, ExactReviewedExtract, ExactReviewedExtractPack
from phyng.source_pressure.slots import build_phi_gradient_source_slots


VALID_SLOTS = {slot.slot_id for slot in build_phi_gradient_source_slots()}
VALID_LOCATION_TYPES = {
    "PAGE",
    "SECTION",
    "EQUATION_NUMBER",
    "FIGURE",
    "TABLE",
    "APPENDIX",
    "ARXIV_ABSTRACT",
    "ARXIV_SECTION",
    "DOI_PAGE",
    "LOCAL_PDF_PAGE",
    "URL_ANCHOR",
}


def validate_exact_extract_locations(
    pack: ExactReviewedExtractPack,
    manifest_source_ids: set[str],
) -> list[ExactExtractLocationValidationResult]:
    return [_validate_extract(extract, manifest_source_ids) for extract in pack.extracts]


def is_validation_ready(extract: ExactReviewedExtract, manifest_source_ids: set[str]) -> bool:
    return _validate_extract(extract, manifest_source_ids).validation_ready


def _validate_extract(extract: ExactReviewedExtract, manifest_source_ids: set[str]) -> ExactExtractLocationValidationResult:
    missing: list[str] = []
    if extract.source_id not in manifest_source_ids:
        missing.append("source_id_in_manifest")
    if extract.slot_id not in VALID_SLOTS:
        missing.append("valid_slot_id")
    if extract.location_type not in VALID_LOCATION_TYPES:
        missing.append("known_location_type")
    if not extract.location_value:
        missing.append("location_value")
    if not _has_exact_content(extract):
        missing.append("exact_content_field")
    if extract.manual_review_required:
        missing.append("manual_review_required_false")
    ready = not missing
    return ExactExtractLocationValidationResult(
        exact_extract_id=extract.exact_extract_id,
        source_id=extract.source_id,
        slot_id=extract.slot_id,
        status="EXACT_EXTRACT_LOCATION_VALID" if ready else "EXACT_EXTRACT_REQUIRES_MORE_REVIEW",
        validation_ready=ready,
        missing_requirements=missing,
    )


def _has_exact_content(extract: ExactReviewedExtract) -> bool:
    return bool(
        extract.exact_quote
        or extract.equation_text
        or extract.observable_text
        or extract.parameter_range_text
        or extract.benchmark_range_text
        or extract.negative_constraint_text
    )
