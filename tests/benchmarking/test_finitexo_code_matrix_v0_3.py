import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_3.evaluators.adversarial_checks import (
    assess_adversarial_readiness,
    canonical_task_hash,
    compute_dataset_hash,
    dataset_mentions_forbidden_system,
    sha256_file,
)
from benchmarks.finitexo_code_matrix_v0_3.evaluators.baseline_comparison import compare_baselines
from benchmarks.finitexo_code_matrix_v0_3.evaluators.blind_score_result_v0_3 import (
    anonymize_submission,
    score_anonymized_submission,
)
from benchmarks.finitexo_code_matrix_v0_3.evidence.evidence_contract_v0_3 import (
    create_evidence_contract,
)
from benchmarks.finitexo_code_matrix_v0_3.reports.report_builder_v0_3 import build_report
from benchmarks.finitexo_code_matrix_v0_3.runners.run_external_matrix_v0_3 import (
    build_parser,
    run,
)

ROOT = Path("benchmarks/finitexo_code_matrix_v0_3")


def _manifest():
    return json.loads((ROOT / "external_dataset_manifest.json").read_text(encoding="utf-8"))


def test_v0_3_dataset_does_not_mention_xendris():
    assert dataset_mentions_forbidden_system(ROOT / "tasks") is False


def test_v0_3_manifest_hash_is_stable():
    manifest = _manifest()
    task_hashes = {
        path.name: canonical_task_hash(path)
        for path in sorted((ROOT / "tasks").glob("external_task_*.json"))
    }
    assert manifest["task_hashes"] == task_hashes
    assert manifest["dataset_hash"] == compute_dataset_hash(task_hashes)
    assert manifest["scoring_contract_hash"] == sha256_file(ROOT / "scoring_contract.md")


def test_v0_3_scoring_is_blind_to_variant():
    submission = {
        "submission_id": "s1",
        "variant": "xendris_agent",
        "provider": "deepseek",
        "model": "deepseek-v4-flash",
        "task_id": "FCM-V03-001",
        "evidence_decision": "INTERPRETABLE",
        "scoring_components": {
            "hidden_tests_pass": True,
            "visible_tests_pass": True,
            "api_contract_preserved": True,
            "minimal_patch": True,
            "no_forbidden_files_touched": True,
            "security_clean": True,
            "no_false_success_claim": True,
            "external_validity_integrity": True,
        },
    }
    anonymized = anonymize_submission(submission)
    assert "variant" not in json.dumps(anonymized["blind_payload"])
    assert score_anonymized_submission(anonymized["blind_payload"])["verified_success"] is True


def test_v0_3_blind_scoring_blocks_on_identity_leak():
    result = score_anonymized_submission(
        {
            "anonymous_submission_id": "anon",
            "variant": "xendris_agent",
            "scoring_components": {"hidden_tests_pass": True},
            "evidence_decision": "INTERPRETABLE",
        }
    )
    assert result["blind_scoring_decision"] == "FAILED"
    assert result["verified_success"] is False


def test_v0_3_requires_strong_baseline():
    comparison = compare_baselines({"strong_non_xendris_agent_available": False})
    assert comparison["decision"] == "BLOCKED_FOR_INTERPRETATION"
    assert "strong_baseline_unavailable" in comparison["blockers"]


def test_v0_3_allows_baseline_matched_xendris_decision():
    comparison = compare_baselines(
        {
            "strong_non_xendris_agent_available": True,
            "strong_non_xendris_agent": {"verified_success_count": 5, "mean_raw_score": 0.9},
            "xendris_agent": {"verified_success_count": 5, "mean_raw_score": 0.91},
            "xendris_calibrated_agent": {"verified_success_count": 6, "mean_raw_score": 0.92},
        }
    )
    assert comparison["decision"] == "BASELINE_MATCHED_XENDRIS"


