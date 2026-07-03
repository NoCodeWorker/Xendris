from __future__ import annotations

import json
from pathlib import Path

from phyng.extract_candidate_review.loader import load_v3_7_review_inputs


def test_missing_candidate_files_blocks_review(tmp_path: Path) -> None:
    candidates, manifest, hashes, blocked_reason = load_v3_7_review_inputs(tmp_path)

    assert candidates == []
    assert manifest == {}
    assert hashes == {}
    assert blocked_reason == "PHI_GRADIENT_EXTRACT_REVIEW_BLOCKED_MISSING_CANDIDATES"


def write_minimal_v3_8_inputs(tmp_path: Path, candidates: list[dict] | None = None, blocked_pedernales: bool = False) -> None:
    root = tmp_path / "data" / "real_sources"
    extracts = root / "extracts"
    extracts.mkdir(parents=True, exist_ok=True)
    source_hashes = {
        "manifest_id": "PHI-GRADIENT-SOURCE-HASHES-v3_6",
        "hashes": [
            {
                "source_id": "SRC-TEST",
                "local_path": "data/real_sources/pdfs/source.pdf",
                "sha256": "abc123",
                "size_bytes": 100,
                "file_type": ".pdf",
            },
            {
                "source_id": "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING",
                "local_path": "data/real_sources/pdfs/Pedernales_2019_Motional_Dynamical_Decoupling.pdf",
                "sha256": "ped123",
                "size_bytes": 100,
                "file_type": ".pdf",
            },
        ],
    }
    (root / "source_hashes_v3_6.json").write_text(json.dumps(source_hashes), encoding="utf-8")
    summaries = []
    if blocked_pedernales:
        summaries.append(
            {
                "source_id": "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING",
                "extraction_status": "EXTRACTION_REQUIRES_PDF_READER_OR_MANUAL_REVIEW",
                "blocked_reason": "blocked",
            }
        )
    (extracts / "phi_gradient_pdf_extraction_manifest_v3_7.json").write_text(
        json.dumps({"manifest_id": "PHI-GRADIENT-PDF-EXTRACTION-MANIFEST-v3_7", "source_summaries": summaries}),
        encoding="utf-8",
    )
    (extracts / "phi_gradient_pdf_text_extraction_v3_7.json").write_text(json.dumps({"pages": []}), encoding="utf-8")
    candidate_payload = {"candidates": candidates or []}
    for name in (
        "phi_gradient_pdf_quote_candidates_v3_7.json",
        "phi_gradient_pdf_equation_candidates_v3_7.json",
        "phi_gradient_pdf_table_range_candidates_v3_7.json",
        "phi_gradient_pdf_negative_constraint_candidates_v3_7.json",
    ):
        (extracts / name).write_text(json.dumps(candidate_payload if name.startswith("phi_gradient_pdf_quote") else {"candidates": []}), encoding="utf-8")


def raw_candidate(**overrides: object) -> dict:
    payload = {
        "candidate_id": "CAND-1",
        "source_id": "SRC-TEST",
        "sha256": "abc123",
        "page_number": 1,
        "location_type": "PAGE_TEXT",
        "location_value": "page=1; candidate_index=1",
        "candidate_type": "QUOTE_CANDIDATE",
        "extracted_text": "The experiment reports visibility decoherence in a matter-wave interferometer.",
        "normalized_text": "the experiment reports visibility decoherence in a matter-wave interferometer.",
        "confidence": "MEDIUM",
        "requires_manual_review": False,
        "notes": [],
    }
    payload.update(overrides)
    return payload
