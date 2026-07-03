"""Tests for candidate evaluation and acceptance rules."""

from __future__ import annotations

from phyng.external_evidence.schemas import TableReviewResult
from phyng.external_evidence.ytrue_candidates import process_external_candidates


def test_external_ytrue_requires_numeric_value() -> None:
    inputs = {
        "normalized_targets_v4_2": {
            "normalized_targets": [
                {
                    "target_id": "TGT-v4_2-001",
                    "observable_class": "VISIBILITY",
                    "benchmark_id": "BM-v4_0-001",
                }
            ]
        },
        "model_predictions_v4_1": {
            "predictions": [
                {
                    "prediction_id": "PRED-001",
                    "target_id": "TGT-v4_2-001",
                }
            ]
        },
    }

    # Case A: Numeric value is None
    table_results = [
        TableReviewResult(
            review_id="REV-001",
            target_id="TGT-v4_2-001",
            source_id="SRC-1",
            local_pdf_path="path/to/file.pdf",
            page_number=3,
            table_number=None,
            candidate_value_text="some text contrast",
            numeric_value=None,
            unit=None,
            uncertainty=None,
            evidence_status="TABLE_VALUE_FOUND",
            blockers=[],
            next_action="",
        )
    ]

    candidates, accepted, rejected = process_external_candidates(
        table_results, [], [], inputs
    )
    assert len(candidates) == 1
    assert candidates[0].can_enter_dataset is False
    assert "NO_NUMERIC_VALUE" in candidates[0].blockers
    assert len(accepted) == 0
    assert len(rejected) == 1


def test_external_ytrue_requires_provenance() -> None:
    inputs = {
        "normalized_targets_v4_2": {
            "normalized_targets": [
                {
                    "target_id": "TGT-v4_2-001",
                    "observable_class": "VISIBILITY",
                    "benchmark_id": "BM-v4_0-001",
                }
            ]
        },
        "model_predictions_v4_1": {
            "predictions": [
                {
                    "prediction_id": "PRED-001",
                    "target_id": "TGT-v4_2-001",
                }
            ]
        },
    }

    # Case B: No source location (provenance missing)
    table_results = [
        TableReviewResult(
            review_id="REV-001",
            target_id="TGT-v4_2-001",
            source_id="SRC-1",
            local_pdf_path="path/to/file.pdf",
            page_number=None,
            table_number=None,
            candidate_value_text="some text contrast",
            numeric_value=0.5,
            unit="dimensionless",
            uncertainty=None,
            evidence_status="TABLE_VALUE_FOUND",
            blockers=[],
            next_action="",
        )
    ]

    candidates, accepted, rejected = process_external_candidates(
        table_results, [], [], inputs
    )
    assert len(candidates) == 1
    assert candidates[0].can_enter_dataset is False
    assert "MISSING_SOURCE_LOCATION" in candidates[0].blockers


def test_external_ytrue_requires_prediction_match() -> None:
    inputs = {
        "normalized_targets_v4_2": {
            "normalized_targets": [
                {
                    "target_id": "TGT-v4_2-001",
                    "observable_class": "VISIBILITY",
                    "benchmark_id": "BM-v4_0-001",
                }
            ]
        },
        "model_predictions_v4_1": {
            # No matching predictions
            "predictions": []
        },
    }

    table_results = [
        TableReviewResult(
            review_id="REV-001",
            target_id="TGT-v4_2-001",
            source_id="SRC-1",
            local_pdf_path="path/to/file.pdf",
            page_number=3,
            table_number="Table 1",
            candidate_value_text="some text contrast",
            numeric_value=0.5,
            unit="dimensionless",
            uncertainty=None,
            evidence_status="TABLE_VALUE_FOUND",
            blockers=[],
            next_action="",
        )
    ]

    candidates, accepted, rejected = process_external_candidates(
        table_results, [], [], inputs
    )
    assert len(candidates) == 1
    assert candidates[0].can_enter_dataset is False
    assert "NO_MATCHED_PREDICTION" in candidates[0].blockers
