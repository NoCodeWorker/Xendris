#!/usr/bin/env python3
"""Run DeepSeek Base vs Xendris+DeepSeek on Programming Reliability v0.1."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import sys
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from xendris.benchmarking.programming import (  # noqa: E402
    ProgrammingRunResult,
    ProgrammingSample,
    load_programming_reliability_v0_1,
    run_programming_benchmark,
    summarize_programming_results,
)
from xendris.benchmarking import assess_benchmark_excellence  # noqa: E402
from xendris.benchmarking.providers.deepseek import DeepSeekBaseProvider  # noqa: E402
from xendris.benchmarking.types import BenchmarkSample  # noqa: E402


RUN_BASENAME = "deepseek_vs_xendris_programming_reliability_v0_1_2026_07_04"


def compute_file_hash(path: str | Path) -> str:
    """Return SHA-256 hash for a file, or empty string if missing."""
    target = Path(path)
    if not target.exists():
        return ""
    hasher = hashlib.sha256()
    hasher.update(target.read_bytes())
    return hasher.hexdigest()


def output_paths(output_dir: str | Path, run_basename: str = RUN_BASENAME) -> dict[str, Path]:
    """Return canonical output paths for the programming A/B run."""
    out = Path(output_dir)
    canonical_runs_dir = (ROOT / "runs").resolve()
    report_path = (
        ROOT / "docs" / "benchmarks" / "RUN_DEEPSEEK_VS_XENDRIS_PROGRAMMING_RELIABILITY_V0_1_2026_07_04.md"
        if out.resolve() == canonical_runs_dir
        else out / "RUN_DEEPSEEK_VS_XENDRIS_PROGRAMMING_RELIABILITY_V0_1_2026_07_04.md"
    )
    return {
        "jsonl": out / f"{run_basename}.jsonl",
        "summary": out / f"{run_basename}_summary.json",
        "excellence": out / f"{run_basename}_excellence.json",
        "report": report_path,
    }


class ProgrammingDeepSeekCallable:
    """Provider-backed callable for programming samples."""

    def __init__(self, provider: DeepSeekBaseProvider, system_name: str, xendris_mode: bool = False):
        self.provider = provider
        self.system_name = system_name
        self.xendris_mode = xendris_mode

    def __call__(self, sample: ProgrammingSample, config: Mapping[str, Any] | None = None) -> dict[str, Any]:
        prompt = _compose_programming_prompt(
            sample,
            xendris_mode=self.xendris_mode,
            calibration_audit=(config or {}).get("calibration_audit") if self.xendris_mode else None,
        )
        benchmark_sample = BenchmarkSample(
            sample_id=sample.sample_id,
            prompt=prompt,
            category=sample.category,
        )
        result = self.provider(benchmark_sample)
        return {
            **result,
            "system_name": self.system_name,
            "answer": result.get("answer", ""),
            "estimated_cost_usd": result.get("estimated_cost_usd", 0.0),
        }


def dry_run_deepseek_callable(sample: ProgrammingSample, config: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Deterministic DeepSeek-base stand-in for dry-run tests."""
    del config
    if sample.category == "normal_control":
        code = _correct_code_for_sample(sample)
    else:
        code = sample.starter_code or "def solve(value):\n    return value\n"
    return {
        "system_name": "deepseek_base",
        "answer": f"```python\n{code}\n```",
        "latency_ms": 100,
        "estimated_cost_usd": 0.0001,
    }


