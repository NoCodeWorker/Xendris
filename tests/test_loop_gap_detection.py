import tempfile
from pathlib import Path
from phyng.rag.schemas import ClaimRecord, SourceRecord
from phyng.loop.gap_detection import (
    detect_claims_without_sources,
    detect_claims_without_tests,
    detect_sources_without_claims,
    detect_blocked_claims_without_safe_rewrite,
    detect_claims_with_low_trust_only,
    detect_research_tasks_pending,
    detect_missing_reports,
    detect_missing_registries,
    detect_api_endpoints_without_tests,
    run_all_gap_detections
)


def test_gap_detection_missing_source():
    claim = ClaimRecord(
        claim_id="CLAIM_TEST_1",
        text="A test claim",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="REQUIRES_SOURCE",
        source_ids=[]
    )
    gaps = detect_claims_without_sources([claim])
    assert len(gaps) == 1
    assert gaps[0].gap_type == "MISSING_SOURCE"
    assert "CLAIM_TEST_1" in gaps[0].description


def test_gap_detection_missing_test():
    claim = ClaimRecord(
        claim_id="CLAIM_UNIQUE_NON_EXISTENT_ID",
        text="A test claim",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=["SRC-1"]
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        
        # Create a dummy test file without the unique claim ID
        with open(tests_dir / "test_dummy.py", "w") as f:
            f.write("def test_something():\n    assert True\n")
            
        gaps = detect_claims_without_tests([claim], tmp_path)
        assert len(gaps) == 1
        assert gaps[0].gap_type == "MISSING_TEST"
        
        # If it is referenced, gap should be gone
        with open(tests_dir / "test_dummy.py", "w") as f:
            f.write("def test_something():\n    # Reference CLAIM_UNIQUE_NON_EXISTENT_ID\n    assert True\n")
            
        gaps = detect_claims_without_tests([claim], tmp_path)
        assert len(gaps) == 0


def test_gap_detection_unused_source():
    source = SourceRecord(
        source_id="SRC-UNUSED",
        title="Unused paper",
        source_type="PAPER",
        trust_level="HIGH",
        relevance="HIGH",
        topics=["Relativity"]
    )
    claim = ClaimRecord(
        claim_id="CLAIM_1",
        text="A test claim",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=["SRC-USED"]
    )
    gaps = detect_sources_without_claims([source], [claim])
    assert len(gaps) == 1
    assert gaps[0].gap_type == "RAG_GAP"


def test_gap_detection_blocked_without_rewrite():
    claim = ClaimRecord(
        claim_id="CLAIM_BLOCKED_NO_REWRITE",
        text="A blocked claim",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="BLOCKED",
        source_ids=["SRC-1"],
        safe_rewrite=None
    )
    gaps = detect_blocked_claims_without_safe_rewrite([claim])
    assert len(gaps) == 1
    assert gaps[0].gap_type == "CLAIM_RISK"


def test_gap_detection_low_trust_only():
    claim = ClaimRecord(
        claim_id="CLAIM-LOW",
        text="A test claim",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=["SRC-LOW"]
    )
    source = SourceRecord(
        source_id="SRC-LOW",
        title="Unverified blog",
        source_type="WEB_ARTICLE",
        trust_level="LOW",
        relevance="MEDIUM",
        topics=["Physics"]
    )
    gaps = detect_claims_with_low_trust_only([claim], [source])
    assert len(gaps) == 1
    assert gaps[0].gap_type == "CLAIM_RISK"
    assert gaps[0].severity == "HIGH"


def test_gap_detection_missing_reports():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        # Create empty reports dir
        (tmp_path / "reports").mkdir()
        gaps = detect_missing_reports(tmp_path)
        # Verify it finds all missing report files
        assert len(gaps) == 6
        assert any("iteration_log_md" in g.gap_id for g in gaps)


def test_gap_detection_missing_registries():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        gaps = detect_missing_registries(tmp_path)
        assert len(gaps) == 6
        assert any("source_manifest_json" in g.gap_id for g in gaps)


def test_gap_detection_api_endpoints_without_tests():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Mock api.py
        api_dir = tmp_path / "phyng"
        api_dir.mkdir()
        with open(api_dir / "api.py", "w") as f:
            f.write('@app.get("/loop/status")\ndef get_loop_status():\n    pass\n')
            f.write('@app.post("/loop/iterate-once")\ndef iterate_once():\n    pass\n')
            
        # Mock empty tests dir
        (tmp_path / "tests").mkdir()
        
        gaps = detect_api_endpoints_without_tests(tmp_path)
        assert len(gaps) == 2
        assert any("loop_status" in g.gap_id for g in gaps)
        
        # If test contains the route, gap is resolved
        with open(tmp_path / "tests" / "test_api.py", "w") as f:
            f.write('client.get("/loop/status")\nclient.post("/loop/iterate-once")\n')
            
        gaps = detect_api_endpoints_without_tests(tmp_path)
        assert len(gaps) == 0

