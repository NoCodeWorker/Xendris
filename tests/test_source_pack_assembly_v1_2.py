"""
Tests for phyng.evidence.source_pack_assembly
"""

import json
from pathlib import Path
import pytest
from phyng.evidence.source_pack_assembly import assemble_baseline_source_pack_templates
from phyng.campaigns.baseline_source_pack_assembly import main as campaign_main

def test_assembly_creates_expected_folders(tmp_path: Path):
    result = assemble_baseline_source_pack_templates(tmp_path)
    assert result.assembly_status == "SOURCE_PACK_TEMPLATE_READY"
    
    baseline_dir = tmp_path / "sources" / "baseline"
    assert baseline_dir.is_dir()
    assert (baseline_dir / "papers").is_dir()
    assert (baseline_dir / "extracts").is_dir()
    assert (baseline_dir / "notes").is_dir()
    assert (baseline_dir / "rejected").is_dir()

def test_assembly_creates_manifest_template(tmp_path: Path):
    result = assemble_baseline_source_pack_templates(tmp_path)
    manifest_path = Path(result.manifest_path)
    assert manifest_path.exists()
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 5
    for entry in data:
        assert entry["title"] is None
        assert entry["authors"] == []
        assert entry["year"] is None

def test_extract_templates_created(tmp_path: Path):
    result = assemble_baseline_source_pack_templates(tmp_path)
    extracts_dir = tmp_path / "sources" / "baseline" / "extracts"
    
    expected_files = [
        "SRC-BASE-DECOH-001_extracts.md",
        "SRC-BASE-VIS-001_extracts.md",
        "SRC-BASE-MWI-001_extracts.md",
        "SRC-BASE-THRESH-001_extracts.md",
        "SRC-BASE-PARAM-001_extracts.md",
    ]
    for fname in expected_files:
        p = extracts_dir / fname
        assert p.exists()
        content = p.read_text(encoding="utf-8")
        assert "TEMPLATE_NOT_EVIDENCE" in content

def test_template_readiness_false(tmp_path: Path):
    result = assemble_baseline_source_pack_templates(tmp_path)
    assert result.ready_for_ingestion_attempt is False

def test_reports_generated(tmp_path: Path):
    result = assemble_baseline_source_pack_templates(tmp_path)
    assert len(result.report_paths) == 4
    for rp in result.report_paths:
        assert Path(rp).exists()

def test_campaign_runner_runs(tmp_path: Path, capsys):
    campaign_main(tmp_path)
    captured = capsys.readouterr()
    assert "BASELINE-SRC-PACK-001 v1.2" in captured.out
    assert "SOURCE_PACK_TEMPLATE_READY" in captured.out

def test_idempotent_template_generation(tmp_path: Path):
    result1 = assemble_baseline_source_pack_templates(tmp_path)
    # Run again
    result2 = assemble_baseline_source_pack_templates(tmp_path)
    assert result1.assembly_status == result2.assembly_status
    assert len(result1.created_files) == len(result2.created_files)
