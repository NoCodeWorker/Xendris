"""
Tests for phyng.evidence.source_pack_templates
"""

import json
from phyng.evidence.source_pack_templates import (
    MANIFEST_TEMPLATE,
    get_extract_template,
    PAPERS_README,
    REJECTED_README,
    SELECTION_NOTES,
)
from phyng.evidence.canonical_source_slots import CANONICAL_SLOTS

def test_manifest_template_has_five_slots():
    assert len(MANIFEST_TEMPLATE) == 5

def test_manifest_template_does_not_fake_metadata():
    for entry in MANIFEST_TEMPLATE:
        assert entry["title"] is None
        assert entry["authors"] == []
        assert entry["year"] is None
        assert entry["url"] is None
        assert entry["source_type"] == "LOCAL_FILE"
        assert entry["trust_level"] == "HIGH"
        assert entry["local_path"].endswith(".pdf")

def test_extract_templates_marked_not_evidence():
    for source_id in CANONICAL_SLOTS:
        template_text = get_extract_template(source_id)
        assert "TEMPLATE_NOT_EVIDENCE" in template_text
        assert "Extracts —" in template_text
        assert "Source Metadata" in template_text

def test_other_templates_exist():
    assert "Baseline Source Papers" in PAPERS_README
    assert "Rejected Sources" in REJECTED_README
    assert "Baseline Source Selection Notes" in SELECTION_NOTES
