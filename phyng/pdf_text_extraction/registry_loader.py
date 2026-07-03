"""Load and enforce the v3.6 hashed local-source boundary."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.pdf_text_extraction.schemas import RegisteredPDFSource


REGISTRY_PATHS = {
    "local_text_registry": Path("data/real_sources/local_text_registry_v3_6.json"),
    "source_file_manifest": Path("data/real_sources/source_file_manifest_v3_6.json"),
    "source_hashes": Path("data/real_sources/source_hashes_v3_6.json"),
    "source_availability": Path("data/real_sources/source_availability_v3_6.json"),
}


def load_hashed_pdf_sources(root: str | Path = ".") -> tuple[list[RegisteredPDFSource], str | None, str | None]:
    repo_root = Path(root)
    missing = [str(path) for path in REGISTRY_PATHS.values() if not (repo_root / path).exists()]
    if missing:
        return [], None, "PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_REGISTRY_MISSING"

    registry = _load_json(repo_root / REGISTRY_PATHS["local_text_registry"])
    file_manifest = _load_json(repo_root / REGISTRY_PATHS["source_file_manifest"])
    hash_manifest = _load_json(repo_root / REGISTRY_PATHS["source_hashes"])
    hash_by_source = {item["source_id"]: item for item in hash_manifest.get("hashes", [])}
    pdf_root = (repo_root / "data/real_sources/pdfs").resolve()

    sources: list[RegisteredPDFSource] = []
    for record in file_manifest.get("source_files", []):
        source_id = record.get("source_id")
        hash_record = hash_by_source.get(source_id)
        if not hash_record:
            continue
        local_path = record.get("local_path") or hash_record.get("local_path")
        resolved_path = (repo_root / local_path).resolve()
        if not _is_inside(resolved_path, pdf_root):
            continue
        if not record.get("exists"):
            continue
        if not record.get("sha256") or record.get("sha256") != hash_record.get("sha256"):
            continue
        file_type = (record.get("file_type") or "").lower()
        if file_type not in {".pdf", ".txt", ".md", ".html"}:
            continue
        sources.append(
            RegisteredPDFSource(
                source_id=source_id,
                local_path=local_path,
                sha256=record["sha256"],
                size_bytes=int(record.get("size_bytes") or hash_record.get("size_bytes") or 0),
                file_type=file_type,
            )
        )
    blocked_reason = "PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_NO_HASHED_FILES" if not sources else None
    return sources, registry.get("registry_id"), blocked_reason


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False
