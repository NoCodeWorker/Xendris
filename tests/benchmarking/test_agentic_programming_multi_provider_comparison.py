from __future__ import annotations

import json

from scripts.run_agentic_programming_benchmark import (
    _build_canonical_summary,
    _compute_deltas,
)
from xendris.benchmarking.agentic_programming.excellence_gate import evaluate_excellence_gate
from xendris.benchmarking.agentic_programming.scorer import compute_scores
from xendris.benchmarking.agentic_programming.types import AgentVariant, BenchmarkConfig, TaskResult


def _result(
    variant: str,
    provider: str,
    model: str,
    passed: bool,
    cost: float = 0.001,
) -> TaskResult:
    return TaskResult(
        sample_id=f"AP-{variant}",
        agent_variant=variant,
        patch_applied=True,
        visible_tests_passed=passed,
        hidden_tests_passed=passed,
        api_contract_preserved=True,
        no_forbidden_files_touched=True,
        no_false_success_claim=True,
        minimal_patch=True,
        security_clean=True,
        iterations_used=1,
        error_message=None,
        patch_content="",
        provider=provider,
        model=model,
        provider_reported_model=model,
        transport="direct",
        latency_ms=100.0,
        cost_estimate=cost,
        cost_estimate_quality="known_pricing",
    )


def _config() -> BenchmarkConfig:
    return BenchmarkConfig(
        dataset_path="benchmarks/agentic_programming/v0_1",
        agent_variants=(
            AgentVariant.DEEPSEEK_BASE_AGENT,
            AgentVariant.OPENAI_BASE_AGENT,
            AgentVariant.DEEPSEEK_XENDRIS_AGENT,
            AgentVariant.OPENAI_XENDRIS_AGENT,
            AgentVariant.DEEPSEEK_XENDRIS_CALIBRATED_AGENT,
            AgentVariant.OPENAI_XENDRIS_CALIBRATED_AGENT,
        ),
        execution_mode="live",
        output_dir="/tmp/multi-provider",
        agent_module="xendris.benchmarking.agentic_programming.agents",
        max_concurrent=1,
        seed=42,
        provider="deepseek,openai",
        transport="direct",
        budget_usd=1.5,
        max_samples=1,
        max_iterations=2,
        credential_sources_by_provider={
            "deepseek": "dotenv:frontend/.env.local/DEEPSEEK_API_KEY",
            "openai": "dotenv:frontend/.env.local/OPENAI_API_KEY",
        },
        model_map={
            "deepseek": "deepseek-v4-flash",
            "openai": "gpt-4.1-mini",
        },
    )


def test_mixed_provider_summary_has_per_variant_metadata():
    results = [
        _result("deepseek_base_agent", "deepseek", "deepseek-v4-flash", False),
        _result("openai_base_agent", "openai", "gpt-4.1-mini", False),
        _result("deepseek_xendris_agent", "deepseek", "deepseek-v4-flash", True),
        _result("openai_xendris_agent", "openai", "gpt-4.1-mini", True),
        _result("deepseek_xendris_calibrated_agent", "deepseek", "deepseek-v4-flash", True),
        _result("openai_xendris_calibrated_agent", "openai", "gpt-4.1-mini", True),
    ]
    scores = compute_scores(results)
    summary = _build_canonical_summary(results, _config(), scores, evaluate_excellence_gate(scores), comparison_mode=True)

    assert summary["providers"] == ["deepseek", "openai"]
    assert summary["transports"] == ["direct"]
    assert summary["no_openrouter_used"] is True
    assert summary["models_by_variant"]["deepseek_base_agent"] == "deepseek-v4-flash"
    assert summary["models_by_variant"]["openai_base_agent"] == "gpt-4.1-mini"
    assert summary["credential_sources_by_provider"]["deepseek"].startswith("dotenv:")
    assert summary["credential_sources_by_provider"]["openai"].startswith("dotenv:")


def test_provider_local_and_cross_provider_deltas_are_computed():
    scores = {
        "deepseek_base_agent": {"total_score": 0.5, "pass_rate": 0.0},
        "deepseek_xendris_agent": {"total_score": 0.8, "pass_rate": 1.0},
        "deepseek_xendris_calibrated_agent": {"total_score": 0.9, "pass_rate": 1.0},
        "openai_base_agent": {"total_score": 0.6, "pass_rate": 0.0},
        "openai_xendris_agent": {"total_score": 0.85, "pass_rate": 1.0},
        "openai_xendris_calibrated_agent": {"total_score": 0.95, "pass_rate": 1.0},
    }

    deltas = _compute_deltas(scores)

    assert deltas["deepseek_xendris_agent"]["delta_vs_base"] == 0.3
    assert deltas["openai_xendris_agent"]["delta_vs_base"] == 0.25
    assert deltas["openai_base_agent"]["delta_vs_deepseek_base"] == 0.1
    assert deltas["openai_xendris_calibrated_agent"]["distance_to_oracle"] == 0.05


def test_benchmark_level_comparison_mode_preserves_variant_decisions():
    results = [
        _result("deepseek_base_agent", "deepseek", "deepseek-v4-flash", False),
        _result("openai_base_agent", "openai", "gpt-4.1-mini", False),
        _result("deepseek_xendris_calibrated_agent", "deepseek", "deepseek-v4-flash", True),
        _result("openai_xendris_calibrated_agent", "openai", "gpt-4.1-mini", True),
    ]
    scores = compute_scores(results)
    decisions = evaluate_excellence_gate(scores)

    summary = _build_canonical_summary(results, _config(), scores, decisions, comparison_mode=True)
    strict_summary = _build_canonical_summary(results, _config(), scores, decisions, comparison_mode=False)

    assert summary["variant_gate_decisions"]["deepseek_base_agent"] == "BLOCKED_FOR_INTERPRETATION"
    assert summary["benchmark_level_decision"] == "WARNINGS_PRESENT"
    assert strict_summary["benchmark_level_decision"] == "BLOCKED_FOR_INTERPRETATION"


def test_missing_provider_metadata_blocks_benchmark_interpretation():
    result = _result("openai_base_agent", "openai", "gpt-4.1-mini", True)
    broken = _config()
    broken = BenchmarkConfig(
        dataset_path=broken.dataset_path,
        agent_variants=broken.agent_variants,
        execution_mode=broken.execution_mode,
        output_dir=broken.output_dir,
        agent_module=broken.agent_module,
        max_concurrent=broken.max_concurrent,
        seed=broken.seed,
        transport=None,
    )

    summary = _build_canonical_summary([result], broken, compute_scores([result]), evaluate_excellence_gate(compute_scores([result])), comparison_mode=True)

    assert summary["interpretation_admissibility"]["admissible"] is False
    assert summary["interpretation_admissibility"]["transport_metadata_sufficient"] is False
    assert "transport_metadata_only_resolved_from_result_level" in summary["interpretation_admissibility"]["limitations"]


def test_summary_artifact_does_not_include_secret_values_or_headers():
    result = _result("openai_base_agent", "openai", "gpt-4.1-mini", True)
    summary = _build_canonical_summary([result], _config(), compute_scores([result]), evaluate_excellence_gate(compute_scores([result])), comparison_mode=True)
    text = json.dumps(summary)

    assert "unit-test-secret" not in text
    assert "Authorization:" not in text
    assert "Bearer" not in text
    assert "OPENROUTER_API_KEY" not in text
