#!/usr/bin/env python3
"""Audit all benchmark summaries in a directory with the excellence gate."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from xendris.benchmarking import assess_benchmark_excellence  # noqa: E402


DEFAULT_JSON = ROOT / "runs" / "benchmark_suite_excellence_audit.json"
DEFAULT_MD = ROOT / "docs" / "benchmarks" / "BENCHMARK_SUITE_EXCELLENCE_AUDIT.md"
DEFAULT_QUARANTINE_MANIFEST = ROOT / "docs" / "benchmarks" / "HISTORICAL_REJECTED_ARTIFACTS.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit benchmark summaries for interpretability readiness.")
    parser.add_argument("--runs-dir", default="runs", help="Directory containing *_summary.json files.")
    parser.add_argument("--docs-dir", default="docs/benchmarks", help="Directory containing benchmark reports.")
    parser.add_argument("--output-json", default=str(DEFAULT_JSON), help="Output audit JSON path.")
    parser.add_argument("--output-md", default=str(DEFAULT_MD), help="Output audit Markdown path.")
    parser.add_argument(
        "--quarantine-manifest",
        default=str(DEFAULT_QUARANTINE_MANIFEST),
        help="Markdown manifest listing historical rejected summaries that should not block release.",
    )
    parser.add_argument("--fail-on-blockers", action="store_true", help="Return non-zero when blockers are found.")
    args = parser.parse_args(argv)

    runs_dir = Path(args.runs_dir)
    docs_dir = Path(args.docs_dir)
    summary_paths = discover_summary_files(runs_dir)
    quarantine_paths = load_quarantined_summary_paths(args.quarantine_manifest)
    records = mark_quarantined_records(
        [audit_summary_file(path, docs_dir) for path in summary_paths],
        quarantine_paths,
    )
    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    payload = build_suite_audit(records)
    payload = preserve_generated_timestamp_if_materially_unchanged(payload, output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    output_md.write_text(render_markdown(payload), encoding="utf-8")

    print(
        "BENCHMARK_SUITE_EXCELLENCE "
        f"summaries={payload['summary_count']} "
        f"ready={payload['ready_count']} "
        f"blocked={payload['blocked_count']} "
        f"quarantined={payload['quarantined_rejected_count']}"
    )
    print(f"Audit JSON saved to: {output_json}")
    print(f"Audit report saved to: {output_md}")
    if args.fail_on_blockers and payload["blocked_count"] > 0:
        return 1
    return 0


def discover_summary_files(runs_dir: str | Path) -> list[Path]:
    """Return sorted summary JSON files under a runs directory."""
    root = Path(runs_dir)
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*_summary.json") if path.is_file())


def audit_summary_file(summary_path: str | Path, docs_dir: str | Path) -> dict[str, Any]:
    """Audit one benchmark summary JSON file."""
    path = Path(summary_path)
    report_path = infer_report_path(path, docs_dir)
    summary = json.loads(path.read_text(encoding="utf-8"))
    report_text = report_path.read_text(encoding="utf-8") if report_path and report_path.exists() else None
    assessment = assess_benchmark_excellence(summary, report_text=report_text)
    return {
        "summary_path": str(path),
        "report_path": str(report_path) if report_path and report_path.exists() else None,
        "decision": assessment.decision.value,
        "has_blockers": assessment.has_blockers,
        "is_ready": assessment.is_ready,
        "issues": [issue.to_dict() for issue in assessment.issues],
        "blocker_count": len(assessment.blockers),
        "warning_count": len(assessment.warnings),
        "note_count": len(assessment.notes),
        "is_quarantined_historical": False,
    }


def infer_report_path(summary_path: Path, docs_dir: str | Path) -> Path | None:
    """Infer a benchmark report path from known Xendris run naming patterns."""
    stem = summary_path.name.removesuffix("_summary.json")
    sibling_report = summary_path.with_name(f"{stem}_report.md")
    if sibling_report.exists():
        return sibling_report
    docs = Path(docs_dir)
    known_reports = {
        "deepseek_vs_xendris_programming_reliability_v0_1_2026_07_04": (
            "RUN_DEEPSEEK_VS_XENDRIS_PROGRAMMING_RELIABILITY_V0_1_2026_07_04.md"
        ),
        "deepseek_vs_xendris_trust_traps_v0_1_2026_07_04_v2": (
            "RUN_DEEPSEEK_VS_XENDRIS_TRUST_TRAPS_V0_1_2026_07_04_V2.md"
        ),
        "deepseek_vs_xendris_trust_traps_v0_1_2026_07_04": (
            "RUN_DEEPSEEK_VS_XENDRIS_TRUST_TRAPS_V0_1_2026_07_04.md"
        ),
        "deepseek_vs_xendris_trust_traps_v0_1": (
            "RUN_DEEPSEEK_VS_XENDRIS_TRUST_TRAPS_V0_1.md.template"
        ),
    }
    if stem in known_reports:
        return docs / known_reports[stem]
    return None


def load_quarantined_summary_paths(manifest_path: str | Path) -> set[str]:
    """Load quarantined summary paths from the historical artifact manifest."""
    path = Path(manifest_path)
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    candidates = re.findall(r"`([^`]+_summary\.json)`", text)
    return {_normalize_path(candidate) for candidate in candidates}


def mark_quarantined_records(
    records: list[dict[str, Any]],
    quarantined_summary_paths: set[str],
) -> list[dict[str, Any]]:
    """Mark audit records that are historical rejected artifacts."""
    marked: list[dict[str, Any]] = []
    for record in records:
        updated = dict(record)
        updated["is_quarantined_historical"] = (
            _normalize_path(str(updated.get("summary_path", ""))) in quarantined_summary_paths
        )
        marked.append(updated)
    return marked


def build_suite_audit(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build aggregate audit metrics."""
    ready = [record for record in records if record["decision"] == "READY_FOR_INTERPRETATION"]
    warning = [record for record in records if record["decision"] == "WARNINGS_PRESENT"]
    active_blocked = [
        record
        for record in records
        if record["has_blockers"] and not record.get("is_quarantined_historical", False)
    ]
    quarantined_rejected = [
        record
        for record in records
        if record["has_blockers"] and record.get("is_quarantined_historical", False)
    ]
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "summary_count": len(records),
        "ready_count": len(ready),
        "warning_count": len(warning),
        "blocked_count": len(active_blocked),
        "quarantined_rejected_count": len(quarantined_rejected),
        "records": records,
    }


