"""
Phygn v1.1 — Extract File Validation

Validates .md extract files in sources/baseline/extracts/ against the
protocol defined in docs/65_PHYGN_EXTRACTS_AND_SUPPORT_TAGGING_PROTOCOL.md.

Extract files are claim-permission artifacts, not rhetoric.
"""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel, Field

# ── Allowed values ─────────────────────────────────────────────────────────

ALLOWED_SUPPORT_TAGS = {
    "FORMULA_SUPPORT",
    "OBSERVABLE_SUPPORT",
    "PARAMETER_SUPPORT",
    "CONTEXT_SUPPORT",
    "BENCHMARK_SUPPORT",
    "ASSUMPTION_SUPPORT",
    "CONTRADICTION",
}

FORBIDDEN_PHRASES = [
    "frontera c is validated",
    "predicts decoherence",
    "predicts gravitational decoherence",
    "candidate is validated",
    "baseline is source-backed",
    "synthetic gain is physical",
    "phygn predicts",
    "template_not_evidence",
]

_SUPPORT_TYPE_RE = re.compile(r"support type\s*:\s*(\S+)", re.IGNORECASE)
_CLAIM_TARGET_RE = re.compile(r"claim target\s*:\s*(\S+)", re.IGNORECASE)
_LOCAL_REF_RE = re.compile(r"local reference\s*:", re.IGNORECASE)
_AUDIT_NOTES_RE = re.compile(r"audit notes\s*:", re.IGNORECASE)
_HEADER_RE = re.compile(r"^#\s+extracts\s+[—\-–]\s+\S+", re.IGNORECASE | re.MULTILINE)


# ── Models ─────────────────────────────────────────────────────────────────

class ExtractValidationResult(BaseModel):
    extract_path: str
    valid: bool = False
    has_source_header: bool = False
    support_types_found: list[str] = Field(default_factory=list)
    invalid_support_types: list[str] = Field(default_factory=list)
    has_claim_target: bool = False
    has_local_reference: bool = False
    has_audit_notes: bool = False
    forbidden_phrases_found: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)
    report_path: str = ""


# ── Core function ──────────────────────────────────────────────────────────

def validate_extract_file(path: Path) -> ExtractValidationResult:
    """
    Validate a single extract .md file against the extract protocol.
    """
    ev = ExtractValidationResult(extract_path=str(path))

    if not path.exists():
        ev.issues.append("File does not exist.")
        return ev

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        ev.issues.append(f"Cannot read file: {exc}")
        return ev

    text_lower = text.lower()

    # 1. Source header check: "# Extracts — SOURCE_ID"
    ev.has_source_header = bool(_HEADER_RE.search(text))
    if not ev.has_source_header:
        ev.issues.append("Missing '# Extracts — <SOURCE_ID>' header.")

    # 2. Support types
    found_tags = _SUPPORT_TYPE_RE.findall(text)
    ev.support_types_found = list({t.strip().upper() for t in found_tags})
    invalid = [t for t in ev.support_types_found if t not in ALLOWED_SUPPORT_TAGS]
    ev.invalid_support_types = invalid
    if not ev.support_types_found:
        ev.issues.append("No 'Support type:' tag found.")
    if invalid:
        ev.issues.append(f"Invalid support types: {invalid}")

    # 3. Claim target
    ev.has_claim_target = bool(_CLAIM_TARGET_RE.search(text))
    if not ev.has_claim_target:
        ev.issues.append("No 'Claim target:' field found.")

    # 4. Local reference
    ev.has_local_reference = bool(_LOCAL_REF_RE.search(text))
    if not ev.has_local_reference:
        ev.issues.append("No 'Local reference:' field found.")

    # 5. Audit notes
    ev.has_audit_notes = bool(_AUDIT_NOTES_RE.search(text))
    if not ev.has_audit_notes:
        ev.issues.append("No 'Audit notes:' section found.")

    # 6. Forbidden phrases
    triggered = [phrase for phrase in FORBIDDEN_PHRASES if phrase in text_lower]
    ev.forbidden_phrases_found = triggered
    if triggered:
        ev.issues.append(f"Forbidden overclaim phrases found: {triggered}")

    # Determine validity
    ev.valid = (
        ev.has_source_header
        and bool(ev.support_types_found)
        and not ev.invalid_support_types
        and ev.has_claim_target
        and ev.has_local_reference
        and ev.has_audit_notes
        and not ev.forbidden_phrases_found
    )

    return ev


def validate_extract_folder(
    extracts_dir: Path,
) -> list[ExtractValidationResult]:
    """Validate all .md files in the extracts directory."""
    if not extracts_dir.exists():
        return []
    results = []
    for f in sorted(extracts_dir.glob("*.md")):
        results.append(validate_extract_file(f))
    return results


# ── Report writer ──────────────────────────────────────────────────────────

def write_extract_support_tags_report(
    results: list[ExtractValidationResult],
    project_root: Path,
) -> Path:
    out_dir = project_root / "reports" / "rag"
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / "extract_support_tags_v1_1.md"

    valid_count = sum(1 for r in results if r.valid)
    lines = [
        "# Extract Support Tags Validation — v1.1",
        "",
        f"- **Extracts validated**: {len(results)}",
        f"- **Valid**: {valid_count}",
        f"- **Invalid**: {len(results) - valid_count}",
        "",
        "## Results",
        "",
        "| File | Valid | Support Types | Forbidden | Issues |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        fname = Path(r.extract_path).name
        tags = ", ".join(r.support_types_found) or "—"
        forbidden = ", ".join(r.forbidden_phrases_found) or "—"
        issues = "; ".join(r.issues) or "—"
        lines.append(f"| {fname} | {r.valid} | {tags} | {forbidden} | {issues} |")

    if not results:
        lines.append("| — | — | No extracts found. | — | — |")

    lines += [
        "",
        "## Discipline Note",
        "",
        "A tagged extract is a legal argument. A vague source is just noise.",
        "FORMULA_SUPPORT + OBSERVABLE_SUPPORT + PASSED_LIMITED → possible BASELINE_SOURCE_BACKED_LIMITED.",
        "CONTEXT_SUPPORT alone → no upgrade.",
    ]

    p.write_text("\n".join(lines), encoding="utf-8")
    return p
