"""
Tests for phyng.evidence.source_acquisition_tasks
"""

import json
from pathlib import Path

import pytest

from phyng.evidence.source_acquisition_tasks import (
    ALL_CATEGORIES,
    SourceAcquisitionTask,
    generate_source_acquisition_tasks,
    get_missing_categories,
)


class TestGenerateSourceAcquisitionTasks:
    def test_generates_all_five_tasks(self, tmp_path: Path) -> None:
        tasks = generate_source_acquisition_tasks(tmp_path)
        assert len(tasks) == 5

    def test_all_categories_covered(self, tmp_path: Path) -> None:
        tasks = generate_source_acquisition_tasks(tmp_path)
        categories = {t.category for t in tasks}
        assert categories == set(ALL_CATEGORIES)

    def test_json_files_written(self, tmp_path: Path) -> None:
        generate_source_acquisition_tasks(tmp_path)
        out_dir = tmp_path / "rag" / "research_tasks"
        json_files = list(out_dir.glob("*.json"))
        assert len(json_files) == 5

    def test_json_structure_valid(self, tmp_path: Path) -> None:
        generate_source_acquisition_tasks(tmp_path)
        out_dir = tmp_path / "rag" / "research_tasks"
        for jf in out_dir.glob("*.json"):
            data = json.loads(jf.read_text(encoding="utf-8"))
            assert "task_id" in data
            assert "category" in data
            assert "description" in data
            assert "desired_support_types" in data
            assert "suggested_queries" in data
            assert "requirement_id" in data
            assert "priority" in data
            assert "status" in data

    def test_all_open_when_no_covered(self, tmp_path: Path) -> None:
        tasks = generate_source_acquisition_tasks(tmp_path, covered_categories=[])
        assert all(t.status == "OPEN" for t in tasks)

    def test_covered_category_marked_resolved(self, tmp_path: Path) -> None:
        tasks = generate_source_acquisition_tasks(
            tmp_path, covered_categories=["VISIBILITY_DECAY"]
        )
        for t in tasks:
            if t.category == "VISIBILITY_DECAY":
                assert t.status == "RESOLVED"
            else:
                assert t.status == "OPEN"

    def test_all_resolved_when_all_covered(self, tmp_path: Path) -> None:
        tasks = generate_source_acquisition_tasks(
            tmp_path, covered_categories=ALL_CATEGORIES
        )
        assert all(t.status == "RESOLVED" for t in tasks)

    def test_idempotent_run(self, tmp_path: Path) -> None:
        tasks1 = generate_source_acquisition_tasks(tmp_path)
        tasks2 = generate_source_acquisition_tasks(tmp_path)
        assert len(tasks1) == len(tasks2)

    def test_task_ids_unique(self, tmp_path: Path) -> None:
        tasks = generate_source_acquisition_tasks(tmp_path)
        ids = [t.task_id for t in tasks]
        assert len(ids) == len(set(ids))

    def test_visibility_decay_task_id(self, tmp_path: Path) -> None:
        tasks = generate_source_acquisition_tasks(tmp_path)
        vd = next(t for t in tasks if t.category == "VISIBILITY_DECAY")
        assert vd.task_id == "RT-V1-1-SRC-VISIBILITY_DECAY"

    def test_detectability_task_priority_medium(self, tmp_path: Path) -> None:
        tasks = generate_source_acquisition_tasks(tmp_path)
        det = next(t for t in tasks if t.category == "DETECTABILITY_OR_VISIBILITY_THRESHOLD")
        assert det.priority == "MEDIUM"


class TestGetMissingCategories:
    def test_all_open_returns_all(self, tmp_path: Path) -> None:
        tasks = generate_source_acquisition_tasks(tmp_path)
        missing = get_missing_categories(tasks)
        assert set(missing) == set(ALL_CATEGORIES)

    def test_one_resolved_not_in_missing(self, tmp_path: Path) -> None:
        tasks = generate_source_acquisition_tasks(
            tmp_path, covered_categories=["VISIBILITY_DECAY"]
        )
        missing = get_missing_categories(tasks)
        assert "VISIBILITY_DECAY" not in missing
        assert len(missing) == 4
