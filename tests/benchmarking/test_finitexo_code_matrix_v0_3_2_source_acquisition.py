import json
from dataclasses import replace
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_3.source_acquisition import (
    ContaminationRisk,
    OriginCandidate,
    SourceAcquisitionRecord,
    SourceType,
    evaluate_promotion_eligibility,
)
from benchmarks.finitexo_code_matrix_v0_3.source_acquisition.acquisition_report_builder import (
    build_acquisition_summary,
    load_acquisition_records,
    write_acquisition_artifacts,
)

ROOT = Path("benchmarks/finitexo_code_matrix_v0_3")


def _valid_external_verified_record():
    return SourceAcquisitionRecord(
        source_id="test_001",
        source_type=SourceType.PUBLIC_DOC_EXAMPLE,
        source_url="https://example.invalid/source",
        retrieved_at="2026-07-07T00:00:00Z",
        license="REFERENCE_ONLY",
        source_hash="sha256:test",
        raw_snapshot_path="raw/test.txt",
        normalized_snapshot_path="normalized/test.json",
        adapted_task_path=None,
        origin_candidate=OriginCandidate.EXTERNAL_VERIFIED,
        contamination_risk=ContaminationRisk.LOW,
        adaptation_required=False,
        adaptation_notes=None,
    )


def test_valid_external_verified_style_record_can_be_eligible():
    decision = evaluate_promotion_eligibility(_valid_external_verified_record())
    assert decision.promotion_allowed is True
    assert decision.decision == "ELIGIBLE_FOR_FUTURE_PROMOTION"


def test_valid_external_adapted_style_record_can_be_eligible_only_with_notes():
    record = replace(
        _valid_external_verified_record(),
        source_type=SourceType.PUBLIC_GITHUB_ISSUE,
        origin_candidate=OriginCandidate.EXTERNAL_ADAPTED,
        contamination_risk=ContaminationRisk.MEDIUM,
        adaptation_required=True,
        adaptation_notes="Adapted into a local fixture; no external code copied.",
        adapted_task_path="adapted/test.json",
    )
    assert evaluate_promotion_eligibility(record).promotion_allowed is True
    missing_notes = replace(record, adaptation_notes=None)
    decision = evaluate_promotion_eligibility(missing_notes)
    assert decision.promotion_allowed is False
    assert "missing_adaptation_notes" in decision.blockers


def test_missing_license_blocks_promotion():
    record = replace(_valid_external_verified_record(), license="UNKNOWN")
    decision = evaluate_promotion_eligibility(record)
    assert decision.promotion_allowed is False
    assert "missing_or_unknown_license" in decision.blockers


def test_missing_hash_blocks_promotion():
    record = replace(_valid_external_verified_record(), source_hash=None)
    decision = evaluate_promotion_eligibility(record)
    assert decision.promotion_allowed is False
    assert "missing_source_hash" in decision.blockers


def test_high_or_blocked_contamination_prevents_promotion():
    high = replace(_valid_external_verified_record(), contamination_risk=ContaminationRisk.HIGH)
    blocked = replace(_valid_external_verified_record(), contamination_risk=ContaminationRisk.BLOCKED)
    assert evaluate_promotion_eligibility(high).promotion_allowed is False
    assert evaluate_promotion_eligibility(blocked).promotion_allowed is False


def test_internal_fixture_cannot_become_external_verified():
    record = replace(
        _valid_external_verified_record(),
        source_type=SourceType.INTERNAL_FIXTURE,
        origin_candidate=OriginCandidate.EXTERNAL_VERIFIED,
    )
    decision = evaluate_promotion_eligibility(record)
    assert decision.promotion_allowed is False
    assert "internal_or_unknown_source_cannot_be_external_verified" in decision.blockers


def test_acquisition_examples_are_not_counted_as_frozen_benchmark_tasks():
    manifest = json.loads((ROOT / "external_dataset_manifest.json").read_text(encoding="utf-8"))
    records = load_acquisition_records()
    assert len(records) == 4
    assert len(manifest["task_hashes"]) == 10


def test_report_builder_produces_summary_and_markdown_report(tmp_path):
    summary = write_acquisition_artifacts(tmp_path)
    assert summary["final_decision"] == "SOURCE_ACQUISITION_GATE_IMPLEMENTED_NO_DATASET_PROMOTION"
    assert (tmp_path / "source_acquisition_summary.json").exists()
    report = (tmp_path / "source_acquisition_report.md").read_text(encoding="utf-8")
    assert "No provider execution occurred." in report
    assert "The frozen v0.3 seed dataset was not modified." in report


def test_manifest_contains_v0_3_2_acquisition_section():
    manifest = json.loads((ROOT / "external_dataset_manifest.json").read_text(encoding="utf-8"))
    assert manifest["external_source_acquisition_version"] == "0.3.2"
    policy = manifest["external_source_acquisition_policy"]
    assert policy["acquisition_records_are_not_benchmark_tasks"] is True
    assert policy["acquisition_eligibility_does_not_equal_dataset_promotion"] is True


def test_no_provider_execution_is_required():
    summary = build_acquisition_summary(load_acquisition_records())
    assert summary["providers_executed"] is False


def test_frozen_v0_3_seed_dataset_remains_unchanged():
    manifest = json.loads((ROOT / "external_dataset_manifest.json").read_text(encoding="utf-8"))
    assert manifest["dataset_size"] == 10
    assert len(manifest["task_hashes"]) == 10
    assert manifest["dataset_hash"] == "a1b03f0da1c4e051c4b54df46baae8eef65a8c401f7da7ed5c520f9bf2c29907"
