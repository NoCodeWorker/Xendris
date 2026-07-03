"""
Phygn v1.3 — Manifest Draft Writer

Writes a filled source manifest draft with real candidate details.
Ensures local_file_status is correctly marked as MISSING if the files do not exist.
"""

from __future__ import annotations

import json
from pathlib import Path
from phyng.evidence.real_source_candidates import get_baseline_real_source_candidates

def write_filled_manifest_draft(project_root: Path) -> Path:
    """
    Writes a filled manifest draft containing real source candidates.
    Evaluates if the files actually exist in sources/baseline/papers/.
    """
    candidates = get_baseline_real_source_candidates()
    draft_entries = []
    
    for cand in candidates:
        # Check if local file exists
        local_rel_path = f"sources/baseline/papers/{cand.source_candidate_id}.pdf"
        local_abs_path = project_root / local_rel_path
        
        file_status = "PRESENT" if local_abs_path.exists() else "MISSING"
        
        entry = {
            "source_candidate_id": cand.source_candidate_id,
            "requirement_id": "BSP-001" if "DECOH" in cand.source_candidate_id else ("BSP-002" if "VIS" in cand.source_candidate_id else "BSP-004"),
            "title": cand.title,
            "authors": cand.authors,
            "year": cand.year,
            "source_type": "LOCAL_FILE",
            "local_path": local_rel_path,
            "url": cand.url,
            "trust_level": cand.trust_level,
            "intended_support_types": cand.intended_support_types,
            "notes": cand.notes,
            "local_file_status": file_status
        }
        draft_entries.append(entry)
        
    out_dir = project_root / "sources" / "baseline"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    draft_path = out_dir / "source_manifest_draft_v1_3.json"
    draft_path.write_text(json.dumps(draft_entries, indent=2), encoding="utf-8")
    
    # Also write report
    _write_manifest_draft_report(project_root, draft_entries, draft_path)
    
    return draft_path

def _write_manifest_draft_report(project_root: Path, entries: list[dict], draft_path: Path) -> None:
    report_dir = project_root / "reports" / "rag"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / "filled_manifest_draft_v1_3.md"
    
    lines = [
        "# Filled Source Manifest Draft — v1.3",
        "",
        f"- **Draft Path**: `{draft_path.relative_to(project_root)}`",
        f"- **Total Candidate Entries**: {len(entries)}",
        "",
        "## Candidate Entries",
        "",
        "| ID | Title | Authors | Year | Local File Status | Intended Support |",
        "|---|---|---|---|---|---|",
    ]
    
    for entry in entries:
        title = entry["title"] or "*Unknown*"
        authors = ", ".join(entry["authors"]) if entry["authors"] else "*None*"
        year = entry["year"] or "*Unknown*"
        status = entry["local_file_status"]
        support = ", ".join(entry["intended_support_types"])
        lines.append(f"| {entry['source_candidate_id']} | {title} | {authors} | {year} | **{status}** | {support} |")
        
    lines.extend([
        "",
        "## Discipline Note",
        "No fake local ingestion. If the local file does not exist, `local_file_status` is `MISSING`.",
        "A filled manifest draft is still not evidence. It becomes useful only after local audit."
    ])
    
    report_path.write_text("\n".join(lines), encoding="utf-8")
