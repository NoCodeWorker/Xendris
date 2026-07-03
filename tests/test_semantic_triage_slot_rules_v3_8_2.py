from __future__ import annotations

from phyng.semantic_triage.slot_rules import (
    SLOT_1_DECOHERENCE_BASELINE,
    SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE,
    SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS,
    SLOT_5_PARAMETER_CONSTRAINTS,
    assign_slot,
)


def test_slot_assignment_detects_decoherence_baseline() -> None:
    assert assign_slot("collisional decoherence rate from environmental scattering") == SLOT_1_DECOHERENCE_BASELINE


def test_slot_assignment_detects_visibility_observable() -> None:
    assert assign_slot("fringe visibility and interference contrast are reduced") == SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE


def test_slot_assignment_detects_gradient_dynamics() -> None:
    text = "magnetic field gradient produces spin-motion coupling and effective dynamics"
    assert assign_slot(text, "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING") == SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS


def test_slot_assignment_detects_parameter_constraints() -> None:
    assert assign_slot("CSL lambda and r_C parameter bounds constrain collapse models") == SLOT_5_PARAMETER_CONSTRAINTS
