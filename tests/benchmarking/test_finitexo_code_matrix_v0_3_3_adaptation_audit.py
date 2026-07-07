import json
from dataclasses import replace
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_3.adaptation_audit import (
    AdaptationRecord,
    AdaptationType,
    BenchmarkFitStatus,
    LeakageRisk,
    PromotionRecommendation,
    TaskValidityStatus,
    evaluate_adaptation_candidate,
)
from benchmarks.finitexo_code_matrix_v0_3.adaptation_audit.adaptation_report_builder import (
    load_adaptation_records,
    write_adaptation_audit_artifacts,
)
from benchmarks.finitexo_code_matrix_v0_3.adaptation_audit.leakage_controls import assess_leakage
from benchmarks.finitexo_code_matrix_v0_3.adaptation_audit.task_validity_review import review_task_validity
from benchmarks.finitexo_code_matrix_v0_3.source_acquisition import ContaminationRisk, OriginCandidate

ROOT = Path("benchmarks/finitexo_code_matrix_v0_3")


def _clean_record():
    return AdaptationRecord(
        adaptation_id="test",
        source_id="acq",
        acquisition_record_path="acq.json",
        source_origin_candidate=OriginCandidate.EXTERNAL_VERIFIED,
        adapted_candidate_path="adapted.json",
        normalized_source_path="normalized.json",
        raw_source_hash="sha256:source",
        adapted_candidate_hash="sha256:adapted",
        adaptation_type=AdaptationType.DIRECT_PORT,
        adaptation_summary="Clean direct port into local fixture.",
        semantic_preservation_score=0.9,
        structural_change_score=0.2,
        difficulty_shift_score=0.2,
        contamination_risk=ContaminationRisk.LOW,
        leakage_risk=LeakageRisk.LOW,
        task_validity_status=TaskValidityStatus.VALID,
        benchmark_fit_status=BenchmarkFitStatus.FIT_FOR_AGENTIC_PROGRAMMING,
        requires_human_review=False,
        promotion_recommendation=PromotionRecommendation.DO_NOT_PROMOTE,
    )


def test_clean_external_verified_direct_port_can_be_recommended_for_future_freeze():
    decision = evaluate_adaptation_candidate(_clean_record())
    assert decision.recommendation == PromotionRecommendation.RECOMMEND_FOR_FUTURE_FREEZE


def test_external_adapted_candidate_with_warnings_can_require_human_review():
    record = replace(
        _clean_record(),
        source_origin_candidate=OriginCandidate.EXTERNAL_ADAPTED,
        adaptation_type=AdaptationType.API_NORMALIZATION,
        leakage_risk=LeakageRisk.MEDIUM,
        task_validity_status=TaskValidityStatus.VALID_WITH_WARNINGS,
        benchmark_fit_status=BenchmarkFitStatus.FIT_WITH_LIMITATIONS,
        requires_human_review=True,
        warnings=("needs review",),
    )
    decision = evaluate_adaptation_candidate(record)
    assert decision.recommendation == PromotionRecommendation.RECOMMEND_WITH_HUMAN_REVIEW


def test_synthetic_expansion_cannot_be_recommended_for_future_freeze():
    record = replace(_clean_record(), adaptation_type=AdaptationType.SYNTHETIC_EXPANSION)
    decision = evaluate_adaptation_candidate(record)
    assert decision.recommendation == PromotionRecommendation.DO_NOT_PROMOTE
    assert "blocked_adaptation_type" in decision.rejection_reasons


def test_mutated_internal_fixture_is_blocked():
    record = replace(
        _clean_record(),
        source_origin_candidate=OriginCandidate.MUTATED_FIXTURE,
        adaptation_type=AdaptationType.MUTATED_INTERNAL_FIXTURE,
        contamination_risk=ContaminationRisk.BLOCKED,
        leakage_risk=LeakageRisk.BLOCKED,
        task_validity_status=TaskValidityStatus.BLOCKED,
        benchmark_fit_status=BenchmarkFitStatus.BLOCKED,
    )
    decision = evaluate_adaptation_candidate(record)
    assert decision.recommendation == PromotionRecommendation.BLOCKED


def test_missing_source_hash_prevents_recommendation():
    decision = evaluate_adaptation_candidate(replace(_clean_record(), raw_source_hash=None))
    assert decision.recommendation == PromotionRecommendation.DO_NOT_PROMOTE
    assert "missing_raw_source_hash" in decision.rejection_reasons


def test_missing_adapted_candidate_hash_prevents_recommendation():
    decision = evaluate_adaptation_candidate(replace(_clean_record(), adapted_candidate_hash=None))
    assert decision.recommendation == PromotionRecommendation.DO_NOT_PROMOTE
    assert "missing_adapted_candidate_hash" in decision.rejection_reasons


