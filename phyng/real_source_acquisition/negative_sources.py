"""Negative source extraction from slot coverage."""

from __future__ import annotations

from phyng.real_source_acquisition.schemas import NegativeSourceRecord, RealExtractIngestionResult


def collect_negative_sources(ingestion_results: list[RealExtractIngestionResult]) -> list[NegativeSourceRecord]:
    records: list[NegativeSourceRecord] = []
    for result in ingestion_results:
        validation = result.validation
        if validation is None or validation.status != "EXTRACT_VALID_CONTRADICTS_CANDIDATE":
            continue
        for component in validation.contradicted_components:
            records.append(
                NegativeSourceRecord(
                    source_id=validation.source_id,
                    slot_id=validation.slot_id,
                    contradicted_component=component,
                )
            )
    return records
