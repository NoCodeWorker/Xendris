"""Tests for v4.3 y_true extraction queues."""

from __future__ import annotations

from phyng.ytrue_extraction.extraction_queues import build_queues


def test_manual_table_queue_created_for_table_targets() -> None:
    targets = [
        {
            "target_id": "TGT-v4_2-001",
            "source_id": "SRC-1",
            "observable_class": "VISIBILITY",
            "source_observable_text": "halve the interference visibility in table 2",
        }
    ]
    candidates = [
        {
            "target_id": "TGT-v4_2-001",
            "can_enter_dataset": False,
            "blockers": ["No numeric value."],
        }
    ]
    table_q, fig_q, pub_q, supp_q = build_queues(targets, candidates)
    assert len(table_q) == 1
    assert table_q[0].target_id == "TGT-v4_2-001"
    assert "table" in table_q[0].required_action.lower()


def test_public_lookup_queue_created_for_public_targets() -> None:
    targets = [
        {
            "target_id": "TGT-v4_2-002",
            "source_id": "SRC-1",
            "observable_class": "MASS_REGIME",
            "source_observable_text": "mass exceeds 10 000 amu",
        }
    ]
    candidates = [
        {
            "target_id": "TGT-v4_2-002",
            "can_enter_dataset": False,
            "blockers": ["Regime bound."],
        }
    ]
    table_q, fig_q, pub_q, supp_q = build_queues(targets, candidates)
    assert len(pub_q) == 1
    assert pub_q[0].target_id == "TGT-v4_2-002"
