import tempfile
from pathlib import Path
from phyng.rag.schemas import ClaimRecord
from phyng.rag.research_planner import plan_research_for_claim, list_research_tasks


def test_research_planner_creates_task_for_unsourced_claim():
    claim = ClaimRecord(
        claim_id="CLAIM-UNSOURCED",
        text="A test claim about Schwarzschild metrics",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="REQUIRES_SOURCE",
        source_ids=[]
    )
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        task = plan_research_for_claim(claim, "GAP-001", tmp_path)
        assert task is not None
        assert task.task_id == "RSC_TASK_CLAIM-UNSOURCED"
        assert task.priority == "P0"  # PHYSICAL_CORE claims get P0
        assert task.status == "TODO"
        
        # Verify it lists
        all_tasks = list_research_tasks(tmp_path)
        assert len(all_tasks) == 1
        assert all_tasks[0].task_id == "RSC_TASK_CLAIM-UNSOURCED"


def test_research_planner_ignores_allowed_claims():
    claim = ClaimRecord(
        claim_id="CLAIM-ALLOWED",
        text="A test claim",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=["SRC-1"]
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        task = plan_research_for_claim(claim, "GAP-001", tmp_path)
        assert task is None
