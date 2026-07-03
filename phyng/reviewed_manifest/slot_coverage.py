"""Slot coverage for reviewed manifests."""

from __future__ import annotations

from phyng.real_source_acquisition.schemas import RealExtractIngestionResult, RealSourceCandidate
from phyng.real_source_acquisition.slot_coverage import build_slot_coverage_matrix
from phyng.reviewed_manifest.schemas import (
    ReviewedSlotCoverageMatrix,
    ReviewedSlotCoverageRecord,
    ReviewedSourceExtractValidationResult,
    ReviewedSourceManifest,
)


def build_reviewed_slot_coverage_matrix(
    manifest: ReviewedSourceManifest,
    validations: list[ReviewedSourceExtractValidationResult],
) -> ReviewedSlotCoverageMatrix:
    candidates = [
        RealSourceCandidate(
            source_id=entry.source_id,
            title=entry.title,
            authors=entry.authors,
            year=entry.year,
            source_type=entry.source_type,
            url=entry.url,
            doi=entry.doi,
            arxiv_id=entry.arxiv_id,
            local_path=entry.local_path,
            targeted_slots=entry.target_slots,
            expected_components=entry.expected_components,
            acquisition_status="REVIEWED_LOCAL_MANIFEST_ENTRY",
            reason_for_inclusion="Reviewed local manifest entry.",
            is_support=False,
        )
        for entry in manifest.entries
    ]
    ingestion = [
        RealExtractIngestionResult(
            source_id=validation.source_id,
            attempted=True,
            status=validation.status,
            validation=validation.bridge_validation,
        )
        for validation in validations
    ]
    matrix = build_slot_coverage_matrix(candidates, ingestion)
    return ReviewedSlotCoverageMatrix(
        records=[
            ReviewedSlotCoverageRecord(
                slot_id=record.slot_id,
                coverage_status=record.coverage_status,
                candidate_sources=record.candidate_sources,
                validated_extracts=record.validated_extracts,
                accepted_support_count=record.accepted_support_count,
                missing_requirements=record.missing_requirements,
            )
            for record in matrix.records
        ],
        missing_slots=matrix.missing_slots,
    )
