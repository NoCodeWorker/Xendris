from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from xendris.benchmarking.agentic_programming.real_world_tasks import (
    RealWorldTask,
    load_real_world_tasks,
)


class TestRealWorldTaskSchema:
    def test_task_has_required_fields(self):
        task = load_real_world_tasks("real_world_v0_2")[0]
        assert task.task_id
        assert task.title
        assert task.repository_area
        assert task.instruction
        assert task.source_files
        assert task.expected_files_allowed
        assert task.forbidden_files
        assert task.validation_command
        assert task.success_criteria
        assert task.risk_level
        assert task.oracle_notes

    def test_all_tasks_have_unique_ids(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        ids = [t.task_id for t in tasks]
        assert len(ids) == len(set(ids)), "Duplicate task IDs found"

    def test_all_tasks_have_source_files(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        for t in tasks:
            assert len(t.source_files) >= 1, f"{t.task_id} has no source files"
            for sf in t.source_files:
                assert sf.endswith(".py"), f"{t.task_id} source file {sf} must be .py"

    def test_all_tasks_have_validation_command(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        for t in tasks:
            assert "python" in t.validation_command.lower(), f"{t.task_id} validation must use python"

    def test_forbidden_files_always_includes_tests(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        for t in tasks:
            assert any("tests" in f for f in t.forbidden_files), f"{t.task_id} must forbid tests/"

    def test_risk_level_is_valid(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        valid = {"low", "medium", "high"}
        for t in tasks:
            assert t.risk_level in valid, f"{t.task_id} risk_level must be one of {valid}"

    def test_exactly_ten_tasks(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        assert len(tasks) == 10, f"Expected 10 tasks, got {len(tasks)}"


class TestRealWorldTaskContent:
    def test_format_cost_task_exists(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        task = next(t for t in tasks if t.task_id == "RW-001")
        assert "format_cost" in task.instruction
        assert "report.py" in task.source_files[0]

    def test_is_readable_file_task_exists(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        task = next(t for t in tasks if t.task_id == "RW-002")
        assert "is_readable_file" in task.instruction
        assert "runner.py" in task.source_files[0]

    def test_format_pass_rate_task_exists(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        task = next(t for t in tasks if t.task_id == "RW-003")
        assert "format_pass_rate" in task.instruction

    def test_get_blocked_variant_names_task_exists(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        task = next(t for t in tasks if t.task_id == "RW-004")
        assert "get_blocked_variant_names" in task.instruction
        assert "types.py" in task.source_files[0]

    def test_format_delta_task_exists(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        task = next(t for t in tasks if t.task_id == "RW-005")
        assert "format_delta" in task.instruction

    def test_is_admitted_decision_task_exists(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        task = next(t for t in tasks if t.task_id == "RW-006")
        assert "is_admitted_decision" in task.instruction
        assert "excellence_gate.py" in task.source_files[0]

    def test_safe_filename_task_exists(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        task = next(t for t in tasks if t.task_id == "RW-007")
        assert "safe_filename" in task.instruction
        assert "export_jsonl.py" in task.source_files[0]

    def test_get_warning_variant_names_task_exists(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        task = next(t for t in tasks if t.task_id == "RW-008")
        assert "get_warning_variant_names" in task.instruction

    def test_calculate_total_cost_task_exists(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        task = next(t for t in tasks if t.task_id == "RW-009")
        assert "calculate_total_cost" in task.instruction
        assert "scorer.py" in task.source_files[0]

    def test_get_provider_from_variant_task_exists(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        task = next(t for t in tasks if t.task_id == "RW-010")
        assert "get_provider_from_variant" in task.instruction


class TestForbiddenFileDetection:
    def test_forbidden_file_check_real_world(self):
        from xendris.benchmarking.agentic_programming.runner import _check_forbidden_files

        tasks = load_real_world_tasks("real_world_v0_2")
        for t in tasks:
            assert _check_forbidden_files(["src/solver.py"], t.forbidden_files) is True
            assert _check_forbidden_files(["tests/test_solver.py"], t.forbidden_files) is False

    def test_changed_files_in_forbidden_path(self):
        from xendris.benchmarking.agentic_programming.runner import _check_forbidden_files

        tasks = load_real_world_tasks("real_world_v0_2")
        for t in tasks:
            for f in t.forbidden_files:
                assert _check_forbidden_files([f"{f}some_file.py"], t.forbidden_files) is False


class TestTaskSerialization:
    def test_to_dict_roundtrip(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        for t in tasks:
            d = t.to_dict()
            assert d["task_id"] == t.task_id
            assert d["title"] == t.title
            assert d["repository_area"] == t.repository_area
            assert isinstance(d["source_files"], tuple)
            assert isinstance(d["expected_files_allowed"], tuple)
            assert isinstance(d["forbidden_files"], tuple)

    def test_real_world_task_immutable(self):
        tasks = load_real_world_tasks("real_world_v0_2")
        t = tasks[0]
        with pytest.raises(Exception):
            t.source_files = ("new_file.py",)
