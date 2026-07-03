"""Availability classification for local source text files."""

from __future__ import annotations

from phyng.local_source_text.schemas import LocalSourceFileRecord, SourceAvailabilityManifest, SourceAvailabilityRecord


def build_source_availability_manifest(records: list[LocalSourceFileRecord]) -> SourceAvailabilityManifest:
    availability = []
    for record in records:
        if not record.exists:
            status = "SOURCE_FILE_REQUIRES_MANUAL_DOWNLOAD"
            notes = ["No local file is available for exact extraction."]
        elif record.exists and not record.sha256:
            status = "SOURCE_FILE_AVAILABLE_BUT_UNHASHED"
            notes = ["Local file exists, but it is not reproducibly registered."]
        else:
            status = "SOURCE_FILE_AVAILABLE_AND_HASHED"
            notes = ["Local file exists and has a SHA256 hash."]
        availability.append(
            SourceAvailabilityRecord(
                source_id=record.source_id,
                local_path=record.local_path,
                availability_status=status,
                exists=record.exists,
                hashed=bool(record.sha256),
                notes=notes,
            )
        )
    return SourceAvailabilityManifest(availability=availability)
