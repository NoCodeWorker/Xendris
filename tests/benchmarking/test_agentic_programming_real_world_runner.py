from __future__ import annotations

import os
import tempfile
from unittest.mock import patch

import pytest

from xendris.benchmarking.agentic_programming.types import AgentVariant, BenchmarkConfig, TaskResult
from xendris.benchmarking.agentic_programming.runner import (
    _run_real_world_single_task,
    _copy_source_files_to_sandbox,
    _run_validation,
)
from xendris.benchmarking.agentic_programming.real_world_tasks import RealWorldTask, load_real_world_tasks


MOCK_PATCH = '{"src/solver.py": "def solve():\\n    return 42\\n"}'


@pytest.fixture
def mock_deepseek_call():
    with patch("xendris.benchmarking.agentic_programming.agents.deepseek_provider.call_deepseek") as mock:
        mock.return_value = (MOCK_PATCH, 1500.0, 0.0015, "deepseek-v4-flash", None)
        yield mock


@pytest.fixture
def mock_openai_call():
    with patch("xendris.benchmarking.agentic_programming.agents.openai_provider.call_openai") as mock:
        mock.return_value = (MOCK_PATCH, 2000.0, 0.002, "gpt-4.1-mini", None, 100, 50)
        yield mock


class TestCopySourceFiles:
    def test_copies_single_file_to_sandbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = os.path.join(tmp, "repo_root")
            os.makedirs(os.path.dirname(os.path.join(repo_root, "xendris/benchmarking/agentic_programming")))
            src_file = os.path.join(repo_root, "xendris/benchmarking/agentic_programming/report.py")
            os.makedirs(os.path.dirname(src_file))
            with open(src_file, "w") as f:
                f.write("# original content\n")

            sandbox = os.path.join(tmp, "sandbox")
            os.makedirs(sandbox)
            task = RealWorldTask(
                task_id="RW-TEST",
                title="test",
                repository_area="test",
                instruction="test",
                source_files=("xendris/benchmarking/agentic_programming/report.py",),
                expected_files_allowed=("xendris/benchmarking/agentic_programming/report.py",),
                forbidden_files=("tests/",),
                validation_command="python --version",
                success_criteria="test",
                risk_level="low",
                oracle_notes="test",
            )

            working_dir = _copy_source_files_to_sandbox(task, sandbox, repo_root)
            copied = os.path.join(working_dir, "xendris/benchmarking/agentic_programming/report.py")
            assert os.path.isfile(copied)

    def test_missing_source_file_does_not_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = os.path.join(tmp, "repo_root")
            os.makedirs(repo_root)
            sandbox = os.path.join(tmp, "sandbox")
            os.makedirs(sandbox)
            task = RealWorldTask(
                task_id="RW-TEST",
                title="test",
                repository_area="test",
                instruction="test",
                source_files=("nonexistent.py",),
                expected_files_allowed=("nonexistent.py",),
                forbidden_files=("tests/",),
                validation_command="python --version",
                success_criteria="test",
                risk_level="low",
                oracle_notes="test",
            )
            working_dir = _copy_source_files_to_sandbox(task, sandbox, repo_root)
            assert os.path.isdir(working_dir)


class TestValidationRunner:
    def test_run_validation_success(self):
        fixture_dir = tempfile.mkdtemp()
        repo_dir = os.path.join(fixture_dir, "repo")
        os.makedirs(repo_dir)
        ok, output = _run_validation(fixture_dir, "python --version")
        assert ok is True

    def test_run_validation_failure(self):
        fixture_dir = tempfile.mkdtemp()
        repo_dir = os.path.join(fixture_dir, "repo")
        os.makedirs(repo_dir)
        ok, output = _run_validation(fixture_dir, "python -c \"exit(1)\"")
        assert ok is False