def test_missing_adaptation_summary_prevents_recommendation():
    decision = evaluate_adaptation_candidate(replace(_clean_record(), adaptation_summary=None))
    assert decision.recommendation == PromotionRecommendation.DO_NOT_PROMOTE
    assert "missing_adaptation_summary" in decision.rejection_reasons


def test_high_contamination_risk_blocks_promotion_recommendation():
    decision = evaluate_adaptation_candidate(replace(_clean_record(), contamination_risk=ContaminationRisk.HIGH))
    assert decision.recommendation == PromotionRecommendation.DO_NOT_PROMOTE
    assert "contamination_risk_blocks_recommendation" in decision.rejection_reasons


def test_blocked_leakage_risk_blocks_promotion_recommendation():
    decision = evaluate_adaptation_candidate(replace(_clean_record(), leakage_risk=LeakageRisk.BLOCKED))
    assert decision.recommendation == PromotionRecommendation.BLOCKED
    assert "leakage_risk_blocks_recommendation" in decision.rejection_reasons


def test_task_depending_on_live_network_state_is_invalid_or_blocked():
    review = review_task_validity(
        {
            "expected_behavior": "Fetch live state.",
            "visible_tests": ["requires network"],
            "depends_on_live_network": True,
            "reproducible_setup": False,
        }
    )
    assert review["task_validity_status"] == TaskValidityStatus.BLOCKED


def test_task_requiring_secrets_is_invalid_or_blocked():
    review = review_task_validity(
        {
            "expected_behavior": "Use private key.",
            "visible_tests": ["requires key"],
            "requires_secrets": True,
            "reproducible_setup": False,
        }
    )
    assert review["task_validity_status"] == TaskValidityStatus.BLOCKED


def test_candidate_exposing_scoring_formula_or_hidden_tests_is_blocked_or_rejected():
    assert assess_leakage("Use raw_score and expected hidden tests.")["leakage_risk"] == LeakageRisk.BLOCKED


def test_semantic_preservation_score_below_threshold_prevents_recommendation():
    decision = evaluate_adaptation_candidate(replace(_clean_record(), semantic_preservation_score=0.69))
    assert "semantic_preservation_below_threshold" in decision.rejection_reasons


def test_structural_change_score_above_threshold_prevents_recommendation():
    decision = evaluate_adaptation_candidate(replace(_clean_record(), structural_change_score=0.66))
    assert "structural_change_above_threshold" in decision.rejection_reasons


def test_difficulty_shift_score_above_threshold_prevents_recommendation():
    decision = evaluate_adaptation_candidate(replace(_clean_record(), difficulty_shift_score=0.51))
    assert "difficulty_shift_above_threshold" in decision.rejection_reasons


def test_example_records_are_not_counted_as_frozen_benchmark_tasks():
    manifest = json.loads((ROOT / "external_dataset_manifest.json").read_text(encoding="utf-8"))
    assert len(load_adaptation_records()) == 5
    assert len(manifest["task_hashes"]) == 10


def test_report_builder_produces_json_summary_and_markdown_report(tmp_path):
    summary = write_adaptation_audit_artifacts(tmp_path)
    assert summary["final_decision"] == "EXTERNAL_ADAPTATION_AUDIT_IMPLEMENTED_NO_FROZEN_DATASET_CHANGE"
    assert (tmp_path / "adaptation_audit_summary.json").exists()
    report = (tmp_path / "adaptation_audit_report.md").read_text(encoding="utf-8")
    assert "No providers were executed." in report
    assert "The frozen v0.3 seed dataset was not modified." in report


def test_manifest_contains_v0_3_3_adaptation_audit_section():
    manifest = json.loads((ROOT / "external_dataset_manifest.json").read_text(encoding="utf-8"))
    assert manifest["external_adaptation_audit_version"] == "0.3.3"
    assert manifest["external_adaptation_audit_policy"]["adaptation_recommendation_is_not_dataset_promotion"] is True


def test_no_provider_execution_is_required(tmp_path):
    summary = write_adaptation_audit_artifacts(tmp_path)
    assert summary["providers_executed"] is False


def test_frozen_v0_3_seed_dataset_remains_unchanged():
    manifest = json.loads((ROOT / "external_dataset_manifest.json").read_text(encoding="utf-8"))
    assert manifest["dataset_size"] == 10
    assert len(manifest["task_hashes"]) == 10
    assert manifest["dataset_hash"] == "a1b03f0da1c4e051c4b54df46baae8eef65a8c401f7da7ed5c520f9bf2c29907"
