import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_6_0.real_provider_controlled_run import (
    ControlledProviderResult,
    ControlledProviderSpec,
    ControlledRunConfig,
    run_controlled_provider_benchmark,
    write_controlled_run_artifacts,
)


COMPLETED = "REAL_PROVIDER_CONTROLLED_RUN_COMPLETED_DIAGNOSTIC_ONLY"
PARTIAL = "REAL_PROVIDER_CONTROLLED_RUN_PARTIAL_DIAGNOSTIC_ONLY"
BLOCKED_INSUFFICIENT_TASKS = "REAL_PROVIDER_CONTROLLED_RUN_BLOCKED_INSUFFICIENT_TASKS"
BLOCKED_PROVIDER_CONFIGURATION = "REAL_PROVIDER_CONTROLLED_RUN_BLOCKED_PROVIDER_CONFIGURATION"


def _write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def _dataset(tmp_path: Path, count: int = 30, dataset_hash: str = "dataset-hash", manifest_hash: str = "manifest-hash") -> Path:
    root = tmp_path / "dataset"
    _write_json(root / "frozen_dataset_hashes.json", {"dataset_hash": dataset_hash, "manifest_hash": manifest_hash})
    _write_json(root / "frozen_dataset_manifest.json", {"dataset_name": "test_dataset", "dataset_version": "test-v"})
    for index in range(1, count + 1):
        _write_json(
            root / "tasks" / f"frozen_task_{index:03d}.json",
            {
                "task_id": f"task-{index:03d}",
                "task_version": "test-v",
                "content_hash": f"hash-{index:03d}",
                "prompt": "Return a diagnostic answer and mention the API contract.",
            },
        )
    return root


def _ready(tmp_path: Path, ready: bool = True) -> Path:
    path = tmp_path / "v057.json"
    _write_json(
        path,
        {
            "final_decision": "REAL_PROVIDER_REPORT_ADMISSIBILITY_APPROVED_DIAGNOSTIC_ONLY" if ready else "BLOCKED",
            "ready_for_v0_6_0_controlled_run": ready,
        },
    )
    return path


def _config(tmp_path: Path, task_count: int = 30, ready: bool = True, providers=None, budget=0.50) -> ControlledRunConfig:
    return ControlledRunConfig(
        dataset_path=_dataset(tmp_path, count=task_count),
        readiness_summary_path=_ready(tmp_path, ready=ready),
        output_dir=tmp_path / "out",
        providers=providers
        or (
            ControlledProviderSpec("deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, "unused"),
            ControlledProviderSpec("openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, "unused"),
        ),
        expected_dataset_hash="dataset-hash",
        expected_manifest_hash="manifest-hash",
        budget_cap_usd=budget,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )


def _adapter(provider, task, config):
    return ControlledProviderResult(
        raw_response_text=f"{task['task_id']} diagnostic response preserves API contract.",
        estimated_cost_usd=provider.estimated_cost_per_task_usd,
    )


def test_preflight_blocks_if_v0_5_7_readiness_summary_missing(tmp_path):
    config = _config(tmp_path)
    config = ControlledRunConfig(
        dataset_path=config.dataset_path,
        readiness_summary_path=tmp_path / "missing.json",
        output_dir=config.output_dir,
        providers=config.providers,
        expected_dataset_hash=config.expected_dataset_hash,
        expected_manifest_hash=config.expected_manifest_hash,
        environ=config.environ,
    )
    result = run_controlled_provider_benchmark(config, adapter=_adapter)
    assert result["final_decision"] != COMPLETED
    assert "missing_v0_5_7_readiness_summary" in result["preflight"]["blockers"]


def test_preflight_blocks_if_v0_5_7_not_ready(tmp_path):
    result = run_controlled_provider_benchmark(_config(tmp_path, ready=False), adapter=_adapter)
    assert result["final_decision"] != COMPLETED
    assert "v0_5_7_not_ready_for_v0_6_0" in result["preflight"]["blockers"]


def test_insufficient_tasks_blocks(tmp_path):
    result = run_controlled_provider_benchmark(_config(tmp_path, task_count=10), adapter=_adapter)
    assert result["final_decision"] == BLOCKED_INSUFFICIENT_TASKS


def test_provider_list_must_be_exactly_deepseek_and_openai(tmp_path):
    providers = (ControlledProviderSpec("deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, "unused"),)
    result = run_controlled_provider_benchmark(_config(tmp_path, providers=providers), adapter=_adapter)
    assert result["final_decision"] == BLOCKED_PROVIDER_CONFIGURATION


def test_expected_response_cardinality_for_n30_x_2_is_60(tmp_path):
    summary = write_controlled_run_artifacts(run_controlled_provider_benchmark(_config(tmp_path), adapter=_adapter))
    assert summary["expected_responses"] == 60
    assert summary["responses_count"] == 60
    assert summary["scores_count"] == 60
    assert summary["metadata_rows_count"] == 60


def test_completed_run_summary_remains_diagnostic_only(tmp_path):
    summary = write_controlled_run_artifacts(run_controlled_provider_benchmark(_config(tmp_path), adapter=_adapter))
    assert summary["final_decision"] == COMPLETED
    assert summary["diagnostic_only"] is True


def test_no_stronger_claims_are_authorized(tmp_path):
    summary = write_controlled_run_artifacts(run_controlled_provider_benchmark(_config(tmp_path), adapter=_adapter))
    assert summary["statistical_claim_authorized"] is False
    assert summary["provider_superiority_claim_authorized"] is False
    assert summary["xendris_superiority_claim_authorized"] is False
    assert summary["production_readiness_claim_authorized"] is False
    assert summary["universal_benchmark_claim_authorized"] is False


def test_partial_provider_failure_cannot_produce_completed_decision(tmp_path):
    def failing_adapter(provider, task, config):
        if provider.provider_name == "openai":
            raise RuntimeError("provider error")
        return _adapter(provider, task, config)

    summary = write_controlled_run_artifacts(run_controlled_provider_benchmark(_config(tmp_path), adapter=failing_adapter))
    assert summary["final_decision"] == PARTIAL
    assert summary["provider_failure_count"] == 30


def test_budget_cap_breach_blocks_before_execution(tmp_path):
    config = _config(tmp_path, budget=0.00001)
    summary = write_controlled_run_artifacts(run_controlled_provider_benchmark(config, adapter=_adapter))
    assert summary["final_decision"] == "REAL_PROVIDER_CONTROLLED_RUN_BLOCKED_BUDGET_CAP"


def test_run_manifest_preserves_dataset_hash_and_task_ids(tmp_path):
    config = _config(tmp_path)
    summary = write_controlled_run_artifacts(run_controlled_provider_benchmark(config, adapter=_adapter))
    manifest = json.loads((config.output_dir / "run_manifest.json").read_text(encoding="utf-8"))
    assert manifest["dataset_hash"] == "dataset-hash"
    assert len(set(manifest["task_ids"])) == 30
    assert summary["dataset_hash_verified"] is True
