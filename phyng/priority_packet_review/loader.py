"""Load v3.8.3 priority packet review inputs."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.priority_packet_review.schemas import PriorityPacketReviewInputs
from phyng.semantic_triage.schemas import PriorityReviewItem, SemanticTriageRecord


INPUT_PATHS = {
    "triage_map": Path("data/real_sources/extracts/phi_gradient_semantic_triage_map_v3_8_2.json"),
    "priority_packet": Path("data/real_sources/extracts/phi_gradient_priority_review_packet_v3_8_2.json"),
    "slot_review_queues": Path("data/real_sources/extracts/phi_gradient_slot_review_queues_v3_8_2.json"),
    "next_gate_readiness": Path("data/real_sources/extracts/phi_gradient_v3_8_2_next_gate_readiness.json"),
    "pdf_text_extraction": Path("data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json"),
    "extraction_manifest": Path("data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json"),
    "source_hashes": Path("data/real_sources/source_hashes_v3_6.json"),
}


def load_priority_packet_review_inputs(root: str | Path = ".") -> PriorityPacketReviewInputs:
    repo_root = Path(root)
    missing = [str(path) for path in INPUT_PATHS.values() if not (repo_root / path).exists()]
    if missing:
        return PriorityPacketReviewInputs(blocked_reason="PHI_GRADIENT_PRIORITY_PACKET_REVIEW_BLOCKED_MISSING_INPUTS")
    triage_map = _load_json(repo_root / INPUT_PATHS["triage_map"])
    priority_packet = _load_json(repo_root / INPUT_PATHS["priority_packet"])
    return PriorityPacketReviewInputs(
        triage_records=[SemanticTriageRecord(**item) for item in triage_map.get("triage_records", [])],
        priority_packet=[PriorityReviewItem(**item) for item in priority_packet.get("priority_review_packet", [])],
        slot_review_queues=_load_json(repo_root / INPUT_PATHS["slot_review_queues"]),
        next_gate_readiness=_load_json(repo_root / INPUT_PATHS["next_gate_readiness"]),
        pdf_text_extraction=_load_json(repo_root / INPUT_PATHS["pdf_text_extraction"]),
        extraction_manifest=_load_json(repo_root / INPUT_PATHS["extraction_manifest"]),
        source_hashes=_load_json(repo_root / INPUT_PATHS["source_hashes"]),
    )


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
