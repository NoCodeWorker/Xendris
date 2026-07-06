#!/usr/bin/env python3
"""Run Programming Reliability calibration ablation in dry-run mode."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import sys
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from xendris.benchmarking import assess_programming_calibration_ablation  # noqa: E402
from xendris.benchmarking.programming import (  # noqa: E402
    ProgrammingRunResult,
    ProgrammingSample,
    load_programming_reliability_v0_1,
    run_programming_benchmark,
    summarize_programming_results,
)


DEFAULT_OUTPUT_DIR = ROOT / "runs" / "programming_calibration_ablation_v0_2_5"
VARIANTS = ("deepseek_base", "xendris_uncalibrated", "xendris_calibrated")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Programming Reliability calibration ablation.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args(argv)

    samples = load_programming_reliability_v0_1()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    base_results = run_programming_benchmark(samples, deepseek_base_callable, {"system_name": "deepseek_base"})
    uncalibrated_results = run_programming_benchmark(
        samples,
        xendris_uncalibrated_callable,
        {"system_name": "xendris_uncalibrated"},
    )
    calibrated_results = run_programming_benchmark(
        samples,
        xendris_calibrated_callable,
        {
            "system_name": "xendris_calibrated",
            "experimental_calibration": True,
            "calibration_execution_mode": "CODE_SANDBOX",
        },
    )
    result_sets = {
        "deepseek_base": base_results,
        "xendris_uncalibrated": uncalibrated_results,
        "xendris_calibrated": calibrated_results,
    }
    summary = build_calibration_ablation_summary(samples, result_sets)
    report = render_calibration_ablation_report(summary)
    gate = assess_programming_calibration_ablation(summary, report)
    summary = {**summary, "evidence_gate": gate.to_dict()}

    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    write_results_jsonl(samples, result_sets, output_dir / "results.jsonl")
    (output_dir / "report.md").write_text(report, encoding="utf-8")

    print(f"Summary saved to: {output_dir / 'summary.json'}")
    print(f"Results saved to: {output_dir / 'results.jsonl'}")
    print(f"Report saved to: {output_dir / 'report.md'}")
    print(f"Evidence status: {gate.status}")
    print(f"Calibrated vs uncalibrated delta: {summary['score_deltas']['calibrated_vs_uncalibrated']}")
    return 0


def deepseek_base_callable(sample: ProgrammingSample, config: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Dry-run base model stand-in."""
    del config
    if sample.category in {"normal_control", "api_contracts", "performance", "refactor_safety"}:
        code = _minimal_correct_code(sample)
    elif sample.category == "edge_cases":
        code = sample.starter_code or _minimal_correct_code(sample)
    elif sample.category == "security_basics":
        code = sample.starter_code or _minimal_correct_code(sample)
    else:
        code = _minimal_correct_code(sample)
    return _payload("deepseek_base", code, latency_ms=100, cost=0.0001)


