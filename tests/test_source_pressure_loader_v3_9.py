"""Tests for v3.9 source pressure loader."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.source_pressure_decision.loader import load_source_pressure_inputs


def test_missing_validation_ready_pack_blocks_pressure_gate(tmp_path: Path) -> None:
    inputs = load_source_pressure_inputs(tmp_path)

    assert inputs.blocked_reason == "PHI_GRADIENT_SOURCE_PRESSURE_BLOCKED_MISSING_VALIDATION_READY_PACK"


def test_loads_all_inputs(tmp_path: Path) -> None:
    write_minimal_v3_9_inputs(tmp_path)

    inputs = load_source_pressure_inputs(tmp_path)

    assert inputs.blocked_reason is None
    assert "extracts" in inputs.validation_ready_pack
    assert "hashes" in inputs.source_hashes


# --- Helpers ---

def write_minimal_v3_9_inputs(
    tmp_path: Path,
    extracts: list[dict] | None = None,
    *,
    include_slot4: bool = False,
    include_negative: bool = False,
) -> None:
    root = tmp_path / "data" / "real_sources"
    extracts_dir = root / "extracts"
    extracts_dir.mkdir(parents=True, exist_ok=True)
    hashes = [
        _hash("SRC-TEST-BASELINE", "abc123"),
        _hash("SRC-TEST-OBSERVABLE", "def456"),
        _hash("SRC-TEST-BENCHMARK", "ghi789"),
        _hash("SRC-TEST-GRADIENT", "jkl012"),
        _hash("SRC-TEST-CONSTRAINT", "mno345"),
        _hash("SRC-TEST-NEGATIVE", "pqr678"),
    ]
    (root / "source_hashes_v3_6.json").write_text(json.dumps({"hashes": hashes}), encoding="utf-8")
    if extracts is None:
        extracts = [
            _extract("VRX-001", "SRC-TEST-BASELINE", "abc123", "SLOT_1_DECOHERENCE_BASELINE",
                     "DECOHERENCE_BASELINE", "BASELINE_CANDIDATE",
                     "The experiment reports thermal decoherence as the primary loss of coherence mechanism."),
            _extract("VRX-002", "SRC-TEST-OBSERVABLE", "def456", "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE",
                     "VISIBILITY_COHERENCE_OBSERVABLE", "SUPPORT_CANDIDATE",
                     "Interference visibility was measured at 42 percent loss under environmental decoherence conditions."),
            _extract("VRX-003", "SRC-TEST-BENCHMARK", "ghi789", "SLOT_3_BENCHMARK_RANGES",
                     "BENCHMARK_RANGE", "BENCHMARK_CANDIDATE",
                     "The mass range of 500-2000 amu at temperatures below 1000 K and pressure of 1e-8 mbar defines the benchmark regime."),
            _extract("VRX-004", "SRC-TEST-CONSTRAINT", "mno345", "SLOT_5_PARAMETER_CONSTRAINTS",
                     "PARAMETER_CONSTRAINT", "PARAMETER_CONSTRAINT_CANDIDATE",
                     "CSL collapse model bounds constrain lambda to less than 1e-8 and r_c hypothesis testing."),
        ]
        if include_slot4:
            extracts.append(
                _extract("VRX-005", "SRC-TEST-GRADIENT", "jkl012", "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS",
                         "GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS", "SUPPORT_CANDIDATE",
                         "The gradient of the motional Hamiltonian governs spin-motion coupling in the transition effective dynamics regime.")
            )
        if include_negative:
            extracts.append(
                _extract("VRX-006", "SRC-TEST-NEGATIVE", "pqr678", "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS",
                         "NEGATIVE_CONSTRAINT_LIMITATION", "CONTRADICTION_CANDIDATE",
                         "Environmental noise dominates over any candidate gradient effect making it incompatible with the observed regime.")
            )
    (extracts_dir / "phi_gradient_validation_ready_extract_pack_v3_8_3.json").write_text(
        json.dumps({"extracts": extracts, "validation_ready_count": len(extracts), "status": "PHI_GRADIENT_PRIORITY_PACKET_REVIEW_READY_FOR_SOURCE_PRESSURE", "ready_for_v3_9": True}),
        encoding="utf-8",
    )
    (extracts_dir / "phi_gradient_priority_packet_review_decisions_v3_8_3.json").write_text(
        json.dumps({"review_decisions": [], "decision_count": 0}), encoding="utf-8",
    )
    (extracts_dir / "phi_gradient_analogy_only_items_v3_8_3.json").write_text(
        json.dumps({"analogy_only_items": [], "analogy_only_count": 0}), encoding="utf-8",
    )
    (extracts_dir / "phi_gradient_manual_review_queue_v3_8_3.json").write_text(
        json.dumps({"manual_review_queue": [], "manual_review_count": 0}), encoding="utf-8",
    )
    (extracts_dir / "phi_gradient_v3_8_3_next_source_pressure_inputs.json").write_text(
        json.dumps({"ready_for_v3_9": True, "validation_ready_count": len(extracts)}), encoding="utf-8",
    )


def _extract(
    extract_id: str,
    source_id: str,
    sha256: str,
    slot: str,
    role: str,
    direction: str,
    text: str,
    page: int = 1,
) -> dict:
    return {
        "extract_id": extract_id,
        "source_id": source_id,
        "sha256": sha256,
        "page_number": page,
        "assigned_slot": slot,
        "component_role": role,
        "exact_text": text,
        "source_candidate_id": f"CAND-{extract_id}",
        "location_type": "PAGE_TEXT",
        "location_value": f"page={page}",
        "promotion_decision": "PROMOTE_VALIDATION_READY",
        "why_promoted": "test extract",
        "limitations": ["Validation-ready only; v3.8.3 does not grant source support."],
        "possible_pressure_direction": direction,
        "validation_questions": [],
        "next_gate_required": "v3.9 source-pressure decision gate",
    }


def _hash(source_id: str, sha256: str) -> dict:
    return {
        "source_id": source_id,
        "local_path": f"data/real_sources/pdfs/{source_id}.pdf",
        "sha256": sha256,
        "size_bytes": 100,
        "file_type": ".pdf",
    }
