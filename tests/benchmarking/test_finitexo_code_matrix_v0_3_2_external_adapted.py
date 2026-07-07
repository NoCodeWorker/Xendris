import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_3.dataset_intake.external_task_intake import (
    load_candidate_tasks,
    load_source_registry,
    run_intake,
    validate_candidate_task,
)

ROOT = Path("benchmarks/finitexo_code_matrix_v0_3")


def _new_candidates():
    return [
        candidate
        for candidate in load_candidate_tasks()
        if candidate["task_id"].startswith("fcm_v0_3_2_")
    ]


def _value_text(value):
    if isinstance(value, dict):
        return "\n".join(_value_text(item) for item in value.values())
    if isinstance(value, list):
        return "\n".join(_value_text(item) for item in value)
    return str(value).lower()


def test_v0_3_2_new_candidates_exist():
    assert len(_new_candidates()) == 5


def test_v0_3_2_external_adapted_candidates_have_sources():
    registry = load_source_registry()
    sources = {source["source_id"]: source for source in registry["sources"]}
    adapted = [candidate for candidate in _new_candidates() if candidate["origin"] == "EXTERNAL_ADAPTED"]
    assert len(adapted) >= 3
    for candidate in adapted:
        assert candidate["source_id"] in sources
        assert sources[candidate["source_id"]]["source_type"] == "EXTERNAL_ADAPTED"


def test_v0_3_2_external_adapted_requires_adaptation_notes():
    registry = load_source_registry()
    source = next(item for item in registry["sources"] if item["source_type"] == "EXTERNAL_ADAPTED")
    source["adaptation_notes"] = ""
    registry["sources"] = [source if item["source_id"] == source["source_id"] else item for item in registry["sources"]]
    candidate = next(item for item in _new_candidates() if item["source_id"] == source["source_id"])
    decision = validate_candidate_task(candidate, registry)
    assert "external_adapted_missing_adaptation_notes" in decision["blocking_issues"]


def test_v0_3_2_external_adapted_requires_traceability():
    registry = load_source_registry()
    source = next(item for item in registry["sources"] if item["source_type"] == "EXTERNAL_ADAPTED")
    source["traceability_confidence"] = "LOW"
    registry["sources"] = [source if item["source_id"] == source["source_id"] else item for item in registry["sources"]]
    candidate = next(item for item in _new_candidates() if item["source_id"] == source["source_id"])
    decision = validate_candidate_task(candidate, registry)
    assert "external_adapted_insufficient_traceability" in decision["blocking_issues"]


def test_v0_3_2_externality_target_is_reported(tmp_path):
    summary = run_intake(tmp_path, phase="v0.3.2")
    adapted_summary = json.loads((tmp_path / "external_adapted_summary.json").read_text(encoding="utf-8"))
    assert summary["target_mean_externality_score"] == 0.60
    assert adapted_summary["target_met"] is True
    assert adapted_summary["mean_externality_score_new_candidates"] >= 0.60


def test_v0_3_2_externality_score_is_diagnostic_only(tmp_path):
    run_intake(tmp_path, phase="v0.3.2")
    report = (tmp_path / "intake_report.md").read_text(encoding="utf-8")
    assert "Externality is diagnostic and does not authorize performance claims." in report


def test_v0_3_2_candidate_pool_still_not_dataset():
    manifest = json.loads((ROOT / "external_dataset_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["task_hashes"]) == 10
    assert manifest["externality_summary"]["candidate_pool_size"] == 10
    assert manifest["promotion_policy"] == "dataset promotion requires a future explicit phase"


def test_v0_3_2_no_provider_execution(tmp_path):
    summary = run_intake(tmp_path, phase="v0.3.2")
    adapted_summary = json.loads((tmp_path / "external_adapted_summary.json").read_text(encoding="utf-8"))
    assert summary["providers_executed"] is False
    assert adapted_summary["providers_executed"] is False


def test_v0_3_2_manifest_updated_without_dataset_promotion():
    manifest = json.loads((ROOT / "external_dataset_manifest.json").read_text(encoding="utf-8"))
    assert manifest["external_dataset_intake_version"] == "v0.3.2"
    assert manifest["externality_summary"]["external_adapted"] == 4
    assert manifest["externality_summary"]["target_met"] is True


def test_v0_3_2_no_xendris_mentions_in_candidates():
    for candidate in _new_candidates():
        candidate_text = _value_text(candidate)
        assert "xendris" not in candidate_text


def test_v0_3_2_no_internal_gate_mentions_in_candidates():
    forbidden = ("benchmark gate", "trust gate", "internal gate", "response contract")
    for candidate in _new_candidates():
        candidate_text = _value_text(candidate)
        assert not any(term in candidate_text for term in forbidden)


def test_v0_3_2_report_does_not_claim_external_validation_completed(tmp_path):
    run_intake(tmp_path, phase="v0.3.2")
    report = (tmp_path / "intake_report.md").read_text(encoding="utf-8")
    assert "External validation completed" not in report
    assert "No real provider execution was performed." in report
