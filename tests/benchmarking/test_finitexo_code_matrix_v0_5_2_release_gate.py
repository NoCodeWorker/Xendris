import json
import shutil
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_5.release_gate import (
    APPROVED_DECISION,
    ReleaseGateConfig,
    evaluate_release_gate,
    write_release_gate_artifacts,
)


DATASET_ROOT = Path("benchmarks/finitexo_code_matrix_v0_4_3")
V0_5_RUN = Path("runs/finitexo_code_matrix_v0_5_provider_smoke")
V0_5_1_RUN = Path("runs/finitexo_code_matrix_v0_5_1_real_provider_smoke")
V0_5_2_RUN = Path("runs/finitexo_code_matrix_v0_5_2_real_provider_execution")
DOCS = (
    Path("docs/status/FINITEXO_CODE_MATRIX_V0_5_PROVIDER_SMOKE_FROZEN_N10.md"),
    Path("docs/status/FINITEXO_CODE_MATRIX_V0_5_1_REAL_PROVIDER_SMOKE_FROZEN_N10.md"),
    Path("docs/status/FINITEXO_CODE_MATRIX_V0_5_2_REAL_PROVIDER_EXECUTION_FROZEN_N10.md"),
)


def _copy_tree(source: Path, target: Path) -> None:
    shutil.copytree(source, target)


def _fixture(tmp_path: Path) -> ReleaseGateConfig:
    run_root = tmp_path / "runs"
    docs_root = tmp_path / "docs" / "status"
    _copy_tree(V0_5_RUN, run_root / V0_5_RUN.name)
    _copy_tree(V0_5_1_RUN, run_root / V0_5_1_RUN.name)
    _copy_tree(V0_5_2_RUN, run_root / V0_5_2_RUN.name)
    docs_root.mkdir(parents=True)
    copied_docs = []
    for doc in DOCS:
        target = docs_root / doc.name
        target.write_text(doc.read_text(encoding="utf-8"), encoding="utf-8")
        copied_docs.append(target)
    return ReleaseGateConfig(
        workspace_root=Path("."),
        dataset_path=DATASET_ROOT,
        v0_5_run_dir=run_root / V0_5_RUN.name,
        v0_5_1_run_dir=run_root / V0_5_1_RUN.name,
        v0_5_2_run_dir=run_root / V0_5_2_RUN.name,
        output_dir=tmp_path / "release_gate",
        status_docs=tuple(copied_docs),
    )


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_release_gate_passes_with_expected_no_execution_artifacts(tmp_path):
    config = _fixture(tmp_path)
    summary = evaluate_release_gate(config)
    assert summary["decision"] == APPROVED_DECISION
    assert summary["finding_count"] == 0
    assert summary["real_providers_executed"] is False
    assert summary["env_files_read"] is False


def test_blocks_on_dataset_hash_mismatch(tmp_path):
    config = _fixture(tmp_path)
    path = config.v0_5_2_run_dir / "real_provider_execution_summary.json"
    summary = _load_json(path)
    summary["dataset_hash"] = "bad"
    _write_json(path, summary)
    result = evaluate_release_gate(config)
    assert result["decision"] == "BLOCKED_ARTIFACT_INCONSISTENCY"


def test_blocks_on_manifest_hash_mismatch(tmp_path):
    config = _fixture(tmp_path)
    path = config.v0_5_2_run_dir / "real_provider_execution_summary.json"
    summary = _load_json(path)
    summary["manifest_hash"] = "bad"
    _write_json(path, summary)
    result = evaluate_release_gate(config)
    assert result["decision"] == "BLOCKED_ARTIFACT_INCONSISTENCY"


def test_blocks_on_missing_v0_5_1_artifact(tmp_path):
    config = _fixture(tmp_path)
    (config.v0_5_1_run_dir / "real_provider_gate.json").unlink()
    result = evaluate_release_gate(config)
    assert result["decision"] == "BLOCKED_MISSING_ARTIFACTS"


def test_blocks_on_missing_v0_5_2_artifact(tmp_path):
    config = _fixture(tmp_path)
    (config.v0_5_2_run_dir / "real_provider_gate.json").unlink()
    result = evaluate_release_gate(config)
    assert result["decision"] == "BLOCKED_MISSING_ARTIFACTS"


def test_blocks_on_secret_looking_generated_artifact_content(tmp_path):
    config = _fixture(tmp_path)
    (config.v0_5_2_run_dir / "real_provider_errors.jsonl").write_text(
        '{"error_message_sanitized":"sk-thisshouldnotappear"}\n',
        encoding="utf-8",
    )
    result = evaluate_release_gate(config)
    assert result["decision"] == "BLOCKED_SECRET_RISK"


def test_blocks_on_documentation_overclaim(tmp_path):
    config = _fixture(tmp_path)
    doc = config.status_docs[0]
    doc.write_text("This proves statistically significant provider superiority.\n", encoding="utf-8")
    result = evaluate_release_gate(config)
    assert result["decision"] == "BLOCKED_DOCUMENTATION_OVERCLAIM"


def test_blocks_on_inconsistent_provider_counts(tmp_path):
    config = _fixture(tmp_path)
    path = config.v0_5_2_run_dir / "real_provider_execution_summary.json"
    summary = _load_json(path)
    summary["providers_completed"] = ["deepseek"]
    _write_json(path, summary)
    result = evaluate_release_gate(config)
    assert result["decision"] == "BLOCKED_ARTIFACT_INCONSISTENCY"


def test_blocks_if_real_execution_artifacts_contain_mock_fallback_response(tmp_path):
    config = _fixture(tmp_path)
    (config.v0_5_2_run_dir / "real_provider_responses.jsonl").write_text(
        '{"provider_name":"deepseek","response_text":"mock fallback response"}\n',
        encoding="utf-8",
    )
    result = evaluate_release_gate(config)
    assert result["decision"] == "BLOCKED_REAL_EXECUTION_PATH_UNSAFE"


def test_blocks_if_cost_nonzero_while_no_providers_attempted(tmp_path):
    config = _fixture(tmp_path)
    path = config.v0_5_2_run_dir / "real_provider_execution_summary.json"
    summary = _load_json(path)
    summary["total_estimated_cost_usd"] = 0.01
    _write_json(path, summary)
    result = evaluate_release_gate(config)
    assert result["decision"] == "BLOCKED_ARTIFACT_INCONSISTENCY"


def test_blocks_if_responses_exist_while_task_attempts_completed_zero(tmp_path):
    config = _fixture(tmp_path)
    (config.v0_5_2_run_dir / "real_provider_responses.jsonl").write_text(
        '{"provider_name":"deepseek","response_text":"real response"}\n',
        encoding="utf-8",
    )
    result = evaluate_release_gate(config)
    assert result["decision"] == "BLOCKED_ARTIFACT_INCONSISTENCY"


def test_write_release_gate_artifacts(tmp_path):
    config = _fixture(tmp_path)
    summary = write_release_gate_artifacts(config)
    assert summary["decision"] == APPROVED_DECISION
    assert (config.output_dir / "release_gate_summary.json").exists()
    assert (config.output_dir / "release_gate_report.md").exists()
    assert (config.output_dir / "release_gate_findings.jsonl").exists()
