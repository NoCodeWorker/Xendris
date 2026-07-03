from __future__ import annotations

import hashlib
import json
from pathlib import Path

from phyng.pdf_text_extraction.registry_loader import load_hashed_pdf_sources


def test_registry_required_for_extraction(tmp_path: Path) -> None:
    sources, registry_id, blocked_reason = load_hashed_pdf_sources(tmp_path)

    assert sources == []
    assert registry_id is None
    assert blocked_reason == "PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_REGISTRY_MISSING"


def test_unhashed_file_is_not_extracted(tmp_path: Path) -> None:
    _write_registry(tmp_path, sha256=None, exists=True)

    sources, _, blocked_reason = load_hashed_pdf_sources(tmp_path)

    assert sources == []
    assert blocked_reason == "PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_NO_HASHED_FILES"


def test_missing_files_block_extraction(tmp_path: Path) -> None:
    _write_registry(tmp_path, sha256="abc123", exists=False)

    sources, _, blocked_reason = load_hashed_pdf_sources(tmp_path)

    assert sources == []
    assert blocked_reason == "PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_NO_HASHED_FILES"


def test_hashed_pdf_can_be_queued_for_extraction(tmp_path: Path) -> None:
    pdf_path = tmp_path / "data" / "real_sources" / "pdfs" / "source.pdf"
    pdf_path.parent.mkdir(parents=True)
    pdf_path.write_bytes(b"%PDF-1.4\n")
    sha256 = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    _write_registry(tmp_path, sha256=sha256, exists=True, size_bytes=pdf_path.stat().st_size)

    sources, registry_id, blocked_reason = load_hashed_pdf_sources(tmp_path)

    assert registry_id == "PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6"
    assert blocked_reason is None
    assert len(sources) == 1
    assert sources[0].sha256 == sha256


def _write_registry(tmp_path: Path, sha256: str | None, exists: bool, size_bytes: int = 10) -> None:
    root = tmp_path / "data" / "real_sources"
    root.mkdir(parents=True, exist_ok=True)
    record = {
        "source_id": "SRC-TEST",
        "canonical_filename": "source.pdf",
        "local_path": "data/real_sources/pdfs/source.pdf",
        "exists": exists,
        "file_type": ".pdf",
        "size_bytes": size_bytes if exists else None,
        "sha256": sha256,
        "text_extractable": None,
        "registry_status": "LOCAL_SOURCE_FILE_HASHED" if sha256 else "LOCAL_SOURCE_FILE_REQUIRES_MANUAL_DOWNLOAD",
        "notes": [],
    }
    (root / "local_text_registry_v3_6.json").write_text(
        json.dumps({"registry_id": "PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6", "source_records": [record]}),
        encoding="utf-8",
    )
    (root / "source_file_manifest_v3_6.json").write_text(json.dumps({"source_files": [record]}), encoding="utf-8")
    (root / "source_hashes_v3_6.json").write_text(
        json.dumps({"hashes": [{"source_id": "SRC-TEST", "local_path": record["local_path"], "sha256": sha256, "size_bytes": size_bytes, "file_type": ".pdf"}] if sha256 else []}),
        encoding="utf-8",
    )
    (root / "source_availability_v3_6.json").write_text(json.dumps({"availability": []}), encoding="utf-8")
