from __future__ import annotations

import json
from pathlib import Path

from phyng.priority_packet_review.loader import load_priority_packet_review_inputs


def test_missing_inputs_block_priority_packet_review(tmp_path: Path) -> None:
    inputs = load_priority_packet_review_inputs(tmp_path)

    assert inputs.blocked_reason == "PHI_GRADIENT_PRIORITY_PACKET_REVIEW_BLOCKED_MISSING_INPUTS"


def write_minimal_v3_8_3_inputs(tmp_path: Path, triage_records: list[dict], packet_items: list[dict] | None = None) -> None:
    root = tmp_path / "data" / "real_sources"
    extracts = root / "extracts"
    extracts.mkdir(parents=True, exist_ok=True)
    hashes = [
        _hash("SRC-TEST", "abc123"),
        _hash("SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING", "ped123"),
    ]
    (root / "source_hashes_v3_6.json").write_text(json.dumps({"hashes": hashes}), encoding="utf-8")
    (extracts / "phi_gradient_semantic_triage_map_v3_8_2.json").write_text(
        json.dumps({"triage_records": triage_records, "triage_count": len(triage_records)}),
        encoding="utf-8",
    )
    packet = packet_items if packet_items is not None else [_packet_from_record(record, index + 1) for index, record in enumerate(triage_records[:1])]
    (extracts / "phi_gradient_priority_review_packet_v3_8_2.json").write_text(
        json.dumps({"priority_review_packet": packet, "packet_count": len(packet)}),
        encoding="utf-8",
    )
    (extracts / "phi_gradient_slot_review_queues_v3_8_2.json").write_text(json.dumps({"slot_review_queues": []}), encoding="utf-8")
    (extracts / "phi_gradient_v3_8_2_next_gate_readiness.json").write_text(json.dumps({"ready_for_v3_9": False}), encoding="utf-8")
    (extracts / "phi_gradient_pdf_text_extraction_v3_7.json").write_text(json.dumps({"pages": []}), encoding="utf-8")
    (extracts / "phi_gradient_pdf_extraction_manifest_v3_7.json").write_text(json.dumps({"source_summaries": []}), encoding="utf-8")


def triage_record(**overrides: object) -> dict:
    payload = {
        "candidate_id": "CAND-1",
        "source_id": "SRC-TEST",
        "sha256": "abc123",
        "page_number": 1,
        "candidate_type": "QUOTE_CANDIDATE",
        "extracted_text": "The experiment reports interference visibility loss caused by environmental decoherence.",
        "normalized_text": "the experiment reports interference visibility loss caused by environmental decoherence.",
        "assigned_slot": "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE",
        "semantic_score": 1.0,
        "source_priority_score": 0.8,
        "slot_relevance_score": 1.0,
        "cleanliness_score": 1.0,
        "specificity_score": 0.5,
        "risk_score": 0.4,
        "triage_score": 0.8,
        "priority": "HIGH",
        "include_in_priority_packet": True,
        "review_question": "review?",
        "decision_needed": "decide",
        "notes": [],
    }
    payload.update(overrides)
    return payload


def _packet_from_record(record: dict, index: int) -> dict:
    return {
        "review_item_id": f"TRIAGE-v3_8_2-{index:03d}",
        "candidate_id": record["candidate_id"],
        "source_id": record["source_id"],
        "page_number": record.get("page_number"),
        "assigned_slot": record["assigned_slot"],
        "priority": record["priority"],
        "exact_text_or_preview": record["extracted_text"],
        "why_relevant": "test",
        "review_question": record["review_question"],
        "decision_needed": record["decision_needed"],
        "possible_outcomes": ["VALIDATION_READY_EXTRACT"],
        "next_gate_impact": "v3.8.3 review",
    }


def _hash(source_id: str, sha256: str) -> dict:
    return {
        "source_id": source_id,
        "local_path": f"data/real_sources/pdfs/{source_id}.pdf",
        "sha256": sha256,
        "size_bytes": 100,
        "file_type": ".pdf",
    }
