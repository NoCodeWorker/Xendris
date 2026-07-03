"""Build priority exact fill records without fabricating source text."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.exact_extract_review.schemas import ExactReviewedExtractPack
from phyng.priority_exact_fill.schemas import (
    PriorityExactFillLocationRecord,
    PriorityExactFillRecord,
    PrioritySourceAvailabilityRecord,
)
from phyng.source_pack_population.schemas import SeedSourceExtractPack, SeedSourceManifest

EXACT_OUTPUT_PATH = Path("data/real_sources/extracts/phi_gradient_priority_exact_extracts_v3_5.json")
LOCATION_OUTPUT_PATH = Path("data/real_sources/extracts/phi_gradient_priority_exact_extract_locations_v3_5.json")
REVIEW_NOTES_PATH = Path("data/real_sources/extracts/phi_gradient_priority_review_notes_v3_5.md")


def build_priority_fill_records(
    manifest: SeedSourceManifest,
    seed_extract_pack: SeedSourceExtractPack,
    reviewed_pack: ExactReviewedExtractPack,
    availability: list[PrioritySourceAvailabilityRecord],
) -> list[PriorityExactFillRecord]:
    manifest_by_id = {entry.source_id: entry for entry in manifest.entries}
    seed_by_id = {extract.source_id: extract for extract in seed_extract_pack.extracts}
    reviewed_by_id = {extract.source_id: extract for extract in reviewed_pack.extracts}
    records: list[PriorityExactFillRecord] = []
    for available in availability:
        if not available.matched_source_id:
            records.append(
                PriorityExactFillRecord(
                    priority_source_id=available.priority_source_id,
                    source_id="UNRESOLVED_PRIORITY_SOURCE",
                    slot_id="UNKNOWN_SLOT_REQUIRES_REVIEW",
                    source_text_status=available.source_text_status,
                    risk_flags=["RISK_PRIORITY_SOURCE_MISSING"],
                    reviewer_notes=["Priority source could not be matched to local manifest."],
                )
            )
            continue
        source_id = available.matched_source_id
        entry = manifest_by_id[source_id]
        seed_extract = seed_by_id.get(source_id)
        reviewed_extract = reviewed_by_id.get(source_id)
        exact_source_available = available.source_text_status == "SOURCE_TEXT_AVAILABLE_LOCAL"
        record = PriorityExactFillRecord(
            priority_source_id=available.priority_source_id,
            source_id=source_id,
            slot_id=(reviewed_extract.slot_id if reviewed_extract else seed_extract.slot_id if seed_extract else _first_slot(entry)),
            source_title=entry.title,
            source_text_status=available.source_text_status,
            location_type=reviewed_extract.location_type if reviewed_extract else "UNKNOWN_LOCATION_REQUIRES_REVIEW",
            location_value=reviewed_extract.location_value if reviewed_extract else "",
            exact_quote=reviewed_extract.exact_quote if exact_source_available and reviewed_extract else None,
            equation_text=reviewed_extract.equation_text if exact_source_available and reviewed_extract else None,
            observable_text=reviewed_extract.observable_text if exact_source_available and reviewed_extract else None,
            parameter_range_text=reviewed_extract.parameter_range_text if exact_source_available and reviewed_extract else None,
            benchmark_range_text=reviewed_extract.benchmark_range_text if exact_source_available and reviewed_extract else None,
            negative_constraint_text=reviewed_extract.negative_constraint_text if exact_source_available and reviewed_extract else None,
            supported_components=list(reviewed_extract.supported_components if reviewed_extract else seed_extract.supported_components if seed_extract else entry.expected_components),
            contradicted_components=list(reviewed_extract.contradicted_components if reviewed_extract else seed_extract.contradicted_components if seed_extract else []),
            risk_flags=list(entry.risk_flags),
            reviewer_notes=_reviewer_notes(available, exact_source_available),
        )
        if exact_source_available and _has_exact_content(record):
            record.review_status = "EXACT_FILL_VALIDATION_READY"
        elif exact_source_available:
            record.review_status = "EXACT_FILL_NO_VALIDATABLE_CONTENT"
        else:
            record.review_status = "EXACT_FILL_REQUIRES_SOURCE_TEXT"
        record.validation_ready = is_validation_ready(record)
        records.append(record)
    return records


def validate_priority_fill_locations(records: list[PriorityExactFillRecord]) -> list[PriorityExactFillLocationRecord]:
    results: list[PriorityExactFillLocationRecord] = []
    for record in records:
        missing = []
        if record.source_text_status != "SOURCE_TEXT_AVAILABLE_LOCAL":
            missing.append("source_text")
        if record.location_type == "UNKNOWN_LOCATION_REQUIRES_REVIEW":
            missing.append("location_type")
        if not record.location_value:
            missing.append("location_value")
        if not _has_exact_content(record):
            missing.append("exact_content")
        ready = not missing and record.review_status != "EXACT_FILL_REQUIRES_SOURCE_TEXT"
        results.append(
            PriorityExactFillLocationRecord(
                priority_source_id=record.priority_source_id,
                source_id=record.source_id,
                status="PRIORITY_EXACT_FILL_VALIDATION_READY" if ready else "PRIORITY_EXACT_FILL_UNRESOLVED",
                validation_ready=ready,
                missing_requirements=missing,
            )
        )
    return results


def is_validation_ready(record: PriorityExactFillRecord) -> bool:
    return (
        record.source_text_status == "SOURCE_TEXT_AVAILABLE_LOCAL"
        and record.location_type != "UNKNOWN_LOCATION_REQUIRES_REVIEW"
        and bool(record.location_value)
        and _has_exact_content(record)
        and record.review_status not in {"EXACT_FILL_REQUIRES_SOURCE_TEXT", "EXACT_FILL_NO_VALIDATABLE_CONTENT"}
    )


def write_priority_fill_outputs(
    root: str | Path,
    records: list[PriorityExactFillRecord],
    location_records: list[PriorityExactFillLocationRecord],
) -> dict[str, str]:
    repo_root = Path(root)
    exact_path = repo_root / EXACT_OUTPUT_PATH
    locations_path = repo_root / LOCATION_OUTPUT_PATH
    review_notes_path = repo_root / REVIEW_NOTES_PATH
    exact_path.parent.mkdir(parents=True, exist_ok=True)
    exact_path.write_text(json.dumps([record.model_dump(mode="json") for record in records], indent=2, sort_keys=True), encoding="utf-8")
    locations_path.write_text(
        json.dumps([record.model_dump(mode="json") for record in location_records], indent=2, sort_keys=True),
        encoding="utf-8",
    )
    review_notes_path.write_text(_render_review_notes(records), encoding="utf-8")
    return {
        "priority_exact_extracts": str(exact_path),
        "priority_locations": str(locations_path),
        "priority_review_notes": str(review_notes_path),
    }


def _has_exact_content(record: PriorityExactFillRecord) -> bool:
    return bool(
        record.exact_quote
        or record.equation_text
        or record.observable_text
        or record.parameter_range_text
        or record.benchmark_range_text
        or record.negative_constraint_text
    )


def _first_slot(entry) -> str:
    return entry.target_slots[0] if entry.target_slots else "UNKNOWN_SLOT_REQUIRES_REVIEW"


def _reviewer_notes(availability: PrioritySourceAvailabilityRecord, exact_source_available: bool) -> list[str]:
    if exact_source_available:
        return ["Exact fields may be used only where reviewed local text supplied them."]
    return ["No exact quote, equation, parameter range, benchmark range, or source text was fabricated."]


def _render_review_notes(records: list[PriorityExactFillRecord]) -> str:
    lines = [
        "# PHI_GRADIENT Priority Review Notes v3.5",
        "",
        "Priority exact fill attempted only against local reviewed inputs.",
        "",
        "## Unresolved Records",
        "",
    ]
    unresolved = [record for record in records if not record.validation_ready]
    lines.extend([f"- `{record.priority_source_id}` -> `{record.source_id}`: `{record.review_status}`" for record in unresolved] or ["- None"])
    lines.extend(["", "## Discipline Note", "", "URLs and arXiv identifiers were not treated as exact source text."])
    return "\n".join(lines) + "\n"
