import json
from pathlib import Path

import scripts.run_programming_calibration_ablation as ablation
from xendris.benchmarking import assess_programming_calibration_ablation
from xendris.benchmarking.programming import ProgrammingSample


def _sample(category: str) -> ProgrammingSample:
    name = f"solve_{category}"
    starter_code = f"def {name}(value):\n    return value\n"
    test_code = f"assert {name}(3) == 3\n"
    if category == "api_contracts":
        starter_code = f"def {name}(payload):\n    return {{'ok': True, 'data': payload}}\n"
        test_code = f"assert {name}('x') == {{'ok': True, 'data': 'x'}}\n"
    elif category == "bug_fixing":
        starter_code = f"def {name}(items):\n    return items[0]\n"
        test_code = f"assert {name}([1, 2]) == 1\nassert {name}([]) is None\n"
    elif category == "security_basics":
        starter_code = f"def {name}(expr):\n    return eval(expr)\n"
        test_code = f"assert {name}('abc') == 'abc'\n"
    elif category == "performance":
        starter_code = f"def {name}(items):\n    return len(set(items))\n"
        test_code = f"assert {name}([1, 1, 2]) == 2\n"
    return ProgrammingSample(
        sample_id=f"PR-{category.upper().replace('_', '-')}-ABL-001",
        category=category,
        language="python",
        prompt=f"Ablation fixture for {category}.",
        starter_code=starter_code,
        test_code=test_code,
        expected_behavior="Return expected value while preserving public contract.",
        expected_decision="INCLUDE",
        expected_reason="PASS",
        forbidden_changes=("public_signature",),
        metadata={},
    )


def _samples() -> list[ProgrammingSample]:
    return [
        _sample("api_contracts"),
        _sample("edge_cases"),
        _sample("unit_tests"),
    ]


def test_ablation_runner_creates_separate_output_path(tmp_path, monkeypatch):
    monkeypatch.setattr(ablation, "load_programming_reliability_v0_1", _samples)

    assert ablation.main(["--output-dir", str(tmp_path)]) == 0

    assert (tmp_path / "summary.json").exists()
    assert (tmp_path / "results.jsonl").exists()
    assert (tmp_path / "report.md").exists()


def test_three_variants_are_present(tmp_path, monkeypatch):
    monkeypatch.setattr(ablation, "load_programming_reliability_v0_1", _samples)
    ablation.main(["--output-dir", str(tmp_path)])

    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))

    assert summary["variants"] == ["deepseek_base", "xendris_uncalibrated", "xendris_calibrated"]
    assert set(summary["systems"]) == {"deepseek_base", "xendris_uncalibrated", "xendris_calibrated"}


def test_calibrated_variant_includes_calibration_metrics(tmp_path, monkeypatch):
    monkeypatch.setattr(ablation, "load_programming_reliability_v0_1", _samples)
    ablation.main(["--output-dir", str(tmp_path)])

    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))

    assert "calibration_metrics" in summary["systems"]["xendris_calibrated"]
    assert summary["systems"]["xendris_calibrated"]["calibration_metrics"]["calibrated_samples"] == 3


def test_uncalibrated_variant_does_not_require_calibration_metrics(tmp_path, monkeypatch):
    monkeypatch.setattr(ablation, "load_programming_reliability_v0_1", _samples)
    ablation.main(["--output-dir", str(tmp_path)])

    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))

    assert "calibration_metrics" not in summary["systems"]["xendris_uncalibrated"]


def test_category_deltas_are_computed_from_fixtures(tmp_path, monkeypatch):
    monkeypatch.setattr(ablation, "load_programming_reliability_v0_1", _samples)
    ablation.main(["--output-dir", str(tmp_path)])

    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))

    assert summary["category_deltas"]["api_contracts"]["calibrated_vs_uncalibrated"] > 0
    assert summary["category_deltas"]["unit_tests"]["calibrated_vs_uncalibrated"] > 0
    assert summary["answers"]["api_contracts_improved"] is True
    assert summary["answers"]["unit_tests_improved"] is True


def test_report_includes_limitations_and_no_universal_superiority_warning(tmp_path, monkeypatch):
    monkeypatch.setattr(ablation, "load_programming_reliability_v0_1", _samples)
    ablation.main(["--output-dir", str(tmp_path)])

    report = (tmp_path / "report.md").read_text(encoding="utf-8").lower()

    assert "## limitations" in report
    assert "no universal superiority" in report


def test_historical_benchmark_artifacts_are_not_overwritten(tmp_path, monkeypatch):
    monkeypatch.setattr(ablation, "load_programming_reliability_v0_1", _samples)
    historical = Path("runs/deepseek_vs_xendris_programming_reliability_v0_1_2026_07_04_summary.json")
    before = historical.stat().st_mtime_ns if historical.exists() else None

    ablation.main(["--output-dir", str(tmp_path)])

    after = historical.stat().st_mtime_ns if historical.exists() else None
    assert before == after


def test_gate_blocks_missing_calibration_disclosure(tmp_path, monkeypatch):
    monkeypatch.setattr(ablation, "load_programming_reliability_v0_1", _samples)
    ablation.main(["--output-dir", str(tmp_path)])
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    report = (tmp_path / "report.md").read_text(encoding="utf-8")
    summary["metadata"]["experimental_calibration_variant_disclosed"] = False

    assessment = assess_programming_calibration_ablation(summary, report)

    assert assessment.status == "BLOCKED_FOR_INTERPRETATION"
    assert any(issue.code == "missing_calibration_disclosure" for issue in assessment.issues)


def test_gate_blocks_universal_superiority_wording(tmp_path, monkeypatch):
    monkeypatch.setattr(ablation, "load_programming_reliability_v0_1", _samples)
    ablation.main(["--output-dir", str(tmp_path)])
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    report = (tmp_path / "report.md").read_text(encoding="utf-8")

    assessment = assess_programming_calibration_ablation(
        summary,
        report + "\nThis proves universal superiority.",
    )

    assert assessment.status == "BLOCKED_FOR_INTERPRETATION"
    assert any(issue.code == "universal_superiority_claim" for issue in assessment.issues)


def test_gate_admits_experimental_analysis(tmp_path, monkeypatch):
    monkeypatch.setattr(ablation, "load_programming_reliability_v0_1", _samples)
    ablation.main(["--output-dir", str(tmp_path)])
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))

    assert summary["evidence_gate"]["status"] == "ADMITTED_EXPERIMENTAL_ANALYSIS"