def dry_run_xendris_callable(sample: ProgrammingSample, config: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Deterministic Xendris+DeepSeek stand-in for dry-run tests."""
    del config
    code = _correct_code_for_sample(sample)
    return {
        "system_name": "xendris_deepseek",
        "answer": f"```python\n{code}\n```\n\nLimit: this is benchmark-local code for this closed test suite.",
        "latency_ms": 110,
        "estimated_cost_usd": 0.00012,
    }


def build_ab_summary(
    samples: list[ProgrammingSample],
    deepseek_results: list[ProgrammingRunResult],
    xendris_results: list[ProgrammingRunResult],
    metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Build the required A/B summary payload."""
    base_summary = summarize_programming_results(deepseek_results)
    xendris_summary = summarize_programming_results(xendris_results)
    pairs = list(zip(samples, deepseek_results, xendris_results))
    wins = sum(xe.score > ds.score for _, ds, xe in pairs)
    losses = sum(ds.score > xe.score for _, ds, xe in pairs)
    ties = len(pairs) - wins - losses
    return {
        "metadata": dict(metadata),
        "total_samples": len(samples),
        "average_score_deepseek": base_summary.average_score,
        "average_score_xendris": xendris_summary.average_score,
        "average_delta": round(xendris_summary.average_score - base_summary.average_score, 4),
        "xendris_wins": wins,
        "deepseek_wins": losses,
        "ties": ties,
        "systems": {
            "deepseek_base": _system_summary_payload(base_summary, deepseek_results),
            "xendris_deepseek": _system_summary_payload(xendris_summary, xendris_results),
        },
        "score_by_category": {
            "deepseek_base": base_summary.score_by_category,
            "xendris_deepseek": xendris_summary.score_by_category,
        },
        "top_xendris_wins": [
            _pair_payload(sample, ds, xe)
            for sample, ds, xe in pairs
            if xe.score > ds.score
        ][:10],
        "top_xendris_losses": [
            _pair_payload(sample, ds, xe)
            for sample, ds, xe in pairs
            if ds.score > xe.score
        ][:10],
    }


def write_ab_results_jsonl(
    samples: list[ProgrammingSample],
    deepseek_results: list[ProgrammingRunResult],
    xendris_results: list[ProgrammingRunResult],
    path: str | Path,
) -> None:
    """Write paired programming A/B results as JSONL."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        for sample, ds, xe in zip(samples, deepseek_results, xendris_results):
            payload = _pair_payload(sample, ds, xe)
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def write_report(summary: Mapping[str, Any], path: str | Path) -> None:
    """Write markdown report for the A/B run."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    systems = summary["systems"]
    category_rows = []
    categories = sorted(summary["score_by_category"]["deepseek_base"])
    for category in categories:
        ds_score = summary["score_by_category"]["deepseek_base"].get(category, 0.0)
        xe_score = summary["score_by_category"]["xendris_deepseek"].get(category, 0.0)
        category_rows.append(
            f"| `{category}` | {ds_score:.3f} | {xe_score:.3f} | {xe_score - ds_score:.3f} |"
        )
    report = f"""# DeepSeek Base vs Xendris+DeepSeek - Programming Reliability v0.1

Date: 2026-07-04

## Purpose

Measure programming reliability under a closed dataset with executable tests,
contract preservation, basic security checks, and production-overclaim control.

## Configuration

| Field | Value |
|---|---|
| Execution mode | `{summary['metadata']['execution_mode']}` |
| Provider | `{summary['metadata']['provider']}` |
| Model | `{summary['metadata']['model']}` |
| Temperature | `{summary['metadata']['temperature']}` |
| Top p | `{summary['metadata']['top_p']}` |
| Max tokens | `{summary['metadata']['max_tokens']}` |
| Sample timeout | `{summary['metadata']['sample_timeout_seconds']} s` |
| Started UTC | `{summary['metadata']['started_at_utc']}` |
| Dataset hash | `{summary['metadata']['dataset_hash']}` |
| Xendris version | `{summary['metadata']['xendris_version']}` |
| Python version | `{summary['metadata']['python_version']}` |

## No Universal Superiority Warning

This run is valid only for Programming Reliability v0.1 under the listed
configuration. It does not imply universal programming superiority over DeepSeek
or any frontier model.

## Programming Reliability vs Production Claims

Passing benchmark-owned tests means the output satisfied this local dataset and
sandbox. It does not prove production readiness, security completeness,
operational robustness, or real-world performance.

## Global Results

| Metric | Value |
|---|---:|
| Total samples | {summary['total_samples']} |
| DeepSeek average score | {summary['average_score_deepseek']:.3f} |
| Xendris average score | {summary['average_score_xendris']:.3f} |
| Average delta | {summary['average_delta']:.3f} |
| Xendris wins | {summary['xendris_wins']} |
| DeepSeek wins | {summary['deepseek_wins']} |
| Ties | {summary['ties']} |

## Category Results

| Category | DeepSeek score | Xendris score | Delta |
|---|---:|---:|---:|
{chr(10).join(category_rows)}

## System Diagnostics

| Metric | DeepSeek Base | Xendris+DeepSeek |
|---|---:|---:|
| Tests passed | {systems['deepseek_base']['tests_passed_count']} | {systems['xendris_deepseek']['tests_passed_count']} |
| Contract preserved | {systems['deepseek_base']['contract_preserved_count']} | {systems['xendris_deepseek']['contract_preserved_count']} |
| Runtime errors | {systems['deepseek_base']['runtime_error_count']} | {systems['xendris_deepseek']['runtime_error_count']} |
| Security risks | {systems['deepseek_base']['security_risk_count']} | {systems['xendris_deepseek']['security_risk_count']} |
| Performance regressions | {systems['deepseek_base']['performance_regression_count']} | {systems['xendris_deepseek']['performance_regression_count']} |
| Production overclaim rate | {systems['deepseek_base']['production_overclaim_rate']:.3f} | {systems['xendris_deepseek']['production_overclaim_rate']:.3f} |
| Cost per correct solution | {systems['deepseek_base']['cost_per_correct_solution']} | {systems['xendris_deepseek']['cost_per_correct_solution']} |
| Average latency ms | {systems['deepseek_base']['latency_average_ms']:.2f} | {systems['xendris_deepseek']['latency_average_ms']:.2f} |

## Main Xendris Wins

{_markdown_pair_list(summary['top_xendris_wins'])}

## Main Xendris Losses

{_markdown_pair_list(summary['top_xendris_losses'])}

## Costs

Costs are estimated from provider-reported usage where available. Dry-run costs
are deterministic placeholders and not billing records.

## Latency

Latency is measured per sample by the benchmark runner and includes local
post-processing in the Xendris path.

## Limitations

- Dataset is closed and initial.
- Sandbox is intentionally narrow.
- Tests are benchmark-owned and cannot prove full correctness.
- Security detection is basic.
- Real provider results can vary by model version, account state, latency,
  prompts, and API availability.

## Next Steps

- Run real-provider mode after explicit approval to send dataset prompts to the
  external API.
- Add stronger code extraction and language-specific sandboxes.
- Add multi-model comparison against frontier providers.
"""
    destination.write_text(report, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Programming Reliability A/B benchmark.")
    parser.add_argument("--dry-run", action="store_true", help="Use deterministic local callables.")
    parser.add_argument("--output-dir", default="runs")
    parser.add_argument("--model", default=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"))
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--timeout", type=float, default=95.0)
    parser.add_argument("--sample-timeout", type=float, default=2.0)
    parser.add_argument(
        "--experimental-calibration",
        action="store_true",
        help="Enable experimental benchmark-aware intervention calibration for the Xendris path.",
    )
    args = parser.parse_args(argv)

    samples = load_programming_reliability_v0_1()
    paths = output_paths(args.output_dir)
    started_at = datetime.now(timezone.utc).isoformat()
    dataset_path = ROOT / "xendris" / "benchmarking" / "datasets" / "programming_reliability_v0_1.jsonl"

    if args.dry_run:
        deepseek_callable = dry_run_deepseek_callable
        xendris_callable = dry_run_xendris_callable
        execution_mode = "dry-run"
        provider = "mock"
    else:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            print("Configuration Error: DEEPSEEK_API_KEY environment variable is missing.", file=sys.stderr)
            return 1
        base_provider = DeepSeekBaseProvider(
            api_key=api_key,
            model=args.model,
            temperature=0.0,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
            mock_mode=False,
        )
        deepseek_callable = ProgrammingDeepSeekCallable(base_provider, "deepseek_base", False)
        xendris_callable = ProgrammingDeepSeekCallable(base_provider, "xendris_deepseek", True)
        execution_mode = "real-provider"
        provider = "deepseek"

    config = {"timeout_seconds": args.sample_timeout}
    xendris_config = {**config, "system_name": "xendris_deepseek"}
    if args.experimental_calibration:
        xendris_config.update(
            {
                "experimental_calibration": True,
                "calibration_execution_mode": "CODE_SANDBOX",
            }
        )
    deepseek_results = run_programming_benchmark(
        samples,
        deepseek_callable,
        {**config, "system_name": "deepseek_base"},
    )
    xendris_results = run_programming_benchmark(
        samples,
        xendris_callable,
        xendris_config,
    )
    metadata = {
        "dataset_name": "Programming Reliability v0.1",
        "dataset_version": "0.1",
        "execution_mode": execution_mode,
        "external_data_disclosure": (
            "No external provider call; deterministic local dry-run."
            if execution_mode == "dry-run"
            else "Benchmark prompts are sent to the configured DeepSeek provider only."
        ),
        "dataset_hash_algorithm": "sha256",
        "provider": provider,
        "model": args.model,
        "temperature": 0.0,
        "top_p": 1,
        "max_tokens": args.max_tokens,
        "pricing_assumptions": "Dry-run costs are deterministic placeholders; real runs use provider-reported usage.",
        "provider_timeout_seconds": args.timeout,
        "run_date": started_at[:10],
        "sample_timeout_seconds": args.sample_timeout,
        "experimental_calibration": args.experimental_calibration,
        "started_at_utc": started_at,
        "dataset_hash": compute_file_hash(dataset_path),
        "xendris_version": _xendris_version(),
        "python_version": platform.python_version(),
    }
    summary = build_ab_summary(samples, deepseek_results, xendris_results, metadata)
    write_ab_results_jsonl(samples, deepseek_results, xendris_results, paths["jsonl"])
    paths["summary"].parent.mkdir(parents=True, exist_ok=True)
    paths["summary"].write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_report(summary, paths["report"])
    report_text = paths["report"].read_text(encoding="utf-8")
    excellence_assessment = assess_benchmark_excellence(summary, report_text=report_text)
    paths["excellence"].write_text(
        json.dumps(excellence_assessment.to_dict(), ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"Results saved to: {paths['jsonl']}")
    print(f"Summary saved to: {paths['summary']}")
    print(f"Excellence assessment saved to: {paths['excellence']}")
    print(f"Report saved to: {paths['report']}")
    print(f"Excellence Decision: {excellence_assessment.decision.value}")
    print(f"Average DeepSeek score: {summary['average_score_deepseek']}")
    print(f"Average Xendris score: {summary['average_score_xendris']}")
    return 0


def _compose_programming_prompt(
    sample: ProgrammingSample,
    *,
    xendris_mode: bool,
    calibration_audit: Mapping[str, Any] | None = None,
) -> str:
    instructions = [
        sample.prompt,
        "Return only the final Python code in one fenced code block.",
        "Preserve the public function name and signature.",
        "Do not claim production readiness.",
    ]
    if xendris_mode:
        instructions.extend(
            [
                "Apply Xendris response contract: state limits only outside code if needed.",
                "Avoid unsafe eval/exec/open/subprocess/network access.",
                "Handle edge cases and keep the API contract stable.",
            ]
        )
    if xendris_mode and calibration_audit:
        instructions.extend(_calibration_prompt_instructions(calibration_audit))
    if sample.starter_code:
        instructions.append("Starter code:\n" + sample.starter_code)
    if sample.expected_behavior:
        instructions.append("Expected behavior:\n" + sample.expected_behavior)
    return "\n\n".join(instructions)


def _calibration_prompt_instructions(calibration_audit: Mapping[str, Any]) -> list[str]:
    """Translate experimental calibration policy into conservative prompt constraints."""
    instructions = ["Experimental calibration constraints:"]
    if calibration_audit.get("preserve_signature"):
        instructions.append("- Preserve the exact public function name and signature.")
    if calibration_audit.get("allow_extra_imports") is False:
        instructions.append("- Do not add imports unless the starter code already requires them.")
    if calibration_audit.get("allow_runtime_type_checks") is False:
        instructions.append("- Do not add runtime type-checking wrappers.")
    if calibration_audit.get("allow_test_framework_imports") is False:
        instructions.append("- Do not use pytest or framework-specific test imports.")
    if calibration_audit.get("prefer_minimal_patch"):
        instructions.append("- Prefer the smallest patch that satisfies the benchmark-owned tests.")
    if calibration_audit.get("category") == "UNIT_TESTS":
        instructions.append("- Prefer plain assert-based tests over framework fixtures.")
    if calibration_audit.get("category") == "EDGE_CASES":
        instructions.append("- Add simple boundary handling without import-heavy abstractions.")
    if calibration_audit.get("require_security_scan"):
        instructions.append("- Avoid unsafe eval, exec, subprocess, network, and broad filesystem access.")
    return instructions


def _correct_code_for_sample(sample: ProgrammingSample) -> str:
    name = _first_public_function_name(sample.starter_code) or "solve"
    if sample.category == "bug_fixing":
        return f"def {name}(items):\n    if not items:\n        return None\n    return items[0]\n"
    if sample.category == "api_contracts":
        return f"def {name}(payload):\n    return {{'ok': True, 'data': payload}}\n"
    if sample.category == "performance":
        return f"def {name}(items):\n    return len(set(items))\n"
    if sample.category == "security_basics":
        return f"def {name}(expr):\n    return expr\n"
    return f"def {name}(value):\n    return value\n"


def _first_public_function_name(code: str | None) -> str | None:
    if not code:
        return None
    match = re.search(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code)
    return match.group(1) if match else None


def _system_summary_payload(summary: Any, results: list[ProgrammingRunResult]) -> dict[str, Any]:
    return {
        **summary.to_dict(),
        "performance_regression_count": sum(result.performance_regression for result in results),
        "latency_average_ms": round(sum(result.latency_ms for result in results) / len(results), 4)
        if results
        else 0.0,
        "estimated_cost_usd": round(sum(result.estimated_cost_usd for result in results), 8),
    }


def _pair_payload(sample: ProgrammingSample, ds: ProgrammingRunResult, xe: ProgrammingRunResult) -> dict[str, Any]:
    return {
        "sample_id": sample.sample_id,
        "category": sample.category,
        "language": sample.language,
        "deepseek_result": ds.to_dict(),
        "xendris_result": xe.to_dict(),
        "delta": round(xe.score - ds.score, 4),
        "winner": "xendris" if xe.score > ds.score else "deepseek" if ds.score > xe.score else "tie",
    }


def _markdown_pair_list(items: list[Mapping[str, Any]]) -> str:
    if not items:
        return "- None recorded."
    return "\n".join(
        f"- `{item['sample_id']}` `{item['category']}` delta `{item['delta']}`"
        for item in items
    )


def _xendris_version() -> str:
    try:
        import xendris

        return str(xendris.__version__)
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
