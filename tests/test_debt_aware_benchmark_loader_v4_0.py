"""Tests for v4.0 debt-aware benchmark loader."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.benchmark_construction.loader import load_benchmark_construction_inputs


def test_missing_source_pressure_blocks_benchmark(tmp_path: Path) -> None:
    inputs = load_benchmark_construction_inputs(tmp_path)
    assert inputs.blocked_reason == "PHI_GRADIENT_BENCHMARK_BLOCKED_MISSING_SOURCE_PRESSURE"


def test_loader_loads_all_inputs(tmp_path: Path) -> None:
    write_minimal_v4_0_inputs(tmp_path)
    inputs = load_benchmark_construction_inputs(tmp_path)
    assert inputs.blocked_reason is None
    assert "extract_pressure_records" in inputs.extract_pressure_map


def write_minimal_v4_0_inputs(
    tmp_path: Path,
    records: list[dict] | None = None,
) -> None:
    sp_dir = tmp_path / "data" / "real_sources" / "source_pressure"
    ext_dir = tmp_path / "data" / "real_sources" / "extracts"

    sp_dir.mkdir(parents=True, exist_ok=True)
    ext_dir.mkdir(parents=True, exist_ok=True)

    if records is None:
        records = [
            {
                "extract_id": "VRX-001",
                "source_id": "SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS",
                "sha256": "abc123",
                "page_number": 1,
                "assigned_slot": "SLOT_1_DECOHERENCE_BASELINE",
                "component_role": "DECOHERENCE_BASELINE",
                "exact_text": "thermal emission and gas scattering cause decoherence",
                "pressure_class": "SUPPORTS_BASELINE_ONLY",
                "pressure_direction": "BASELINE_CANDIDATE",
                "pressure_score": 0.3,
                "confidence": "LOW",
                "reasoning": "test baseline",
                "limitations": ["baseline limits"],
            },
            {
                "extract_id": "VRX-002",
                "source_id": "SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST",
                "sha256": "def456",
                "page_number": 2,
                "assigned_slot": "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE",
                "component_role": "VISIBILITY_COHERENCE_OBSERVABLE",
                "exact_text": "measured interference visibility loss is 0.45",
                "pressure_class": "SUPPORTS_OBSERVABLE_ONLY",
                "pressure_direction": "SUPPORT_CANDIDATE",
                "pressure_score": 0.4,
                "confidence": "LOW",
                "reasoning": "test visibility",
                "limitations": ["visibility limits"],
            },
            {
                "extract_id": "VRX-003",
                "source_id": "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING",
                "sha256": "ghi789",
                "page_number": 3,
                "assigned_slot": "SLOT_3_BENCHMARK_RANGES",
                "component_role": "BENCHMARK_RANGE",
                "exact_text": "mass range of 1000 amu at 1e-8 mbar",
                "pressure_class": "SUPPORTS_BENCHMARK_ALIGNMENT",
                "pressure_direction": "BENCHMARK_CANDIDATE",
                "pressure_score": 0.5,
                "confidence": "LOW",
                "reasoning": "test benchmark",
                "limitations": ["benchmark limits"],
            },
            {
                "extract_id": "VRX-004",
                "source_id": "SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS",
                "sha256": "abc123",
                "page_number": 4,
                "assigned_slot": "SLOT_5_PARAMETER_CONSTRAINTS",
                "component_role": "PARAMETER_CONSTRAINT",
                "exact_text": "bounds collapse lambda parameter",
                "pressure_class": "SUPPORTS_PARAMETER_CONSTRAINT",
                "pressure_direction": "PARAMETER_CONSTRAINT_CANDIDATE",
                "pressure_score": 0.4,
                "confidence": "LOW",
                "reasoning": "test parameters",
                "limitations": ["parameter limits"],
            },
            {
                "extract_id": "VRX-005",
                "source_id": "SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST",
                "sha256": "def456",
                "page_number": 5,
                "assigned_slot": "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS",
                "component_role": "NEGATIVE_CONSTRAINT_LIMITATION",
                "exact_text": "environmental noise dominates over candidate signal",
                "pressure_class": "LIMITS_COMPONENT",
                "pressure_direction": "CONTRADICTION_CANDIDATE",
                "pressure_score": -0.5,
                "confidence": "MEDIUM",
                "reasoning": "test limitation",
                "limitations": ["limitation limits"],
            },
        ]

    # Write source pressure files
    (sp_dir / "phi_gradient_source_pressure_decision_v3_9.json").write_text(
        json.dumps({"primary_decision": "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED", "decision_id": "PHI-GRADIENT-v3_9"}), encoding="utf-8"
    )
    (sp_dir / "phi_gradient_extract_pressure_map_v3_9.json").write_text(
        json.dumps({"extract_pressure_records": records, "extract_count": len(records)}), encoding="utf-8"
    )
    (sp_dir / "phi_gradient_slot_pressure_summary_v3_9.json").write_text(
        json.dumps({"slot_pressure_summary": []}), encoding="utf-8"
    )
    (sp_dir / "phi_gradient_benchmark_alignment_v3_9.json").write_text(
        json.dumps({"benchmark_decision": "BENCHMARK_WITH_RANGE"}), encoding="utf-8"
    )
    (sp_dir / "phi_gradient_contradiction_and_limitation_map_v3_9.json").write_text(
        json.dumps({"contradictions": [], "limitations": []}), encoding="utf-8"
    )
    (sp_dir / "phi_gradient_next_model_update_recommendations_v3_9.json").write_text(
        json.dumps({"recommendations": []}), encoding="utf-8"
    )

    # Write extracts & hashes
    (ext_dir / "phi_gradient_validation_ready_extract_pack_v3_8_3.json").write_text(
        json.dumps({"extracts": [], "validation_ready_count": 0}), encoding="utf-8"
    )
    (tmp_path / "data" / "real_sources" / "source_hashes_v3_6.json").write_text(
        json.dumps({"hashes": []}), encoding="utf-8"
    )
