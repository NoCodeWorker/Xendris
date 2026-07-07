"""Plan/dry-run runner for Finitexo Code Matrix v0.3."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_3.evaluators.adversarial_checks import (
    BENCHMARK_DIR,
    assess_adversarial_readiness,
)
from benchmarks.finitexo_code_matrix_v0_3.evaluators.baseline_comparison import compare_baselines
from benchmarks.finitexo_code_matrix_v0_3.reports.report_builder_v0_3 import build_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--plan-only", action="store_true", default=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--samples", type=int, default=10)
    parser.add_argument("--models", default="")
    parser.add_argument("--variants", default="")
    parser.add_argument("--budget", type=float, default=None)
    parser.add_argument("--max-concurrent", type=int, default=1)
    parser.add_argument("--max-iterations", type=int, default=1)
    parser.add_argument("--output-dir", default="runs/finitexo_code_matrix_v0_3_plan")
    parser.add_argument("--blind-scoring", action="store_true", default=True)
    parser.add_argument("--allow-semi-external", action="store_true")
    return parser


def run(args: argparse.Namespace) -> dict[str, object]:
    manifest_path = BENCHMARK_DIR / "external_dataset_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    blockers: list[str] = []
    if args.execute:
        if args.budget is None or args.budget <= 0:
            blockers.append("unsafe_or_missing_budget")
        if not args.blind_scoring:
            blockers.append("blind_scoring_unavailable")
        blockers.append("real_provider_execution_not_implemented_in_v0_3_infrastructure")

    readiness = assess_adversarial_readiness(
        manifest=manifest,
        execute_requested=args.execute,
        provider_execution_attempted=args.execute,
    )
    blockers.extend(readiness["blockers"])

    comparison = (
        {
            "decision": "BENCHMARK_INCONCLUSIVE",
            "h0_status": "LIVE",
            "blockers": [],
            "interpretation": "No provider matrix was executed; no baseline comparison evidence exists yet.",
        }
        if not args.execute
        else compare_baselines(
            {
                "strong_non_xendris_agent_available": True,
                "strong_non_xendris_agent": {"verified_success_count": 0, "mean_raw_score": 0.0},
                "xendris_agent": {"verified_success_count": 0, "mean_raw_score": 0.0},
                "xendris_calibrated_agent": {"verified_success_count": 0, "mean_raw_score": 0.0},
                "blockers": blockers,
                "blind_scoring_decision": "REQUIRED" if args.blind_scoring else "FAILED",
            }
        )
    )

    execution_mode = "execute" if args.execute else "dry-run" if args.dry_run else "plan-only"
    summary = {
        "benchmark_name": "Finitexo Code Matrix",
        "benchmark_version": "0.3",
        "execution_mode": execution_mode,
        "provider_execution": "NO_PROVIDER_EXECUTION" if not args.execute else "BLOCKED_FOR_INTERPRETATION",
        "samples": args.samples,
        "models": args.models.split(",") if args.models else [],
        "variants": args.variants.split(",") if args.variants else [],
        "dataset_hash": readiness["dataset_hash"],
        "scoring_contract_hash": readiness["scoring_contract_hash"],
        "blind_scoring_decision": "REQUIRED" if args.blind_scoring else "FAILED",
        "adversarial_decision": "BLOCKED_FOR_INTERPRETATION" if blockers else readiness["adversarial_decision"],
        "h0_status": "LIVE",
        "baseline_comparison": comparison,
        "warnings": readiness["warnings"],
        "blockers": blockers,
        "result_decision": "BLOCKED_FOR_INTERPRETATION" if blockers else "IMPLEMENTED_SEMI_EXTERNAL_ADVERSARIAL_INFRASTRUCTURE",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "report.md").write_text(build_report(summary), encoding="utf-8")
    return summary


def main() -> int:
    args = build_parser().parse_args()
    summary = run(args)
    return 1 if summary["result_decision"] == "BLOCKED_FOR_INTERPRETATION" and args.execute else 0


if __name__ == "__main__":
    raise SystemExit(main())