def xendris_uncalibrated_callable(
    sample: ProgrammingSample,
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Dry-run uncalibrated Xendris stand-in with known overengineering failures."""
    del config
    if sample.category == "api_contracts":
        code = "from decimal import Decimal\n" + _minimal_correct_code(sample)
    elif sample.category == "unit_tests":
        code = "import pytest\n" + _minimal_correct_code(sample)
    elif sample.category == "security_basics":
        code = _minimal_correct_code(sample)
        return {**_payload("xendris_uncalibrated", code, latency_ms=110, cost=0.00012), "security_risk": True}
    else:
        code = _minimal_correct_code(sample)
    return _payload("xendris_uncalibrated", code, latency_ms=110, cost=0.00012)


def xendris_calibrated_callable(
    sample: ProgrammingSample,
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Dry-run calibrated Xendris stand-in that follows calibration audit constraints."""
    audit = (config or {}).get("calibration_audit") or {}
    code = _minimal_correct_code(sample)
    payload = _payload("xendris_calibrated", code, latency_ms=108, cost=0.00012)
    if sample.category == "security_basics" and audit.get("require_security_scan"):
        payload["reason"] = "PASS_WITH_SECURITY_SCAN"
    return payload


def build_calibration_ablation_summary(
    samples: list[ProgrammingSample],
    result_sets: Mapping[str, list[ProgrammingRunResult]],
) -> dict[str, Any]:
    """Build the calibration ablation summary payload."""
    summaries = {name: summarize_programming_results(results) for name, results in result_sets.items()}
    systems = {
        name: {
            **summary.to_dict(),
            "latency_average_ms": _average_latency(result_sets[name]),
            "estimated_cost_usd": round(sum(result.estimated_cost_usd for result in result_sets[name]), 8),
            "import_failure_count": _import_failure_count(result_sets[name]),
            "overengineering_failure_count": _overengineering_failure_count(result_sets[name]),
        }
        for name, summary in summaries.items()
    }
    category_breakdown = _category_breakdown(summaries)
    category_deltas = _category_deltas(category_breakdown)
    score_deltas = {
        "calibrated_vs_uncalibrated": _delta(summaries["xendris_calibrated"].average_score, summaries["xendris_uncalibrated"].average_score),
        "calibrated_vs_base": _delta(summaries["xendris_calibrated"].average_score, summaries["deepseek_base"].average_score),
        "uncalibrated_vs_base": _delta(summaries["xendris_uncalibrated"].average_score, summaries["deepseek_base"].average_score),
    }
    return {
        "metadata": {
            "dataset_name": "Programming Reliability v0.1",
            "dataset_version": "0.1",
            "dataset_hash": compute_file_hash(ROOT / "xendris" / "benchmarking" / "datasets" / "programming_reliability_v0_1.jsonl"),
            "dataset_hash_algorithm": "sha256",
            "execution_mode": "dry-run",
            "provider_mode": "mock",
            "external_data_disclosure": "No external provider call; deterministic local dry-run only.",
            "pricing_assumptions": "Costs are deterministic placeholders and not billing records.",
            "run_date": datetime.now(timezone.utc).date().isoformat(),
            "python_version": platform.python_version(),
            "xendris_version": _xendris_version(),
            "experimental_calibration_variant_disclosed": True,
            "historical_artifacts_overwritten": False,
        },
        "variants": list(VARIANTS),
        "total_samples": len(samples),
        "systems": systems,
        "scores": {name: summaries[name].average_score for name in VARIANTS},
        "score_deltas": score_deltas,
        "category_breakdown": category_breakdown,
        "category_deltas": category_deltas,
        "answers": {
            "api_contracts_improved": _improved(category_deltas, "api_contracts"),
            "unit_tests_improved": _improved(category_deltas, "unit_tests"),
            "edge_cases_preserved": _preserved(category_breakdown, "edge_cases"),
            "import_failures_reduced": systems["xendris_calibrated"]["import_failure_count"] < systems["xendris_uncalibrated"]["import_failure_count"],
            "overengineering_failures_reduced": systems["xendris_calibrated"]["overengineering_failure_count"] < systems["xendris_uncalibrated"]["overengineering_failure_count"],
        },
        "limitations": [
            "Dry-run only.",
            "Mock provider behavior is deterministic and cannot prove real-provider performance.",
            "Closed Programming Reliability v0.1 dataset only.",
            "Experimental calibration evidence does not imply global programming improvement.",
        ],
        "warnings": [
            "No universal superiority is implied.",
            "No real-provider performance is measured.",
        ],
    }


def render_calibration_ablation_report(summary: Mapping[str, Any]) -> str:
    """Render a conservative Markdown report."""
    rows = []
    for category in sorted(summary["category_breakdown"]):
        scores = summary["category_breakdown"][category]
        deltas = summary["category_deltas"][category]
        rows.append(
            "| `{category}` | {base:.3f} | {uncal:.3f} | {cal:.3f} | {delta:.3f} |".format(
                category=category,
                base=scores["deepseek_base"],
                uncal=scores["xendris_uncalibrated"],
                cal=scores["xendris_calibrated"],
                delta=deltas["calibrated_vs_uncalibrated"],
            )
        )
    answers = summary["answers"]
    return f"""# Programming Calibration Ablation v0.2.5

## Purpose

Measure whether experimental benchmark-aware calibration reduces Xendris
overengineering harm in Programming Reliability v0.1 while preserving useful
edge-case behavior.

## Configuration

| Field | Value |
|---|---|
| Dataset | `{summary['metadata']['dataset_name']}` |
| Dataset version | `{summary['metadata']['dataset_version']}` |
| Dataset hash | `{summary['metadata']['dataset_hash']}` |
| Execution mode | `{summary['metadata']['execution_mode']}` |
| Provider mode | `{summary['metadata']['provider_mode']}` |
| Variants | `{', '.join(summary['variants'])}` |
| Historical artifacts overwritten | `{summary['metadata']['historical_artifacts_overwritten']}` |

## No Universal Superiority Warning

This dry-run ablation does not imply universal superiority and does not show
global programming improvement.

## No External Provider Warning

This run uses deterministic local mock behavior only. It does not measure
external provider behavior.

## Global Scores

| Variant | Score |
|---|---:|
| `deepseek_base` | {summary['scores']['deepseek_base']:.3f} |
| `xendris_uncalibrated` | {summary['scores']['xendris_uncalibrated']:.3f} |
| `xendris_calibrated` | {summary['scores']['xendris_calibrated']:.3f} |

## Score Deltas

| Delta | Value |
|---|---:|
| calibrated vs uncalibrated | {summary['score_deltas']['calibrated_vs_uncalibrated']:.3f} |
| calibrated vs base | {summary['score_deltas']['calibrated_vs_base']:.3f} |
| uncalibrated vs base | {summary['score_deltas']['uncalibrated_vs_base']:.3f} |

## Category Breakdown

| Category | Base | Uncalibrated | Calibrated | Calibrated vs uncalibrated |
|---|---:|---:|---:|---:|
{chr(10).join(rows)}

## Direct Questions

| Question | Computed answer |
|---|---|
| Did calibration improve api_contracts vs uncalibrated? | `{answers['api_contracts_improved']}` |
| Did calibration improve unit_tests vs uncalibrated? | `{answers['unit_tests_improved']}` |
| Did calibration preserve edge_cases? | `{answers['edge_cases_preserved']}` |
| Did calibration reduce import-related failures? | `{answers['import_failures_reduced']}` |
| Did calibration reduce overengineering-style failures? | `{answers['overengineering_failures_reduced']}` |

## Limitations

- Dry-run only.
- Mock behavior is deterministic and cannot prove external provider behavior.
- Closed Programming Reliability v0.1 dataset only.
- Experimental calibration evidence is not stable public API evidence.
- Results must not be used as proof of broad programming superiority.

## Interpretation

This artifact is experimental analysis. It measures the net effect of Xendris
intervention policy under a closed dry-run benchmark, not model quality in the
general case.
"""


def write_results_jsonl(
    samples: list[ProgrammingSample],
    result_sets: Mapping[str, list[ProgrammingRunResult]],
    path: str | Path,
) -> None:
    """Write per-sample three-way ablation results."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        for index, sample in enumerate(samples):
            payload = {
                "sample": sample.to_dict(),
                "results": {name: result_sets[name][index].to_dict() for name in VARIANTS},
            }
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def compute_file_hash(path: str | Path) -> str:
    target = Path(path)
    if not target.exists():
        return ""
    return hashlib.sha256(target.read_bytes()).hexdigest()


def _payload(system_name: str, code: str, *, latency_ms: float, cost: float) -> dict[str, Any]:
    return {
        "system_name": system_name,
        "answer": f"```python\n{code}\n```",
        "latency_ms": latency_ms,
        "estimated_cost_usd": cost,
    }


def _minimal_correct_code(sample: ProgrammingSample) -> str:
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


def _average_latency(results: list[ProgrammingRunResult]) -> float:
    return round(sum(result.latency_ms for result in results) / len(results), 4) if results else 0.0


def _import_failure_count(results: list[ProgrammingRunResult]) -> int:
    return sum("import" in (result.runtime_error or "").lower() for result in results)


def _overengineering_failure_count(results: list[ProgrammingRunResult]) -> int:
    return sum(
        result.score == 0.0
        and (
            result.reason in {"RUNTIME_ERROR", "CONTRACT_BROKEN", "SECURITY_RISK"}
            or "import" in (result.runtime_error or "").lower()
        )
        for result in results
    )


def _category_breakdown(summaries: Mapping[str, Any]) -> dict[str, dict[str, float]]:
    categories = sorted({category for summary in summaries.values() for category in summary.score_by_category})
    return {
        category: {
            name: float(summary.score_by_category.get(category, 0.0))
            for name, summary in summaries.items()
        }
        for category in categories
    }


def _category_deltas(category_breakdown: Mapping[str, Mapping[str, float]]) -> dict[str, dict[str, float]]:
    return {
        category: {
            "calibrated_vs_uncalibrated": _delta(scores["xendris_calibrated"], scores["xendris_uncalibrated"]),
            "calibrated_vs_base": _delta(scores["xendris_calibrated"], scores["deepseek_base"]),
            "uncalibrated_vs_base": _delta(scores["xendris_uncalibrated"], scores["deepseek_base"]),
        }
        for category, scores in category_breakdown.items()
    }


def _delta(left: float, right: float) -> float:
    return round(left - right, 4)


def _improved(category_deltas: Mapping[str, Mapping[str, float]], category: str) -> bool:
    return category_deltas.get(category, {}).get("calibrated_vs_uncalibrated", 0.0) > 0.0


def _preserved(category_breakdown: Mapping[str, Mapping[str, float]], category: str) -> bool:
    scores = category_breakdown.get(category, {})
    return scores.get("xendris_calibrated", 0.0) >= scores.get("xendris_uncalibrated", 0.0)


def _xendris_version() -> str:
    try:
        import xendris

        return str(xendris.__version__)
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