class TestRealWorldSingleTask:
    def test_real_world_supports_task_suite(self):
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
            execution_mode="live",
            output_dir="/tmp/rw_test",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
            task_suite="real_world_v0_2",
        )
        assert config.task_suite == "real_world_v0_2"

    def test_dry_run_real_world_task(self, monkeypatch):
        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        config = BenchmarkConfig(
            dataset_path="",
            agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
            execution_mode="dry-run",
            output_dir="/tmp/rw_test",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
            task_suite="real_world_v0_2",
        )

        from xendris.benchmarking.agentic_programming.runner import run_benchmark
        results = run_benchmark(config)
        assert len(results) == 10
        for r in results:
            assert r.patch_applied is True

    def test_deepseek_real_world_task(self, mock_deepseek_call):
        with tempfile.TemporaryDirectory() as tmp:
            task = load_real_world_tasks("real_world_v0_2")[0]
            config = BenchmarkConfig(
                dataset_path="",
                agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
                execution_mode="live",
                output_dir="/tmp/rw_test",
                agent_module="xendris.benchmarking.agentic_programming.agents",
                max_concurrent=1,
                seed=42,
                provider="deepseek",
                model="deepseek-v4-flash",
                transport="direct",
                task_suite="real_world_v0_2",
            )
            result = _run_real_world_single_task(task, AgentVariant.DEEPSEEK_BASE_AGENT, config, tmp)
            assert result.patch_applied is True
            assert result.provider == "deepseek"

    def test_openai_real_world_task(self, mock_openai_call):
        with tempfile.TemporaryDirectory() as tmp:
            task = load_real_world_tasks("real_world_v0_2")[0]
            config = BenchmarkConfig(
                dataset_path="",
                agent_variants=(AgentVariant.OPENAI_BASE_AGENT,),
                execution_mode="live",
                output_dir="/tmp/rw_test",
                agent_module="xendris.benchmarking.agentic_programming.agents",
                max_concurrent=1,
                seed=42,
                provider="openai",
                model="gpt-4.1-mini",
                transport="direct",
                task_suite="real_world_v0_2",
            )
            result = _run_real_world_single_task(task, AgentVariant.OPENAI_BASE_AGENT, config, tmp)
            assert result.patch_applied is True
            assert result.provider == "openai"

    def test_no_secrets_in_real_world_result(self, mock_deepseek_call):
        with tempfile.TemporaryDirectory() as tmp:
            task = load_real_world_tasks("real_world_v0_2")[0]
            config = BenchmarkConfig(
                dataset_path="",
                agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
                execution_mode="live",
                output_dir="/tmp/rw_test",
                agent_module="xendris.benchmarking.agentic_programming.agents",
                max_concurrent=1,
                seed=42,
                provider="deepseek",
                transport="direct",
                task_suite="real_world_v0_2",
            )
            result = _run_real_world_single_task(task, AgentVariant.DEEPSEEK_BASE_AGENT, config, tmp)
            d = result.to_dict()
            text = str(d)
            for secret_pattern in ["sk-", "Authorization:", "Bearer"]:
                assert secret_pattern not in text, f"Secret pattern '{secret_pattern}' leaked in result"


class TestRealWorldCLI:
    def test_cli_accepts_task_suite_argument(self):
        import subprocess
        result = subprocess.run(
            ["python", "scripts/run_agentic_programming_benchmark.py", "--task-suite", "real_world_v0_2", "--preflight-only"],
            capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), "..", ".."),
        )
        assert result.returncode in (0, 1)


