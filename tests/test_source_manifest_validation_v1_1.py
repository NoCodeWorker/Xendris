"""
Tests for phyng.evidence.source_manifest_validation
"""

import json
from pathlib import Path

import pytest

from phyng.evidence.source_manifest_validation import (
    ManifestValidationResult,
    validate_source_manifest,
    write_manifest_validation_report,
)

# ── Helpers ────────────────────────────────────────────────────────────────

def _make_manifest(tmp_path: Path, entries: list[dict] | str) -> Path:
    baseline = tmp_path / "sources" / "baseline"
    baseline.mkdir(parents=True, exist_ok=True)
    p = baseline / "source_manifest.json"
    if isinstance(entries, str):
        p.write_text(entries, encoding="utf-8")
    else:
        p.write_text(json.dumps(entries), encoding="utf-8")
    return p


def _minimal_entry(**overrides) -> dict:
    base = {
        "source_candidate_id": "SRC-001",
        "requirement_id": "BSP-001",
        "title": None,
        "authors": [],
        "year": None,
        "source_type": "MANUAL_RECORD",
        "local_path": None,
        "url": None,
        "trust_level": "HIGH",
        "intended_support_types": ["FORMULA_SUPPORT"],
        "notes": "test",
    }
    base.update(overrides)
    return base


# ── Tests ──────────────────────────────────────────────────────────────────

class TestCreateBaselineSourceFolders:
    """Tested here because this module is the natural companion."""

    def test_creates_five_folders(self, tmp_path: Path) -> None:
        from phyng.evidence.source_pack_readiness_v1_1 import create_baseline_source_folders
        folders = create_baseline_source_folders(tmp_path)
        assert len(folders) == 5
        for f in folders:
            assert f.is_dir()

    def test_no_fake_files_created(self, tmp_path: Path) -> None:
        from phyng.evidence.source_pack_readiness_v1_1 import create_baseline_source_folders
        create_baseline_source_folders(tmp_path)
        all_files = list((tmp_path / "sources").rglob("*.*"))
        assert all_files == []

    def test_idempotent(self, tmp_path: Path) -> None:
        from phyng.evidence.source_pack_readiness_v1_1 import create_baseline_source_folders
        create_baseline_source_folders(tmp_path)
        create_baseline_source_folders(tmp_path)  # should not raise


class TestManifestValidation:
    def test_missing_manifest_not_valid(self, tmp_path: Path) -> None:
        p = tmp_path / "sources" / "baseline" / "source_manifest.json"
        result = validate_source_manifest(p, tmp_path)
        assert result.json_valid is False
        assert result.overall_valid is False

    def test_malformed_json_invalid(self, tmp_path: Path) -> None:
        p = _make_manifest(tmp_path, "{bad json")
        result = validate_source_manifest(p, tmp_path)
        assert result.json_valid is False

    def test_non_list_top_level_invalid(self, tmp_path: Path) -> None:
        p = _make_manifest(tmp_path, '{"key": "value"}')
        result = validate_source_manifest(p, tmp_path)
        assert result.is_list is False
        assert result.overall_valid is False

    def test_empty_list_not_overall_valid(self, tmp_path: Path) -> None:
        p = _make_manifest(tmp_path, [])
        result = validate_source_manifest(p, tmp_path)
        assert result.total_entries == 0
        assert result.overall_valid is False

    def test_missing_required_field_invalid(self, tmp_path: Path) -> None:
        entry = _minimal_entry()
        del entry["trust_level"]
        p = _make_manifest(tmp_path, [entry])
        result = validate_source_manifest(p, tmp_path)
        assert result.invalid_entries == 1
        assert "trust_level" in result.entry_results[0].missing_fields

    def test_all_required_fields_present_valid(self, tmp_path: Path) -> None:
        p = _make_manifest(tmp_path, [_minimal_entry()])
        result = validate_source_manifest(p, tmp_path)
        assert result.valid_entries == 1
        assert result.overall_valid is True

    def test_invalid_source_type_rejected(self, tmp_path: Path) -> None:
        entry = _minimal_entry(source_type="FAKE_TYPE")
        p = _make_manifest(tmp_path, [entry])
        result = validate_source_manifest(p, tmp_path)
        assert result.invalid_entries == 1

    def test_invalid_trust_level_rejected(self, tmp_path: Path) -> None:
        entry = _minimal_entry(trust_level="SUPER")
        p = _make_manifest(tmp_path, [entry])
        result = validate_source_manifest(p, tmp_path)
        assert result.invalid_entries == 1

    def test_invalid_support_type_rejected(self, tmp_path: Path) -> None:
        entry = _minimal_entry(intended_support_types=["FAKE_SUPPORT"])
        p = _make_manifest(tmp_path, [entry])
        result = validate_source_manifest(p, tmp_path)
        assert result.entry_results[0].invalid_support_types == ["FAKE_SUPPORT"]
        assert result.invalid_entries == 1

    def test_external_url_record_not_ingested(self, tmp_path: Path) -> None:
        entry = _minimal_entry(
            source_type="EXTERNAL_URL_RECORD",
            url="https://example.com",
        )
        p = _make_manifest(tmp_path, [entry])
        result = validate_source_manifest(p, tmp_path)
        assert result.non_ingested_entries == 1
        # EXTERNAL_URL_RECORD is valid but not ingested
        assert result.entry_results[0].not_ingested is True

    def test_research_task_only_not_ingested(self, tmp_path: Path) -> None:
        entry = _minimal_entry(source_type="RESEARCH_TASK_ONLY")
        p = _make_manifest(tmp_path, [entry])
        result = validate_source_manifest(p, tmp_path)
        assert result.non_ingested_entries == 1

    def test_local_file_missing_blocks_entry(self, tmp_path: Path) -> None:
        entry = _minimal_entry(
            source_type="LOCAL_FILE",
            local_path="sources/baseline/papers/missing.pdf",
        )
        p = _make_manifest(tmp_path, [entry])
        result = validate_source_manifest(p, tmp_path)
        assert result.entry_results[0].local_file_missing is True
        assert result.invalid_entries == 1

    def test_local_file_exists_valid(self, tmp_path: Path) -> None:
        papers = tmp_path / "sources" / "baseline" / "papers"
        papers.mkdir(parents=True)
        (papers / "real.pdf").write_bytes(b"content")
        entry = _minimal_entry(
            source_type="LOCAL_FILE",
            local_path="sources/baseline/papers/real.pdf",
        )
        p = _make_manifest(tmp_path, [entry])
        result = validate_source_manifest(p, tmp_path)
        assert result.valid_entries == 1
        assert result.entry_results[0].local_file_missing is False

    def test_multiple_entries_mixed(self, tmp_path: Path) -> None:
        good = _minimal_entry(source_candidate_id="GOOD-001")
        bad = _minimal_entry(source_candidate_id="BAD-001", source_type="INVALID")
        p = _make_manifest(tmp_path, [good, bad])
        result = validate_source_manifest(p, tmp_path)
        assert result.valid_entries == 1
        assert result.invalid_entries == 1
        assert result.overall_valid is False

    def test_report_written(self, tmp_path: Path) -> None:
        p = _make_manifest(tmp_path, [_minimal_entry()])
        result = validate_source_manifest(p, tmp_path)
        rp = write_manifest_validation_report(result, tmp_path)
        assert rp.exists()
        content = rp.read_text(encoding="utf-8")
        assert "Manifest Validation" in content
