"""
Tests for phyng.evidence.canonical_source_slots
"""

from phyng.evidence.canonical_source_slots import CANONICAL_SLOTS, CanonicalSourceSlot

def test_canonical_slots_count():
    assert len(CANONICAL_SLOTS) == 5

def test_canonical_slots_keys():
    expected = {
        "SRC-BASE-DECOH-001",
        "SRC-BASE-VIS-001",
        "SRC-BASE-MWI-001",
        "SRC-BASE-THRESH-001",
        "SRC-BASE-PARAM-001",
    }
    assert set(CANONICAL_SLOTS.keys()) == expected

def test_slot_structure():
    for slot_id, slot in CANONICAL_SLOTS.items():
        assert isinstance(slot, CanonicalSourceSlot)
        assert slot.source_candidate_id == slot_id
        assert slot.requirement_id.startswith("BSP-")
        assert len(slot.purpose) > 0
        assert len(slot.intended_support_types) > 0
        assert len(slot.required_limitation) > 0
        assert len(slot.suggested_queries) > 0
