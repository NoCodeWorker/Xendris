"""Tests for v4.3 assembled y_true dataset."""

from __future__ import annotations

from phyng.ytrue_extraction.dataset_assembly import assemble_y_true_dataset


def test_assembled_dataset_created_even_if_empty() -> None:
    targets = [
        {
            "target_id": "TGT-v4_2-001",
            "benchmark_id": "BM-001",
            "source_id": "SRC-1",
            "observable_class": "VISIBILITY",
        }
    ]
    candidates = [
        {
            "target_id": "TGT-v4_2-001",
            "can_enter_dataset": False,
            "blockers": ["Prose only."],
        }
    ]
    source_hashes = {"hashes": []}
    model_predictions = {"predictions": []}

    assembled, blocked, next_inputs = assemble_y_true_dataset(
        targets, candidates, source_hashes, model_predictions
    )
    assert assembled.y_true_record_count == 0
    assert len(assembled.records) == 0
    assert len(blocked) == 1
    assert assembled.ready_for_predictive_gain is False
    assert next_inputs.ready_for_predictive_gain is False


def test_predictive_gain_requires_minimum_ytrue_count() -> None:
    # 2 accepted targets (less than threshold of 3)
    targets = [
        {
            "target_id": "TGT-v4_2-001",
            "benchmark_id": "BM-001",
            "source_id": "SRC-1",
            "observable_class": "VISIBILITY",
        },
        {
            "target_id": "TGT-v4_2-002",
            "benchmark_id": "BM-002",
            "source_id": "SRC-1",
            "observable_class": "VISIBILITY",
        },
    ]
    candidates = [
        {
            "target_id": "TGT-v4_2-001",
            "can_enter_dataset": True,
            "numeric_value": 0.45,
            "unit": "dimensionless",
            "extraction_method": "AUTO",
            "blockers": [],
        },
        {
            "target_id": "TGT-v4_2-002",
            "can_enter_dataset": True,
            "numeric_value": 0.55,
            "unit": "dimensionless",
            "extraction_method": "AUTO",
            "blockers": [],
        },
    ]
    source_hashes = {
        "hashes": [
            {"source_id": "SRC-1", "sha256": "hash_1", "local_path": "a.pdf"}
        ]
    }
    model_predictions = {
        "predictions": [
            {"prediction_id": "P-1", "target_id": "TGT-v4_2-001"},
            {"prediction_id": "P-2", "target_id": "TGT-v4_2-002"},
        ]
    }

    assembled, blocked, next_inputs = assemble_y_true_dataset(
        targets, candidates, source_hashes, model_predictions
    )
    assert assembled.y_true_record_count == 2
    assert assembled.ready_for_predictive_gain is False
    assert next_inputs.ready_for_predictive_gain is False


def test_prediction_matching_required_for_predictive_gain() -> None:
    # 3 accepted targets, but less than 3 matched predictions
    targets = [
        {
            "target_id": "TGT-v4_2-001",
            "benchmark_id": "BM-001",
            "source_id": "SRC-1",
            "observable_class": "VISIBILITY",
        },
        {
            "target_id": "TGT-v4_2-002",
            "benchmark_id": "BM-002",
            "source_id": "SRC-1",
            "observable_class": "VISIBILITY",
        },
        {
            "target_id": "TGT-v4_2-003",
            "benchmark_id": "BM-003",
            "source_id": "SRC-1",
            "observable_class": "VISIBILITY",
        },
    ]
    candidates = [
        {
            "target_id": "TGT-v4_2-001",
            "can_enter_dataset": True,
            "numeric_value": 0.45,
            "unit": "dimensionless",
            "extraction_method": "AUTO",
            "blockers": [],
        },
        {
            "target_id": "TGT-v4_2-002",
            "can_enter_dataset": True,
            "numeric_value": 0.55,
            "unit": "dimensionless",
            "extraction_method": "AUTO",
            "blockers": [],
        },
        {
            "target_id": "TGT-v4_2-003",
            "can_enter_dataset": True,
            "numeric_value": 0.65,
            "unit": "dimensionless",
            "extraction_method": "AUTO",
            "blockers": [],
        },
    ]
    source_hashes = {
        "hashes": [
            {"source_id": "SRC-1", "sha256": "hash_1", "local_path": "a.pdf"}
        ]
    }
    # Only 2 predictions matched!
    model_predictions = {
        "predictions": [
            {"prediction_id": "P-1", "target_id": "TGT-v4_2-001"},
            {"prediction_id": "P-2", "target_id": "TGT-v4_2-002"},
        ]
    }

    assembled, blocked, next_inputs = assemble_y_true_dataset(
        targets, candidates, source_hashes, model_predictions
    )
    assert assembled.y_true_record_count == 3
    assert assembled.ready_for_predictive_gain is False
    assert next_inputs.ready_for_predictive_gain is False


def test_slot4_debt_remains_open_blocking() -> None:
    targets = [
        {
            "target_id": "TGT-v4_2-001",
            "benchmark_id": "BM-001",
            "source_id": "SRC-1",
            "observable_class": "VISIBILITY",
        }
    ]
    candidates = [
        {
            "target_id": "TGT-v4_2-001",
            "can_enter_dataset": False,
            "blockers": ["Prose only."],
        }
    ]
    source_hashes = {"hashes": []}
    model_predictions = {"predictions": []}

    assembled, blocked, next_inputs = assemble_y_true_dataset(
        targets, candidates, source_hashes, model_predictions
    )
    assert assembled.slot4_debt_status == "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"
    assert assembled.physical_claim_permission == "BLOCKED"
