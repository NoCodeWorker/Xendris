"""Tests for v3.9 source pressure campaign end-to-end."""

from __future__ import annotations

from pathlib import Path

from phyng.source_pressure_decision.campaign import run_phi_gradient_source_pressure_decision_campaign
from phyng.semantic_triage.campaign import run_phi_gradient_semantic_triage_campaign

from tests.test_source_pressure_loader_v3_9 import write_minimal_v3_9_inputs
from tests.test_semantic_triage_loader_v3_8_2 import raw_candidate, write_minimal_v3_8_2_inputs


def test_campaign_generates_v3_9_outputs(tmp_path: Path) -> None:
    write_minimal_v3_9_inputs(tmp_path)

    result = run_phi_gradient_source_pressure_decision_campaign(tmp_path)

    assert result.status != "PHI_GRADIENT_SOURCE_PRESSURE_BLOCKED_MISSING_VALIDATION_READY_PACK"
    assert result.gate_result.validation_ready_count > 0
    # Data outputs
    for path_str in result.gate_result.output_paths.values():
        assert (tmp_path / path_str).exists(), f"Missing data output: {path_str}"
    # Report outputs
    for path_str in result.report_paths.values():
        rpath = tmp_path / path_str if not Path(path_str).is_absolute() else Path(path_str)
        assert rpath.exists(), f"Missing report: {path_str}"


def test_campaign_blocked_without_inputs(tmp_path: Path) -> None:
    result = run_phi_gradient_source_pressure_decision_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_SOURCE_PRESSURE_BLOCKED_MISSING_VALIDATION_READY_PACK"


def test_campaign_no_slot4_blocks_gradient_support(tmp_path: Path) -> None:
    """Without SLOT_4 extracts, gradient_component_support must be false."""
    write_minimal_v3_9_inputs(tmp_path, include_slot4=False)

    result = run_phi_gradient_source_pressure_decision_campaign(tmp_path)

    assert result.gate_result.decision.gradient_component_support is False
    assert "The current extract pack does not support the gradient-component mechanism." in result.gate_result.decision.allowed_claims


def test_campaign_with_slot4_enables_gradient_support(tmp_path: Path) -> None:
    write_minimal_v3_9_inputs(tmp_path, include_slot4=True)

    result = run_phi_gradient_source_pressure_decision_campaign(tmp_path)

    assert result.gate_result.decision.gradient_component_support is True


def test_campaign_with_contradiction(tmp_path: Path) -> None:
    write_minimal_v3_9_inputs(tmp_path, include_negative=True)

    result = run_phi_gradient_source_pressure_decision_campaign(tmp_path)

    assert "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED" in result.gate_result.decision.global_decisions


def test_physical_claims_remain_blocked(tmp_path: Path) -> None:
    write_minimal_v3_9_inputs(tmp_path)

    result = run_phi_gradient_source_pressure_decision_campaign(tmp_path)

    blocked = result.gate_result.decision.blocked_claims
    assert "PHI_GRADIENT is physically validated." in blocked
    assert "Frontera C is validated." in blocked
    assert result.gate_result.decision.physical_claim_permission == "BLOCKED"


def test_existing_v3_8_3_behavior_preserved(tmp_path: Path) -> None:
    """v3.8.2 semantic triage must still work unchanged."""
    write_minimal_v3_8_2_inputs(tmp_path, [raw_candidate()])

    result = run_phi_gradient_semantic_triage_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY"
    assert result.gate_result.next_gate_readiness.ready_for_v3_9 is False
