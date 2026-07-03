from __future__ import annotations

import json
from pathlib import Path

from phyng.semantic_triage.loader import load_semantic_triage_inputs


def test_missing_inputs_block_triage(tmp_path: Path) -> None:
    inputs = load_semantic_triage_inputs(tmp_path)

    assert inputs.blocked_reason == "PHI_GRADIENT_SEMANTIC_TRIAGE_BLOCKED_MISSING_INPUTS"
    assert inputs.candidates == []


def write_minimal_v3_8_2_inputs(tmp_path: Path, candidates: list[dict] | None = None, validation_ready_count: int = 0) -> None:
    root = tmp_path / "data" / "real_sources"
    extracts = root / "extracts"
    extracts.mkdir(parents=True, exist_ok=True)
    hashes = [
        _hash("SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE", "h1"),
        _hash("SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE", "h2"),
        _hash("SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST", "h3"),
        _hash("SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS", "h4"),
        _hash("SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING", "h5"),
        _hash("SRC-TEST", "abc123"),
    ]
    (root / "source_hashes_v3_6.json").write_text(json.dumps({"hashes": hashes}), encoding="utf-8")
    (extracts / "phi_gradient_pdf_text_extraction_v3_7.json").write_text(json.dumps({"pages": []}), encoding="utf-8")
    (extracts / "phi_gradient_pdf_extraction_manifest_v3_7.json").write_text(json.dumps({"source_summaries": []}), encoding="utf-8")
    payload_by_file = {
        "phi_gradient_pdf_quote_candidates_v3_7.json": {"candidates": candidates or []},
        "phi_gradient_pdf_equation_candidates_v3_7.json": {"candidates": []},
        "phi_gradient_pdf_table_range_candidates_v3_7.json": {"candidates": []},
        "phi_gradient_pdf_negative_constraint_candidates_v3_7.json": {"candidates": []},
    }
    for name, payload in payload_by_file.items():
        (extracts / name).write_text(json.dumps(payload), encoding="utf-8")
    (extracts / "phi_gradient_manual_review_queue_v3_8.json").write_text(json.dumps({"manual_review_queue": []}), encoding="utf-8")
    (extracts / "phi_gradient_rejected_extraction_candidates_v3_8.json").write_text(json.dumps({"rejected_candidates": []}), encoding="utf-8")
    (extracts / "phi_gradient_reviewed_candidate_map_v3_8.json").write_text(json.dumps({"reviewed_candidate_map": []}), encoding="utf-8")
    (extracts / "phi_gradient_validation_ready_extract_pack_v3_8.json").write_text(
        json.dumps({"extracts": [], "validation_ready_count": validation_ready_count}),
        encoding="utf-8",
    )


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
        "requires_manual_review": True,
        "notes": [],
    }
    payload.update(overrides)
    return payload


def _hash(source_id: str, sha256: str) -> dict:
    return {
        "source_id": source_id,
        "local_path": f"data/real_sources/pdfs/{source_id}.pdf",
        "sha256": sha256,
        "size_bytes": 100,
        "file_type": ".pdf",
    }
