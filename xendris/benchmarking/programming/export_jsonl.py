"""JSONL utilities for Programming Reliability Benchmark."""

from __future__ import annotations

import json
from pathlib import Path

from .types import ProgrammingRunResult


def write_programming_results_jsonl(
    results: list[ProgrammingRunResult],
    path: str | Path,
) -> None:
    """Write programming benchmark results as JSON Lines."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")


def read_programming_results_jsonl(path: str | Path) -> list[ProgrammingRunResult]:
    """Read programming benchmark results from JSON Lines."""
    results: list[ProgrammingRunResult] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            item = json.loads(line)
            results.append(
                ProgrammingRunResult(
                    sample_id=item["sample_id"],
                    system_name=item["system_name"],
                    language=item["language"],
                    answer=item["answer"],
                    extracted_code=item.get("extracted_code"),
                    tests_passed=item["tests_passed"],
                    contract_preserved=item["contract_preserved"],
                    runtime_error=item.get("runtime_error"),
                    security_risk=item["security_risk"],
                    performance_regression=item["performance_regression"],
                    decision=item["decision"],
                    reason=item.get("reason"),
                    score=item["score"],
                    latency_ms=item["latency_ms"],
                    estimated_cost_usd=item["estimated_cost_usd"],
                    fingerprint=item["fingerprint"],
                    calibration_audit=item.get("calibration_audit"),
                )
            )
    return results
