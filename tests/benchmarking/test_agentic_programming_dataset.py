from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest

from xendris.benchmarking.agentic_programming.dataset import (
    get_manifest_path,
    get_repo_path,
    load_dataset,
    validate_fixture,
)
from xendris.benchmarking.agentic_programming.types import TaskSample


class TestLoadDataset:
    def test_load_from_v0_1_directory(self):
        path = "benchmarks/agentic_programming/v0_1"
        samples = load_dataset(path)
        assert len(samples) == 20
        assert all(isinstance(s, TaskSample) for s in samples)
        assert samples[0].sample_id == "AP-001"

    def test_load_from_subdirectory(self):
        path = "benchmarks/agentic_programming"
        samples = load_dataset(path)
        assert len(samples) == 20

    def test_load_via_dataset_path_direct(self):
        path = "benchmarks/agentic_programming/v0_1"
        samples = load_dataset(path)
        ids = [s.sample_id for s in samples]
        assert "AP-001" in ids
        assert "AP-020" in ids

    def test_load_nonexistent_path_raises(self):
        with pytest.raises(FileNotFoundError):
            load_dataset("nonexistent/path")

    def test_load_empty_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "dataset.json"), "w") as f:
                json.dump({"samples": []}, f)
            samples = load_dataset(tmp)
            assert samples == []


class TestGetPaths:
    def test_get_repo_path(self):
        import os as _os
        task = TaskSample(
            sample_id="AP-001",
            task_type="bug_fixing",
            category="bug_fixing",
            issue_description="test",
            allowed_files=("src/solver.py",),
            forbidden_files=("tests/",),
            visible_test_command="pytest",
            hidden_test_command="pytest",
            success_criteria="pass",
            risk_level="low",
            max_iterations=5,
            expected_public_api=("solve",),
            disallowed_dependencies=(),
            fixture_dir="/tmp/fixtures",
        )
        expected = _os.path.join("/tmp/fixtures", "repo")
        assert get_repo_path(task) == expected

    def test_get_manifest_path(self):
        import os as _os
        task = TaskSample(
            sample_id="AP-001",
            task_type="bug_fixing",
            category="bug_fixing",
            issue_description="test",
            allowed_files=("src/solver.py",),
            forbidden_files=("tests/",),
            visible_test_command="pytest",
            hidden_test_command="pytest",
            success_criteria="pass",
            risk_level="low",
            max_iterations=5,
            expected_public_api=("solve",),
            disallowed_dependencies=(),
            fixture_dir="/tmp/fixtures",
        )
        expected = _os.path.join("/tmp/fixtures", "manifest.json")
        assert get_manifest_path(task) == expected


class TestValidateFixture:
    def test_valid_fixture(self):
        fixtures_base = "benchmarks/agentic_programming/v0_1/fixtures"
        task_001 = [
            t for t in load_dataset("benchmarks/agentic_programming/v0_1")
            if t.sample_id == "AP-001"
        ][0]
        errors = validate_fixture(task_001)
        assert errors == [], f"Validation errors: {errors}"

    def test_invalid_fixture_reports_errors(self):
        task = TaskSample(
            sample_id="AP-999",
            task_type="bug_fixing",
            category="bug_fixing",
            issue_description="test",
            allowed_files=("src/solver.py",),
            forbidden_files=("tests/",),
            visible_test_command="pytest",
            hidden_test_command="pytest",
            success_criteria="pass",
            risk_level="low",
            max_iterations=5,
            expected_public_api=("solve",),
            disallowed_dependencies=(),
            fixture_dir="/nonexistent/path",
        )
        errors = validate_fixture(task)
        assert len(errors) > 0

    def test_all_fixtures_valid(self):
        samples = load_dataset("benchmarks/agentic_programming/v0_1")
        all_errors = {}
        for s in samples:
            errs = validate_fixture(s)
            if errs:
                all_errors[s.sample_id] = errs
        assert not all_errors, f"Fixture validation errors: {all_errors}"