class TestLiveProviderBlockers:
    """Live-mode blocking gates on real_world v0_2 results."""

    def test_provider_call_fields_populated_deepseek(self, mock_deepseek_call):
        with tempfile.TemporaryDirectory() as tmp:
            task = load_real_world_tasks("real_world_v0_2")[0]
            config = BenchmarkConfig(
                dataset_path="",
                agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
                execution_mode="live",
                output_dir="/tmp/rw_test",
                agent_module="xendris.benchmarking.agentic_programming.agents",
                max_concurrent=1, seed=42,
                provider="deepseek", model="deepseek-v4-flash", transport="direct",
                task_suite="real_world_v0_2",
            )
            result = _run_real_world_single_task(task, AgentVariant.DEEPSEEK_BASE_AGENT, config, tmp)
            assert result.provider_call_attempted is True
            assert result.provider_call_succeeded is True
            assert result.block_reason is None

    def test_provider_call_fields_populated_openai(self, mock_openai_call):
        with tempfile.TemporaryDirectory() as tmp:
            task = load_real_world_tasks("real_world_v0_2")[0]
            config = BenchmarkConfig(
                dataset_path="",
                agent_variants=(AgentVariant.OPENAI_BASE_AGENT,),
                execution_mode="live",
                output_dir="/tmp/rw_test",
                agent_module="xendris.benchmarking.agentic_programming.agents",
                max_concurrent=1, seed=42,
                provider="openai", model="gpt-4.1-mini", transport="direct",
                task_suite="real_world_v0_2",
            )
            result = _run_real_world_single_task(task, AgentVariant.OPENAI_BASE_AGENT, config, tmp)
            assert result.provider_call_attempted is True
            assert result.provider_call_succeeded is True
            assert result.block_reason is None

    def test_latency_and_cost_recorded(self, mock_deepseek_call):
        with tempfile.TemporaryDirectory() as tmp:
            task = load_real_world_tasks("real_world_v0_2")[0]
            config = BenchmarkConfig(
                dataset_path="",
                agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
                execution_mode="live",
                output_dir="/tmp/rw_test",
                agent_module="xendris.benchmarking.agentic_programming.agents",
                max_concurrent=1, seed=42,
                provider="deepseek", model="deepseek-v4-flash", transport="direct",
                task_suite="real_world_v0_2",
            )
            result = _run_real_world_single_task(task, AgentVariant.DEEPSEEK_BASE_AGENT, config, tmp)
            assert result.latency_ms is not None
            assert result.cost_estimate is not None

    def test_latency_and_cost_with_openai(self, mock_openai_call):
        with tempfile.TemporaryDirectory() as tmp:
            task = load_real_world_tasks("real_world_v0_2")[0]
            config = BenchmarkConfig(
                dataset_path="",
                agent_variants=(AgentVariant.OPENAI_BASE_AGENT,),
                execution_mode="live",
                output_dir="/tmp/rw_test",
                agent_module="xendris.benchmarking.agentic_programming.agents",
                max_concurrent=1, seed=42,
                provider="openai", model="gpt-4.1-mini", transport="direct",
                task_suite="real_world_v0_2",
            )
            result = _run_real_world_single_task(task, AgentVariant.OPENAI_BASE_AGENT, config, tmp)
            assert result.latency_ms is not None
            assert result.cost_estimate is not None

    def test_blocked_dummy_patch_in_live_mode(self):
        """Non-live variant in live mode with no provider routes dummy patch -> BLOCKED."""
        with tempfile.TemporaryDirectory() as tmp:
            task = load_real_world_tasks("real_world_v0_2")[0]
            config = BenchmarkConfig(
                dataset_path="",
                agent_variants=(AgentVariant.BASE_AGENT,),
                execution_mode="live",
                output_dir="/tmp/rw_test",
                agent_module="xendris.benchmarking.agentic_programming.agents",
                max_concurrent=1, seed=42,
                provider=None, model=None, transport=None,
                task_suite="real_world_v0_2",
            )
            result = _run_real_world_single_task(task, AgentVariant.BASE_AGENT, config, tmp)
            assert result.block_reason == "BLOCKED_DUMMY_PATCH_IN_LIVE_MODE"

    def test_blocked_cost_or_latency_not_recorded(self):
        """Successful provider call without latency/cost -> BLOCKED."""
        with patch("xendris.benchmarking.agentic_programming.agents.openai_provider.call_openai") as mock:
            mock.return_value = (MOCK_PATCH, None, None, "gpt-4.1-mini", None, 100, 50)
            with tempfile.TemporaryDirectory() as tmp:
                task = load_real_world_tasks("real_world_v0_2")[0]
                config = BenchmarkConfig(
                    dataset_path="",
                    agent_variants=(AgentVariant.OPENAI_BASE_AGENT,),
                    execution_mode="live",
                    output_dir="/tmp/rw_test",
                    agent_module="xendris.benchmarking.agentic_programming.agents",
                    max_concurrent=1, seed=42,
                    provider="openai", model="gpt-4.1-mini", transport="direct",
                    task_suite="real_world_v0_2",
                )
                result = _run_real_world_single_task(task, AgentVariant.OPENAI_BASE_AGENT, config, tmp)
            assert result.block_reason == "BLOCKED_COST_OR_LATENCY_NOT_RECORDED"

    def test_base_agent_routed_through_openai_in_live_mode(self, mock_openai_call):
        """base_agent with provider=openai routes through openai_base_agent."""
        with tempfile.TemporaryDirectory() as tmp:
            task = load_real_world_tasks("real_world_v0_2")[0]
            config = BenchmarkConfig(
                dataset_path="",
                agent_variants=(AgentVariant.BASE_AGENT,),
                execution_mode="live",
                output_dir="/tmp/rw_test",
                agent_module="xendris.benchmarking.agentic_programming.agents",
                max_concurrent=1, seed=42,
                provider="openai", model="gpt-5.5", transport="direct",
                task_suite="real_world_v0_2",
            )
            result = _run_real_world_single_task(task, AgentVariant.BASE_AGENT, config, tmp)
            assert result.provider == "openai"
            assert result.model == "gpt-5.5"
            assert result.provider_call_attempted is True
            assert result.provider_call_succeeded is True
            assert result.block_reason is None
            assert result.patch_content.strip() not in {"def solve():\n    pass\n", "def solve():\n    return 42\n"}

    def test_xendris_agent_routed_through_openai(self, mock_openai_call):
        """xendris_agent with provider=openai routes through openai_xendris_agent."""
        with tempfile.TemporaryDirectory() as tmp:
            task = load_real_world_tasks("real_world_v0_2")[0]
            config = BenchmarkConfig(
                dataset_path="",
                agent_variants=(AgentVariant.XENDRIS_AGENT,),
                execution_mode="live",
                output_dir="/tmp/rw_test",
                agent_module="xendris.benchmarking.agentic_programming.agents",
                max_concurrent=1, seed=42,
                provider="openai", model="gpt-5.5", transport="direct",
                task_suite="real_world_v0_2",
            )
            result = _run_real_world_single_task(task, AgentVariant.XENDRIS_AGENT, config, tmp)
            assert result.provider_call_attempted is True
            assert result.provider_call_succeeded is True
            assert result.block_reason is None

    def test_dry_run_no_blockers(self):
        """dry-run mode does not trigger live blockers."""
        with tempfile.TemporaryDirectory() as tmp:
            task = load_real_world_tasks("real_world_v0_2")[0]
            config = BenchmarkConfig(
                dataset_path="",
                agent_variants=(AgentVariant.BASE_AGENT,),
                execution_mode="dry-run",
                output_dir="/tmp/rw_test",
                agent_module="xendris.benchmarking.agentic_programming.agents",
                max_concurrent=1, seed=42,
                provider="openai", model="gpt-5.5", transport=None,
                task_suite="real_world_v0_2",
            )
            result = _run_real_world_single_task(task, AgentVariant.BASE_AGENT, config, tmp)
            assert result.block_reason is None
            assert result.provider_call_attempted is False
