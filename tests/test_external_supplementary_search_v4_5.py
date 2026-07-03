"""Tests for supplementary search in Track B."""

from __future__ import annotations

from pathlib import Path
from phyng.external_evidence.supplementary_search import run_supplementary_search


def test_supplementary_search_reports_not_found_without_files(tmp_path: Path) -> None:
    inputs = {
        "supplementary_lookup_queue_v4_3": {
            "supplementary_lookup_queue": [
                {
                    "source_id": "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING",
                    "target_id": "TGT-v4_2-006",
                }
            ]
        }
    }

    # Ensure local directory is empty/non-existent
    results = run_supplementary_search(inputs, tmp_path)
    assert len(results) == 1
    assert results[0].evidence_status == "SUPPLEMENTARY_NOT_FOUND"
    assert results[0].found_numeric_values is False
    assert "SUPPLEMENTARY_NOT_FOUND" in results[0].blockers