def preserve_generated_timestamp_if_materially_unchanged(
    payload: dict[str, Any],
    output_json: Path,
) -> dict[str, Any]:
    """Keep tracked audit outputs stable when only the timestamp would change."""
    if not output_json.exists():
        return payload
    try:
        existing = json.loads(output_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return payload
    if _without_generated_at(existing) == _without_generated_at(payload):
        updated = dict(payload)
        updated["generated_at_utc"] = existing.get("generated_at_utc", payload["generated_at_utc"])
        return updated
    return payload


def _without_generated_at(payload: dict[str, Any]) -> dict[str, Any]:
    comparable = dict(payload)
    comparable.pop("generated_at_utc", None)
    return comparable


def render_markdown(payload: dict[str, Any]) -> str:
    """Render a concise Markdown report from an audit payload."""
    rows = []
    for record in payload["records"]:
        blockers = sum(1 for issue in record["issues"] if issue["severity"] == "BLOCKER")
        warnings = sum(1 for issue in record["issues"] if issue["severity"] == "WARNING")
        rows.append(
            "| {summary} | {decision} | {scope} | {blockers} | {warnings} | {report} |".format(
                summary=record["summary_path"],
                decision=record["decision"],
                scope="historical_quarantine" if record.get("is_quarantined_historical") else "active",
                blockers=blockers,
                warnings=warnings,
                report=record["report_path"] or "not found",
            )
        )

    blocker_details = []
    for record in payload["records"]:
        for issue in record["issues"]:
            if issue["severity"] == "BLOCKER" and not record.get("is_quarantined_historical", False):
                blocker_details.append(f"- `{record['summary_path']}` `{issue['code']}`: {issue['message']}")

    quarantine_details = []
    for record in payload["records"]:
        if record.get("is_quarantined_historical", False):
            quarantine_details.append(f"- `{record['summary_path']}` remains rejected historical non-evidence.")

    return f"""# Benchmark Suite Excellence Audit

Generated UTC: `{payload['generated_at_utc']}`

## Summary

| Metric | Value |
|---|---:|
| Summary files | {payload['summary_count']} |
| Ready | {payload['ready_count']} |
| Warnings | {payload['warning_count']} |
| Blocked | {payload['blocked_count']} |
| Historical rejected quarantine | {payload['quarantined_rejected_count']} |

## Artifact Decisions

| Summary | Decision | Scope | Blockers | Warnings | Report |
|---|---|---|---:|---:|---|
{chr(10).join(rows) if rows else '| none | none | 0 | 0 | none |'}

## Blockers

{chr(10).join(blocker_details) if blocker_details else '- None.'}

## Historical Rejected Non-Evidence

{chr(10).join(quarantine_details) if quarantine_details else '- None.'}

## Interpretation

This audit checks whether benchmark artifacts are ready for careful
interpretation. It does not validate universal model superiority, production
readiness, or scientific truth.
"""


def _normalize_path(value: str) -> str:
    return value.replace("\\", "/").lower()


if __name__ == "__main__":
    raise SystemExit(main())
