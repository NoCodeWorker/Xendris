"""
tests/test_baseline_literature_requirements.py

Tests for BaselineSourceRequirement creation and ResearchTask generation.
"""

import tempfile
from pathlib import Path

from phyng.baselines.source_support import build_baseline_source_requirements
from phyng.baselines.visibility_decay import ensure_baseline_research_tasks
from phyng.rag.research_planner import list_research_tasks


def test_baseline_requirements_defined():
    reqs = build_baseline_source_requirements()
    assert len(reqs) >= 3
    ids = [r.requirement_id for r in reqs]
    assert "BSR-001" in ids
    assert "BSR-002" in ids


def test_all_requirements_awaiting_by_default():
    reqs = build_baseline_source_requirements()
    for r in reqs:
        assert r.status == "AWAITING_SOURCE_INGESTION"


def test_missing_visibility_source_creates_requirement():
    """When no sources exist, research tasks must be created for each baseline category."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        task_ids = ensure_baseline_research_tasks(root)
        tasks = list_research_tasks(root)
        assert len(tasks) >= 4
        task_id_set = {t.task_id for t in tasks}
        assert "RT-BASELINE-SRC-001" in task_id_set
        assert "RT-BASELINE-SRC-002" in task_id_set


def test_research_tasks_not_duplicated():
    """Running twice should not duplicate tasks."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        ids1 = ensure_baseline_research_tasks(root)
        ids2 = ensure_baseline_research_tasks(root)
        tasks = list_research_tasks(root)
        # All task_ids are unique
        all_ids = [t.task_id for t in tasks]
        assert len(all_ids) == len(set(all_ids))
