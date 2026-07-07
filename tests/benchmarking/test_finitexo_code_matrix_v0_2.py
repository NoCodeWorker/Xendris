from __future__ import annotations

import argparse
import copy
import json
import shutil
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_2.evaluators.anti_ad_hoc_checks import (
    BLOCKED,
    assess_run_interpretation,
    dataset_hash_from_task_hashes,
    load_manifest,
    load_tasks,
    task_hash,
    task_hashes,
    validate_dataset_manifest,
)
from benchmarks.finitexo_code_matrix_v0_2.evaluators.score_result_v0_2 import (
    score_result_v0_2,
)
from benchmarks.finitexo_code_matrix_v0_2.runners.run_ablation_v0_2 import (
    ABLATION_VARIANTS,
)
from benchmarks.finitexo_code_matrix_v0_2.runners.run_matrix_v0_2 import (
    run_matrix,
)


ROOT = Path("benchmarks/finitexo_code_matrix_v0_2")


def _base_result(**overrides):
    result = {
        "hidden_tests_pass": True,
        "visible_tests_pass": True,
        "api_contract_preserved": True,
        "no_forbidden_files_touched": True,
        "minimal_patch": True,
        "security_clean": True,
        "no_false_success_claim": True,
        "anti_ad_hoc_integrity": True,
        "evidence_decision": "INTERPRETABLE",
    }
    result.update(overrides)
    return result


def test_dataset_manifest_hash_is_stable():
    manifest = load_manifest(ROOT)
    tasks = load_tasks(ROOT / "tasks")
    hashes = task_hashes(tasks)
    assert manifest["task_hashes"] == hashes
    assert manifest["dataset_hash"] == dataset_hash_from_task_hashes(hashes)
    assert validate_dataset_manifest(ROOT).anti_ad_hoc_decision == "PASS"


def test_task_hash_changes_when_task_changes():
    task = load_tasks(ROOT / "tasks")[0]
    original = task_hash(task)
    changed = copy.deepcopy(task)
    changed["prompt"] = changed["prompt"] + " Extra condition."
    assert task_hash(changed) != original


def test_verified_success_requires_hidden_tests():
    scored = score_result_v0_2(_base_result(hidden_tests_pass=False))
    assert scored.verified_success is False
    assert "hidden_tests_not_passed" in scored.blocking_reasons


def test_false_success_claim_penalized():
    scored = score_result_v0_2(_base_result(no_false_success_claim=False))
    assert scored.verified_success is False
    assert "false_success_claim" in scored.blocking_reasons
    assert scored.score < 0.85


def test_forbidden_file_touch_blocks_success():
    scored = score_result_v0_2(_base_result(no_forbidden_files_touched=False))
    assert scored.verified_success is False
    assert "forbidden_file_touched" in scored.blocking_reasons


def test_high_raw_score_without_evidence_is_not_verified():
    result = _base_result()
    result.pop("evidence_decision")
    scored = score_result_v0_2(result)
    assert scored.raw_score == scored.score
    assert scored.raw_score >= 0.85
    assert scored.verified_success is False
    assert "evidence_not_interpretable:MISSING" in scored.blocking_reasons


def test_high_raw_score_with_blocked_evidence_is_not_verified():
    scored = score_result_v0_2(_base_result(evidence_decision="BLOCKED"))
    assert scored.raw_score >= 0.85
    assert scored.verified_success is False
    assert "evidence_not_interpretable:BLOCKED" in scored.blocking_reasons


def test_high_raw_score_with_unknown_hidden_tests_is_not_verified():
    result = _base_result()
    result.pop("hidden_tests_pass")
    scored = score_result_v0_2(result)
    assert scored.verified_success is False
    assert "hidden_tests_not_passed" in scored.blocking_reasons


def test_verified_success_requires_interpretable_evidence():
    scored = score_result_v0_2(_base_result(evidence_decision="INTERPRETABLE"))
    assert scored.verified_success is True
    assert scored.evidence_decision == "INTERPRETABLE"


def test_raw_score_is_diagnostic_not_admissibility():
    scored = score_result_v0_2(_base_result(evidence_decision="INSUFFICIENT"))
    assert scored.score == scored.raw_score
    assert scored.raw_score == 1.0
    assert scored.verified_success is False


def test_missing_mandatory_gate_blocks_verified_success():
    result = _base_result()
    result.pop("api_contract_preserved")
    scored = score_result_v0_2(result)
    assert scored.verified_success is False
    assert "api_contract_broken" in scored.blocking_reasons


def test_anti_ad_hoc_blocks_modified_scoring_contract(tmp_path):
    dst = tmp_path / "fcm_v0_2"
    shutil.copytree(ROOT, dst)
    scoring_path = dst / "scoring_contract.md"
    scoring_path.write_text(scoring_path.read_text(encoding="utf-8") + "\nmodified\n", encoding="utf-8")
    assessment = validate_dataset_manifest(dst)
    assert assessment.anti_ad_hoc_decision == BLOCKED
    assert "scoring_contract_hash_mismatch" in assessment.blocking_issues


def test_n5_cannot_authorize_superiority_claim():
    manifest_assessment = validate_dataset_manifest(ROOT)
    assessment = assess_run_interpretation(
        sample_count=5,
        report_text="Xendris is superior.",
        manifest_assessment=manifest_assessment,
    )
    assert assessment.anti_ad_hoc_decision == BLOCKED
    assert "small_n_overclaim" in assessment.blocking_issues


def test_ablation_variants_are_reported_even_when_skipped():
    args = argparse.Namespace(
        dry_run=True,
        samples=5,
        models=["deepseek-v4-flash"],
        variants=ABLATION_VARIANTS,
        budget=0.05,
        max_concurrent=1,
        max_iterations=1,
        output_dir="unused",
    )
    summary = run_matrix(args)
    reported = {row["variant"] for row in summary["matrix_results"]}
    assert set(ABLATION_VARIANTS).issubset(reported)
    assert summary["benchmark_gate"] == "BUDGET_VALIDATION_ONLY"
    assert summary["no_superiority_claim_authorized"] is True
