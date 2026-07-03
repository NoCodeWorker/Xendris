"""v5.9.2 common condition axis recovery for candidate reformulation."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from phyng.core.report_contract import append_canonical_status_section, build_report_contract


TARGET_COLUMNS = {
    "value",
    "value_numeric",
    "visibility_fraction",
    "interference_contrast",
    "original_value_text",
}
LOCAL_IDENTIFIER_COLUMNS = {
    "source_id",
    "local_pdf_hash",
    "local_pdf_path",
    "page_number",
    "figure_id",
    "location_label",
}
MIN_AXIS_RECORDS = 3
MIN_AXIS_SOURCES = 2


def run_common_condition_axis_recovery(root: str | Path = ".") -> dict[str, Any]:
    repo_root = Path(root)
    dataset = _load_json(repo_root / "data/frontera_c/master_goal/dataset_v5_7_4_master.json")
    records = list(dataset.get("records", []))
    axis_records = _build_axis_records(records)
    candidate_groups = _build_candidate_groups(axis_records)
    decision = _build_decision(records, axis_records, candidate_groups)
    payload = {
        "dataset_id": dataset.get("dataset_id"),
        "record_count": len(records),
        "source_count": len({record.get("source_id") for record in records}),
        "axis_records": axis_records,
        "candidate_groups": candidate_groups,
        "decision": decision,
        "forbidden_actions_avoided": [
            "target value used as feature",
            "source_id used as feature",
            "page or figure lookup used as feature",
            "post-hoc axis selection promoted to PredictiveGain",
            "single-source axis promoted to out-of-source candidate",
        ],
    }
    return payload


def write_common_condition_axis_outputs(root: str | Path, payload: dict[str, Any]) -> dict[str, str]:
    repo_root = Path(root)
    data_dir = repo_root / "data/frontera_c/candidates"
    report_dir = repo_root / "reports/frontera_c/candidates"
    campaign_dir = repo_root / "reports/campaigns"
    docs_dir = repo_root / "docs"
    data_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "axis_json": data_dir / "common_condition_axis_recovery_v5_9_2.json",
        "groups_json": data_dir / "common_condition_axis_candidate_groups_v5_9_2.json",
        "next_gate_json": data_dir / "common_condition_axis_next_gate_v5_9_2.json",
        "axis_report": report_dir / "common_condition_axis_recovery_v5_9_2.md",
        "campaign_report": campaign_dir / "FRONTERA-C-COMMON-CONDITION-AXIS-RECOVERY-v5_9_2.md",
        "final_doc": docs_dir / "380_PHYGN_V5_9_2_COMMON_CONDITION_AXIS_RECOVERY_RESULTS.md",
    }
    paths["axis_json"].write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    paths["groups_json"].write_text(
        json.dumps({"candidate_groups": payload["candidate_groups"]}, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    paths["next_gate_json"].write_text(json.dumps(payload["decision"], indent=2, sort_keys=True), encoding="utf-8")
    report = _canonical(_render_axis_report(payload), payload)
    paths["axis_report"].write_text(report, encoding="utf-8")
    paths["campaign_report"].write_text(_canonical(_render_campaign_report(payload), payload), encoding="utf-8")
    paths["final_doc"].write_text(_canonical(_render_final_doc(payload), payload), encoding="utf-8")
    return {key: path.relative_to(repo_root).as_posix() for key, path in paths.items()}


def _build_axis_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[tuple[dict[str, Any], Any]]] = defaultdict(list)
    for record in records:
        for key, value in (record.get("conditions") or {}).items():
            if key == "unit":
                continue
            grouped[key].append((record, value))
    axis_records: list[dict[str, Any]] = []
    for axis_name, values in sorted(grouped.items()):
        source_ids = sorted({record.get("source_id") for record, _ in values})
        ytrue_ids = [record.get("y_true_id") for record, _ in values]
        raw_values = [value for _, value in values]
        numeric_values = [value for value in raw_values if isinstance(value, (int, float))]
        value_type = "numeric" if len(numeric_values) == len(raw_values) else "categorical_or_text"
        record_count = len(values)
        source_count = len(source_ids)
        axis_records.append(
            {
                "axis_name": axis_name,
                "value_type": value_type,
                "record_count": record_count,
                "source_count": source_count,
                "coverage_fraction": record_count / len(records) if records else 0.0,
                "source_ids": source_ids,
                "y_true_ids": ytrue_ids,
                "sample_values": raw_values[:6],
                "is_target_or_identifier": axis_name in TARGET_COLUMNS or axis_name in LOCAL_IDENTIFIER_COLUMNS,
                "leakage_status": "PASS" if axis_name not in TARGET_COLUMNS and axis_name not in LOCAL_IDENTIFIER_COLUMNS else "BLOCKING",
                "passes_common_numeric_axis_threshold": (
                    value_type == "numeric"
                    and record_count >= MIN_AXIS_RECORDS
                    and source_count >= MIN_AXIS_SOURCES
                    and axis_name not in TARGET_COLUMNS
                    and axis_name not in LOCAL_IDENTIFIER_COLUMNS
                ),
                "failure_reasons": _axis_failure_reasons(axis_name, value_type, record_count, source_count),
            }
        )
    return axis_records


def _axis_failure_reasons(axis_name: str, value_type: str, record_count: int, source_count: int) -> list[str]:
    reasons: list[str] = []
    if axis_name in TARGET_COLUMNS or axis_name in LOCAL_IDENTIFIER_COLUMNS:
        reasons.append("LEAKAGE_COLUMN")
    if value_type != "numeric":
        reasons.append("NOT_NUMERIC_AXIS")
    if record_count < MIN_AXIS_RECORDS:
        reasons.append("INSUFFICIENT_RECORD_COVERAGE")
    if source_count < MIN_AXIS_SOURCES:
        reasons.append("SINGLE_SOURCE_OR_INSUFFICIENT_SOURCE_COVERAGE")
    return reasons


def _build_candidate_groups(axis_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups = []
    for axis in axis_records:
        if axis["passes_common_numeric_axis_threshold"]:
            status = "AXIS_READY_FOR_CANDIDATE_REFORMULATION"
        elif axis["value_type"] == "numeric" and axis["record_count"] >= MIN_AXIS_RECORDS:
            status = "AXIS_PROMISING_BUT_SINGLE_SOURCE"
        elif axis["source_count"] >= MIN_AXIS_SOURCES:
            status = "AXIS_CONTEXT_ONLY_NOT_NUMERIC"
        else:
            status = "AXIS_REJECTED_INSUFFICIENT_COVERAGE"
        groups.append(
            {
                "candidate_group_id": f"AXIS-GROUP-v5_9_2-{axis['axis_name'].upper()}",
                "axis_name": axis["axis_name"],
                "axis_status": status,
                "record_count": axis["record_count"],
                "source_count": axis["source_count"],
                "can_support_source_agnostic_candidate": axis["passes_common_numeric_axis_threshold"],
                "can_support_v6_0": axis["passes_common_numeric_axis_threshold"],
                "notes": _group_notes(axis, status),
            }
        )
    return groups


def _group_notes(axis: dict[str, Any], status: str) -> list[str]:
    if status == "AXIS_READY_FOR_CANDIDATE_REFORMULATION":
        return ["Numeric non-target axis has multi-source coverage."]
    if status == "AXIS_PROMISING_BUT_SINGLE_SOURCE":
        return ["Numeric axis has enough records but only one source; out-of-source test would be invalid."]
    if status == "AXIS_CONTEXT_ONLY_NOT_NUMERIC":
        return ["Axis can help stratify mechanism/context but cannot be the shared numeric condition axis."]
    return ["Axis does not meet common-condition coverage requirements."]


def _build_decision(
    records: list[dict[str, Any]],
    axis_records: list[dict[str, Any]],
    candidate_groups: list[dict[str, Any]],
) -> dict[str, Any]:
    ready_axes = [axis for axis in axis_records if axis["passes_common_numeric_axis_threshold"]]
    promising_single_source = [
        axis for axis in axis_records if axis["value_type"] == "numeric" and axis["record_count"] >= MIN_AXIS_RECORDS
    ]
    if ready_axes:
        final_status = "COMMON_CONDITION_AXIS_FOUND_FOR_REFORMULATION"
        allowed_next_phase = "v5.9.3 - Candidate Rule Reformulation"
        blocker = None
    elif promising_single_source:
        final_status = "COMMON_CONDITION_AXIS_BLOCKED_SINGLE_SOURCE_ONLY"
        allowed_next_phase = None
        blocker = "The only sufficiently populated numeric axis is single-source and cannot support out-of-source PredictiveGain."
    else:
        final_status = "COMMON_CONDITION_AXIS_BLOCKED_INSUFFICIENT_COVERAGE"
        allowed_next_phase = None
        blocker = "No non-target numeric condition axis reaches minimum record and source coverage."
    return {
        "final_status": final_status,
        "allowed_next_phase": allowed_next_phase,
        "record_count": len(records),
        "source_count": len({record.get("source_id") for record in records}),
        "ready_axis_count": len(ready_axes),
        "promising_single_source_axis_count": len(promising_single_source),
        "selected_axis": ready_axes[0]["axis_name"] if ready_axes else None,
        "selected_candidate_family": "SOURCE_AGNOSTIC_DECOHERENCE_RESPONSE" if ready_axes else None,
        "predictive_gain_permitted": False,
        "v6_0_permitted": False,
        "blocker": blocker,
        "next_required_action": _next_required_action(ready_axes, promising_single_source),
        "blocked_claims": [
            "PredictiveGain exists",
            "Frontera C is validated",
            "SOURCE_AGNOSTIC_DECOHERENCE_RESPONSE is selected",
            "single-source axis supports out-of-source validation",
        ],
    }


def _next_required_action(ready_axes: list[dict[str, Any]], promising_single_source: list[dict[str, Any]]) -> str:
    if ready_axes:
        return "Define a candidate prediction rule over the recovered axis, then rerun candidate selection."
    if promising_single_source:
        axis_names = ", ".join(axis["axis_name"] for axis in promising_single_source)
        return f"Acquire or extract independent-source y_true records on the same numeric axis: {axis_names}."
    return "Perform targeted y_true expansion around a predeclared shared numeric condition axis."


def _render_axis_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Common Condition Axis Recovery v5.9.2",
        "",
        f"Final status: `{payload['decision']['final_status']}`",
        f"Record count: `{payload['record_count']}`",
        f"Source count: `{payload['source_count']}`",
        f"Selected axis: `{payload['decision']['selected_axis']}`",
        "",
        "| Axis | Type | Records | Sources | Status |",
        "|---|---|---:|---:|---|",
    ]
    group_by_axis = {group["axis_name"]: group for group in payload["candidate_groups"]}
    for axis in payload["axis_records"]:
        group = group_by_axis[axis["axis_name"]]
        lines.append(
            f"| `{axis['axis_name']}` | `{axis['value_type']}` | {axis['record_count']} | {axis['source_count']} | `{group['axis_status']}` |"
        )
    lines.extend(
        [
            "",
            "No PredictiveGain was computed. No candidate was selected. No physical claim was upgraded.",
        ]
    )
    return "\n".join(lines) + "\n"


def _canonical(markdown: str, payload: dict[str, Any]) -> str:
    decision = payload["decision"]
    contract = build_report_contract(
        title="Common Condition Axis Recovery v5.9.2",
        campaign_id="FRONTERA-C-COMMON-CONDITION-AXIS-RECOVERY-v5_9_2",
        domain_status=decision["final_status"],
        domain="common_condition_axis_recovery",
        next_actions=[decision["next_required_action"]],
        discipline_note="A common axis is permission to formulate a candidate, not permission to score it.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_campaign_report(payload: dict[str, Any]) -> str:
    decision = payload["decision"]
    return "\n".join(
        [
            "# Campaign Report - FRONTERA-C-COMMON-CONDITION-AXIS-RECOVERY-v5_9_2",
            "",
            f"- status: `{decision['final_status']}`",
            f"- selected_axis: `{decision['selected_axis']}`",
            f"- selected_candidate_family: `{decision['selected_candidate_family']}`",
            f"- v6_0_permitted: `{decision['v6_0_permitted']}`",
            f"- predictive_gain_permitted: `{decision['predictive_gain_permitted']}`",
            f"- next_required_action: {decision['next_required_action']}",
        ]
    ) + "\n"


def _render_final_doc(payload: dict[str, Any]) -> str:
    decision = payload["decision"]
    lines = [
        "# Phygn v5.9.2 - Common Condition Axis Recovery Results",
        "",
        "Date: 2026-07-02",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{decision['final_status']}`",
        f"Selected axis: `{decision['selected_axis']}`",
        f"Selected candidate family: `{decision['selected_candidate_family']}`",
        f"v6.0 permitted: `{decision['v6_0_permitted']}`",
        f"PredictiveGain permitted: `{decision['predictive_gain_permitted']}`",
        "",
        "## Interpretation",
        "",
        decision["blocker"] or "A shared non-target numeric axis was found for candidate reformulation.",
        "",
        "## Next Required Action",
        "",
        decision["next_required_action"],
        "",
        "## Blocked Claims",
        "",
        "- Frontera C is validated.",
        "- PredictiveGain exists.",
        "- A single-source axis is sufficient for out-of-source validation.",
        "- Common-axis recovery is evidence support.",
        "",
        "Final discipline:",
        "",
        "```txt",
        "A common axis is permission to formulate a candidate.",
        "It is not permission to score it.",
        "```",
    ]
    return "\n".join(lines) + "\n"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
