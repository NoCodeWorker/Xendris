"""Artifact scanner for v4.4.1 audit scope."""

from __future__ import annotations

from pathlib import Path

from phyng.full_suite_logic_audit.schemas import ArtifactScanResult, AuditArtifact


AUDIT_SCOPE = [
    "docs",
    "reports",
    "data",
    "tests",
    "phyng/core",
    "phyng/source_pressure",
    "phyng/real_source_ingestion",
    "phyng/exact_extract_review",
    "phyng/priority_exact_fill",
    "phyng/pdf_text_extraction",
    "phyng/extract_candidate_review",
    "phyng/semantic_triage",
    "phyng/priority_packet_review",
    "phyng/source_pressure_decision",
    "phyng/benchmark_construction",
    "phyng/scientific_debt",
    "phyng/model_comparison",
    "phyng/observable_dataset",
    "phyng/ytrue_extraction",
    "phyng/manual_data_extraction",
    "phyng/campaigns",
]

SUPPORTED_SUFFIXES = {".py", ".md", ".json", ".txt"}


def scan_artifacts(root: str | Path = ".", scope: list[str] | None = None) -> ArtifactScanResult:
    repo_root = Path(root)
    scanned_paths: list[str] = []
    missing_scope_paths: list[str] = []
    artifacts: list[AuditArtifact] = []
    for scope_path in scope or AUDIT_SCOPE:
        absolute = repo_root / scope_path
        if not absolute.exists():
            missing_scope_paths.append(scope_path)
            continue
        if absolute.is_file():
            candidates = [absolute]
        else:
            candidates = [path for path in absolute.rglob("*") if path.is_file()]
        for path in candidates:
            if "__pycache__" in path.parts or path.suffix.lower() not in SUPPORTED_SUFFIXES:
                continue
            rel = path.relative_to(repo_root).as_posix()
            if rel.startswith("data/audits/") or rel.startswith("reports/audits/"):
                continue
            scanned_paths.append(rel)
            artifacts.append(AuditArtifact(path=rel, artifact_type=path.suffix.lower().lstrip(".")))
    return ArtifactScanResult(scanned_paths=sorted(scanned_paths), missing_scope_paths=missing_scope_paths, artifacts=artifacts)
