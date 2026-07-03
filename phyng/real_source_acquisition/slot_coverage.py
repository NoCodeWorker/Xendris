"""Slot coverage matrix for real source acquisition."""

from __future__ import annotations

from phyng.source_pressure.slots import build_phi_gradient_source_slots
from phyng.real_source_acquisition.schemas import RealExtractIngestionResult, RealSourceCandidate, SlotCoverageMatrix, SlotCoverageRecord


def build_slot_coverage_matrix(
    candidates: list[RealSourceCandidate],
    ingestion_results: list[RealExtractIngestionResult],
) -> SlotCoverageMatrix:
    records: list[SlotCoverageRecord] = []
    for slot in build_phi_gradient_source_slots():
        slot_candidates = [candidate.source_id for candidate in candidates if slot.slot_id in candidate.targeted_slots]
        validations = [
            result.validation
            for result in ingestion_results
            if result.validation is not None and result.validation.slot_id == slot.slot_id
        ]
        accepted = [validation.extract_id for validation in validations if validation.counts_as_real_support]
        analogy_count = sum(1 for validation in validations if validation.status == "EXTRACT_REJECTED_ANALOGY_ONLY")
        negative_count = sum(1 for validation in validations if validation.status == "EXTRACT_VALID_CONTRADICTS_CANDIDATE")
        status = _coverage_status(slot.slot_id, slot_candidates, accepted, analogy_count, negative_count)
        missing = [] if accepted else [slot.required_component]
        records.append(
            SlotCoverageRecord(
                slot_id=slot.slot_id,
                required_component=slot.required_component,
                candidate_sources=slot_candidates,
                validated_extracts=accepted,
                accepted_support_count=len(accepted),
                analogy_only_count=analogy_count,
                negative_count=negative_count,
                coverage_status=status,
                missing_requirements=missing,
            )
        )
    return SlotCoverageMatrix(records=records, missing_slots=[record.slot_id for record in records if record.accepted_support_count == 0])


def _coverage_status(slot_id: str, candidates: list[str], accepted: list[str], analogy_count: int, negative_count: int) -> str:
    if negative_count:
        return "SLOT_CONTRADICTED"
    if accepted and slot_id in {"SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS"}:
        return "SLOT_BENCHMARK_COMPARABLE"
    if accepted:
        return "SLOT_COVERED_LIMITED"
    if analogy_count:
        return "SLOT_ANALOGY_ONLY"
    if candidates:
        return "SLOT_CANDIDATES_FOUND"
    return "SLOT_UNTOUCHED"
