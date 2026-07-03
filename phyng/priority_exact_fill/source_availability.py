"""Priority source selection and source-text availability classification."""

from __future__ import annotations

from pathlib import Path

from phyng.priority_exact_fill.schemas import PrioritySourceAvailabilityRecord
from phyng.source_pack_population.schemas import SeedSourceManifest, SeedSourceManifestEntry

PRIORITY_SOURCE_MAP: dict[str, str] = {
    "SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE": "SRC-PHI-V32-001",
    "SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE": "SRC-PHI-V32-002",
    "SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST": "SRC-PHI-V32-005",
    "SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS": "SRC-PHI-V32-009",
    "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING": "SRC-PHI-V32-010",
}


def select_priority_sources(manifest: SeedSourceManifest) -> list[tuple[str, SeedSourceManifestEntry | None]]:
    entries_by_id = {entry.source_id: entry for entry in manifest.entries}
    return [(priority_id, entries_by_id.get(source_id)) for priority_id, source_id in PRIORITY_SOURCE_MAP.items()]


def classify_priority_source_availability(
    manifest: SeedSourceManifest,
    root: str | Path = ".",
) -> list[PrioritySourceAvailabilityRecord]:
    repo_root = Path(root)
    records: list[PrioritySourceAvailabilityRecord] = []
    for priority_id, entry in select_priority_sources(manifest):
        if entry is None:
            records.append(
                PrioritySourceAvailabilityRecord(
                    priority_source_id=priority_id,
                    source_text_status="SOURCE_RECORD_MISSING",
                    notes=["Priority source did not resolve to a reviewed manifest entry."],
                )
            )
            continue
        status = "SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD"
        notes = ["URLs and arXiv identifiers are traceability hints, not exact source text."]
        if entry.local_path:
            local_path = repo_root / entry.local_path
            if local_path.exists() and local_path.is_file():
                status = "SOURCE_TEXT_AVAILABLE_LOCAL"
                notes = ["Local source text exists and may be reviewed for exact extracts."]
            else:
                status = "SOURCE_TEXT_LOCAL_PATH_MISSING"
                notes = ["Manifest has a local_path, but the file is not present."]
        records.append(
            PrioritySourceAvailabilityRecord(
                priority_source_id=priority_id,
                matched_source_id=entry.source_id,
                source_title=entry.title,
                local_path=entry.local_path,
                traceable_identifier=entry.arxiv_id or entry.doi or entry.url,
                source_text_status=status,
                notes=notes,
            )
        )
    return records
