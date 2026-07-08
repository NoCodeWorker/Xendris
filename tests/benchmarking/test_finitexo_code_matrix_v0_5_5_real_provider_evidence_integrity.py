import json
import shutil
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_5.real_provider_evidence_integrity import (
    EvidenceIntegrityConfig,
    evaluate_evidence_integrity,
    write_evidence_integrity_artifacts,
)


SOURCE_RUN = Path("runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized")
APPROVED = "REAL_PROVIDER_EVIDENCE_INTEGRITY_APPROVED_DIAGNOSTIC_ONLY"


def _fixture(tmp_path):
    run_dir = tmp_path / SOURCE_RUN.name
    shutil.copytree(SOURCE_RUN, run_dir)
    return EvidenceIntegrityConfig(
        run_dir=run_dir,
        output_dir=tmp_path / "integrity_gate",
    )


def _load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_approves_current_v0_5_4_diagnostic_evidence(tmp_path):
    config = _fixture(tmp_path)
    summary = evaluate_evidence_integrity(config)
    assert summary["decision"] == APPROVED
    assert summary["responses_count"] == 20
    assert summary["scores_count"] == 20
    assert summary["metadata_count"] == 20


def test_blocks_missing_artifact(tmp_path):
    config = _fixture(tmp_path)
    (config.run_dir / "real_provider_scores.jsonl").unlink()
    summary = evaluate_evidence_integrity(config)
    assert summary["decision"] == "REAL_PROVIDER_EVIDENCE_INTEGRITY_BLOCKED_MISSING_ARTIFACT"


def test_blocks_dataset_hash_mismatch(tmp_path):
    config = _fixture(tmp_path)
    path = config.run_dir / "real_provider_diagnostic_summary.json"
    data = _load_json(path)
    data["dataset_hash"] = "bad"
    _write_json(path, data)
    summary = evaluate_evidence_integrity(config)
    assert summary["decision"] == "REAL_PROVIDER_EVIDENCE_INTEGRITY_BLOCKED_DATASET_HASH_MISMATCH"


def test_blocks_traceability_failure(tmp_path):
    config = _fixture(tmp_path)
    path = config.run_dir / "real_provider_scores.jsonl"
    rows = path.read_text(encoding="utf-8").splitlines()
    first = json.loads(rows[0])
    first["task_id"] = "bad-task"
    rows[0] = json.dumps(first, sort_keys=True)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    summary = evaluate_evidence_integrity(config)
    assert summary["decision"] == "REAL_PROVIDER_EVIDENCE_INTEGRITY_BLOCKED_TRACEABILITY_FAILURE"


def test_blocks_unauthorized_claim_in_report(tmp_path):
    config = _fixture(tmp_path)
    report = config.run_dir / "real_provider_diagnostic_report.md"
    report.write_text(report.read_text(encoding="utf-8") + "\nThis establishes provider superiority.\n", encoding="utf-8")
    summary = evaluate_evidence_integrity(config)
    assert summary["decision"] == "REAL_PROVIDER_EVIDENCE_INTEGRITY_BLOCKED_UNAUTHORIZED_CLAIM"


def test_blocks_mock_or_stub_text_in_responses(tmp_path):
    config = _fixture(tmp_path)
    path = config.run_dir / "real_provider_responses.jsonl"
    rows = path.read_text(encoding="utf-8").splitlines()
    first = json.loads(rows[0])
    first["response_text"] = "mock response"
    rows[0] = json.dumps(first, sort_keys=True)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    summary = evaluate_evidence_integrity(config)
    assert summary["decision"] == "REAL_PROVIDER_EVIDENCE_INTEGRITY_BLOCKED_ARTIFACT_INCONSISTENCY"


def test_blocks_cost_breakdown_mismatch(tmp_path):
    config = _fixture(tmp_path)
    path = config.run_dir / "real_provider_costs.json"
    costs = _load_json(path)
    costs["provider_costs_usd"]["deepseek"] = 99
    _write_json(path, costs)
    summary = evaluate_evidence_integrity(config)
    assert summary["decision"] == "REAL_PROVIDER_EVIDENCE_INTEGRITY_BLOCKED_ARTIFACT_INCONSISTENCY"


def test_writes_evidence_integrity_artifacts(tmp_path):
    config = _fixture(tmp_path)
    summary = write_evidence_integrity_artifacts(config)
    assert summary["decision"] == APPROVED
    assert (config.output_dir / "evidence_integrity_summary.json").exists()
    assert (config.output_dir / "evidence_integrity_report.md").exists()
