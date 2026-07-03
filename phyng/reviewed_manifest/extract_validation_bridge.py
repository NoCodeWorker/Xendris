"""Bridge reviewed extracts into the v2.9 real-source extract validator."""

from __future__ import annotations

from phyng.real_source_ingestion.extract_validation import validate_real_source_extract
from phyng.real_source_ingestion.schemas import RealSourceExtract
from phyng.reviewed_manifest.manifest_validation import VALID_SLOTS
from phyng.reviewed_manifest.schemas import (
    ReviewedSourceExtract,
    ReviewedSourceExtractPack,
    ReviewedSourceExtractValidationResult,
    ReviewedSourceManifest,
)


def validate_reviewed_extract_pack(
    manifest: ReviewedSourceManifest,
    pack: ReviewedSourceExtractPack,
) -> list[ReviewedSourceExtractValidationResult]:
    manifest_ids = {entry.source_id for entry in manifest.entries}
    fixture_ids = {entry.source_id for entry in manifest.entries if entry.is_fixture}
    test_double_ids = {entry.source_id for entry in manifest.entries if entry.is_test_double}
    results: list[ReviewedSourceExtractValidationResult] = []
    for extract in pack.extracts:
        reasons: list[str] = []
        if extract.source_id not in manifest_ids:
            results.append(_rejected(extract, "EXTRACT_REJECTED_SOURCE_NOT_IN_MANIFEST", ["Extract source_id is absent from manifest."]))
            continue
        if extract.slot_id not in VALID_SLOTS:
            results.append(_rejected(extract, "EXTRACT_REJECTED_NO_TARGET_SLOT", ["Extract targets an unknown slot."]))
            continue
        if extract.manual_review_required:
            reasons.append("Extract is marked for manual review.")
        bridged = _to_real_source_extract(extract)
        if extract.source_id in fixture_ids:
            bridged.is_fixture = True
            reasons.append("Fixture manifest entry cannot count as real support.")
        if extract.source_id in test_double_ids:
            bridged.is_test_double = True
            reasons.append("Test-double manifest entry cannot count as real support.")
        validation = validate_real_source_extract(bridged)
        status = validation.status
        if status.startswith("EXTRACT_VALID_") and not extract.supported_components and not extract.contradicted_components:
            status = "EXTRACT_REJECTED_NO_COMPONENT_SUPPORT"
            reasons.append("Extract lacks concrete supported or contradicted components.")
        results.append(
            ReviewedSourceExtractValidationResult(
                extract_id=extract.extract_id,
                source_id=extract.source_id,
                slot_id=extract.slot_id,
                status=status,
                counts_as_real_support=validation.counts_as_real_support and not extract.manual_review_required,
                bridge_validation=validation,
                reasons=[*validation.reasons, *reasons],
            )
        )
    return results


def _to_real_source_extract(extract: ReviewedSourceExtract) -> RealSourceExtract:
    return RealSourceExtract(
        extract_id=extract.extract_id,
        source_id=extract.source_id,
        slot_id=extract.slot_id,
        extracted_text_or_paraphrase=extract.extract_text_or_paraphrase,
        exact_quote_available=extract.exact_quote_available,
        equation_text=extract.equation_text,
        observable_text=extract.observable_text,
        parameter_constraint_text=extract.parameter_constraint_text,
        benchmark_data_text=extract.benchmark_data_text,
        supported_components=list(extract.supported_components),
        contradicted_components=list(extract.contradicted_components),
        limitations=list(extract.limitations),
        extractor_notes=list(extract.extraction_notes),
        is_fixture=extract.is_fixture,
        is_test_double=extract.is_test_double,
    )


def _rejected(extract: ReviewedSourceExtract, status: str, reasons: list[str]) -> ReviewedSourceExtractValidationResult:
    return ReviewedSourceExtractValidationResult(
        extract_id=extract.extract_id,
        source_id=extract.source_id,
        slot_id=extract.slot_id,
        status=status,
        counts_as_real_support=False,
        reasons=reasons,
    )
