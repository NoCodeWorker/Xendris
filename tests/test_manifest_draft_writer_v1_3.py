"""
Tests for phyng.evidence.manifest_draft_writer
"""

import json
from pathlib import Path
from phyng.evidence.manifest_draft_writer import write_filled_manifest_draft

def test_manifest_draft_does_not_mark_sources_ingested(tmp_path: Path):
    draft_path = write_filled_manifest_draft(tmp_path)
    assert draft_path.exists()
    
    with open(draft_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert len(data) > 0
    # No fake local ingestion: since files do not exist, status should be MISSING
    for entry in data:
        assert entry["local_file_status"] == "MISSING"

def test_missing_local_files_keep_missing_status(tmp_path: Path):
    draft_path = write_filled_manifest_draft(tmp_path)
    
    # Verify that the report is also written
    report_path = tmp_path / "reports" / "rag" / "filled_manifest_draft_v1_3.md"
    assert report_path.exists()
    
    content = report_path.read_text(encoding="utf-8")
    assert "MISSING" in content
    assert "No fake local ingestion" in content
