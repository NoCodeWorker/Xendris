"""
Phygn v1.1 — Baseline Source Pack Readiness

Evaluates the readiness of sources/baseline/ for an ingestion attempt
and creates the required folder scaffold.

Readiness statuses (ordered):
    NO_SOURCE_FOLDER → NO_MANIFEST → MANIFEST_INVALID →
    EXTRACTS_MISSING → PARTIAL_READY → READY_FOR_INGESTION_ATTEMPT

Does NOT claim ingestion has happened. Does NOT unlock baseline upgrade.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from phyng.evidence.extract_validation import validate_extract_folder
from phyng.evidence.source_manifest_validation import (
    validate_source_manifest,
    write_manifest_validation_report,
)

# ── Readiness statuses ─────────────────────────────────────────────────────

READINESS_STATUSES = [
    "NO_SOURCE_FOLDER",
    "NO_MANIFEST",
    "MANIFEST_INVALID",
    "EXTRACTS_MISSING",
    "PARTIAL_READY",
    "READY_FOR_INGESTION_ATTEMPT",
]

_SOURCE_FOLDERS = [
    "sources/baseline",
    "sources/baseline/papers",
    "sources/baseline/extracts",
    "sources/baseline/notes",
    "sources/baseline/rejected",
]


# ── Models ─────────────────────────────────────────────────────────────────

class SourcePackReadinessResult(BaseModel):
    project_root: str
    folders_exist: bool = False
    manifest_exists: bool = False
    manifest_valid: bool = False
    extracts_count: int = 0
    validated_extracts_count: int = 0
    missing_categories: list[str] = Field(default_factory=list)
    readiness_status: str = "NO_SOURCE_FOLDER"
    ready_for_ingestion_attempt: bool = False
    allowed_next_action: str = ""
    report_paths: list[str] = Field(default_factory=list)


# ── Folder scaffolding ─────────────────────────────────────────────────────

def create_baseline_source_folders(project_root: Path) -> list[Path]:
    """
    Create the standard baseline source folder structure.
    Does NOT create any fake source files.

    Returns:
        List of created/existing folder paths.
    """
    created: list[Path] = []
    for rel in _SOURCE_FOLDERS:
        folder = project_root / rel
        folder.mkdir(parents=True, exist_ok=True)
        created.append(folder)
    return created


# ── Core function ──────────────────────────────────────────────────────────

def generate_baseline_source_pack_readiness_v1_1(
    project_root: Path,
) -> SourcePackReadinessResult:
    """
    Evaluate readiness of sources/baseline/ for an ingestion attempt.

    Progression:
        NO_SOURCE_FOLDER: baseline dir missing
        NO_MANIFEST: dir exists but no manifest
        MANIFEST_INVALID: manifest JSON invalid or entries invalid
        EXTRACTS_MISSING: manifest valid but no extract files found
        PARTIAL_READY: manifest valid + extracts exist but not all valid
        READY_FOR_INGESTION_ATTEMPT: manifest valid + ≥1 validated extract
    """
    result = SourcePackReadinessResult(project_root=str(project_root))

    baseline_dir = project_root / "sources" / "baseline"
    extracts_dir = baseline_dir / "extracts"
    manifest_path = baseline_dir / "source_manifest.json"

    # Step 1 — folders
    if not baseline_dir.exists():
        result.readiness_status = "NO_SOURCE_FOLDER"
        result.allowed_next_action = (
            "Run create_baseline_source_folders() to scaffold the required directory structure."
        )
        _write_reports(result, project_root, None, [])
        return result

    result.folders_exist = True

    # Step 2 — manifest
    if not manifest_path.exists():
        result.readiness_status = "NO_MANIFEST"
        result.allowed_next_action = (
            "Author sources/baseline/source_manifest.json following "
            "docs/64_PHYGN_SOURCE_MANIFEST_AUTHORING_PROTOCOL.md."
        )
        _write_reports(result, project_root, None, [])
        return result

    result.manifest_exists = True

    # Step 3 — manifest validation
    manifest_result = validate_source_manifest(manifest_path, project_root)
    write_manifest_validation_report(manifest_result, project_root)

    if not manifest_result.overall_valid:
        result.readiness_status = "MANIFEST_INVALID"
        result.allowed_next_action = (
            f"Fix manifest issues: {manifest_result.summary}"
        )
        _write_reports(result, project_root, manifest_result, [])
        return result

    result.manifest_valid = True

    # Step 4 — extracts
    extract_results = validate_extract_folder(extracts_dir)
    result.extracts_count = len(extract_results)
    result.validated_extracts_count = sum(1 for r in extract_results if r.valid)

    if result.extracts_count == 0:
        result.readiness_status = "EXTRACTS_MISSING"
        result.allowed_next_action = (
            "Add extract .md files to sources/baseline/extracts/ following "
            "docs/65_PHYGN_EXTRACTS_AND_SUPPORT_TAGGING_PROTOCOL.md."
        )
        _write_reports(result, project_root, manifest_result, extract_results)
        return result

    if result.validated_extracts_count == 0:
        result.readiness_status = "PARTIAL_READY"
        result.allowed_next_action = (
            "Fix extract files so at least 1 passes validation "
            "(support type, claim target, audit notes, no forbidden phrases)."
        )
        _write_reports(result, project_root, manifest_result, extract_results)
        return result

    # READY
    result.readiness_status = "READY_FOR_INGESTION_ATTEMPT"
    result.ready_for_ingestion_attempt = True
    result.allowed_next_action = (
        "Run: python -m phyng.campaigns.baseline_source_pack_ingestion"
    )

    _write_reports(result, project_root, manifest_result, extract_results)
    return result


# ── Report writers ─────────────────────────────────────────────────────────

def _write_reports(
    result: SourcePackReadinessResult,
    project_root: Path,
    manifest_result,
    extract_results: list,
) -> None:
    rag_dir = project_root / "reports" / "rag"
    camp_dir = project_root / "reports" / "campaigns"
    rag_dir.mkdir(parents=True, exist_ok=True)
    camp_dir.mkdir(parents=True, exist_ok=True)

    # 1. RAG readiness report
    p1 = rag_dir / "baseline_source_pack_readiness_v1_1.md"
    p1.write_text(
        "\n".join([
            "# Baseline Source Pack Readiness — v1.1",
            "",
            f"- **Project root**: `{result.project_root}`",
            f"- **Folders exist**: {result.folders_exist}",
            f"- **Manifest exists**: {result.manifest_exists}",
            f"- **Manifest valid**: {result.manifest_valid}",
            f"- **Extracts count**: {result.extracts_count}",
            f"- **Validated extracts**: {result.validated_extracts_count}",
            f"- **Readiness status**: **{result.readiness_status}**",
            f"- **Ready for ingestion attempt**: {result.ready_for_ingestion_attempt}",
            "",
            "## Allowed Next Action",
            "",
            result.allowed_next_action,
            "",
            "## Discipline Note",
            "",
            "Prepare evidence. Do not pretend it has already spoken.",
            "The baseline can become source-backed only after the ingestion runner",
            "sees real local files and audits them.",
        ]),
        encoding="utf-8",
    )
    result.report_paths.append(str(p1))

    # 2. Campaign readiness report
    p2 = camp_dir / "BASELINE-SRC-PACK-001_v1_1_readiness.md"
    extract_rows = []
    for r in extract_results:
        fname = Path(r.extract_path).name
        extract_rows.append(
            f"| {fname} | {r.valid} | {', '.join(r.support_types_found) or '—'} |"
        )

    manifest_summary = manifest_result.summary if manifest_result else "No manifest validated."
    p2.write_text(
        "\n".join([
            "# BASELINE-SRC-PACK-001 — v1.1 Readiness Report",
            "",
            f"- **Readiness**: **{result.readiness_status}**",
            f"- **Ready for ingestion attempt**: {result.ready_for_ingestion_attempt}",
            "",
            "## Manifest Summary",
            "",
            manifest_summary,
            "",
            "## Extract Validation",
            "",
            "| File | Valid | Support Types |",
            "|---|---|---|",
            *(extract_rows or ["| — | — | No extracts found. |"]),
            "",
            "## Next Action",
            "",
            result.allowed_next_action,
            "",
            "## Blocked Claims",
            "",
            "- Phygn predicts gravitational decoherence. (BLOCKED)",
            "- Frontera C is validated. (BLOCKED)",
            "- The boundary-aware candidate is validated. (BLOCKED)",
            "- SyntheticGain is physical PredictiveGain. (BLOCKED)",
        ]),
        encoding="utf-8",
    )
    result.report_paths.append(str(p2))
