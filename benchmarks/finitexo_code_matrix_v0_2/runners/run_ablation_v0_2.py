from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmarks.finitexo_code_matrix_v0_2.runners.run_matrix_v0_2 import run_matrix


ABLATION_VARIANTS = [
    "base_agent",
    "base_agent_with_contract_prompt",
    "base_agent_with_scoring_awareness",
    "xendris_without_calibration",
    "xendris_without_evidence_gate",
    "xendris_without_claim_gate",
    "xendris_agent",
    "xendris_calibrated_agent",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Finitexo Code Matrix v0.2 ablation")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--samples", type=int, default=5)
    parser.add_argument("--models", nargs="*", default=["deepseek-v4-flash", "gpt-4.1-nano"])
    parser.add_argument("--variants", nargs="*", default=ABLATION_VARIANTS)
    parser.add_argument("--budget", type=float, default=0.05)
    parser.add_argument("--max-concurrent", type=int, default=1)
    parser.add_argument("--max-iterations", type=int, default=1)
    parser.add_argument(
        "--output-dir",
        default="runs/finitexo_code_matrix_v0_2_ablation_dry_run",
    )
    args = parser.parse_args()
    if not args.dry_run:
        raise SystemExit("Ablation v0.2 currently supports --dry-run only.")

    summary = run_matrix(args)
    summary["ablation_protocol"] = {
        "variants_reported": args.variants,
        "unavailable_variants_policy": "report as SKIPPED_VARIANT_NOT_AVAILABLE or DRY_RUN_ONLY; do not hide",
        "performance_claim_authorized": False,
    }

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    lines = [
        "# Finitexo Code Matrix v0.2 - Ablation Dry Run",
        "",
        "This dry run reports all ablation variants without provider calls.",
        "",
        "| variant | status |",
        "|---|---|",
    ]
    for variant in args.variants:
        lines.append(f"| {variant} | DRY_RUN_ONLY |")
    lines.extend(
        [
            "",
            "No superiority claim is authorized.",
            "",
        ]
    )
    (outdir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Summary written to: {outdir / 'summary.json'}")
    print(f"Report written to: {outdir / 'report.md'}")
    print(f"Benchmark gate: {summary['benchmark_gate']}")


if __name__ == "__main__":
    main()
