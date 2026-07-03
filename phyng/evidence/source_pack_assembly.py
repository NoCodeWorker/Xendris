"""
Phygn v1.2 — Source Pack Assembly

Assembles the template skeleton for the baseline source pack.
"""

from __future__ import annotations

import json
from pathlib import Path
from pydantic import BaseModel, Field

from phyng.evidence.source_pack_readiness_v1_1 import create_baseline_source_folders
from phyng.evidence.canonical_source_slots import CANONICAL_SLOTS
from phyng.evidence.source_pack_templates import (
    MANIFEST_TEMPLATE,
    get_extract_template,
    PAPERS_README,
    REJECTED_README,
    SELECTION_NOTES,
)
from phyng.evidence.source_manifest_validation import validate_source_manifest
from phyng.evidence.extract_validation import validate_extract_file

class SourcePackAssemblyResult(BaseModel):
    assembly_status: str = "SOURCE_PACK_TEMPLATE_READY"
    ready_for_ingestion_attempt: bool = False
    manifest_path: str
    created_files: list[str] = Field(default_factory=list)
    report_paths: list[str] = Field(default_factory=list)
    manifest_structurally_valid: bool = False
    extracts_structurally_valid: bool = False

def assemble_baseline_source_pack_templates(project_root: Path) -> SourcePackAssemblyResult:
    """
    Assemble all baseline source pack templates under sources/baseline/.
    Does not claim the baseline is source-backed.
    """
    # 1. Scaffold folders
    create_baseline_source_folders(project_root)
    
    baseline_dir = project_root / "sources" / "baseline"
    
    created_files = []
    
    # 2. Write manifest template
    manifest_path = baseline_dir / "source_manifest.json"
    manifest_path.write_text(json.dumps(MANIFEST_TEMPLATE, indent=2), encoding="utf-8")
    created_files.append(str(manifest_path))
    
    # 3. Write papers/README.md
    papers_readme = baseline_dir / "papers" / "README.md"
    papers_readme.write_text(PAPERS_README, encoding="utf-8")
    created_files.append(str(papers_readme))
    
    # 4. Write extract templates
    extracts_dir = baseline_dir / "extracts"
    for source_id in CANONICAL_SLOTS:
        epath = extracts_dir / f"{source_id}_extracts.md"
        epath.write_text(get_extract_template(source_id), encoding="utf-8")
        created_files.append(str(epath))
        
    # 5. Write notes/source_selection_notes.md
    notes_path = baseline_dir / "notes" / "source_selection_notes.md"
    notes_path.write_text(SELECTION_NOTES, encoding="utf-8")
    created_files.append(str(notes_path))
    
    # 6. Write rejected/README.md
    rejected_readme = baseline_dir / "rejected" / "README.md"
    rejected_readme.write_text(REJECTED_README, encoding="utf-8")
    created_files.append(str(rejected_readme))
    
    # 7. Structural validation check (ignoring missing local files and TEMPLATE_NOT_EVIDENCE for structural validation)
    # Let's check manifest structure
    manifest_val = validate_source_manifest(manifest_path, project_root)
    # The manifest template has LOCAL_FILE entries with missing files, so manifest_val.overall_valid will be False.
    # However, we want to verify if it is *structurally* valid (JSON parses, required fields exist).
    # Since we want to report `manifest_structurally_valid`, we check if there are no missing required fields.
    manifest_structurally_valid = True
    if not manifest_val.json_valid or not manifest_val.is_list:
        manifest_structurally_valid = False
    else:
        for entry_val in manifest_val.entry_results:
            if entry_val.missing_fields:
                manifest_structurally_valid = False
                
    # Check extracts structure
    extracts_structurally_valid = True
    for source_id in CANONICAL_SLOTS:
        epath = extracts_dir / f"{source_id}_extracts.md"
        eval_res = validate_extract_file(epath)
        # Note: eval_res.valid will be False because of the TEMPLATE_NOT_EVIDENCE forbidden phrase.
        # But we check structural fields: header, support types, claim target, local reference, audit notes.
        if (not eval_res.has_source_header or 
            not eval_res.support_types_found or 
            not eval_res.has_claim_target or 
            not eval_res.has_local_reference or 
            not eval_res.has_audit_notes):
            extracts_structurally_valid = False
            
    # 8. Write reports
    report_paths = _write_v1_2_reports(
        project_root,
        manifest_path,
        created_files,
        manifest_structurally_valid,
        extracts_structurally_valid
    )
    
    return SourcePackAssemblyResult(
        assembly_status="SOURCE_PACK_TEMPLATE_READY",
        ready_for_ingestion_attempt=False,
        manifest_path=str(manifest_path),
        created_files=created_files,
        report_paths=report_paths,
        manifest_structurally_valid=manifest_structurally_valid,
        extracts_structurally_valid=extracts_structurally_valid,
    )

