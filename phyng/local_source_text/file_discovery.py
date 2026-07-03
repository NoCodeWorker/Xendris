"""File discovery for priority local source text records."""

from __future__ import annotations

from pathlib import Path

from phyng.local_source_text.hashing import sha256_file
from phyng.local_source_text.schemas import LocalSourceFileRecord, PriorityLocalSourceSpec

SUPPORTED_FILE_TYPES = {".pdf", ".txt", ".md", ".html"}


def discover_local_source_files(
    specs: list[PriorityLocalSourceSpec],
    root: str | Path = ".",
) -> list[LocalSourceFileRecord]:
    repo_root = Path(root)
    records: list[LocalSourceFileRecord] = []
    for spec in specs:
        path = repo_root / spec.target_path
        suffix = path.suffix.lower()
        file_type = suffix if suffix else "UNKNOWN"
        if not path.exists():
            records.append(
                LocalSourceFileRecord(
                    source_id=spec.source_id,
                    canonical_filename=spec.preferred_filename,
                    local_path=spec.target_path,
                    exists=False,
                    file_type=file_type,
                    registry_status="LOCAL_SOURCE_FILE_REQUIRES_MANUAL_DOWNLOAD",
                    notes=["Local source file is missing; URL/arXiv/DOI metadata does not count as local text."],
                )
            )
            continue
        if not path.is_file():
            records.append(
                LocalSourceFileRecord(
                    source_id=spec.source_id,
                    canonical_filename=spec.preferred_filename,
                    local_path=spec.target_path,
                    exists=False,
                    file_type=file_type,
                    registry_status="LOCAL_SOURCE_FILE_UNSUPPORTED_TYPE",
                    notes=["Registered path exists but is not a regular file."],
                )
            )
            continue
        if suffix not in SUPPORTED_FILE_TYPES:
            records.append(
                LocalSourceFileRecord(
                    source_id=spec.source_id,
                    canonical_filename=spec.preferred_filename,
                    local_path=spec.target_path,
                    exists=True,
                    file_type=file_type,
                    size_bytes=path.stat().st_size,
                    registry_status="LOCAL_SOURCE_FILE_UNSUPPORTED_TYPE",
                    notes=["File exists, but v3.6 does not support this file type for exact extraction preparation."],
                )
            )
            continue
        try:
            digest = sha256_file(path)
            status = "LOCAL_SOURCE_FILE_HASHED"
            notes = ["File exists and was reproducibly registered with SHA256."]
        except OSError as exc:
            digest = None
            status = "LOCAL_SOURCE_FILE_HASH_FAILED"
            notes = [f"Hashing failed: {exc}"]
        records.append(
            LocalSourceFileRecord(
                source_id=spec.source_id,
                canonical_filename=spec.preferred_filename,
                local_path=spec.target_path,
                exists=True,
                file_type=file_type,
                size_bytes=path.stat().st_size,
                sha256=digest,
                text_extractable=None if suffix == ".pdf" else True,
                registry_status=status,
                notes=notes,
            )
        )
    return records
