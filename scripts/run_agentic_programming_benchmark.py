from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from xendris.benchmarking.agentic_programming import (
    BenchmarkConfig,
    BenchmarkRunOutput,
    compute_scores,
    evaluate_excellence_gate,
    export_to_jsonl,
    generate_markdown_report,
    load_dataset,
    run_benchmark,
)
from xendris.benchmarking.agentic_programming.types import AgentVariant, BenchmarkRunOutput, TaskResult
from xendris.benchmarking.agentic_programming.agents.deepseek_provider import get_deepseek_api_key


ORACLE_SCORE = 1.0
DEEPSEEK_KEY_NAME = "DEEPSEEK_API_KEY"
READY = "READY_FOR_INTERPRETATION"
WARNINGS = "WARNINGS_PRESENT"
BLOCKED = "BLOCKED_FOR_INTERPRETATION"


def _parse_env_file_value(path: str, key_name: str = DEEPSEEK_KEY_NAME) -> str | None:
    if not os.path.isfile(path):
        return None

    with open(path, encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() != key_name:
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            return value or None

    return None


def load_deepseek_api_key_from_env_files(repo_root: str | None = None) -> dict[str, object]:
    if os.environ.get(DEEPSEEK_KEY_NAME):
        return {
            "detected": True,
            "key_name": DEEPSEEK_KEY_NAME,
            "source": "process_env",
            "credential_source": f"env:{DEEPSEEK_KEY_NAME}",
        }

    root = repo_root or os.getcwd()
    candidates = [
        (".env.local", os.path.join(root, ".env.local")),
        (".env", os.path.join(root, ".env")),
        ("frontend/.env.local", os.path.join(root, "frontend", ".env.local")),
        ("frontend/.env", os.path.join(root, "frontend", ".env")),
    ]
    for source, path in candidates:
        value = _parse_env_file_value(path)
        if value:
            os.environ[DEEPSEEK_KEY_NAME] = value
            return {
                "detected": True,
                "key_name": DEEPSEEK_KEY_NAME,
                "source": source,
                "credential_source": f"dotenv:{source}/{DEEPSEEK_KEY_NAME}",
            }

    return {
        "detected": False,
        "key_name": DEEPSEEK_KEY_NAME,
        "source": "missing",
        "credential_source": "missing",
    }


def _compute_category_breakdown(results: list[TaskResult], dataset_path: str) -> dict:
    tasks = load_dataset(dataset_path)
    task_map = {t.sample_id: t for t in tasks}
    by_category: dict[str, dict] = {}
    for r in results:
        task = task_map.get(r.sample_id)
        cat = task.category if task else "unknown"
        if cat not in by_category:
            by_category[cat] = {"total": 0, "visible_passed": 0, "hidden_passed_or_none": 0}
        by_category[cat]["total"] += 1
        if r.visible_tests_passed:
            by_category[cat]["visible_passed"] += 1
        if r.hidden_tests_passed is not False:
            by_category[cat]["hidden_passed_or_none"] += 1
    return by_category


def _compute_commercial_metrics(results: list[TaskResult]) -> dict:
    total = len(results) or 1
    visible_pass = sum(1 for r in results if r.visible_tests_passed)
    hidden_pass = sum(1 for r in results if r.hidden_tests_passed)
    api_ok = sum(1 for r in results if r.api_contract_preserved)
    forbidden_ok = sum(1 for r in results if r.no_forbidden_files_touched)
    false_success_ok = sum(1 for r in results if r.no_false_success_claim)
    minimal = sum(1 for r in results if r.minimal_patch)
    security_ok = sum(1 for r in results if r.security_clean)
    verified_success = sum(1 for r in results if r.visible_tests_passed and r.hidden_tests_passed is not False)
    total_cost = sum(r.cost_estimate for r in results if r.cost_estimate is not None)
    latencies = [r.latency_ms for r in results if r.latency_ms is not None]

    return {
        "task_success_rate": round(
            verified_success / total, 4
        ),
        "verified_successful_count": verified_success,
        "visible_test_pass_rate": round(visible_pass / total, 4),
        "hidden_test_pass_rate": round(hidden_pass / total, 4),
        "api_preservation_rate": round(api_ok / total, 4),
        "forbidden_file_touch_rate": round((total - forbidden_ok) / total, 4),
        "false_success_claim_rate": round((total - false_success_ok) / total, 4),
        "unauthorized_dependency_rate": 0.0,
        "minimal_patch_rate": round(minimal / total, 4),
        "security_clean_rate": round(security_ok / total, 4),
        "average_latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else None,
        "estimated_cost_total": round(total_cost, 6) if total_cost else None,
        "cost_per_verified_successful_task": round(total_cost / verified_success, 6) if total_cost and verified_success > 0 else None,
    }


def _group_by_variant(results: list[TaskResult]) -> dict[str, list[TaskResult]]:
    grouped: dict[str, list[TaskResult]] = {}
    for result in results:
        grouped.setdefault(result.agent_variant, []).append(result)
    return grouped


def _compute_metrics_by_variant(results: list[TaskResult], scores: dict[str, dict]) -> dict[str, dict]:
    metrics: dict[str, dict] = {}
    for variant, variant_results in _group_by_variant(results).items():
        commercial = _compute_commercial_metrics(variant_results)
        score = scores.get(variant, {})
        total = len(variant_results)
        avg_iterations = (
            sum(r.iterations_used for r in variant_results) / total
            if total
            else 0
        )
        metrics[variant] = {
            "total_samples": total,
            "avg_score": score.get("total_score"),
            "task_success_rate": commercial["task_success_rate"],
            "verified_success_rate": commercial["task_success_rate"],
            "visible_test_pass_rate": commercial["visible_test_pass_rate"],
            "hidden_test_pass_rate": commercial["hidden_test_pass_rate"],
            "api_preservation_rate": commercial["api_preservation_rate"],
            "forbidden_file_touch_rate": commercial["forbidden_file_touch_rate"],
            "false_success_claim_rate": commercial["false_success_claim_rate"],
            "unauthorized_dependency_rate": commercial["unauthorized_dependency_rate"],
            "minimal_patch_rate": commercial["minimal_patch_rate"],
            "average_iterations": round(avg_iterations, 4),
            "average_latency_ms": commercial["average_latency_ms"],
            "estimated_cost_total": commercial["estimated_cost_total"],
            "cost_per_verified_successful_task": commercial["cost_per_verified_successful_task"],
            "distance_to_oracle": round(ORACLE_SCORE - score.get("total_score", 0), 4),
        }
    return metrics


def _compute_deltas(scores: dict[str, dict]) -> dict:
    base_score = None
    for variant, data in scores.items():
        if variant == "deepseek_base_agent":
            base_score = data.get("total_score", 0)
            break

    deltas: dict[str, dict] = {}
    for variant, data in scores.items():
        variant_score = data.get("total_score", 0)
        deltas[variant] = {
            "distance_to_oracle": round(ORACLE_SCORE - variant_score, 4),
            "delta_vs_deepseek_base": round(variant_score - (base_score or variant_score), 4),
        }
    return deltas


def _blocked_variant_reasons(
    scores: dict[str, dict],
    excellence_decisions: dict[str, str],
) -> dict[str, str]:
    reasons: dict[str, str] = {}
    for variant, decision in excellence_decisions.items():
        if decision != BLOCKED:
            continue
        data = scores.get(variant, {})
        reasons[variant] = (
            "Variant-level interpretation gate blocked this result "
            f"(score={data.get('total_score')}, pass_rate={data.get('pass_rate')}). "
            "It is retained for comparison only and is not admitted as positive evidence."
        )
    return reasons


def _evaluate_benchmark_level_decision(summary: dict, comparison_mode: bool) -> str:
    required_fields = [
        "dataset_name",
        "dataset_version",
        "dataset_size",
        "provider",
        "transport",
        "model",
        "limitations",
        "no_universal_superiority_warning",
    ]
    missing = [field for field in required_fields if not summary.get(field)]
    if missing:
        return BLOCKED

    warning_text = str(summary.get("no_universal_superiority_warning", "")).lower()
    if "superiority" not in warning_text or ("no " not in warning_text and "not " not in warning_text):
        return BLOCKED

    if not summary.get("no_openrouter_used"):
        return BLOCKED

    if summary.get("transport") != "direct" or summary.get("provider") != "deepseek":
        return BLOCKED

    if not summary.get("total_results") or not summary.get("scores_by_variant"):
        return BLOCKED

    if summary.get("blocked_variants"):
        return WARNINGS if comparison_mode else BLOCKED

    return READY


def _build_canonical_summary(
    results: list[TaskResult],
    config: BenchmarkConfig,
    scores: dict,
    excellence_decisions: dict[str, str],
    comparison_mode: bool = False,
) -> dict:
    total_tasks = len(load_dataset(config.dataset_path)) if config.max_samples is None else config.max_samples
    agents = sorted(set(r.agent_variant for r in results))
    category_breakdown = _compute_category_breakdown(results, config.dataset_path)
    commercial = _compute_commercial_metrics(results)
    metrics_by_variant = _compute_metrics_by_variant(results, scores)
    is_live = config.execution_mode == "live"
    is_deepseek = any("deepseek" in v for v in agents)
    transport = config.transport if is_live else None
    blocked_variant_reasons = _blocked_variant_reasons(scores, excellence_decisions)
    blocked_variants = sorted(blocked_variant_reasons)

    has_deepseek_variants = any(v in agents for v in ["deepseek_base_agent", "deepseek_xendris_agent", "deepseek_xendris_calibrated_agent"])

    summary = {
        "benchmark_name": "Agentic Programming Reliability",
        "benchmark_version": "v0.1",
        "dataset_name": "Xendris Agentic Programming v0.1",
        "dataset_version": "0.1",
        "dataset_size": total_tasks,
        "execution_mode": config.execution_mode,
        "provider_mode": "real" if is_live else "mock",
        "variants": agents,
        "total_results": len(results),
        "scoring_formula": {
            "weighted_components": {
                "hidden_tests_pass": 0.35,
                "visible_tests_pass": 0.20,
                "api_contract_preserved": 0.15,
                "no_forbidden_files_touched": 0.10,
                "no_false_success_claim": 0.10,
                "minimal_patch": 0.05,
                "security_clean": 0.05,
            },
            "hard_penalties": {
                "critical_error": -1.0,
                "forbidden_file_touch": -0.5,
                "false_success_claim": -0.5,
            },
        },
        "scores_by_variant": scores,
        "deltas": _compute_deltas(scores),
        "metrics_by_variant": metrics_by_variant,
        "category_breakdown": category_breakdown,
        "commercial_metrics": commercial,
        "excellence_gate_decisions": excellence_decisions,
        "variant_gate_decisions": excellence_decisions,
        "blocked_variants": blocked_variants,
        "blocked_variant_reasons": blocked_variant_reasons,
        "comparison_mode": comparison_mode,
        "comparison_interpretation_scope": "Blocked variants are included for comparison only and are not admitted as positive evidence.",
        "no_universal_superiority_warning": "This benchmark evaluates Xendris variants against a DeepSeek base on a specific closed dataset. No claim of universal superiority over any other model or agent framework is made or implied.",
        "no_general_coding_superiority_warning": "This benchmark is not evidence of general coding superiority. Results are limited to the closed Agentic Programming v0.1 dataset, provider, model, and configuration.",
        "evidence_interpretation": "Admitted as real-provider pilot evidence for Agentic Programming v0.1 only. Not admissible as evidence of general coding superiority, production readiness, or performance on open-ended programming tasks.",
    }

    if is_live and is_deepseek:
        summary["provider"] = config.provider
        summary["model"] = config.model
        summary["requested_model"] = config.model
        reported_models = sorted({r.provider_reported_model for r in results if r.provider_reported_model})
        summary["provider_reported_model"] = reported_models[0] if len(reported_models) == 1 else (reported_models or None)
        summary["credential_source"] = config.credential_source or "env:DEEPSEEK_API_KEY"
        summary["no_openrouter_used"] = True
        if transport:
            summary["transport"] = transport
        summary["cost_disclosure"] = "Cost estimates are based on token counts from API responses using published per-token pricing. Actual costs may vary."
        summary["latency_disclosure"] = "Latency is measured as wall-clock time for the API call to complete. Does not include sandbox test execution time."

    if is_live:
        summary["limitations"] = [
            "Execution mode is live: the direct DeepSeek API was called, not OpenRouter.",
            "Dataset is closed synthetic (20 samples); does not represent real-world programming diversity.",
            "Results are specific to the Agentic Programming v0.1 benchmark and should not be generalized.",
            "Results do not transfer to OpenRouter or any other transport.",
            "Deterministic controls (oracle_agent, partial_agent, bad_agent) are reference baselines only, not evidence of real-provider performance.",
            "Cost/latency estimates depend on API response conditions and may not be reproducible.",
            "No comparison against Claude, GPT, Codex, or any other model is included. No superior generalization is claimed.",
            "Pre-existing fitz import error in test_master_goal_frontera_c_decision.py is unrelated and persists.",
        ]
    else:
        summary["limitations"] = [
            "Execution mode is dry-run: no real provider was called, no real model output was evaluated.",
            "Provider mode is mock: patches are generic stubs, not real agent output.",
            "These results are NOT evidence of real-provider agent programming performance.",
            "These results are NOT evidence of general programming superiority.",
            "These results are NOT evidence of production readiness.",
            "Dataset is closed synthetic (20 samples); does not represent real-world programming diversity.",
            "Pre-existing fitz import error in test_master_goal_frontera_c_decision.py is unrelated and persists.",
        ]

    if not is_live:
        summary["no_real_provider_performance_warning"] = "No real provider was called. All task results use mock/stub patches. Real-provider performance requires a separate live-mode run with provider credentials and real agent implementations."
        summary["no_universal_superiority_warning"] = "This dry-run does not compare against any other model or agent framework. No claim of universal superiority is made or implied."

    summary["benchmark_level_decision"] = _evaluate_benchmark_level_decision(summary, comparison_mode)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Xendris Agentic Programming Benchmark v0.1"
    )
    parser.add_argument(
        "--dataset-path",
        default="benchmarks/agentic_programming/v0_1",
        help="Path to benchmark dataset directory",
    )
    parser.add_argument(
        "--execution-mode",
        default="dry-run",
        choices=["dry-run", "live"],
        help="Execution mode (default: dry-run)",
    )
    valid_variants = [v.value for v in AgentVariant]
    parser.add_argument(
        "--agent-variants", "--variants",
        nargs="+",
        default=["base_agent", "xendris_agent", "xendris_calibrated_agent"],
        help="Agent variants to evaluate (space-separated or comma-separated)",
    )
    parser.add_argument(
        "--output-dir", "--outdir",
        default="benchmarks/agentic_programming/v0_1/output",
        help="Output directory for results",
        dest="output_dir",
    )
    parser.add_argument(
        "--agent-module",
        default="xendris.benchmarking.agentic_programming.agents",
        help="Python module path for agent implementations",
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=4,
        help="Maximum concurrent tasks per variant",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed",
    )
    parser.add_argument(
        "--provider",
        default=None,
        help="Provider name (e.g. deepseek)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (e.g. deepseek-v4-flash)",
    )
    parser.add_argument(
        "--transport",
        default=None,
        choices=["direct"],
        help="Transport for live DeepSeek runs. This pilot supports direct only.",
    )
    parser.add_argument(
        "--budget-usd",
        type=float,
        default=None,
        help="Maximum budget in USD",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Maximum number of samples to evaluate (for budget control)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum agent iterations per sample",
    )
    parser.add_argument(
        "--fail-on-gate-blockers",
        action="store_true",
        help="Exit with non-zero status if any variant is BLOCKED_FOR_INTERPRETATION",
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Check DeepSeek credential discovery without running the benchmark",
    )
    parser.add_argument(
        "--comparison-mode",
        action="store_true",
        help="Allow blocked variants to remain in comparative artifacts without aborting if the benchmark-level decision is not blocked",
    )

    args = parser.parse_args()

    raw_variants: list[str] = []
    for item in args.agent_variants:
        raw_variants.extend(item.split(","))

    valid_variants = [v.value for v in AgentVariant]
    for v in raw_variants:
        if v not in valid_variants:
            print(f"Invalid variant '{v}'. Choose from: {valid_variants}")
            sys.exit(1)

    has_deepseek = any("deepseek" in v for v in raw_variants)
    credential_metadata = (
        load_deepseek_api_key_from_env_files()
        if args.execution_mode == "live" and has_deepseek
        else {
            "detected": False,
            "key_name": DEEPSEEK_KEY_NAME,
            "source": "missing",
            "credential_source": "missing",
        }
    )

    if args.preflight_only:
        print(f"{DEEPSEEK_KEY_NAME} detected: {str(bool(credential_metadata['detected'])).lower()}")
        print(f"credential_source: {credential_metadata['credential_source']}")
        if not credential_metadata["detected"]:
            sys.exit(1)
        return

    if args.execution_mode == "live":
        if has_deepseek and args.provider != "deepseek":
            print("ERROR: Live DeepSeek pilot requires --provider deepseek.")
            sys.exit(1)
        if has_deepseek and args.transport != "direct":
            print("ERROR: Live DeepSeek pilot requires --transport direct.")
            sys.exit(1)
        if has_deepseek and args.model != "deepseek-v4-flash":
            print("ERROR: Live DeepSeek pilot requires --model deepseek-v4-flash.")
            sys.exit(1)
        if has_deepseek and not get_deepseek_api_key():
            print("ERROR: Live DeepSeek variants require an API key.")
            print("ERROR: Live DeepSeek direct variants require DEEPSEEK_API_KEY. Set it in the environment, .env.local, or frontend/.env.local.")
            sys.exit(1)
        if has_deepseek and args.agent_module == "xendris.benchmarking.agentic_programming.agents" and args.budget_usd is not None:
            estimated_calls = (len(raw_variants) * (args.max_samples or 20))
            estimated_cost = estimated_calls * 0.002
            if estimated_cost > args.budget_usd:
                print(f"ERROR: Estimated cost (${estimated_cost:.4f}) exceeds budget (${args.budget_usd:.2f}).")
                print(f"Reduce --max-samples or --variants, or increase --budget-usd.")
                sys.exit(1)

    transport = args.transport if args.execution_mode == "live" and any("deepseek" in v for v in raw_variants) else None

    config = BenchmarkConfig(
        dataset_path=args.dataset_path,
        agent_variants=tuple(AgentVariant(v) for v in raw_variants),
        execution_mode=args.execution_mode,
        output_dir=args.output_dir,
        agent_module=args.agent_module,
        max_concurrent=args.max_concurrent,
        seed=args.seed,
        provider=args.provider,
        model=args.model,
        transport=transport,
        budget_usd=args.budget_usd,
        max_samples=args.max_samples,
        max_iterations=args.max_iterations,
        credential_source=str(credential_metadata["credential_source"]) if credential_metadata["detected"] else None,
    )

    print(f"Xendris Agentic Programming Benchmark v0.1")
    print(f"  Dataset: {config.dataset_path}")
    print(f"  Mode: {config.execution_mode}")
    print(f"  Variants: {[v.value for v in config.agent_variants]}")
    if args.provider:
        print(f"  Provider: {args.provider}")
    if args.model:
        print(f"  Model: {args.model}")
    if transport:
        print(f"  Transport: {transport}")
    if args.budget_usd:
        print(f"  Budget: ${args.budget_usd:.2f}")
    if args.max_samples:
        print(f"  Max Samples: {args.max_samples}")
    if args.max_iterations:
        print(f"  Max Iterations: {args.max_iterations}")
    print()

    start = time.time()
    results = run_benchmark(config)
    elapsed = time.time() - start

    scores = compute_scores(results)
    excellence_decisions = evaluate_excellence_gate(scores)
    deltas = _compute_deltas(scores)

    os.makedirs(args.output_dir, exist_ok=True)

    jsonl_path = os.path.join(args.output_dir, "results.jsonl")
    export_to_jsonl(results, jsonl_path)
    print(f"Results exported to: {jsonl_path}")

    md_path = os.path.join(args.output_dir, "report.md")
    summary = _build_canonical_summary(results, config, scores, excellence_decisions, comparison_mode=args.comparison_mode)
    generate_markdown_report(scores, summary, excellence_decisions, md_path)
    print(f"Report written to: {md_path}")

    summary_path = os.path.join(args.output_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Summary exported to: {summary_path}")

    print()
    print("=== Scores ===")
    for variant, data in scores.items():
        print(f"  {variant}: score={data['total_score']}, pass_rate={data['pass_rate']}")

    print()
    print("=== Deltas ===")
    for variant, delta in deltas.items():
        print(f"  {variant}: distance_to_oracle={delta['distance_to_oracle']}, delta_vs_deepseek_base={delta['delta_vs_deepseek_base']}")

    print()
    print("=== Excellence Gate ===")
    for variant, decision in excellence_decisions.items():
        print(f"  {variant}: {decision}")

    print()
    print("=== Benchmark-Level Decision ===")
    print(f"  {summary.get('benchmark_level_decision')}")

    print()
    print(f"Completed in {elapsed:.2f}s")

    if args.fail_on_gate_blockers:
        blocked = [v for v, d in excellence_decisions.items() if d == "BLOCKED_FOR_INTERPRETATION"]
        if args.comparison_mode:
            if summary.get("benchmark_level_decision") == "BLOCKED_FOR_INTERPRETATION":
                print(f"\nERROR: --fail-on-gate-blockers: benchmark-level gate blocked. Blocked variants: {blocked}")
                sys.exit(1)
        elif blocked:
            print(f"\nERROR: --fail-on-gate-blockers: blocked variants: {blocked}")
            sys.exit(1)


if __name__ == "__main__":
    main()
