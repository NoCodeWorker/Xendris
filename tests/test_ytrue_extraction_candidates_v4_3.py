"""Tests for v4.3 y_true extraction candidates."""

from __future__ import annotations

from phyng.ytrue_extraction.extraction_candidates import extract_candidates


def test_prose_without_numeric_value_not_ytrue() -> None:
    targets = [
        {
            "target_id": "TGT-v4_2-001",
            "observable_class": "VISIBILITY",
            "source_id": "SRC-HORNBERGER",
            "extract_id": "VRX-001",
            "source_observable_text": "halve the interference visibility",
        }
    ]
    candidates = extract_candidates(targets)
    assert len(candidates) == 1
    assert candidates[0].numeric_value is None
    assert candidates[0].can_enter_dataset is False
    assert candidates[0].qc_status == "FAIL_NO_NUMERIC_VALUE"


def test_constraint_values_not_admitted_as_ytrue() -> None:
    targets = [
        {
            "target_id": "TGT-v4_2-002",
            "observable_class": "PARAMETER_BOUND",
            "source_id": "SRC-HORNBERGER",
            "extract_id": "VRX-002",
            "source_observable_text": "parameter bounds Lambda set to 10^-8 s^-1",
        }
    ]
    candidates = extract_candidates(targets)
    assert len(candidates) == 1
    assert candidates[0].can_enter_dataset is False
    assert "Parameter constraints" in candidates[0].blockers[0]
    assert candidates[0].qc_status == "FAIL_CONSTRAINT_ONLY"


def test_limitation_flags_not_admitted_as_ytrue() -> None:
    targets = [
        {
            "target_id": "TGT-v4_2-003",
            "observable_class": "LIMITATION_FLAG",
            "source_id": "SRC-HORNBERGER",
            "extract_id": "VRX-003",
            "source_observable_text": "environmental noise exceeds 0.15 threshold",
        }
    ]
    candidates = extract_candidates(targets)
    assert len(candidates) == 1
    assert candidates[0].can_enter_dataset is False
    assert "limitation flags" in candidates[0].blockers[0].lower()
