"""Tests for public dataset search in Track C."""

from __future__ import annotations

from pathlib import Path
from phyng.external_evidence.public_dataset_search import run_public_dataset_search


def test_public_dataset_search_reports_not_found_without_local_data(tmp_path: Path) -> None:
    inputs = {
        "public_dataset_lookup_queue_v4_3": {
            "public_dataset_lookup_queue": [
                {
                    "source_id": "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING",
                    "target_id": "TGT-v4_2-007",
                }
            ]
        }
    }

    results = run_public_dataset_search(inputs, tmp_path)
    assert len(results) == 1
    assert results[0].evidence_status == "PUBLIC_DATASET_NOT_FOUND"
    assert results[0].found_numeric_values is False
    assert "PUBLIC_DATASET_NOT_FOUND" in results[0].blockers
