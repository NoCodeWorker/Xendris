"""Tests for v4.3 y_true source coverage audit."""

from __future__ import annotations

from pathlib import Path

from phyng.ytrue_extraction.source_coverage_audit import run_source_coverage_audit


def test_source_coverage_requires_hash(tmp_path: Path) -> None:
    targets = [
        {
            "target_id": "TGT-v4_2-001",
            "benchmark_id": "BM-v4_0-001",
            "source_id": "SRC-UNREGISTERED",
            "extract_id": "VRX-001",
            "observable_class": "DECOHERENCE_RATE",
            "source_observable_text": "thermal decay rate gamma = 12.5 s^-1 is measured",
        }
    ]
    source_hashes = {"hashes": []}
    benchmark_rows = [
        {
            "benchmark_id": "BM-v4_0-001",
            "page_number": 1,
        }
    ]

    records = run_source_coverage_audit(targets, source_hashes, benchmark_rows, tmp_path)
    assert len(records) == 1
    assert records[0].source_hash_present is False
    assert records[0].source_coverage_status == "SOURCE_COVERAGE_BLOCKED_INSUFFICIENT_PROVENANCE"


def test_source_coverage_requires_location_for_complete(tmp_path: Path) -> None:
    targets = [
        {
            "target_id": "TGT-v4_2-001",
            "benchmark_id": "BM-v4_0-001",
            "source_id": "SRC-HORNBERGER",
            "extract_id": "VRX-001",
            "observable_class": "DECOHERENCE_RATE",
            "source_observable_text": "thermal decay rate gamma = 12.5 s^-1 is measured",
        }
    ]
    source_hashes = {
        "hashes": [
            {
                "source_id": "SRC-HORNBERGER",
                "local_path": "Hornberger.pdf",
                "sha256": "abcdef",
            }
        ]
    }
    # Page number is missing!
    benchmark_rows = [
        {
            "benchmark_id": "BM-v4_0-001",
            "page_number": None,
        }
    ]

    # Create dummy file to bypass PDF check
    (tmp_path / "Hornberger.pdf").write_text("DUMMY")

    records = run_source_coverage_audit(targets, source_hashes, benchmark_rows, tmp_path)
    assert len(records) == 1
    assert records[0].source_hash_present is True
    assert records[0].local_pdf_present is True
    assert records[0].page_reference_present is False
    assert records[0].source_coverage_status == "SOURCE_COVERAGE_LOCAL_PDF_ONLY"
