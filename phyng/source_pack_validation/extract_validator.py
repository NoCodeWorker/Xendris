"""Strict v3.3 extract validation."""

from __future__ import annotations

from phyng.real_source_ingestion.extract_validation import validate_real_source_extract
from phyng.real_source_ingestion.schemas import RealSourceExtract
from phyng.source_pack_population.schemas import SeedSourceExtract, SeedSourceExtractPack, SeedSourceManifest
from phyng.source_pack_validation.schemas import SourcePackExtractValidationResult, SourcePackValidatedExtract
from phyng.source_pressure.slots import build_phi_gradient_source_slots


VALID_SLOTS = {slot.slot_id for slot in build_phi_gradient_source_slots()}


def validate_source_pack_extracts(
    manifest: SeedSourceManifest,
    extract_pack: SeedSourceExtractPack,
) -> list[SourcePackExtractValidationResult]:
    manifest_ids = {entry.source_id for entry in manifest.entries}
    results: list[SourcePackExtractValidationResult] = []
    for extract in extract_pack.extracts:
        if extract.source_id not in manifest_ids:
            results.append(_result(extract, "EXTRACT_REJECTED_SOURCE_NOT_IN_MANIFEST", ["Extract source_id is absent from seed manifest."]))
            continue
        if extract.slot_id not in VALID_SLOTS:
            results.append(_result(extract, "EXTRACT_REJECTED_NO_TARGET_SLOT", ["Extract targets an unknown slot."]))
            continue
        if _requires_manual_review_before_support(extract):
            results.append(_result(extract, "EXTRACT_REQUIRES_MANUAL_REVIEW", ["Manual-review seed extract cannot count as support without exact reviewed fields."], requires_manual_review=True))
            continue
        validation = validate_real_source_extract(_to_real_source_extract(extract))
        status = _strict_status(extract, validation.status)
        results.append(
            SourcePackExtractValidationResult(
                extract_id=extract.extract_id,
                source_id=extract.source_id,
                slot_id=extract.slot_id,
                status=status,
                counts_as_real_support=status.startswith("EXTRACT_VALID_"),
                requires_manual_review=False,
                supported_components=list(extract.supported_components),
                contradicted_components=list(extract.contradicted_components),
                reasons=list(validation.reasons),
            )
        )
    return results


def validated_extracts(results: list[SourcePackExtractValidationResult]) -> list[SourcePackValidatedExtract]:
    return [
        SourcePackValidatedExtract(
            extract_id=result.extract_id,
            source_id=result.source_id,
            slot_id=result.slot_id,
            validation_status=result.status,
        )
        for result in results
        if result.counts_as_real_support
    ]


def _requires_manual_review_before_support(extract: SeedSourceExtract) -> bool:
    if not extract.manual_review_required:
        return False
    has_exact_reviewed_fields = bool(
        extract.exact_quote_available
        and (
            extract.equation_text
            or extract.observable_text
            or extract.parameter_constraint_text
            or extract.benchmark_data_text
            or extract.contradicted_components
        )
    )
    return not has_exact_reviewed_fields


def _strict_status(extract: SeedSourceExtract, base_status: str) -> str:
    if extract.benchmark_data_text and base_status != "EXTRACT_VALID_PROVIDES_BENCHMARK_DATA":
        return "EXTRACT_REJECTED_NOT_COMPARABLE"
    if base_status.startswith("EXTRACT_VALID_") and not extract.supported_components and not extract.contradicted_components:
        return "EXTRACT_REJECTED_NO_COMPONENT_SUPPORT"
    if base_status == "EXTRACT_REQUIRES_MANUAL_REVIEW" and extract.extract_text_or_paraphrase and not extract.supported_components:
        return "EXTRACT_REJECTED_ANALOGY_ONLY"
    return base_status


def _to_real_source_extract(extract: SeedSourceExtract) -> RealSourceExtract:
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
    )


def _result(
    extract: SeedSourceExtract,
    status: str,
    reasons: list[str],
    requires_manual_review: bool = False,
) -> SourcePackExtractValidationResult:
    return SourcePackExtractValidationResult(
        extract_id=extract.extract_id,
        source_id=extract.source_id,
        slot_id=extract.slot_id,
        status=status,
        counts_as_real_support=False,
        requires_manual_review=requires_manual_review,
        supported_components=list(extract.supported_components),
        contradicted_components=list(extract.contradicted_components),
        reasons=reasons,
    )
