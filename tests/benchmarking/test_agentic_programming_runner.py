from __future__ import annotations

import os

import pytest

from xendris.benchmarking.agentic_programming.dataset import load_dataset
from xendris.benchmarking.agentic_programming.runner import (
    _check_api_contract,
    _check_forbidden_files,
    _generate_agent_patch,
    run_benchmark,
)
from xendris.benchmarking.agentic_programming.types import AgentVariant, BenchmarkConfig, TaskSample


class TestGenerateAgentPatch:
    def test_dry_run_returns_default_patch(self):
        task = TaskSample(
            sample_id="AP-TEST",
            task_type="bug_fixing",
            category="bug_fixing",
            issue_description="fix bug",
            allowed_files=("src/solver.py",),
            forbidden_files=("tests/",),
            visible_test_command="pytest",
            hidden_test_command="pytest",
            success_criteria="pass",
            risk_level="low",
            max_iterations=5,
            expected_public_api=("solve",),
            disallowed_dependencies=(),
            fixture_dir="/tmp",
        )
        success, patch, error, metadata = _generate_agent_patch(task, AgentVariant.BASE_AGENT, "dry-run", "xendris.benchmarking.agentic_programming.agents")
        assert success is True
        assert "def solve()" in patch
        assert error == ""
        assert metadata == {}


class TestCheckApiContract:
    def test_expected_api_present(self):
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
            expected_public_api=("count_items",),
            disallowed_dependencies=(),
            fixture_dir="benchmarks/agentic_programming/v0_1/fixtures/task_001",
        )
        repo = os.path.join(task.fixture_dir, "repo")
        assert _check_api_contract(task, repo) is True

    def test_expected_api_absent(self):
        task = TaskSample(
            sample_id="AP-TEST",
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
            expected_public_api=("nonexistent_function",),
            disallowed_dependencies=(),
            fixture_dir="benchmarks/agentic_programming/v0_1/fixtures/task_001",
        )
        repo = os.path.join(task.fixture_dir, "repo")
        assert _check_api_contract(task, repo) is False

    def test_no_expected_api_returns_true(self):
        task = TaskSample(
            sample_id="AP-TEST",
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
            expected_public_api=(),
            disallowed_dependencies=(),
            fixture_dir="benchmarks/agentic_programming/v0_1/fixtures/task_001",
        )
        repo = os.path.join(task.fixture_dir, "repo")
        assert _check_api_contract(task, repo) is True


class TestCheckForbiddenFiles:
    def test_no_forbidden_files_touched(self):
        assert _check_forbidden_files(["src/solver.py"], ("tests/",)) is True

    def test_forbidden_file_touched(self):
        assert _check_forbidden_files(["tests/test_solver.py"], ("tests/",)) is False

    def test_empty_forbidden_list(self):
        assert _check_forbidden_files(["anything"], ()) is True

    def test_forbidden_in_path(self):
        assert _check_forbidden_files(["src/tests/helper.py"], ("tests/",)) is False


class TestRunBenchmarkDryRun:
    def test_dry_run_returns_all_results(self):
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.BASE_AGENT, AgentVariant.XENDRIS_AGENT),
            execution_mode="dry-run",
            output_dir="/tmp/benchmark_out",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=2,
            seed=42,
        )
        results = run_benchmark(config)
        expected_count = 20 * 2
        assert len(results) == expected_count
        assert all(r.patch_applied for r in results)
        assert all(r.error_message is None for r in results)

    def test_all_variants_dry_run(self):
        original_variants = (
            AgentVariant.BASE_AGENT,
            AgentVariant.XENDRIS_AGENT,
            AgentVariant.XENDRIS_CALIBRATED_AGENT,
        )
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=original_variants,
            execution_mode="dry-run",
            output_dir="/tmp/benchmark_out",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
        )
        results = run_benchmark(config)
        variants = set(r.agent_variant for r in results)
        assert variants == {"base_agent", "xendris_agent", "xendris_calibrated_agent"}