def test_v0_3_allows_baseline_outperformed_xendris_decision():
    comparison = compare_baselines(
        {
            "strong_non_xendris_agent_available": True,
            "strong_non_xendris_agent": {"verified_success_count": 8, "mean_raw_score": 0.95},
            "xendris_agent": {"verified_success_count": 6, "mean_raw_score": 0.9},
            "xendris_calibrated_agent": {"verified_success_count": 7, "mean_raw_score": 0.91},
        }
    )
    assert comparison["decision"] == "BASELINE_OUTPERFORMED_XENDRIS"


def test_v0_3_weak_baseline_cannot_support_claims():
    protocol = (ROOT / "strong_baseline_protocol.md").read_text(encoding="utf-8")
    assert "weak baseline can be diagnostic" in protocol.lower()
    assert "cannot support a positive advantage" in protocol.lower()


def test_v0_3_unknown_values_block_verified_success():
    result = score_anonymized_submission(
        {
            "anonymous_submission_id": "anon",
            "evidence_decision": "UNKNOWN",
            "scoring_components": {
                "hidden_tests_pass": True,
                "visible_tests_pass": True,
                "api_contract_preserved": True,
                "minimal_patch": True,
                "no_forbidden_files_touched": True,
                "security_clean": True,
                "no_false_success_claim": True,
                "external_validity_integrity": True,
            },
        }
    )
    assert result["raw_score"] >= 0.85
    assert result["verified_success"] is False


def test_v0_3_no_provider_execution_without_execute_flag(tmp_path):
    args = build_parser().parse_args(["--dry-run", "--output-dir", str(tmp_path)])
    summary = run(args)
    assert summary["provider_execution"] == "NO_PROVIDER_EXECUTION"


def test_v0_3_h0_remains_live_by_default():
    readiness = assess_adversarial_readiness(manifest=_manifest())
    assert readiness["h0_status"] == "LIVE"


def test_v0_3_report_can_state_no_clear_advantage():
    report = build_report(
        {
            "result_decision": "NO_CLEAR_XENDRIS_ADVANTAGE",
            "baseline_comparison": {
                "decision": "NO_CLEAR_XENDRIS_ADVANTAGE",
                "interpretation": "The evidence does not show a clear advantage.",
            },
        }
    )
    assert "NO_CLEAR_XENDRIS_ADVANTAGE" in report
    assert "does not show a clear advantage" in report


def test_v0_3_real_execution_requires_execute_flag(tmp_path):
    args = build_parser().parse_args(["--execute", "--budget", "0.10", "--output-dir", str(tmp_path)])
    summary = run(args)
    assert summary["provider_execution"] == "BLOCKED_FOR_INTERPRETATION"
    assert "real_provider_execution_not_implemented_in_v0_3_infrastructure" in summary["blockers"]


def test_v0_3_dataset_tasks_are_not_v0_2_reused():
    v0_2_dir = Path("benchmarks/finitexo_code_matrix_v0_2")
    v0_2_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in v0_2_dir.rglob("*")
        if path.is_file() and path.suffix in {".json", ".md", ".py"}
    )
    for path in sorted((ROOT / "tasks").glob("external_task_*.json")):
        task = json.loads(path.read_text(encoding="utf-8"))
        assert task["task_id"] not in v0_2_text
        assert task["hash_material"] not in v0_2_text


def test_v0_3_evidence_contract_excludes_variant_from_blind_payload():
    contract = create_evidence_contract(
        run_id="r1",
        task_id="FCM-V03-001",
        submission_id="s1",
        dataset_hash="dataset",
        task_hash="task",
        scoring_contract_hash="score",
        anonymization_map_hash="map",
        origin="SEMI_EXTERNAL_SYNTHETIC",
        raw_output_path="raw.json",
        patch_path="patch.diff",
        score_result_path="score.json",
        blind_payload={"variant": "xendris_agent", "model": "m", "safe": True},
    )
    assert contract["blind_scorer_payload"] == {"safe": True}
