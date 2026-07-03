import tempfile
from pathlib import Path
from phyng.rag.schemas import ClaimRecord
from phyng.rag.claim_registry import add_claim
from phyng.loop.iteration import run_iteration_once


def test_run_iteration_once_executes_entire_loop():
    claim = ClaimRecord(
        claim_id="CLAIM-ITERATION-TEST",
        text="A test claim about speed of light c",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="REQUIRES_SOURCE",
        source_ids=[]
    )
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Setup folder structure
        (tmp_path / "phyng").mkdir(parents=True, exist_ok=True)
        with open(tmp_path / "phyng" / "api.py", "w") as f:
            f.write("# Dummy API")
            
        (tmp_path / "tests").mkdir(parents=True, exist_ok=True)
        with open(tmp_path / "tests" / "test_dummy.py", "w") as f:
            f.write("# Reference CLAIM-ITERATION-TEST")
            
        add_claim(claim, tmp_path)
        
        # Run iteration
        record = run_iteration_once(tmp_path)
        
        assert record.status == "SUCCESS"
        assert len(record.gaps_found) > 0
        assert any(g.gap_type == "MISSING_SOURCE" for g in record.gaps_found)
        
        # Check generated files
        assert (tmp_path / "backlog" / "phygn_core_backlog.json").exists()
        assert (tmp_path / "backlog" / "phygn_core_backlog.md").exists()
        assert (tmp_path / "reports" / "rag_status.md").exists()
        assert (tmp_path / "reports" / "claim_source_matrix.md").exists()
        assert (tmp_path / "reports" / "iteration_log.md").exists()
        assert (tmp_path / "reports" / "research_backlog.md").exists()
        assert (tmp_path / "reports" / "benchmark_status.md").exists()
        assert (tmp_path / "reports" / "core_backlog.md").exists()
        
        # Verify iteration log contains v0.4 format fields
        with open(tmp_path / "reports" / "iteration_log.md", "r", encoding="utf-8") as f:
            log_content = f.read()
            assert "## ITERATION" in log_content
            assert "### Selected Gap" in log_content
            assert "### Mode" in log_content
            assert "### Priority" in log_content

