"""
Tests for phyng.evidence.extract_target_generator
"""

from pathlib import Path
from phyng.evidence.extract_target_generator import generate_extract_targets

def test_extract_targets_include_forbidden_overclaims(tmp_path: Path):
    notes_path = generate_extract_targets(tmp_path)
    assert notes_path.exists()
    
    content = notes_path.read_text(encoding="utf-8")
    assert "CLAIM-BASELINE-FORMULA-001" in content
    assert "Forbidden overclaims" in content
    assert "proves quantum gravity decoherence" in content
    assert "the boundary-aware candidate is validated" in content
    assert "SyntheticGain is PredictiveGain" in content
    
    # Check report copy
    report_path = tmp_path / "reports" / "rag" / "extract_targets_v1_3.md"
    assert report_path.exists()
