"""PredictiveGain, y_true, source-support, and negative-control integrity audits."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.full_suite_logic_audit.schemas import AuditIssue


def audit_metric_integrity(root: str | Path = ".") -> tuple[list[AuditIssue], list[AuditIssue], list[AuditIssue], list[AuditIssue]]:
    repo_root = Path(root)
    json_paths = [
        path
        for path in repo_root.rglob("*.json")
        if "__pycache__" not in path.parts and "audits" not in path.relative_to(repo_root).parts
    ]
    predictive: list[AuditIssue] = []
    ytrue: list[AuditIssue] = []
    source_support: list[AuditIssue] = []
    negative: list[AuditIssue] = []
    for path in json_paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        rel = path.relative_to(repo_root).as_posix()
        predictive.extend(audit_predictive_gain_payload(payload, rel))
        ytrue.extend(audit_ytrue_payload(payload, rel))
        source_support.extend(audit_source_support_payload(payload, rel))
        negative.extend(audit_negative_control_payload(payload, rel))
    return predictive, ytrue, source_support, negative


def audit_predictive_gain_payload(payload: Any, path: str = "inline") -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    for obj in _walk_dicts(payload):
        if "benchmark_score" in obj and "predictive_gain" in obj and obj.get("benchmark_score") == obj.get("predictive_gain"):
            issues.append(_issue("BENCHMARK_SCORE_AS_PREDICTIVE_GAIN", path, "Benchmark score is reused as PredictiveGain.", "Compute PredictiveGain only from matched predictions and accepted y_true."))
        status = str(obj.get("predictive_gain_status", "")).upper()
        ready = obj.get("ready_for_predictive_gain")
        if ready is True or status in {"READY", "COMPUTED", "POSITIVE", "PREDICTIVE_GAIN_COMPUTED"}:
            accepted = int(obj.get("accepted_y_true_count", obj.get("total_y_true_count", 0)) or 0)
            matched = int(obj.get("matched_prediction_count", 0) or 0)
            if accepted < 3 or matched < 3:
                issues.append(_issue("PREDICTIVE_GAIN_WITH_INSUFFICIENT_YTRUE", path, f"PredictiveGain readiness uses accepted={accepted}, matched={matched}.", "Require at least three accepted y_true records with matched predictions."))
    return issues


def audit_ytrue_payload(payload: Any, path: str = "inline") -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    for obj in _walk_dicts(payload):
        if not _looks_like_ytrue_record(obj):
            continue
        missing = [field for field in ("source_id", "source_hash", "unit") if not obj.get(field)]
        has_location = bool(obj.get("source_location_value") or obj.get("page_number") or obj.get("table_number") or obj.get("figure_number"))
        if not has_location:
            missing.append("source_location")
        if missing:
            issues.append(_issue("YTRUE_WITHOUT_PROVENANCE", path, f"Missing y_true provenance fields: {', '.join(missing)}.", "Reject y_true records without source hash, unit, and exact source location."))
    return issues


def audit_source_support_payload(payload: Any, path: str = "inline") -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    for obj in _walk_dicts(payload):
        role = str(obj.get("component_role", "")).upper()
        support = str(obj.get("support_status", obj.get("source_support_status", ""))).upper()
        candidate_id = str(obj.get("candidate_id", ""))
        if "CANDIDATE" in candidate_id.upper() and support in {"SOURCE_SUPPORT", "SUPPORTED", "ACCEPTED_SUPPORT"}:
            issues.append(_issue("EXTRACTION_CANDIDATE_AS_SOURCE_SUPPORT", path, f"Candidate `{candidate_id}` is treated as source support.", "Require validation-ready review and source pressure decision before support claims."))
        if role == "GRADIENT_COMPONENT" and support in {"SUPPORTED", "SOURCE_SUPPORT"}:
            issues.append(_issue("GRADIENT_COMPONENT_SUPPORT_WITHOUT_DEBT_RESOLUTION", path, "Gradient component marked supported.", "Keep gradient mechanism support blocked until SLOT_4 debt resolution."))
    return issues


def audit_negative_control_payload(payload: Any, path: str = "inline") -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    for obj in _walk_dicts(payload):
        name_blob = " ".join(str(obj.get(key, "")) for key in ("id", "control_id", "type", "kind", "status")).lower()
        if "negative" not in name_blob or "control" not in name_blob:
            continue
        if not obj.get("claim_impact"):
            issues.append(_issue("NEGATIVE_CONTROL_WITHOUT_CLAIM_IMPACT", path, "Negative control lacks claim_impact.", "Record how the negative control changes or blocks claims."))
    return issues


def _looks_like_ytrue_record(obj: dict[str, Any]) -> bool:
    keys = set(obj)
    return "y_true_id" in keys or ("value" in keys and ("observable_class" in keys or "normalized_variable_name" in keys))


def _walk_dicts(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_dicts(child)


def _issue(category: str, path: str, evidence: str, remediation: str) -> AuditIssue:
    return AuditIssue(
        issue_id=f"{category}-{abs(hash((path, evidence))) % 100000}",
        severity="BLOCKER",
        category=category,
        path=path,
        message=evidence,
        evidence=evidence,
        remediation=remediation,
    )
