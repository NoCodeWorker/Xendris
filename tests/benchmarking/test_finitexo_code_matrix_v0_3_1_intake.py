import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_3.dataset_intake.external_task_intake import (
    load_candidate_tasks,
    load_source_registry,
    run_intake,
    summarize_intake,
    validate_candidate_task,
)
from benchmarks.finitexo_code_matrix_v0_3.dataset_intake.intake_validation import (
    validate_candidate,
)
from benchmarks.finitexo_code_matrix_v0_3.dataset_intake.source_registry import (
    validate_source_registry,
)

ROOT = Path("benchmarks/finitexo_code_matrix_v0_3")


def test_v0_3_1_source_registry_schema():
    registry = load_source_registry()
    assert validate_source_registry(registry) == []
    assert len(registry["sources"]) >= 5


def test_v0_3_1_candidate_requires_source_id():
    candidate = dict(load_candidate_tasks()[0])
    candidate.pop("source_id")
    decision = validate_candidate(candidate, load_source_registry())
    assert "missing_field:source_id" in decision["blocking_issues"]
    assert decision["intake_decision"] == "REJECTED"


def test_v0_3_1_candidate_source_id_must_exist():
    candidate = dict(load_candidate_tasks()[0])
    candidate["source_id"] = "missing"
    decision = validate_candidate_task(candidate, load_source_registry())
    assert "source_id_not_found" in decision["blocking_issues"]


def test_v0_3_1_externality_score_range():
    candidate = dict(load_candidate_tasks()[0])
    candidate["externality_score"] = 1.5
    decision = validate_candidate_task(candidate, load_source_registry())
    assert "externality_score_out_of_range" in decision["blocking_issues"]


def test_v0_3_1_externality_score_band_warning():
    candidate = dict(load_candidate_tasks()[0])
    candidate["externality_score"] = 0.9
    decision = validate_candidate_task(candidate, load_source_registry())
    assert "externality_score_outside_origin_band" in decision["warnings"]
    assert decision["intake_decision"] == "WARNINGS_PRESENT"


def test_v0_3_1_rejects_xendris_mentions():
    candidate = dict(load_candidate_tasks()[0])
    candidate["prompt"] = "Use Xendris-specific output format."
    decision = validate_candidate_task(candidate, load_source_registry())
    assert "forbidden_term:xendris" in decision["blocking_issues"]


def test_v0_3_1_rejects_internal_gate_mentions():
    candidate = dict(load_candidate_tasks()[0])
    candidate["prompt"] = "Optimize for the benchmark gate."
    decision = validate_candidate_task(candidate, load_source_registry())
    assert "forbidden_term:benchmark gate" in decision["blocking_issues"]


def test_v0_3_1_rejected_candidate_requires_reason():
    candidate = dict(load_candidate_tasks()[0])
    candidate["admissible_for_v0_3"] = False
    candidate["rejection_reason"] = None
    decision = validate_candidate_task(candidate, load_source_registry())
    assert "rejected_candidate_missing_reason" in decision["blocking_issues"]


def test_v0_3_1_preserves_honest_origin_labels():
    candidates = [
        candidate
        for candidate in load_candidate_tasks()
        if candidate["task_id"].startswith("fcm_v0_3_1_")
    ]
    origins = {candidate["origin"] for candidate in candidates}
    assert origins == {"MUTATED_FIXTURE", "SEMI_EXTERNAL_SYNTHETIC"}
    assert "EXTERNAL_VERIFIED" not in origins


def test_v0_3_1_manifest_externality_summary_present():
    manifest = json.loads((ROOT / "external_dataset_manifest.json").read_text(encoding="utf-8"))
    summary = manifest["externality_summary"]
    assert manifest["external_dataset_intake_version"] in {"v0.3.1", "v0.3.2"}
    assert summary["candidate_pool_size"] >= 5
    assert summary["mutated_fixture"] >= 2
    assert summary["semi_external_synthetic"] >= 3


def test_v0_3_1_candidate_pool_does_not_modify_seed_dataset():
    manifest = json.loads((ROOT / "external_dataset_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["task_hashes"]) == 10
    assert manifest["intake_policy"].startswith("candidate pool does not modify")


def test_v0_3_1_no_provider_execution(tmp_path):
    summary = run_intake(tmp_path)
    assert summary["providers_executed"] is False
    assert (tmp_path / "intake_summary.json").exists()
    assert (tmp_path / "intake_report.md").exists()


def test_v0_3_1_report_says_no_claims_authorized(tmp_path):
    run_intake(tmp_path)
    report = (tmp_path / "intake_report.md").read_text(encoding="utf-8")
    assert "Externality is diagnostic and does not authorize performance claims." in report
    assert "No real provider execution was performed." in report
    assert "Universal superiority" in report


def test_v0_3_1_all_current_candidates_are_accepted():
    registry = load_source_registry()
    decisions = [validate_candidate_task(candidate, registry) for candidate in load_candidate_tasks()]
    summary = summarize_intake(decisions)
    assert summary["candidate_count"] >= 5
    assert summary["accepted_count"] == summary["candidate_count"]
    assert summary["warnings_count"] == 0
    assert summary["rejected_count"] == 0
    assert summary["mean_externality_score"] >= 0.468
