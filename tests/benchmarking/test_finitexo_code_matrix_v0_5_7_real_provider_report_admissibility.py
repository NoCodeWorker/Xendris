import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_5.real_provider_report_admissibility import (
    ReportAdmissibilityConfig,
    evaluate_report_admissibility,
    write_report_admissibility_artifacts,
)


APPROVED = "REAL_PROVIDER_REPORT_ADMISSIBILITY_APPROVED_DIAGNOSTIC_ONLY"
BLOCKED = "REAL_PROVIDER_REPORT_ADMISSIBILITY_BLOCKED"


def _config(tmp_path: Path, text: str, suffix: str = ".md") -> ReportAdmissibilityConfig:
    artifact = tmp_path / f"artifact{suffix}"
    artifact.write_text(text, encoding="utf-8")
    return ReportAdmissibilityConfig(
        input_paths=(artifact,),
        optional_paths=(),
        output_dir=tmp_path / "out",
    )


def _summary(text: str, tmp_path: Path, suffix: str = ".md"):
    return evaluate_report_admissibility(_config(tmp_path, text, suffix=suffix))


def test_happy_path_approved_diagnostic_only(tmp_path):
    summary = _summary(
        "This is diagnostic-only. No statistical claim authorized. "
        "No provider superiority claim authorized. No Xendris superiority claim authorized.",
        tmp_path,
    )
    assert summary["final_decision"] == APPROVED
    assert summary["diagnostic_only"] is True


def test_explicit_statistical_overclaim_fails(tmp_path):
    summary = _summary("The benchmark is statistically significant.", tmp_path)
    assert summary["final_decision"] == BLOCKED
    assert any(f["code"] == "statistical_overclaim" for f in summary["findings"])


def test_provider_superiority_overclaim_fails(tmp_path):
    summary = _summary("DeepSeek is better than OpenAI on this benchmark.", tmp_path)
    assert summary["final_decision"] == BLOCKED
    assert any(f["code"] == "provider_superiority_overclaim" for f in summary["findings"])


def test_xendris_superiority_overclaim_fails(tmp_path):
    summary = _summary("This proves Xendris superiority.", tmp_path)
    assert summary["final_decision"] == BLOCKED
    assert any(f["code"] == "xendris_superiority_overclaim" for f in summary["findings"])


def test_production_readiness_overclaim_fails(tmp_path):
    summary = _summary("The system is production ready.", tmp_path)
    assert summary["final_decision"] == BLOCKED
    assert any(f["code"] == "production_readiness_overclaim" for f in summary["findings"])


def test_universal_benchmark_overclaim_fails(tmp_path):
    summary = _summary("This is a universal programming benchmark.", tmp_path)
    assert summary["final_decision"] == BLOCKED
    assert any(f["code"] == "universal_benchmark_overclaim" for f in summary["findings"])


def test_negated_forbidden_phrase_is_allowed(tmp_path):
    summary = _summary(
        "This is not statistically significant and does not prove Xendris superiority.",
        tmp_path,
    )
    assert summary["final_decision"] == APPROVED
    assert summary["negated_claims_allowed"] >= 2


def test_json_string_overclaim_is_detected(tmp_path):
    payload = {"interpretation": "This is a conclusive benchmark."}
    summary = _summary(json.dumps(payload), tmp_path, suffix=".json")
    assert summary["final_decision"] == BLOCKED
    assert any(f["code"] == "statistical_overclaim" for f in summary["findings"])


def test_missing_optional_artifact_is_recorded_but_does_not_fail(tmp_path):
    artifact = tmp_path / "artifact.md"
    missing = tmp_path / "missing_optional.md"
    artifact.write_text("Diagnostic-only. No statistical claim authorized.", encoding="utf-8")
    config = ReportAdmissibilityConfig(
        input_paths=(artifact,),
        optional_paths=(missing,),
        output_dir=tmp_path / "out",
    )
    summary = evaluate_report_admissibility(config)
    assert summary["final_decision"] == APPROVED
    assert summary["missing_optional_artifacts"] == [str(missing)]


def test_final_decision_cannot_exceed_diagnostic_only(tmp_path):
    summary = _summary("Controlled diagnostic only. No universal benchmark claim is authorized.", tmp_path)
    assert summary["final_decision"] == APPROVED
    assert summary["strongest_allowed_interpretation"] == "diagnostic_only"
    assert summary["statistical_claim_authorized"] is False
    assert summary["provider_superiority_claim_authorized"] is False
    assert summary["xendris_superiority_claim_authorized"] is False
    assert summary["production_readiness_claim_authorized"] is False
    assert summary["universal_benchmark_claim_authorized"] is False


def test_writes_report_admissibility_artifacts(tmp_path):
    config = _config(tmp_path, "Diagnostic-only. No provider superiority claim authorized.")
    summary = write_report_admissibility_artifacts(config)
    assert summary["final_decision"] == APPROVED
    assert (config.output_dir / "report_admissibility_summary.json").exists()
    assert (config.output_dir / "report_admissibility_report.md").exists()
