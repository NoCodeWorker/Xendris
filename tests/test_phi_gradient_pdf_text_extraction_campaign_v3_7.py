from __future__ import annotations

import hashlib
import json
from pathlib import Path

from phyng.core.compatibility import normalize_status
from phyng.pdf_text_extraction.campaign import run_phi_gradient_pdf_text_extraction_campaign


def test_campaign_generates_outputs(tmp_path: Path) -> None:
    _write_ready_registry_with_pdf(tmp_path, "Visibility decoherence rate equals lambda for 10 amu. Thermal scattering is negligible.")

    result = run_phi_gradient_pdf_text_extraction_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_PDF_EXTRACTION_COMPLETED"
    assert result.extraction_result.manifest.hashed_sources_seen == 1
    assert result.extraction_result.manifest.sources_extracted == 1
    assert result.extraction_result.manifest.total_candidates > 0
    for path in result.extraction_result.output_paths.values():
        assert (tmp_path / path).exists()


def test_existing_v3_6_behavior_preserved() -> None:
    record = normalize_status("PHI_GRADIENT_LOCAL_SOURCE_FILES_READY", domain="local_source_text")

    assert record.domain_status == "PHI_GRADIENT_LOCAL_SOURCE_FILES_READY"
    assert record.canonical_permission.value == "REVIEW_REQUIRED"
    assert "Physical prediction" in record.blocked_uses


def _write_ready_registry_with_pdf(tmp_path: Path, text: str) -> None:
    pdf_path = tmp_path / "data" / "real_sources" / "pdfs" / "source.pdf"
    pdf_path.parent.mkdir(parents=True)
    pdf_path.write_bytes(_minimal_pdf_with_text(text))
    sha256 = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    root = tmp_path / "data" / "real_sources"
    record = {
        "source_id": "SRC-TEST",
        "canonical_filename": "source.pdf",
        "local_path": "data/real_sources/pdfs/source.pdf",
        "exists": True,
        "file_type": ".pdf",
        "size_bytes": pdf_path.stat().st_size,
        "sha256": sha256,
        "text_extractable": None,
        "registry_status": "LOCAL_SOURCE_FILE_HASHED",
        "notes": [],
    }
    (root / "local_text_registry_v3_6.json").write_text(
        json.dumps({"registry_id": "PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6", "source_records": [record]}),
        encoding="utf-8",
    )
    (root / "source_file_manifest_v3_6.json").write_text(json.dumps({"source_files": [record]}), encoding="utf-8")
    (root / "source_hashes_v3_6.json").write_text(
        json.dumps({"hashes": [{"source_id": "SRC-TEST", "local_path": record["local_path"], "sha256": sha256, "size_bytes": pdf_path.stat().st_size, "file_type": ".pdf"}]}),
        encoding="utf-8",
    )
    (root / "source_availability_v3_6.json").write_text(json.dumps({"availability": []}), encoding="utf-8")


def _minimal_pdf_with_text(text: str) -> bytes:
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET"
    return f"""%PDF-1.4
1 0 obj
<< /Length {len(stream)} >>
stream
{stream}
endstream
endobj
%%EOF
""".encode("latin-1")
