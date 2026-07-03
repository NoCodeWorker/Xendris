"""Negative pressure scoring for source-pack validation."""

from __future__ import annotations

from phyng.source_pack_validation.schemas import SourcePackExtractValidationResult, SourcePackNegativePressureResult


def score_negative_pressure(results: list[SourcePackExtractValidationResult]) -> SourcePackNegativePressureResult:
    negative = [result.extract_id for result in results if result.status == "EXTRACT_VALID_CONTRADICTS_CANDIDATE"]
    if negative:
        return SourcePackNegativePressureResult(
            status="NEGATIVE_PRESSURE_FOUND",
            negative_pressure_count=len(negative),
            negative_extract_ids=negative,
        )
    return SourcePackNegativePressureResult(status="NEGATIVE_PRESSURE_NOT_VALIDATED")
