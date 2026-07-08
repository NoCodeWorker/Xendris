import json
import shutil
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_5.real_provider_scoring_consistency import (
    ScoringConsistencyConfig,
    evaluate_scoring_consistency,
    write_scoring_consistency_artifacts,
)


SOURCE_RUN = Path("runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized")
EVIDENCE_SUMMARY = Path("runs/finitexo_code_matrix_v0_5_5_real_provider_evidence_integrity_gate/evidence_integrity_summary.json")
APPROVED = "REAL_PROVIDER_SCORING_CONSISTENCY_APPROVED_DIAGNOSTIC_ONLY"


def _fixture(tmp_path):
    run_dir = tmp_path / SOURCE_RUN.name
    shutil.copytree(SOURCE_RUN, run_dir)
    evidence = tmp_path / "evidence_integrity_summary.json"
    shutil.copyfile(EVIDENCE_SUMMARY, evidence)
    return ScoringConsistencyConfig(
        run_dir=run_dir,
        evidence_integrity_summary_path=evidence,
        output_dir=tmp_path / "scoring_gate",
    )


def _rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_rows(path, rows):
    path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")


def test_happy_path_approved_diagnostic_only(tmp_path):
    config = _fixture(tmp_path)
    summary = evaluate_scoring_consistency(config)
    assert summary["final_decision"] == APPROVED
    assert summary["scores_checked"] == 20
    assert summary["provider_score_counts"] == {"deepseek": 10, "openai": 10}
    assert summary["diagnostic_only"] is True


def test_missing_score_row_fails(tmp_path):
    config = _fixture(tmp_path)
    path = config.run_dir / "real_provider_scores.jsonl"
    rows = _rows(path)
    _write_rows(path, rows[:-1])
    summary = evaluate_scoring_consistency(config)
    assert summary["final_decision"] != APPROVED


def test_duplicate_score_identity_fails(tmp_path):
    config = _fixture(tmp_path)
    path = config.run_dir / "real_provider_scores.jsonl"
    rows = _rows(path)
    rows[1]["provider_name"] = rows[0]["provider_name"]
    rows[1]["task_id"] = rows[0]["task_id"]
    _write_rows(path, rows)
    summary = evaluate_scoring_consistency(config)
    assert any(finding["code"] == "duplicate_score_identity" for finding in summary["findings"])


def test_score_outside_unit_range_fails(tmp_path):
    config = _fixture(tmp_path)
    path = config.run_dir / "real_provider_scores.jsonl"
    rows = _rows(path)
    rows[0]["score_total"] = 1.2
    _write_rows(path, rows)
    summary = evaluate_scoring_consistency(config)
    assert any(finding["code"] == "score_out_of_range" for finding in summary["findings"])


def test_invalid_formula_weight_sum_fails(tmp_path):
    config = _fixture(tmp_path)
    path = config.run_dir / "real_provider_scores.jsonl"
    rows = _rows(path)
    rows[0]["scoring_formula"] = {"weighted_components": {"a": 0.8, "b": 0.8}, "hard_penalties": []}
    rows[0]["score_components"] = {"a": 0.5, "b": 0.5}
    _write_rows(path, rows)
    summary = evaluate_scoring_consistency(config)
    assert any(finding["code"] == "invalid_scoring_formula_weight_sum" for finding in summary["findings"])


def test_provider_asymmetry_fails(tmp_path):
    config = _fixture(tmp_path)
    path = config.run_dir / "real_provider_scores.jsonl"
    rows = _rows(path)
    rows = [row for row in rows if not (row["provider_name"] == "openai" and row["task_id"].endswith("010"))]
    _write_rows(path, rows)
    summary = evaluate_scoring_consistency(config)
    assert any(finding["code"].startswith("provider_symmetry") for finding in summary["findings"])


def test_explicit_false_success_contradiction_fails(tmp_path):
    config = _fixture(tmp_path)
    path = config.run_dir / "real_provider_scores.jsonl"
    rows = _rows(path)
    rows[0]["success"] = True
    rows[0]["hidden_tests_pass"] = False
    _write_rows(path, rows)
    summary = evaluate_scoring_consistency(config)
    assert any(finding["code"] == "false_success_contradiction" for finding in summary["findings"])


def test_decision_cannot_exceed_diagnostic_only(tmp_path):
    config = _fixture(tmp_path)
    report = config.run_dir / "real_provider_diagnostic_report.md"
    report.write_text(report.read_text(encoding="utf-8") + "\nstatistical claim authorized: true\n", encoding="utf-8")
    summary = evaluate_scoring_consistency(config)
    assert any(finding["code"] == "decision_exceeds_diagnostic_only" for finding in summary["findings"])


def test_writes_scoring_consistency_artifacts(tmp_path):
    config = _fixture(tmp_path)
    summary = write_scoring_consistency_artifacts(config)
    assert summary["final_decision"] == APPROVED
    assert (config.output_dir / "scoring_consistency_summary.json").exists()
    assert (config.output_dir / "scoring_consistency_report.md").exists()
