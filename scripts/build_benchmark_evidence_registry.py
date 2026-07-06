#!/usr/bin/env python3
"""Build Benchmark Evidence Registry from a suite excellence audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from xendris.benchmarking import (  # noqa: E402
    build_benchmark_evidence_registry,
    write_benchmark_evidence_registry_json,
    write_benchmark_evidence_registry_markdown,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build benchmark evidence registry from excellence audit JSON.")
    parser.add_argument("--audit-json", default="runs/benchmark_suite_excellence_audit.json")
    parser.add_argument("--output-json", default="runs/benchmark_evidence_registry.json")
    parser.add_argument("--output-md", default="docs/benchmarks/BENCHMARK_EVIDENCE_REGISTRY.md")
    parser.add_argument("--require-admitted", action="store_true", help="Return non-zero if no artifacts are admitted.")
    args = parser.parse_args(argv)

    audit_payload = json.loads(Path(args.audit_json).read_text(encoding="utf-8"))
    registry = build_benchmark_evidence_registry(audit_payload)
    write_benchmark_evidence_registry_json(registry, args.output_json)
    write_benchmark_evidence_registry_markdown(registry, args.output_md)
    print(
        "BENCHMARK_EVIDENCE_REGISTRY "
        f"total={registry.total_count} admitted={registry.admitted_count} rejected={registry.rejected_count}"
    )
    if args.require_admitted and registry.admitted_count <= 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
