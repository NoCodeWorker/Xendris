from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmarks.finitexo_code_matrix_v0_2.evaluators.anti_ad_hoc_checks import (
    assess_run_interpretation,
    load_manifest,
    load_tasks,
    validate_dataset_manifest,
)


DEFAULT_VARIANTS = [
    "base_agent",
    "base_agent_with_contract_prompt",
    "base_agent_with_scoring_awareness",
    "xendris_agent",
    "xendris_calibrated_agent",
]

DEFAULT_MODELS = ["deepseek-v4-flash", "gpt-4.1-nano"]


def _repo_benchmark_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _select_tasks(root: Path, samples: int | None) -> list[dict[str, Any]]:
    tasks = load_tasks(root / "tasks")
    if samples is None:
        return tasks
    if samples <= 0:
        raise ValueError("--samples must be positive")
    return tasks[: min(samples, len(tasks))]


def _interpretation_for_sample_count(samples: int, anti_ad_hoc_decision: str) -> str:
    if anti_ad_hoc_decision == "BLOCKED":
        return "BLOCKED_FOR_INTERPRETATION"
    if samples < 20:
        return "BUDGET_VALIDATION_ONLY"
    if samples < 50:
        return "SIGNAL_REPLICATION_ONLY"
    return "READY_FOR_INTERPRETATION"


def _build_rows(models: list[str], variants: list[str], dry_run: bool) -> list[dict[str, Any]]:
    status = "DRY_RUN_ONLY" if dry_run else "SKIPPED_VARIANT_NOT_AVAILABLE"
    evidence = "INSUFFICIENT"
    return [
        {
            "model": model,
            "variant": variant,
            "execution_status": status,
            "score": None,
            "verified_successes": None,
            "estimated_cost": None,
            "evidence_decision": evidence,
            "benchmark_gate": "BUDGET_VALIDATION_ONLY",
            "limitations": "No provider execution was performed; no performance metric is generated.",
        }
        for model in models
        for variant in variants
    ]


def _render_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Finitexo Code Matrix v0.2 - Anti-Ad-Hoc Validation",
        "",
        "## Scope",
        "",
        "Infrastructure run for anti-ad-hoc validation. No superiority claim is authorized.",
        "",
        "## Configuration",
        "",
        f"- Execution mode: {summary['execution_mode']}",
        f"- Samples: {summary['sample_count']}",
        f"- Models: {', '.join(summary['models'])}",
        f"- Variants: {', '.join(summary['variants'])}",
        f"- Dataset hash: {summary['dataset_hash']}",
        f"- Scoring contract hash: {summary['scoring_contract_hash']}",
        "",
        "## Dataset Integrity",
        "",
        f"- Anti-ad-hoc decision: {summary['anti_ad_hoc']['anti_ad_hoc_decision']}",
        f"- Warnings: {summary['anti_ad_hoc']['warnings']}",
        f"- Blocking issues: {summary['anti_ad_hoc']['blocking_issues']}",
        "",
        "## Matrix Results",
        "",
        "| model | variant | execution_status | evidence_decision | benchmark_gate | limitations |",
        "|---|---|---|---|---|---|",
    ]
    for row in summary["matrix_results"]:
        lines.append(
            f"| {row['model']} | {row['variant']} | {row['execution_status']} | "
            f"{row['evidence_decision']} | {row['benchmark_gate']} | {row['limitations']} |"
        )
    lines.extend(
        [
            "",
            "## Claims Explicitly Not Authorized",
            "",
            "- Universal superiority.",
            "- General coding superiority.",
            "- Production readiness.",
            "- Transfer to unmeasured models or providers.",
            "",
            "## Conclusion",
            "",
            "This artifact validates benchmark plumbing and anti-ad-hoc controls only. "
            "It does not contain live provider performance results.",
            "",
        ]
    )
    return "\n".join(lines)


def run_matrix(args: argparse.Namespace) -> dict[str, Any]:
    root = _repo_benchmark_root()
    tasks = _select_tasks(root, args.samples)
    manifest = load_manifest(root)
    manifest_assessment = validate_dataset_manifest(root)
    run_assessment = assess_run_interpretation(
        sample_count=len(tasks),
        report_text="",
        manifest_assessment=manifest_assessment,
    )

    if not args.dry_run:
        raise RuntimeError(
            "Live/provider execution is not implemented for Finitexo Code Matrix v0.2 yet. "
            "Use --dry-run for the current infrastructure validation pass."
        )

    models = args.models or DEFAULT_MODELS
    variants = args.variants or DEFAULT_VARIANTS
    rows = _build_rows(models, variants, dry_run=True)
    benchmark_gate = _interpretation_for_sample_count(
        len(tasks),
        run_assessment.anti_ad_hoc_decision,
    )
    for row in rows:
        row["benchmark_gate"] = benchmark_gate

    summary = {
        "benchmark_name": "Finitexo Code Matrix",
        "benchmark_version": "v0.2",
        "dataset_name": manifest["dataset_name"],
        "dataset_version": manifest["dataset_version"],
        "dataset_hash": manifest["dataset_hash"],
        "scoring_contract_hash": manifest["scoring_contract_hash"],
        "execution_mode": "dry-run",
        "run_id": f"fcm-v0-2-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sample_count": len(tasks),
        "task_ids": [task["task_id"] for task in tasks],
        "models": models,
        "variants": variants,
        "matrix_results": rows,
        "anti_ad_hoc": run_assessment.to_dict(),
        "benchmark_gate": benchmark_gate,
        "claim_policy": manifest["claim_policy"],
        "no_superiority_claim_authorized": True,
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Finitexo Code Matrix v0.2")
    parser.add_argument("--dry-run", action="store_true", help="Validate plumbing without provider calls")
    parser.add_argument("--samples", type=int, default=5, help="Number of tasks to include")
    parser.add_argument("--models", nargs="*", default=None, help="Models to include in the matrix")
    parser.add_argument("--variants", nargs="*", default=None, help="Variants to include in the matrix")
    parser.add_argument("--budget", type=float, default=0.05, help="Budget guard for future live runs")
    parser.add_argument("--max-concurrent", type=int, default=1)
    parser.add_argument("--max-iterations", type=int, default=1)
    parser.add_argument(
        "--output-dir",
        default="runs/finitexo_code_matrix_v0_2_dry_run",
        help="Output directory",
    )
    args = parser.parse_args()

    if args.budget > 0.50:
        raise SystemExit("Budget exceeds absolute stop threshold for v0.2 infrastructure pass.")

    summary = run_matrix(args)
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (outdir / "report.md").write_text(_render_report(summary), encoding="utf-8")
    print(f"Summary written to: {outdir / 'summary.json'}")
    print(f"Report written to: {outdir / 'report.md'}")
    print(f"Benchmark gate: {summary['benchmark_gate']}")


if __name__ == "__main__":
    main()
