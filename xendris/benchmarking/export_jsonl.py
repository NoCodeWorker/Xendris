"""JSON and JSONL export utilities for A/B Benchmarking."""

from __future__ import annotations

import json
from .types import ABComparisonResult, ABRunSummary, SystemRunResult


def write_ab_results_jsonl(results: list[ABComparisonResult], path: str) -> None:
    """Serialize comparison results to a JSON Lines (JSONL) file."""
    with open(path, "w", encoding="utf-8") as f:
        for r in results:
            line = json.dumps(r.to_dict(), ensure_ascii=False)
            f.write(line + "\n")


def read_ab_results_jsonl(path: str) -> list[ABComparisonResult]:
    """Deserialize comparison results from a JSON Lines (JSONL) file."""
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)

            ds_data = item["deepseek_result"]
            xe_data = item["xendris_result"]

            ds_res = SystemRunResult(
                sample_id=ds_data["sample_id"],
                system_name=ds_data["system_name"],
                base_model=ds_data["base_model"],
                answer=ds_data["answer"],
                decision=ds_data.get("decision"),
                reason=ds_data.get("reason"),
                scoring_allowed=ds_data.get("scoring_allowed"),
                latency_ms=ds_data.get("latency_ms"),
                input_tokens=ds_data.get("input_tokens"),
                output_tokens=ds_data.get("output_tokens"),
                estimated_cost_usd=ds_data.get("estimated_cost_usd"),
                error=ds_data.get("error"),
                fingerprint=ds_data.get("fingerprint", ""),
            )

            xe_res = SystemRunResult(
                sample_id=xe_data["sample_id"],
                system_name=xe_data["system_name"],
                base_model=xe_data["base_model"],
                answer=xe_data["answer"],
                decision=xe_data.get("decision"),
                reason=xe_data.get("reason"),
                scoring_allowed=xe_data.get("scoring_allowed"),
                latency_ms=xe_data.get("latency_ms"),
                input_tokens=xe_data.get("input_tokens"),
                output_tokens=xe_data.get("output_tokens"),
                estimated_cost_usd=xe_data.get("estimated_cost_usd"),
                error=xe_data.get("error"),
                fingerprint=xe_data.get("fingerprint", ""),
            )

            results.append(
                ABComparisonResult(
                    sample_id=item["sample_id"],
                    category=item["category"],
                    deepseek_result=ds_res,
                    xendris_result=xe_res,
                    deepseek_score=item["deepseek_score"],
                    xendris_score=item["xendris_score"],
                    delta_score=item["delta_score"],
                    winner=item["winner"],
                    notes=item.get("notes"),
                )
            )
    return results


def write_ab_summary_json(summary: ABRunSummary, path: str) -> None:
    """Serialize the run summary to a standard JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary.to_dict(), f, ensure_ascii=False, indent=2)
