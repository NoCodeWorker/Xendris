"""Tests for v4.0 negative control plan."""

from __future__ import annotations

from phyng.benchmark_construction.negative_controls import generate_negative_control_plan


def test_negative_control_plan_includes_no_slot4_control() -> None:
    records = [
        {
            "extract_id": "VRX-001",
            "assigned_slot": "SLOT_1_DECOHERENCE_BASELINE",
            "pressure_class": "SUPPORTS_BASELINE_ONLY",
        }
    ]

    plan = generate_negative_control_plan(records)
    controls = plan.controls

    # Should contain the slot 1 control plus the mandatory NO_SLOT4 control
    assert len(controls) == 2

    ctrl_types = {c.control_type for c in controls}
    assert "BASELINE_ONLY_CONTROL" in ctrl_types
    assert "NO_SLOT4_CONTROL" in ctrl_types

    no_slot4_ctrl = next(c for c in controls if c.control_type == "NO_SLOT4_CONTROL")
    assert no_slot4_ctrl.slot_id == "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS"
