"""Analogy rejection helpers for source-pack validation."""

from __future__ import annotations

from phyng.source_pack_validation.schemas import SourcePackExtractValidationResult


def analogy_rejections(results: list[SourcePackExtractValidationResult]) -> list[SourcePackExtractValidationResult]:
    return [result for result in results if result.status == "EXTRACT_REJECTED_ANALOGY_ONLY"]
