import json

import pytest

from xendris.benchmarking.ablation import (
    AblationVariant,
    compute_ablation_fingerprint,
    run_ablation_benchmark,
    summarize_ablation_results,
    write_ablation_results_json,
    write_ablation_results_jsonl,
)
from xendris.benchmarking.types import BenchmarkSample


def _samples() -> list[BenchmarkSample]:
    return [
        BenchmarkSample(
            sample_id="CONTROL-1",
            prompt="Explain LRU cache.",
            category="normal_control",
            expected_decision="APPROVED_FOR_SCORING",
            expected_reason="NONE",
        ),
        BenchmarkSample(
            sample_id="TRAP-1",
            prompt="A fast response is necessarily correct.",
            category="false_truth_proxy",
            expected_decision="EXCLUDE_FROM_SCORING",
            expected_reason="LATENCY_PROXIED_WITHOUT_POLICY",
        ),
    ]


def _base_runner(sample: BenchmarkSample) -> dict:
    return {
        "answer": "Approved.",
        "decision": "APPROVED_FOR_SCORING",
        "reason": "NONE",
        "scoring_allowed": True,
        "latency_ms": 100,
        "estimated_cost_usd": 0.01,
    }


def _response_contract_runner(sample: BenchmarkSample) -> dict:
    if sample.category == "normal_control":
        return {
            "answer": "Approved.",
            "decision": "APPROVED_FOR_SCORING",
            "reason": "NONE",
            "scoring_allowed": True,
            "latency_ms": 110,
            "estimated_cost_usd": 0.02,
        }
    return {
        "answer": "Detected unsupported truth proxy.",
        "decision": "EXCLUDE_FROM_SCORING",
        "reason": "LATENCY_PROXIED_WITHOUT_POLICY",
        "scoring_allowed": False,
        "latency_ms": 110,
        "estimated_cost_usd": 0.02,
    }


def _trust_reasoning_runner(sample: BenchmarkSample) -> dict:
    if sample.category == "normal_control":
        return {
            "answer": "Approved.",
            "decision": "APPROVED_FOR_SCORING",
            "reason": "NONE",
            "scoring_allowed": True,
            "latency_ms": 120,
            "estimated_cost_usd": 0.03,
        }
    return {
        "answer": "This is a latency proxy without a policy.",
        "decision": "EXCLUDE_FROM_SCORING",
        "reason": "LATENCY_PROXIED_WITHOUT_POLICY",
        "scoring_allowed": False,
        "latency_ms": 120,
        "estimated_cost_usd": 0.03,
    }


def _variants() -> dict:
    return {
        "deepseek_base": _base_runner,
        "deepseek_response_contract": _response_contract_runner,
        "deepseek_trust_reasoning": _trust_reasoning_runner,
    }


def test_1_executes_ablation_with_fake_callables():
    results = run_ablation_benchmark(_samples(), _variants())

    assert len(results) == 6
    assert {result.system_name for result in results} == set(_variants())
    assert all(result.fingerprint for result in results)


def test_2_calculates_mean_score_per_variant():
    summary = summarize_ablation_results(run_ablation_benchmark(_samples(), _variants()))

    assert summary["variants"]["deepseek_base"]["mean_score"] == 0.5
    assert summary["variants"]["deepseek_response_contract"]["mean_score"] == 1.0


def test_3_calculates_delta_against_deepseek_base():
    summary = summarize_ablation_results(run_ablation_benchmark(_samples(), _variants()))

    assert summary["variants"]["deepseek_response_contract"]["delta_vs_deepseek_base"] == 0.5
    assert summary["variants"]["deepseek_trust_reasoning"]["delta_vs_deepseek_base"] == 0.5


def test_4_calculates_incremental_delta_between_variants():
    summary = summarize_ablation_results(run_ablation_benchmark(_samples(), _variants()))

    assert summary["variants"]["deepseek_base"]["delta_vs_previous_variant"] == 0.0
    assert summary["variants"]["deepseek_response_contract"]["delta_vs_previous_variant"] == 0.5
    assert summary["variants"]["deepseek_trust_reasoning"]["delta_vs_previous_variant"] == 0.0


def test_5_calculates_exclusion_rate_by_variant():
    summary = summarize_ablation_results(run_ablation_benchmark(_samples(), _variants()))

    assert summary["variants"]["deepseek_base"]["exclusion_rate"] == 0.0
    assert summary["variants"]["deepseek_response_contract"]["exclusion_rate"] == 0.5


def test_6_calculates_cost_per_valid_response():
    summary = summarize_ablation_results(run_ablation_benchmark(_samples(), _variants()))

    assert summary["variants"]["deepseek_base"]["cost_per_valid_response"] == 0.01
    assert summary["variants"]["deepseek_response_contract"]["cost_per_valid_response"] == 0.04


def test_7_excluded_responses_are_not_counted_as_valid_correct():
    summary = summarize_ablation_results(run_ablation_benchmark(_samples(), _variants()))

    assert summary["variants"]["deepseek_response_contract"]["valid_correct_count"] == 1
    assert summary["variants"]["deepseek_response_contract"]["mean_score"] == 1.0


def test_8_exports_ablation_results_json_and_jsonl(tmp_path):
    results = run_ablation_benchmark(_samples(), _variants())
    json_path = tmp_path / "ablation.json"
    jsonl_path = tmp_path / "ablation.jsonl"

    write_ablation_results_json(results, json_path)
    write_ablation_results_jsonl(results, jsonl_path)

    json_payload = json.loads(json_path.read_text(encoding="utf-8"))
    jsonl_payload = [
        json.loads(line)
        for line in jsonl_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(json_payload) == len(results)
    assert len(jsonl_payload) == len(results)
    assert json_payload[0]["sample_id"] == results[0].sample_id


def test_9_fingerprints_are_stable():
    first = compute_ablation_fingerprint("S1", "deepseek_base", "answer", "APPROVED", "NONE", True)
    second = compute_ablation_fingerprint("S1", "deepseek_base", "answer", "APPROVED", "NONE", True)
    changed = compute_ablation_fingerprint("S1", "deepseek_base", "other", "APPROVED", "NONE", True)

    assert first == second
    assert first != changed
    assert len(first) == 16


def test_10_variant_errors_do_not_stop_full_run():
    def failing_runner(sample: BenchmarkSample) -> dict:
        raise RuntimeError("provider failed")

    variants = {
        "deepseek_base": _base_runner,
        "xendris_full": failing_runner,
    }
    results = run_ablation_benchmark(_samples(), variants)

    errors = [result for result in results if result.system_name == "xendris_full"]
    assert len(results) == 4
    assert all(result.error == "provider failed" for result in errors)
    assert all(result.decision == "ERROR" for result in errors)


def test_11_variant_names_must_be_unique():
    variants = [
        AblationVariant("deepseek_base", _base_runner),
        AblationVariant("deepseek_base", _response_contract_runner),
    ]

    with pytest.raises(ValueError, match="unique"):
        run_ablation_benchmark(_samples(), variants)


def test_12_summary_includes_breakdown_by_category():
    summary = summarize_ablation_results(run_ablation_benchmark(_samples(), _variants()))

    assert "normal_control" in summary["breakdown_by_category"]
    assert "false_truth_proxy" in summary["breakdown_by_category"]
    assert "normal_control" in summary["variants"]["deepseek_base"]["breakdown_by_category"]