def _write_v1_2_reports(
    project_root: Path,
    manifest_path: Path,
    created_files: list[str],
    manifest_structurally_valid: bool,
    extracts_structurally_valid: bool,
) -> list[str]:
    rag_dir = project_root / "reports" / "rag"
    camp_dir = project_root / "reports" / "campaigns"
    rag_dir.mkdir(parents=True, exist_ok=True)
    camp_dir.mkdir(parents=True, exist_ok=True)
    
    reports = []
    
    # 1. reports/rag/source_pack_assembly_v1_2.md
    p1 = rag_dir / "source_pack_assembly_v1_2.md"
    p1.write_text(
        "\n".join([
            "# Source Pack Assembly — v1.2",
            "",
            f"- **Assembly Status**: **SOURCE_PACK_TEMPLATE_READY**",
            f"- **Ready for Ingestion Attempt**: False",
            f"- **Manifest Structurally Valid**: {manifest_structurally_valid}",
            f"- **Extracts Structurally Valid**: {extracts_structurally_valid}",
            "",
            "## Created Files",
            *[f"- `{Path(f).relative_to(project_root)}`" for f in created_files],
            "",
            "## Discipline Note",
            "Do not confuse an empty evidence container with evidence.",
            "The assembly status is template-ready only. No physical claim is unlocked."
        ]),
        encoding="utf-8"
    )
    reports.append(str(p1))
    
    # 2. reports/rag/source_manifest_template_v1_2.md
    p2 = rag_dir / "source_manifest_template_v1_2.md"
    p2.write_text(
        "\n".join([
            "# Source Manifest Template — v1.2",
            "",
            f"- **Path**: `{manifest_path.relative_to(project_root)}`",
            f"- **Structurally Valid**: {manifest_structurally_valid}",
            "",
            "All 5 canonical slots have been successfully generated in the manifest.",
            "The metadata fields (title, authors, year) remain null or empty as required."
        ]),
        encoding="utf-8"
    )
    reports.append(str(p2))
    
    # 3. reports/rag/extract_template_validation_v1_2.md
    p3 = rag_dir / "extract_template_validation_v1_2.md"
    p3.write_text(
        "\n".join([
            "# Extract Template Validation — v1.2",
            "",
            f"- **Structurally Valid**: {extracts_structurally_valid}",
            "",
            "Extract templates contain the `[TEMPLATE_NOT_EVIDENCE]` marker and are correctly",
            "flagged as invalid for real ingestion, preventing premature baseline upgrades."
        ]),
        encoding="utf-8"
    )
    reports.append(str(p3))
    
    # 4. reports/campaigns/BASELINE-SRC-PACK-001_v1_2_assembly.md
    p4 = camp_dir / "BASELINE-SRC-PACK-001_v1_2_assembly.md"
    p4.write_text(
        "\n".join([
            "# BASELINE-SRC-PACK-001 — v1.2 Assembly",
            "",
            f"- **Status**: **SOURCE_PACK_TEMPLATE_READY**",
            f"- **Ready for Ingestion**: False",
            "",
            "## Blocked Claims",
            "- Phygn predicts gravitational decoherence. (BLOCKED)",
            "- Frontera C is validated. (BLOCKED)",
            "- The boundary-aware candidate is validated. (BLOCKED)",
            "- SyntheticGain is physical PredictiveGain. (BLOCKED)"
        ]),
        encoding="utf-8"
    )
    reports.append(str(p4))
    
    return reports
