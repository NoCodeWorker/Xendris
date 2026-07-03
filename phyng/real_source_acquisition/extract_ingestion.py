"""Extract ingestion bridge for acquired source candidates."""

from __future__ import annotations

from phyng.real_source_acquisition.schemas import RealExtractIngestionResult, RealSourceCandidate
from phyng.real_source_ingestion.extract_validation import validate_real_source_extract
from phyng.real_source_ingestion.schemas import RealSourceExtract


def ingest_candidate_extracts(
    candidates: list[RealSourceCandidate],
    extracts_by_source_id: dict[str, RealSourceExtract] | None = None,
) -> list[RealExtractIngestionResult]:
    extracts_by_source_id = extracts_by_source_id or {}
    results: list[RealExtractIngestionResult] = []
    for candidate in candidates:
        extract = extracts_by_source_id.get(candidate.source_id)
        if extract is None:
            results.append(
                RealExtractIngestionResult(
                    source_id=candidate.source_id,
                    attempted=False,
                    status="REAL_EXTRACT_MISSING",
                    notes=["Candidate has no extract; it cannot count as support."],
                )
            )
            continue
        validation = validate_real_source_extract(extract)
        results.append(
            RealExtractIngestionResult(
                source_id=candidate.source_id,
                attempted=True,
                status=validation.status,
                validation=validation,
            )
        )
    return results
