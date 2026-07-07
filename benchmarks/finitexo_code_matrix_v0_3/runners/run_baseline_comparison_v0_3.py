"""Dry-run strong-baseline comparison runner for Finitexo Code Matrix v0.3."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_3.evaluators.baseline_comparison import compare_baselines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="runs/finitexo_code_matrix_v0_3_baseline_comparison")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    comparison = compare_baselines(
        {
            "strong_non_xendris_agent_available": True,
            "strong_non_xendris_agent": {"verified_success_count": 5, "mean_raw_score": 0.9},
            "xendris_agent": {"verified_success_count": 5, "mean_raw_score": 0.9},
            "xendris_calibrated_agent": {"verified_success_count": 5, "mean_raw_score": 0.91},
        }
    )
    (output_dir / "baseline_comparison_summary.json").write_text(
        json.dumps(comparison, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

