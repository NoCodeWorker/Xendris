from pathlib import Path

import scripts.run_deepseek_vs_xendris_programming_reliability as run_script
from scripts.run_deepseek_vs_xendris_programming_reliability import (
    RUN_BASENAME,
    dry_run_xendris_callable,
    output_paths,
)
from xendris.benchmarking.programming import (
    ProgrammingSample,
    run_programming_benchmark,
    summarize_programming_results,
)


def _sample(category: str) -> ProgrammingSample:
    function_name = f"solve_{category}"
    return ProgrammingSample(
        sample_id=f"PR-{category.upper().replace('_', '-')}-CAL-001",
        category=category,
        language="python",
        prompt=f"Programming calibration fixture for {category}.",
        starter_code=f"def {function_name}(value):\n    return value\n",
        test_code=f"assert {function_name}(3) == 3\n",
        expected_behavior="Return the input unchanged.",
        expected_decision="INCLUDE",
        expected_reason="PASS",
        forbidden_changes=("public_signature",),
        metadata={},
    )


def _answer_callable(sample: ProgrammingSample, config: dict | None = None) -> dict:
    del config
    function_name = (sample.starter_code or "def solve(value):").split("def ", 1)[1].split("(", 1)[0]
    return {
        "system_name": "xendris_deepseek",
        "answer": f"```python\ndef {function_name}(value):\n    return value\n```",
        "latency_ms": 10,
        "estimated_cost_usd": 0.01,
    }


def test_default_runner_behavior_does_not_enable_calibration():
    result = run_programming_benchmark([_sample("api_contracts")], _answer_callable)[0]
    summary = summarize_programming_results([result])

    assert result.calibration_audit is None
    assert "calibration_audit" not in result.to_dict()
    assert summary.calibration_metrics is None
    assert "calibration_metrics" not in summary.to_dict()


def test_calibration_flag_enables_audit_fields():
    result = run_programming_benchmark(
        [_sample("api_contracts")],
        _answer_callable,
        {"experimental_calibration": True, "system_name": "xendris_deepseek"},
    )[0]

    assert result.calibration_audit is not None
    assert result.calibration_audit["calibration_enabled"] is True
    assert result.calibration_audit["domain"] == "PROGRAMMING"


def test_api_contracts_use_minimal_intervention_and_import_restriction():
    result = run_programming_benchmark(
        [_sample("api_contracts")],
        _answer_callable,
        {"experimental_calibration": True},
    )[0]

    audit = result.calibration_audit or {}
    assert audit["category"] == "API_CONTRACTS"
    assert audit["intervention_level"] == "MINIMAL"
    assert audit["allow_extra_imports"] is False
    assert audit["preserve_signature"] is True


def test_unit_tests_disallow_test_framework_imports_in_code_sandbox_mode():
    result = run_programming_benchmark(
        [_sample("unit_tests")],
        _answer_callable,
        {"experimental_calibration": True, "calibration_execution_mode": "CODE_SANDBOX"},
    )[0]

    audit = result.calibration_audit or {}
    assert audit["category"] == "UNIT_TESTS"
    assert audit["allow_test_framework_imports"] is False


def test_edge_cases_use_moderate_intervention_while_preserving_signature():
    result = run_programming_benchmark(
        [_sample("edge_cases")],
        _answer_callable,
        {"experimental_calibration": True},
    )[0]

    audit = result.calibration_audit or {}
    assert audit["intervention_level"] == "MODERATE"
    assert audit["preserve_signature"] is True


def test_summary_includes_calibration_metrics_when_enabled():
    samples = [_sample("api_contracts"), _sample("edge_cases"), _sample("security_basics")]
    results = run_programming_benchmark(samples, _answer_callable, {"experimental_calibration": True})
    summary = summarize_programming_results(results)

    assert summary.calibration_metrics is not None
    assert summary.calibration_metrics["calibrated_samples"] == 3
    assert summary.calibration_metrics["minimal_intervention_samples"] == 1
    assert summary.calibration_metrics["moderate_intervention_samples"] == 2
    assert summary.calibration_metrics["import_restricted_samples"] == 3
    assert summary.calibration_metrics["signature_preservation_required_samples"] == 3
    assert summary.calibration_metrics["test_framework_import_restricted_samples"] == 3
    assert summary.calibration_metrics["security_false_positive_warning_samples"] == 1


def test_no_calibration_metrics_are_required_when_disabled():
    results = run_programming_benchmark([_sample("edge_cases")], _answer_callable)

    assert summarize_programming_results(results).calibration_metrics is None


def _patch_script_samples(monkeypatch) -> None:
    monkeypatch.setattr(
        run_script,
        "load_programming_reliability_v0_1",
        lambda: [_sample("api_contracts"), _sample("edge_cases")],
    )


def test_historical_benchmark_artifacts_are_not_rewritten(tmp_path, monkeypatch):
    _patch_script_samples(monkeypatch)
    canonical_paths = output_paths("runs")
    before = {
        key: path.stat().st_mtime_ns
        for key, path in canonical_paths.items()
        if path.exists()
    }

    exit_code = run_script.main(["--dry-run", "--experimental-calibration", "--output-dir", str(tmp_path)])

    after = {
        key: path.stat().st_mtime_ns
        for key, path in canonical_paths.items()
        if path.exists()
    }
    assert exit_code == 0
    assert before == after
    assert (tmp_path / f"{RUN_BASENAME}_summary.json").exists()


def test_policy_integration_is_deterministic():
    config = {"experimental_calibration": True}
    first = run_programming_benchmark([_sample("api_contracts")], dry_run_xendris_callable, config)[0]
    second = run_programming_benchmark([_sample("api_contracts")], dry_run_xendris_callable, config)[0]

    assert first.calibration_audit == second.calibration_audit


def test_script_summary_contains_xendris_calibration_metrics_when_flag_is_enabled(tmp_path, monkeypatch):
    _patch_script_samples(monkeypatch)
    exit_code = run_script.main(["--dry-run", "--experimental-calibration", "--output-dir", str(tmp_path)])
    summary_path = Path(tmp_path) / f"{RUN_BASENAME}_summary.json"

    assert exit_code == 0
    summary_text = summary_path.read_text(encoding="utf-8")
    assert '"experimental_calibration": true' in summary_text
    assert '"calibration_metrics"' in summary_text
