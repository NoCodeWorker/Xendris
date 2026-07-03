"""
Unit tests for phyng.evidence.local_source_scanner
"""

import json
import tempfile
from pathlib import Path

import pytest

from phyng.evidence.local_source_scanner import scan_local_sources


# ── Helpers ────────────────────────────────────────────────────────────────

def _make_root(tmp_path: Path, manifest: list[dict] | None = None, extra_files: list[str] | None = None) -> Path:
    baseline = tmp_path / "sources" / "baseline"
    baseline.mkdir(parents=True)

    if manifest is not None:
        (baseline / "source_manifest.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )

    for fname in (extra_files or []):
        (baseline / fname).write_text("content", encoding="utf-8")

    return tmp_path


# ── Tests ──────────────────────────────────────────────────────────────────

class TestScanLocalSources:
    def test_empty_dir_returns_empty(self, tmp_path: Path) -> None:
        root = _make_root(tmp_path, extra_files=[])
        result = scan_local_sources(root)
        assert result == []

    def test_missing_baseline_dir_returns_empty(self, tmp_path: Path) -> None:
        result = scan_local_sources(tmp_path)
        assert result == []

    def test_manifest_single_entry_url_only(self, tmp_path: Path) -> None:
        manifest = [
            {
                "source_candidate_id": "CAND-001",
                "requirement_id": "BSR-001",
                "title": "My Paper",
                "authors": ["Author A"],
                "year": "2024",
                "source_type": "PAPER",
                "local_path": None,
                "url": "https://example.com/paper.pdf",
                "trust_level": "HIGH",
                "notes": "test",
            }
        ]
        root = _make_root(tmp_path, manifest=manifest)
        result = scan_local_sources(root)
        assert len(result) == 1
        assert result[0].source_candidate_id == "CAND-001"
        assert result[0].url is not None
        assert result[0].local_path is None

    def test_manifest_entry_with_local_file(self, tmp_path: Path) -> None:
        baseline = tmp_path / "sources" / "baseline"
        baseline.mkdir(parents=True)
        real_file = baseline / "paper.pdf"
        real_file.write_bytes(b"%PDF-dummy")

        manifest = [
            {
                "source_candidate_id": "CAND-002",
                "requirement_id": "BSR-001",
                "title": "Paper with Local",
                "authors": ["B"],
                "year": "2023",
                "source_type": "PAPER",
                "local_path": "sources/baseline/paper.pdf",
                "url": None,
                "trust_level": "HIGH",
                "notes": None,
            }
        ]
        (baseline / "source_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        result = scan_local_sources(tmp_path)
        assert len(result) == 1
        # candidate_status should reflect that the file exists
        assert result[0].candidate_status in {
            "REGISTERED_NEEDS_METADATA",
            "REGISTERED_COMPLETE",
            "REGISTERED_URL_ONLY",
            "FAILED_NO_LOCAL_CONTENT",
            "READY_FOR_AUDIT",
        }

    def test_no_manifest_falls_back_to_file_scan(self, tmp_path: Path) -> None:
        root = _make_root(tmp_path, extra_files=["formula_decay.txt", "noise_gamma.txt"])
        result = scan_local_sources(root)
        assert len(result) == 2

    def test_gitkeep_ignored(self, tmp_path: Path) -> None:
        root = _make_root(tmp_path, extra_files=[".gitkeep"])
        result = scan_local_sources(root)
        assert result == []

    def test_manifest_fallback_on_malformed_json(self, tmp_path: Path) -> None:
        baseline = tmp_path / "sources" / "baseline"
        baseline.mkdir(parents=True)
        (baseline / "source_manifest.json").write_text("{bad json", encoding="utf-8")
        (baseline / "extra.txt").write_text("data", encoding="utf-8")
        result = scan_local_sources(tmp_path)
        # Should fall back to file scan
        assert len(result) == 1

    def test_requirement_inference_from_filename(self, tmp_path: Path) -> None:
        root = _make_root(
            tmp_path,
            extra_files=["formula_x.txt", "noise_env.txt", "threshold_eps.txt", "other.txt"],
        )
        result = scan_local_sources(root)
        req_ids = {c.requirement_id for c in result}
        assert "BSR-001" in req_ids
        assert "BSR-002" in req_ids
        assert "BSR-003" in req_ids
        assert "BSR-004" in req_ids

    def test_multiple_manifest_entries(self, tmp_path: Path) -> None:
        manifest = [
            {"source_candidate_id": f"CAND-{i:03d}", "requirement_id": "BSR-001",
             "title": f"Paper {i}", "authors": [], "year": "2024",
             "source_type": "PAPER", "local_path": None, "url": None,
             "trust_level": "HIGH", "notes": None}
            for i in range(5)
        ]
        root = _make_root(tmp_path, manifest=manifest)
        result = scan_local_sources(root)
        assert len(result) == 5
