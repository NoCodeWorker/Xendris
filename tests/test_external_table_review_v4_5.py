"""Tests for table review logic in Track A."""

from __future__ import annotations

from pathlib import Path
from phyng.external_evidence.table_review import run_table_review


def test_table_review_does_not_fabricate_page_location(tmp_path: Path) -> None:
    inputs = {
        "manual_extraction_review_records_v4_4": {
            "review_records": [
                {
                    "target_id": "TGT-v4_2-001",
                    "source_id": "SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS",
                    "page_number": None,
                    "table_number": None,
                    "figure_number": None,
                    "extracted_value_text": "prose without numbers",
                    "numeric_value": None,
                    "unit": None,
                }
            ]
        },
        "source_hashes_v3_6": {
            "hashes": [
                {
                    "source_id": "SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS",
                    "local_path": "data/real_sources/pdfs/Schrinski_2020_QC_Hypothesis_Tests.pdf",
                }
            ]
        },
    }

    # Make dummy PDF file exist to bypass PDF availability check
    pdf_path = tmp_path / "data/real_sources/pdfs/Schrinski_2020_QC_Hypothesis_Tests.pdf"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.write_text("dummy pdf content")

    results = run_table_review(inputs, tmp_path)
    assert len(results) == 1
    assert results[0].evidence_status == "PAGE_LOCATION_MISSING"
    assert results[0].page_number is None
    assert results[0].table_number is None
    assert "PAGE_LOCATION_MISSING" in results[0].blockers
