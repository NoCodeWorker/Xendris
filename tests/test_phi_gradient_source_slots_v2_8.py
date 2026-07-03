from phyng.source_pressure.slots import build_phi_gradient_source_slots


def test_source_slots_exist():
    slots = build_phi_gradient_source_slots()
    slot_ids = {slot.slot_id for slot in slots}

    assert len(slots) == 8
    assert "SLOT_1_DECOHERENCE_BASELINE_MODELS" in slot_ids
    assert "SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS" in slot_ids
    assert "SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES" in slot_ids
