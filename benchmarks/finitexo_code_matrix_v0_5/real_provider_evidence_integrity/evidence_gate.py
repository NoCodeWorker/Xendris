"""Evidence integrity gate for v0.5.4 real-provider diagnostics."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPECTED_DATASET_HASH = "a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4"
EXPECTED_MANIFEST_HASH = "6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e"
APPROVED = "REAL_PROVIDER_EVIDENCE_INTEGRITY_APPROVED_DIAGNOSTIC_ONLY"


@dataclass(frozen=True)
class EvidenceIntegrityConfig:
    run_dir: Path = Path("runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized")
    output_dir: Path = Path("runs/finitexo_code_matrix_v0_5_5_real_provider_evidence_integrity_gate")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _jsonl(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return []
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def _finding(code: str, message: str, path: Path | None = None) -> dict[str, Any]:
    return {"code": code, "message": message, "path": str(path) if path else None}


def _required_paths(run_dir: Path) -> dict[str, Path]:
    return {
        "summary": run_dir / "real_provider_diagnostic_summary.json",
        "report": run_dir / "real_provider_diagnostic_report.md",
        "responses": run_dir / "real_provider_responses.jsonl",
        "scores": run_dir / "real_provider_scores.jsonl",
        "costs": run_dir / "real_provider_costs.json",
        "errors": run_dir / "real_provider_errors.jsonl",
        "gate": run_dir / "real_provider_gate.json",
        "metadata": run_dir / "provider_request_metadata.jsonl",
        "preflight": run_dir / "provider_preflight.json",
    }


def _key(row: dict[str, Any]) -> tuple[str, str]:
    return (row.get("provider_name", ""), row.get("task_id", ""))


def _decision(findings: list[dict[str, Any]]) -> str:
    codes = {finding["code"] for finding in findings}
    if "missing_artifact" in codes:
        return "REAL_PROVIDER_EVIDENCE_INTEGRITY_BLOCKED_MISSING_ARTIFACT"
    if "dataset_hash_mismatch" in codes:
        return "REAL_PROVIDER_EVIDENCE_INTEGRITY_BLOCKED_DATASET_HASH_MISMATCH"
    if "traceability_failure" in codes:
        return "REAL_PROVIDER_EVIDENCE_INTEGRITY_BLOCKED_TRACEABILITY_FAILURE"
    if "unauthorized_claim" in codes:
        return "REAL_PROVIDER_EVIDENCE_INTEGRITY_BLOCKED_UNAUTHORIZED_CLAIM"
    if findings:
        return "REAL_PROVIDER_EVIDENCE_INTEGRITY_BLOCKED_ARTIFACT_INCONSISTENCY"
    return APPROVED


def _contains_forbidden_execution_text(text: str) -> bool:
    forbidden = ("mock", "stub", "fake", "simulated", "dry_run")
    for line in text.lower().splitlines():
        if "mock_fallback_used" in line and "false" in line:
            continue
        if any(term in line for term in forbidden):
            return True
    return False


def _contains_overclaim(text: str) -> bool:
    patterns = [
        r"statistical significance",
        r"provider superiority",
        r"xendris superiority",
        r"benchmark validation",
        r"production-grade evidence",
        r"universal conclusion",
    ]
    lowered = text.lower()
    for pattern in patterns:
        for match in re.finditer(pattern, lowered):
            window = lowered[max(0, match.start() - 40):match.start()]
            if "no " in window or "not " in window or "does not" in window:
                continue
            return True
    return False


def evaluate_evidence_integrity(config: EvidenceIntegrityConfig = EvidenceIntegrityConfig()) -> dict[str, Any]:
    paths = _required_paths(config.run_dir)
    findings: list[dict[str, Any]] = []
    for path in paths.values():
        if not path.exists():
            findings.append(_finding("missing_artifact", "Required v0.5.4 artifact is missing.", path))
    if findings:
        return _summary(config, findings, None, [], [], [], {})

    summary = _load_json(paths["summary"])
    costs = _load_json(paths["costs"])
    responses = _jsonl(paths["responses"])
    scores = _jsonl(paths["scores"])
    metadata = _jsonl(paths["metadata"])
    errors = _jsonl(paths["errors"])
    report = paths["report"].read_text(encoding="utf-8")

    if summary.get("dataset_hash") != EXPECTED_DATASET_HASH:
        findings.append(_finding("dataset_hash_mismatch", "Summary dataset hash mismatch.", paths["summary"]))
    if summary.get("manifest_hash") != EXPECTED_MANIFEST_HASH:
        findings.append(_finding("manifest_hash_mismatch", "Summary manifest hash mismatch.", paths["summary"]))
    if summary.get("frozen_task_count") != 10:
        findings.append(_finding("artifact_inconsistency", "Frozen task count must be 10.", paths["summary"]))
    if summary.get("provider_mode") != "real":
        findings.append(_finding("artifact_inconsistency", "provider_mode must be real.", paths["summary"]))
    if set(summary.get("providers_attempted", [])) != {"deepseek", "openai"}:
        findings.append(_finding("artifact_inconsistency", "providers_attempted must be exactly deepseek and openai.", paths["summary"]))
    if not errors and set(summary.get("providers_completed", [])) != {"deepseek", "openai"}:
        findings.append(_finding("artifact_inconsistency", "providers_completed must be exactly deepseek and openai when no errors exist.", paths["summary"]))

    expected = summary.get("task_attempts_expected")
    attempted = summary.get("task_attempts_attempted")
    completed = summary.get("task_attempts_completed")
    failed = summary.get("task_attempts_failed")
    skipped = summary.get("task_attempts_skipped")
    budget_blocked = summary.get("task_attempts_budget_blocked")
    if expected != 20:
        findings.append(_finding("artifact_inconsistency", "task_attempts_expected must be 20.", paths["summary"]))
    if attempted != completed + failed:
        findings.append(_finding("artifact_inconsistency", "attempted must equal completed plus failed.", paths["summary"]))
    if expected != attempted + skipped + budget_blocked:
        findings.append(_finding("artifact_inconsistency", "expected attempts do not match attempted + skipped + budget_blocked.", paths["summary"]))
    if completed == 20 and len(responses) != 20:
        findings.append(_finding("artifact_inconsistency", "responses must contain 20 lines when completed is 20.", paths["responses"]))
    if completed == 20 and len(scores) != 20:
        findings.append(_finding("artifact_inconsistency", "scores must contain 20 lines when completed is 20.", paths["scores"]))
    if attempted == 20 and len(metadata) != 20:
        findings.append(_finding("artifact_inconsistency", "metadata must contain 20 lines when attempted is 20.", paths["metadata"]))

    response_keys = {_key(row) for row in responses}
    score_keys = {_key(row) for row in scores}
    metadata_keys = {_key(row) for row in metadata}
    if score_keys != response_keys:
        findings.append(_finding("traceability_failure", "Score rows do not map exactly to response rows by provider/task.", paths["scores"]))
    if response_keys != metadata_keys:
        findings.append(_finding("traceability_failure", "Response rows do not map exactly to metadata rows by provider/task.", paths["metadata"]))

    provider_costs = costs.get("provider_costs_usd")
    if not isinstance(provider_costs, dict):
        findings.append(_finding("artifact_inconsistency", "real_provider_costs.json must contain provider_costs_usd.", paths["costs"]))
    else:
        cost_sum = round(sum(float(value) for value in provider_costs.values()), 8)
        if abs(cost_sum - float(costs.get("total_estimated_cost_usd", -1))) > 1e-8:
            findings.append(_finding("artifact_inconsistency", "Provider cost sum does not match cost total.", paths["costs"]))
    if costs.get("total_estimated_cost_usd") != summary.get("total_estimated_cost_usd"):
        findings.append(_finding("artifact_inconsistency", "Cost total does not match summary total.", paths["costs"]))

    if summary.get("mock_fallback_used") is not False:
        findings.append(_finding("artifact_inconsistency", "mock_fallback_used must be false.", paths["summary"]))
    for key in ("statistical_claim_authorized", "provider_superiority_claim_authorized", "xendris_superiority_claim_authorized"):
        if summary.get(key) is not False:
            findings.append(_finding("unauthorized_claim", f"{key} must be false.", paths["summary"]))

    execution_text = "\n".join(
        [
            paths["responses"].read_text(encoding="utf-8"),
            paths["metadata"].read_text(encoding="utf-8"),
            report,
        ]
    )
    if _contains_forbidden_execution_text(execution_text):
        findings.append(_finding("artifact_inconsistency", "Forbidden mock/stub/fake/simulated/dry_run text found.", config.run_dir))
    if _contains_overclaim(report):
        findings.append(_finding("unauthorized_claim", "Report contains unauthorized claim wording.", paths["report"]))

    return _summary(config, findings, summary, responses, scores, metadata, costs)


def _summary(
    config: EvidenceIntegrityConfig,
    findings: list[dict[str, Any]],
    source_summary: dict[str, Any] | None,
    responses: list[dict[str, Any]],
    scores: list[dict[str, Any]],
    metadata: list[dict[str, Any]],
    costs: dict[str, Any],
) -> dict[str, Any]:
    decision = _decision(findings)
    return {
        "gate_name": "Finitexo Code Matrix v0.5.5 Real Provider Evidence Integrity Gate",
        "decision": decision,
        "source_run_dir": str(config.run_dir),
        "dataset_hash": (source_summary or {}).get("dataset_hash"),
        "manifest_hash": (source_summary or {}).get("manifest_hash"),
        "frozen_task_count": (source_summary or {}).get("frozen_task_count"),
        "providers_attempted": (source_summary or {}).get("providers_attempted", []),
        "providers_completed": (source_summary or {}).get("providers_completed", []),
        "task_attempts_expected": (source_summary or {}).get("task_attempts_expected", 0),
        "task_attempts_attempted": (source_summary or {}).get("task_attempts_attempted", 0),
        "task_attempts_completed": (source_summary or {}).get("task_attempts_completed", 0),
        "responses_count": len(responses),
        "scores_count": len(scores),
        "metadata_count": len(metadata),
        "total_estimated_cost_usd": costs.get("total_estimated_cost_usd", 0),
        "provider_costs_usd": costs.get("provider_costs_usd", {}),
        "statistical_claim_authorized": False,
        "provider_superiority_claim_authorized": False,
        "xendris_superiority_claim_authorized": False,
        "finding_count": len(findings),
        "findings": findings,
    }


def build_evidence_integrity_report(summary: dict[str, Any]) -> str:
    findings = summary["findings"] or [{"code": "none", "message": "No findings.", "path": None}]
    finding_lines = [f"- `{item['code']}`: {item['message']}" for item in findings]
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.5.5 - Real Provider Evidence Integrity Gate",
            "",
            "## Scope",
            "",
            "This gate validates diagnostic real-provider evidence integrity. It does not execute providers and does not authorize superiority claims.",
            "",
            "## Summary",
            "",
            f"- Decision: `{summary['decision']}`",
            f"- Dataset hash: `{summary['dataset_hash']}`",
            f"- Manifest hash: `{summary['manifest_hash']}`",
            f"- Frozen task count: {summary['frozen_task_count']}",
            f"- Responses: {summary['responses_count']}",
            f"- Scores: {summary['scores_count']}",
            f"- Metadata rows: {summary['metadata_count']}",
            f"- Total estimated cost: ${float(summary['total_estimated_cost_usd']):.8f}",
            "",
            "## Claims",
            "",
            "- No statistical claim is authorized.",
            "- No provider superiority claim is authorized.",
            "- No Xendris superiority claim is authorized.",
            "",
            "## Findings",
            "",
            *finding_lines,
            "",
        ]
    )


def write_evidence_integrity_artifacts(config: EvidenceIntegrityConfig = EvidenceIntegrityConfig()) -> dict[str, Any]:
    summary = evaluate_evidence_integrity(config)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    (config.output_dir / "evidence_integrity_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (config.output_dir / "evidence_integrity_report.md").write_text(
        build_evidence_integrity_report(summary),
        encoding="utf-8",
    )
    return summary
