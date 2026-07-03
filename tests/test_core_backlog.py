import tempfile
from pathlib import Path
from phyng.loop.schemas import BacklogTask
from phyng.loop.backlog import load_backlog, save_backlog, update_backlog_md_report


def test_backlog_tasks_persistence_and_reporting():
    task = BacklogTask(
        task_id="TASK-GAP-1",
        title="Resolve gap: GAP_SRC_CLAIM_EINSTEIN",
        task_type="MISSING_SOURCE",
        priority="P1",
        status="TODO",
        blocked_by=["TASK-GAP-0"],
        acceptance_criteria=["Link claim to source"]
    )
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Save backlog
        save_backlog([task], tmp_path)
        
        # Load backlog
        loaded = load_backlog(tmp_path)
        assert len(loaded) == 1
        assert loaded[0].task_id == "TASK-GAP-1"
        assert loaded[0].blocked_by == ["TASK-GAP-0"]
        
        # Update markdown
        md_path = update_backlog_md_report(loaded, tmp_path)
        assert md_path.exists()
        assert md_path.name == "phygn_core_backlog.md"
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "TASK-GAP-1" in content
            assert "TODO" in content
            assert "TASK-GAP-0" in content
