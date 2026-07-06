#!/usr/bin/env python3
"""Validate benchmark artifacts against the Xendris excellence gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from xendris.benchmarking import assess_benchmark_excellence  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a benchmark summary for safe interpretation.")
    parser.add_argument("summary_json", help="Path to benchmark summary JSON.")
    parser.add_argument("--report", help="Optional benchmark report Markdown path.")
    parser.add_argument("--output", help="Optional output JSON path for the excellence assessment.")
    parser.add_argument(
        "--allow-blockers",
        action="store_true",
        help="Return 0 even when blockers are found. Useful for inventory runs.",
    )
    args = parser.parse_args(argv)

    try:
        summary = _read_json(args.summary_json)
    except Exception as exc:
        print(f"Failed to read summary JSON: {exc}", file=sys.stderr)
        return 2

    report_text = None
    if args.report:
        try:
            report_text = Path(args.report).read_text(encoding="utf-8")
        except Exception as exc:
            print(f"Failed to read report: {exc}", file=sys.stderr)
            return 2

    assessment = assess_benchmark_excellence(summary, report_text=report_text)
    payload = assessment.to_dict()

    if args.output:
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    print(f"BENCHMARK_EXCELLENCE_DECISION {assessment.decision}")
    if assessment.issues:
        for issue in assessment.issues:
            print(f"{issue.severity.value} {issue.code}: {issue.message}")

    if assessment.has_blockers and not args.allow_blockers:
        return 1
    return 0


def _read_json(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("summary JSON must contain an object at the top level")
    return payload


if __name__ == "__main__":
    raise SystemExit(main())
