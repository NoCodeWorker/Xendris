"""Slot coverage scoring for source-pack validation."""

from __future__ import annotations

from phyng.source_pack_population.schemas import SeedSourceExtractPack, SeedSourceManifest
from phyng.source_pack_validation.schemas import SourcePackExtractValidationResult, SourcePackSlotCoverageMatrix, SourcePackSlotCoverageRecord
from phyng.source_pressure.slots import build_phi_gradient_source_slots


def score_slot_coverage(
    manifest: SeedSourceManifest,
    extract_pack: SeedSourceExtractPack,
    validations: list[SourcePackExtractValidationResult],
) -> SourcePackSlotCoverageMatrix:
    records: list[SourcePackSlotCoverageRecord] = []
    for slot in build_phi_gradient_source_slots():
        candidate_sources = [entry for entry in manifest.entries if slot.slot_id in entry.target_slots]
        extracts = [extract for extract in extract_pack.extracts if extract.slot_id == slot.slot_id]
        slot_validations = [validation for validation in validations if validation.slot_id == slot.slot_id]
        validated = [validation for validation in slot_validations if validation.counts_as_real_support]
        analogy = [validation for validation in slot_validations if validation.status == "EXTRACT_REJECTED_ANALOGY_ONLY"]
        manual = [validation for validation in slot_validations if validation.status == "EXTRACT_REQUIRES_MANUAL_REVIEW"]
        contradiction = [validation for validation in slot_validations if validation.status == "EXTRACT_VALID_CONTRADICTS_CANDIDATE"]
        benchmark = [validation for validation in slot_validations if validation.status == "EXTRACT_VALID_PROVIDES_BENCHMARK_DATA"]
        status = _coverage_status(candidate_sources, extracts, validated, analogy, manual, contradiction, benchmark)
        records.append(
            SourcePackSlotCoverageRecord(
                slot_id=slot.slot_id,
                candidate_source_count=len(candidate_sources),
                extract_count=len(extracts),
                validated_support_count=len(validated),
                analogy_rejection_count=len(analogy),
                manual_review_count=len(manual),
                contradiction_count=len(contradiction),
                benchmark_comparable_count=len(benchmark),
                coverage_status=status,
                missing_requirements=[] if validated else [slot.required_component],
            )
        )
    return SourcePackSlotCoverageMatrix(
        records=records,
        source_pressure_score=_source_pressure_score(records),
        manual_review_debt=sum(record.manual_review_count for record in records),
        missing_slots=[record.slot_id for record in records if record.validated_support_count == 0],
    )


def _coverage_status(candidate_sources, extracts, validated, analogy, manual, contradiction, benchmark) -> str:
    if contradiction:
        return "SLOT_CONTRADICTED"
    if benchmark:
        return "SLOT_BENCHMARK_COMPARABLE"
    if validated:
        return "SLOT_COVERED_LIMITED"
    if manual:
        return "SLOT_REQUIRES_MANUAL_REVIEW"
    if analogy:
        return "SLOT_ANALOGY_ONLY"
    if extracts or candidate_sources:
        return "SLOT_CANDIDATES_FOUND"
    return "SLOT_UNTOUCHED"


def _source_pressure_score(records: list[SourcePackSlotCoverageRecord]) -> float:
    by_slot = {record.slot_id: record for record in records}
    observable = int(
        by_slot["SLOT_1_DECOHERENCE_BASELINE_MODELS"].validated_support_count > 0
        or by_slot["SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"].validated_support_count > 0
    )
    gradient = int(by_slot["SLOT_4_GRADIENT_TRANSITION_OPERATORS"].validated_support_count > 0)
    parameter = int(by_slot["SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS"].validated_support_count > 0)
    analogy_penalty = min(sum(record.analogy_rejection_count for record in records), 3)
    score = 0.35 * observable + 0.35 * gradient + 0.20 * parameter - 0.10 * analogy_penalty
    return round(max(score, 0.0), 3)
