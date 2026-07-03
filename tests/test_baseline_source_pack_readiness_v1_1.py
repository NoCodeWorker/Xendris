"""
Tests for phyng.evidence.source_pack_readiness_v1_1
"""

import json
from pathlib import Path

import pytest

from phyng.evidence.source_pack_readiness_v1_1 import (
    create_baseline_source_folders,
    generate_baseline_source_pack_readiness_v1_1,
)

# ── Valid extract content for testing ─────────────────────────────────────

_VALID_EXTRACT = """\
# Extracts — SRC-BASE-DECOH-001

## Source Metadata

- Title: Decoherence Paper
- Trust level: HIGH

## Extract 1

Support type: FORMULA_SUPPORT
Claim target: CLAIM-BASELINE-FORMULA-001
Local reference: page 12
Text:

> V(t) = exp(-Gamma t)

Audit notes:

- Why: explicit exponential form.
- What not: does not validate candidate.
"""

_INVALID_EXTRACT = """\
# Some other header

No support type, no claim target, no audit notes.
"""


# ── Helpers ────────────────────────────────────────────────────────────────

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


def _write_manifest(root: Path, entries: list[dict]) -> Path:
    baseline = root / "sources" / "baseline"
    baseline.mkdir(parents=True, exist_ok=True)
    p = baseline / "source_manifest.json"
    p.write_text(json.dumps(entries), encoding="utf-8")
    return p


def _write_extract(root: Path, name: str, content: str) -> Path:
    extracts = root / "sources" / "baseline" / "extracts"
    extracts.mkdir(parents=True, exist_ok=True)
    p = extracts / name
    p.write_text(content, encoding="utf-8")
    return p


# ── Tests ──────────────────────────────────────────────────────────────────

class TestReadinessStateMachine:
    def test_no_source_folder(self, tmp_path: Path) -> None:
        result = generate_baseline_source_pack_readiness_v1_1(tmp_path)
        assert result.readiness_status == "NO_SOURCE_FOLDER"
        assert result.ready_for_ingestion_attempt is False

    def test_no_manifest(self, tmp_path: Path) -> None:
        (tmp_path / "sources" / "baseline").mkdir(parents=True)
        result = generate_baseline_source_pack_readiness_v1_1(tmp_path)
        assert result.readiness_status == "NO_MANIFEST"
        assert result.ready_for_ingestion_attempt is False

    def test_invalid_manifest(self, tmp_path: Path) -> None:
        baseline = tmp_path / "sources" / "baseline"
        baseline.mkdir(parents=True)
        (baseline / "source_manifest.json").write_text("{bad", encoding="utf-8")
        result = generate_baseline_source_pack_readiness_v1_1(tmp_path)
        assert result.readiness_status == "MANIFEST_INVALID"
        assert result.ready_for_ingestion_attempt is False

    def test_extracts_missing(self, tmp_path: Path) -> None:
        _write_manifest(tmp_path, [_minimal_entry()])
        result = generate_baseline_source_pack_readiness_v1_1(tmp_path)
        assert result.readiness_status == "EXTRACTS_MISSING"
        assert result.ready_for_ingestion_attempt is False

    def test_partial_ready_invalid_extracts_only(self, tmp_path: Path) -> None:
        _write_manifest(tmp_path, [_minimal_entry()])
        _write_extract(tmp_path, "invalid.md", _INVALID_EXTRACT)
        result = generate_baseline_source_pack_readiness_v1_1(tmp_path)
        assert result.readiness_status == "PARTIAL_READY"
        assert result.ready_for_ingestion_attempt is False

    def test_ready_for_ingestion_attempt(self, tmp_path: Path) -> None:
        _write_manifest(tmp_path, [_minimal_entry()])
        _write_extract(tmp_path, "valid.md", _VALID_EXTRACT)
        result = generate_baseline_source_pack_readiness_v1_1(tmp_path)
        assert result.readiness_status == "READY_FOR_INGESTION_ATTEMPT"
        assert result.ready_for_ingestion_attempt is True

    def test_ready_only_with_valid_manifest_and_extracts(self, tmp_path: Path) -> None:
        # Valid manifest but invalid extract → not ready
        _write_manifest(tmp_path, [_minimal_entry()])
        _write_extract(tmp_path, "bad.md", _INVALID_EXTRACT)
        result = generate_baseline_source_pack_readiness_v1_1(tmp_path)
        assert result.ready_for_ingestion_attempt is False

    def test_extracts_count_reported(self, tmp_path: Path) -> None:
        _write_manifest(tmp_path, [_minimal_entry()])
        _write_extract(tmp_path, "a.md", _VALID_EXTRACT)
        _write_extract(tmp_path, "b.md", _INVALID_EXTRACT)
        result = generate_baseline_source_pack_readiness_v1_1(tmp_path)
        assert result.extracts_count == 2
        assert result.validated_extracts_count == 1


class TestReportsGenerated:
    def test_two_reports_always_written(self, tmp_path: Path) -> None:
        result = generate_baseline_source_pack_readiness_v1_1(tmp_path)
        assert len(result.report_paths) == 2

    def test_rag_readiness_report_exists(self, tmp_path: Path) -> None:
        generate_baseline_source_pack_readiness_v1_1(tmp_path)
        p = tmp_path / "reports" / "rag" / "baseline_source_pack_readiness_v1_1.md"
        assert p.exists()

    def test_campaign_readiness_report_exists(self, tmp_path: Path) -> None:
        generate_baseline_source_pack_readiness_v1_1(tmp_path)
        p = tmp_path / "reports" / "campaigns" / "BASELINE-SRC-PACK-001_v1_1_readiness.md"
        assert p.exists()

    def test_reports_contain_blocked_claims(self, tmp_path: Path) -> None:
        generate_baseline_source_pack_readiness_v1_1(tmp_path)
        content = (
            tmp_path / "reports" / "campaigns" / "BASELINE-SRC-PACK-001_v1_1_readiness.md"
        ).read_text(encoding="utf-8")
        assert "BLOCKED" in content

    def test_report_idempotent(self, tmp_path: Path) -> None:
        generate_baseline_source_pack_readiness_v1_1(tmp_path)
        generate_baseline_source_pack_readiness_v1_1(tmp_path)
        p = tmp_path / "reports" / "rag" / "baseline_source_pack_readiness_v1_1.md"
        assert p.exists()


class TestFolderScaffolding:
    def test_five_folders_created(self, tmp_path: Path) -> None:
        folders = create_baseline_source_folders(tmp_path)
        assert len(folders) == 5
        for f in folders:
            assert f.is_dir()

    def test_no_fake_source_files(self, tmp_path: Path) -> None:
        create_baseline_source_folders(tmp_path)
        files = list((tmp_path / "sources").rglob("*.*"))
        assert files == []

    def test_expected_subfolder_names(self, tmp_path: Path) -> None:
        create_baseline_source_folders(tmp_path)
        expected = {"baseline", "papers", "extracts", "notes", "rejected"}
        actual = {f.name for f in (tmp_path / "sources").rglob("*") if f.is_dir()}
        assert expected.issubset(actual)
