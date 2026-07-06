import json

from scripts.run_deepseek_vs_xendris_programming_reliability import (
    RUN_BASENAME,
    build_ab_summary,
    compute_file_hash,
    dry_run_deepseek_callable,
    dry_run_xendris_callable,
    main,
    output_paths,
)
from xendris.benchmarking.programming import (
    ProgrammingSample,
    load_programming_reliability_v0_1,
    run_programming_benchmark,
)


def _sample() -> ProgrammingSample:
    return ProgrammingSample(
        sample_id="PR-NORMAL-CONTROL-AB-001",
        category="normal_control",
        language="python",
        prompt="Return value unchanged.",
        starter_code="def solve(value):\n    return None\n",
        test_code="assert solve(5) == 5\n",
        expected_behavior="Return the input unchanged.",
        expected_decision="INCLUDE",
    )


def test_1_script_supports_dry_run_with_fake_callables(tmp_path):
    exit_code = main(["--dry-run", "--output-dir", str(tmp_path)])

    assert exit_code == 0
    assert (tmp_path / f"{RUN_BASENAME}.jsonl").exists()
    assert (tmp_path / f"{RUN_BASENAME}_summary.json").exists()
    assert (tmp_path / f"{RUN_BASENAME}_excellence.json").exists()


def test_2_dry_run_does_not_call_real_apis():
    result = dry_run_deepseek_callable(_sample())

    assert result["system_name"] == "deepseek_base"
    assert "answer" in result


def test_3_missing_api_key_returns_controlled_error(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    assert main(["--output-dir", "runs"]) == 1


def test_4_output_paths_are_correct(tmp_path):
    paths = output_paths(tmp_path)

    assert paths["jsonl"].name == f"{RUN_BASENAME}.jsonl"
    assert paths["summary"].name == f"{RUN_BASENAME}_summary.json"
    assert paths["excellence"].name == f"{RUN_BASENAME}_excellence.json"
    assert paths["report"].name == "RUN_DEEPSEEK_VS_XENDRIS_PROGRAMMING_RELIABILITY_V0_1_2026_07_04.md"


def test_5_dataset_hash_is_stable():
    dataset_path = "xendris/benchmarking/datasets/programming_reliability_v0_1.jsonl"

    assert compute_file_hash(dataset_path) == compute_file_hash(dataset_path)
    assert len(compute_file_hash(dataset_path)) == 64


def test_6_summary_contains_required_metrics():
    samples = [_sample()]
    ds = run_programming_benchmark(samples, dry_run_deepseek_callable, {"system_name": "deepseek_base"})
    xe = run_programming_benchmark(samples, dry_run_xendris_callable, {"system_name": "xendris_deepseek"})
    summary = build_ab_summary(samples, ds, xe, {"execution_mode": "dry-run"})

    for key in (
        "total_samples",
        "average_score_deepseek",
        "average_score_xendris",
        "average_delta",
        "xendris_wins",
        "deepseek_wins",
        "ties",
        "systems",
        "score_by_category",
    ):
        assert key in summary


def test_7_correct_code_scores_high():
    result = run_programming_benchmark([_sample()], dry_run_xendris_callable)[0]

    assert result.score == 1.0


def test_8_broken_contract_scores_low():
    def broken(sample: ProgrammingSample) -> dict:
        return {"answer": "```python\ndef solve(value, extra=None):\n    return value\n```"}

    result = run_programming_benchmark([_sample()], broken)[0]

    assert result.contract_preserved is False
    assert result.score == 0.0


def test_9_unsafe_pattern_marks_security_risk():
    def unsafe(sample: ProgrammingSample) -> dict:
        return {"answer": "```python\ndef solve(value):\n    return eval(value)\n```"}

    result = run_programming_benchmark([_sample()], unsafe)[0]

    assert result.security_risk is True
    assert result.score == 0.0


def test_10_runner_continues_after_sample_error():
    samples = [_sample(), _sample()]

    def flaky(sample: ProgrammingSample) -> dict:
        if not hasattr(flaky, "called"):
            flaky.called = True
            raise RuntimeError("boom")
        return dry_run_xendris_callable(sample)

    results = run_programming_benchmark(samples, flaky)

    assert len(results) == 2
    assert results[0].runtime_error is not None
    assert results[1].score == 1.0


def test_dry_run_summary_json_has_metrics(tmp_path):
    main(["--dry-run", "--output-dir", str(tmp_path)])
    payload = json.loads((tmp_path / f"{RUN_BASENAME}_summary.json").read_text(encoding="utf-8"))
    excellence = json.loads((tmp_path / f"{RUN_BASENAME}_excellence.json").read_text(encoding="utf-8"))

    assert payload["total_samples"] == 100
    assert "cost_per_correct_solution" in payload["systems"]["deepseek_base"]
    assert "latency_average_ms" in payload["systems"]["xendris_deepseek"]
    assert excellence["decision"] == "READY_FOR_INTERPRETATION"
    assert excellence["has_blockers"] is False


def test_dataset_available_for_run():
    assert len(load_programming_reliability_v0_1()) == 100
