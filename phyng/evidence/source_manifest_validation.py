"""
Phygn v1.1 — Source Manifest Validation

Validates sources/baseline/source_manifest.json against the protocol
defined in docs/64_PHYGN_SOURCE_MANIFEST_AUTHORING_PROTOCOL.md.

Does NOT claim sources have been ingested.
Reports what is valid, what is missing, and what is not ready.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

# ── Allowed values ─────────────────────────────────────────────────────────

ALLOWED_SOURCE_TYPES = {
    "LOCAL_FILE",
    "MANUAL_RECORD",
    "EXTERNAL_URL_RECORD",
    "BIBTEX_RECORD",
    "RESEARCH_TASK_ONLY",
}

ALLOWED_TRUST_LEVELS = {"PRIMARY", "HIGH", "MEDIUM", "LOW", "UNKNOWN"}

ALLOWED_SUPPORT_TYPES = {
    "FORMULA_SUPPORT",
    "OBSERVABLE_SUPPORT",
    "PARAMETER_SUPPORT",
    "CONTEXT_SUPPORT",
    "BENCHMARK_SUPPORT",
    "ASSUMPTION_SUPPORT",
    "CONTRADICTION",
}

# source_types that cannot count as local ingestion
NON_INGESTED_TYPES = {"EXTERNAL_URL_RECORD", "RESEARCH_TASK_ONLY"}

REQUIRED_FIELDS = {
    "source_candidate_id",
    "requirement_id",
    "title",
    "authors",
    "year",
    "source_type",
    "local_path",
    "url",
    "trust_level",
    "intended_support_types",
    "notes",
}


# ── Models ─────────────────────────────────────────────────────────────────

class EntryValidationResult(BaseModel):
    entry_index: int
    source_candidate_id: str | None
    valid: bool
    missing_fields: list[str] = Field(default_factory=list)
    invalid_source_type: str | None = None
    invalid_trust_level: str | None = None
    invalid_support_types: list[str] = Field(default_factory=list)
    local_file_missing: bool = False
    not_ingested: bool = False
    notes: list[str] = Field(default_factory=list)


class ManifestValidationResult(BaseModel):
    manifest_path: str
    json_valid: bool = False
    is_list: bool = False
    total_entries: int = 0
    valid_entries: int = 0
    invalid_entries: int = 0
    non_ingested_entries: int = 0
    local_file_missing_entries: int = 0
    entry_results: list[EntryValidationResult] = Field(default_factory=list)
    overall_valid: bool = False
    summary: str = ""
    report_path: str = ""


# ── Core function ──────────────────────────────────────────────────────────

def validate_source_manifest(
    manifest_path: Path,
    project_root: Path | None = None,
) -> ManifestValidationResult:
    """
    Validate a source_manifest.json file.

    Args:
        manifest_path: Path to the manifest JSON file.
        project_root: Used to resolve relative local_path entries.
                      Defaults to the manifest's parent parent parent (project root).
    """
    result = ManifestValidationResult(manifest_path=str(manifest_path))

    if project_root is None:
        # sources/baseline/source_manifest.json → project root is 3 levels up
        project_root = manifest_path.parent.parent.parent

    # Step 1 — parse JSON
    if not manifest_path.exists():
        result.summary = "Manifest file does not exist."
        return result

    try:
        raw = manifest_path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (json.JSONDecodeError, OSError) as exc:
        result.json_valid = False
        result.summary = f"JSON parse error: {exc}"
        return result

    result.json_valid = True

    # Step 2 — must be a list
    if not isinstance(data, list):
        result.is_list = False
        result.summary = "Top-level element is not a list."
        return result

    result.is_list = True
    result.total_entries = len(data)

    # Step 3 — validate each entry
    for idx, entry in enumerate(data):
        ev = _validate_entry(idx, entry, project_root)
        result.entry_results.append(ev)
        if ev.valid:
            result.valid_entries += 1
        else:
            result.invalid_entries += 1
        if ev.not_ingested:
            result.non_ingested_entries += 1
        if ev.local_file_missing:
            result.local_file_missing_entries += 1

    result.overall_valid = (result.invalid_entries == 0 and result.total_entries > 0)
    result.summary = (
        f"{result.valid_entries}/{result.total_entries} entries valid. "
        f"{result.invalid_entries} invalid. "
        f"{result.non_ingested_entries} not ingested. "
        f"{result.local_file_missing_entries} missing local files."
    )
    return result


def _validate_entry(
    idx: int, entry: Any, project_root: Path
) -> EntryValidationResult:
    if not isinstance(entry, dict):
        return EntryValidationResult(
            entry_index=idx,
            source_candidate_id=None,
            valid=False,
            notes=["Entry is not a JSON object."],
        )

    cid = entry.get("source_candidate_id")
    ev = EntryValidationResult(entry_index=idx, source_candidate_id=cid, valid=True)

    # Required fields
    missing = [f for f in REQUIRED_FIELDS if f not in entry]
    if missing:
        ev.missing_fields = sorted(missing)
        ev.valid = False

    # source_type
    source_type = entry.get("source_type")
    if source_type and source_type not in ALLOWED_SOURCE_TYPES:
        ev.invalid_source_type = source_type
        ev.valid = False

    # trust_level
    trust = entry.get("trust_level")
    if trust and trust not in ALLOWED_TRUST_LEVELS:
        ev.invalid_trust_level = trust
        ev.valid = False

    # intended_support_types
    support_types = entry.get("intended_support_types", [])
    if isinstance(support_types, list):
        bad = [s for s in support_types if s not in ALLOWED_SUPPORT_TYPES]
        if bad:
            ev.invalid_support_types = bad
            ev.valid = False
    elif support_types is not None:
        ev.invalid_support_types = [str(support_types)]
        ev.valid = False

    # non-ingested types
    if source_type in NON_INGESTED_TYPES:
        ev.not_ingested = True
        ev.notes.append(f"{source_type} cannot count as local ingestion.")

    # LOCAL_FILE must have existing file
    local_path = entry.get("local_path")
    if source_type == "LOCAL_FILE" and local_path:
        resolved = project_root / local_path
        if not resolved.exists():
            ev.local_file_missing = True
            ev.valid = False
            ev.notes.append(f"Local file not found: {local_path}")

    return ev


# ── Report writer ──────────────────────────────────────────────────────────

def write_manifest_validation_report(
    result: ManifestValidationResult,
    project_root: Path,
) -> Path:
    out_dir = project_root / "reports" / "rag"
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / "source_manifest_validation_v1_1.md"

    lines = [
        "# Source Manifest Validation — v1.1",
        "",
        f"- **Manifest**: `{result.manifest_path}`",
        f"- **JSON Valid**: {result.json_valid}",
        f"- **Is List**: {result.is_list}",
        f"- **Total Entries**: {result.total_entries}",
        f"- **Valid**: {result.valid_entries}",
        f"- **Invalid**: {result.invalid_entries}",
        f"- **Not Ingested**: {result.non_ingested_entries}",
        f"- **Missing Local Files**: {result.local_file_missing_entries}",
        f"- **Overall Valid**: **{result.overall_valid}**",
        "",
        f"**Summary**: {result.summary}",
        "",
        "## Entry Results",
        "",
        "| # | ID | Valid | Missing Fields | Notes |",
        "|---|---|---|---|---|",
    ]
    for ev in result.entry_results:
        missing = ", ".join(ev.missing_fields) or "—"
        notes = "; ".join(ev.notes) or "—"
        lines.append(
            f"| {ev.entry_index} | {ev.source_candidate_id or '—'} | {ev.valid} | {missing} | {notes} |"
        )

    lines += [
        "",
        "## Discipline Note",
        "",
        "The manifest points to evidence. It is not evidence.",
        "URL-only and RESEARCH_TASK_ONLY entries cannot unlock baseline upgrade.",
    ]

    p.write_text("\n".join(lines), encoding="utf-8")
    result.report_path = str(p)
    return p
