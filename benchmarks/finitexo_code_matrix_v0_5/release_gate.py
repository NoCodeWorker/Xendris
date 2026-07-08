"""Release gate for Finitexo Code Matrix v0.5.x infrastructure.

The gate checks documentation and artifact integrity only. It never executes
providers, never reads .env files, never prints secrets, and does not authorize
statistical, provider-superiority, Xendris-superiority, external-validation, or
production-readiness claims.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.dataset_loader import (
    EXPECTED_DATASET_HASH,
    EXPECTED_MANIFEST_HASH,
    load_frozen_dataset,
)


APPROVED_DECISION = "APPROVED_FOR_EXPLICIT_REAL_PROVIDER_DIAGNOSTIC_EXECUTION"


@dataclass(frozen=True)
class ReleaseGateConfig:
    workspace_root: Path = Path(".")
    dataset_path: Path = Path("benchmarks/finitexo_code_matrix_v0_4_3")
    v0_5_run_dir: Path = Path("runs/finitexo_code_matrix_v0_5_provider_smoke")
    v0_5_1_run_dir: Path = Path("runs/finitexo_code_matrix_v0_5_1_real_provider_smoke")
    v0_5_2_run_dir: Path = Path("runs/finitexo_code_matrix_v0_5_2_real_provider_execution")
    output_dir: Path = Path("runs/finitexo_code_matrix_v0_5_2_release_gate")
    status_docs: tuple[Path, ...] = (
        Path("docs/status/FINITEXO_CODE_MATRIX_V0_5_PROVIDER_SMOKE_FROZEN_N10.md"),
        Path("docs/status/FINITEXO_CODE_MATRIX_V0_5_1_REAL_PROVIDER_SMOKE_FROZEN_N10.md"),
        Path("docs/status/FINITEXO_CODE_MATRIX_V0_5_2_REAL_PROVIDER_EXECUTION_FROZEN_N10.md"),
    )

    def resolve(self, path: Path) -> Path:
        return path if path.is_absolute() else self.workspace_root / path


@dataclass(frozen=True)
class ReleaseGateFinding:
    code: str
    severity: str
    message: str
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "path": self.path,
        }


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _jsonl_rows(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return []
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def _require_files(paths: list[Path], findings: list[ReleaseGateFinding]) -> bool:
    ok = True
    for path in paths:
        if not path.exists():
            findings.append(
                ReleaseGateFinding(
                    "missing_artifact",
                    "BLOCKER",
                    "Required artifact is missing.",
                    str(path),
                )
            )
            ok = False
    return ok


def _secret_patterns() -> list[re.Pattern[str]]:
    return [
        re.compile(r"sk-[A-Za-z0-9_\-]{8,}"),
        re.compile(r"Authorization:\s*Bearer\s+\S+", re.IGNORECASE),
        re.compile(r"\bBearer\s+[A-Za-z0-9_\-]{16,}", re.IGNORECASE),
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        re.compile(r'"(?:api_key|token)"\s*:\s*"[A-Za-z0-9_\-]{12,}"', re.IGNORECASE),
        re.compile(r"\b(?:OPENAI_API_KEY|DEEPSEEK_API_KEY)\s*[:=]\s*[A-Za-z0-9_\-]{12,}"),
    ]


def _add(findings: list[ReleaseGateFinding], code: str, message: str, path: Path | None = None) -> None:
    findings.append(ReleaseGateFinding(code, "BLOCKER", message, str(path) if path else None))


def _check_dataset(config: ReleaseGateConfig, findings: list[ReleaseGateFinding]) -> dict[str, Any]:
    dataset = load_frozen_dataset(config.resolve(config.dataset_path))
    if dataset.dataset_hash != EXPECTED_DATASET_HASH:
        _add(findings, "dataset_hash_mismatch", "Frozen dataset hash mismatch.", config.dataset_path)
    if dataset.manifest_hash != EXPECTED_MANIFEST_HASH:
        _add(findings, "manifest_hash_mismatch", "Frozen manifest hash mismatch.", config.dataset_path)
    if len(dataset.tasks) != 10:
        _add(findings, "frozen_task_count_mismatch", "Frozen task count is not 10.", config.dataset_path)
    return {
        "dataset_hash": dataset.dataset_hash,
        "manifest_hash": dataset.manifest_hash,
        "frozen_task_count": len(dataset.tasks),
    }


def _check_v0_5(config: ReleaseGateConfig, findings: list[ReleaseGateFinding]) -> None:
    run_dir = config.resolve(config.v0_5_run_dir)
    required = [
        run_dir / "provider_smoke_summary.json",
        run_dir / "provider_smoke_report.md",
        run_dir / "provider_responses.jsonl",
        run_dir / "provider_scores.jsonl",
        run_dir / "provider_costs.json",
        run_dir / "provider_errors.jsonl",
    ]
    if not _require_files(required, findings):
        return
    summary = _load_json(run_dir / "provider_smoke_summary.json")
    responses = _jsonl_rows(run_dir / "provider_responses.jsonl")
    scores = _jsonl_rows(run_dir / "provider_scores.jsonl")
    costs = _load_json(run_dir / "provider_costs.json")
    errors = _jsonl_rows(run_dir / "provider_errors.jsonl")
    if summary.get("provider_mode") != "mock":
        _add(findings, "v0_5_provider_mode_not_mock", "v0.5 provider mode must be mock.", run_dir)
    if summary.get("dataset_hash") != EXPECTED_DATASET_HASH:
        _add(findings, "v0_5_summary_dataset_hash_mismatch", "v0.5 summary dataset hash mismatch.", run_dir)
    if summary.get("manifest_hash") != EXPECTED_MANIFEST_HASH:
        _add(findings, "v0_5_summary_manifest_hash_mismatch", "v0.5 summary manifest hash mismatch.", run_dir)
    if summary.get("final_decision", "").startswith("REAL_PROVIDER_"):
        _add(findings, "v0_5_implies_real_provider", "v0.5 must not imply real-provider execution.", run_dir)
    if summary.get("task_attempts_total") != len(responses):
        _add(findings, "v0_5_response_count_mismatch", "v0.5 response count mismatches summary.", run_dir)
    if len(scores) != len(responses):
        _add(findings, "v0_5_score_count_mismatch", "v0.5 score count mismatches responses.", run_dir)
    if costs.get("total_estimated_cost_usd") != summary.get("total_estimated_cost_usd"):
        _add(findings, "v0_5_cost_mismatch", "v0.5 cost artifact mismatches summary.", run_dir)
    if errors and summary.get("providers_failed") == []:
        _add(findings, "v0_5_hidden_errors", "v0.5 errors exist but summary has no failed providers.", run_dir)


def _check_v0_5_1(config: ReleaseGateConfig, findings: list[ReleaseGateFinding]) -> None:
    run_dir = config.resolve(config.v0_5_1_run_dir)
    required = [
        run_dir / "real_provider_smoke_summary.json",
        run_dir / "real_provider_smoke_report.md",
        run_dir / "real_provider_responses.jsonl",
        run_dir / "real_provider_scores.jsonl",
        run_dir / "real_provider_costs.json",
        run_dir / "real_provider_errors.jsonl",
        run_dir / "real_provider_gate.json",
    ]
    if not _require_files(required, findings):
        return
    summary = _load_json(run_dir / "real_provider_smoke_summary.json")
    responses = _jsonl_rows(run_dir / "real_provider_responses.jsonl")
    costs = _load_json(run_dir / "real_provider_costs.json")
    expected_configured = {"deepseek", "openai"}
    if summary.get("provider_mode") != "real":
        _add(findings, "v0_5_1_provider_mode_not_real", "v0.5.1 provider mode must be real.", run_dir)
    if summary.get("dataset_hash") != EXPECTED_DATASET_HASH:
        _add(findings, "v0_5_1_summary_dataset_hash_mismatch", "v0.5.1 summary dataset hash mismatch.", run_dir)
    if summary.get("manifest_hash") != EXPECTED_MANIFEST_HASH:
        _add(findings, "v0_5_1_summary_manifest_hash_mismatch", "v0.5.1 summary manifest hash mismatch.", run_dir)
    if set(summary.get("providers_configured", [])) != expected_configured:
        _add(findings, "v0_5_1_provider_config_mismatch", "v0.5.1 configured providers mismatch.", run_dir)
    if summary.get("providers_attempted") != [] or summary.get("providers_completed") != [] or summary.get("providers_failed") != []:
        _add(findings, "v0_5_1_provider_attempt_contradiction", "v0.5.1 must not show provider attempts.", run_dir)
    if summary.get("task_attempts_skipped") != 20 or summary.get("task_attempts_total") != 0:
        _add(findings, "v0_5_1_skipped_count_mismatch", "v0.5.1 skipped attempts are inconsistent.", run_dir)
    if summary.get("total_estimated_cost_usd") != 0.0 or costs.get("total_estimated_cost_usd") != 0.0:
        _add(findings, "v0_5_1_nonzero_cost_without_execution", "v0.5.1 cost must be zero without attempts.", run_dir)
    if summary.get("final_decision") != "REAL_PROVIDER_SMOKE_READY_CONFIGURATION_MISSING_NO_EXECUTION":
        _add(findings, "v0_5_1_decision_mismatch", "v0.5.1 decision must be configuration missing.", run_dir)
    if responses:
        _add(findings, "v0_5_1_responses_without_execution", "v0.5.1 responses exist despite no task completion.", run_dir)


def _check_v0_5_2(config: ReleaseGateConfig, findings: list[ReleaseGateFinding]) -> None:
    run_dir = config.resolve(config.v0_5_2_run_dir)
    required = [
        run_dir / "real_provider_execution_summary.json",
        run_dir / "real_provider_execution_report.md",
        run_dir / "real_provider_responses.jsonl",
        run_dir / "real_provider_scores.jsonl",
        run_dir / "real_provider_costs.json",
        run_dir / "real_provider_errors.jsonl",
        run_dir / "real_provider_gate.json",
        run_dir / "provider_request_metadata.jsonl",
    ]
    if not _require_files(required, findings):
        return
    summary = _load_json(run_dir / "real_provider_execution_summary.json")
    responses = _jsonl_rows(run_dir / "real_provider_responses.jsonl")
    costs = _load_json(run_dir / "real_provider_costs.json")
    gate = _load_json(run_dir / "real_provider_gate.json")
    expected_configured = {"deepseek", "openai"}
    if summary.get("provider_mode") != "real":
        _add(findings, "v0_5_2_provider_mode_not_real", "v0.5.2 provider mode must be real.", run_dir)
    if summary.get("dataset_hash") != EXPECTED_DATASET_HASH:
        _add(findings, "v0_5_2_summary_dataset_hash_mismatch", "v0.5.2 summary dataset hash mismatch.", run_dir)
    if summary.get("manifest_hash") != EXPECTED_MANIFEST_HASH:
        _add(findings, "v0_5_2_summary_manifest_hash_mismatch", "v0.5.2 summary manifest hash mismatch.", run_dir)
    if set(summary.get("providers_configured", [])) != expected_configured:
        _add(findings, "v0_5_2_provider_config_mismatch", "v0.5.2 configured providers mismatch.", run_dir)
    if summary.get("providers_attempted") != [] or summary.get("providers_completed") != [] or summary.get("providers_failed") != []:
        _add(findings, "v0_5_2_provider_attempt_contradiction", "v0.5.2 must not show provider attempts.", run_dir)
    if summary.get("task_attempts_completed") != 0 or summary.get("task_attempts_failed") != 0:
        _add(findings, "v0_5_2_task_count_contradiction", "v0.5.2 completed/failed attempts must be zero.", run_dir)
    if summary.get("task_attempts_skipped") != 20:
        _add(findings, "v0_5_2_skipped_count_mismatch", "v0.5.2 skipped attempts must be 20.", run_dir)
    if summary.get("total_estimated_cost_usd") != 0.0 or costs.get("total_estimated_cost_usd") != 0.0:
        _add(findings, "v0_5_2_nonzero_cost_without_execution", "v0.5.2 cost must be zero without attempts.", run_dir)
    if summary.get("budget_decision") != "BLOCKED":
        _add(findings, "v0_5_2_budget_decision_mismatch", "v0.5.2 budget decision must be BLOCKED.", run_dir)
    if summary.get("final_decision") != "REAL_PROVIDER_SMOKE_CONFIGURATION_MISSING_NO_EXECUTION":
        _add(findings, "v0_5_2_decision_mismatch", "v0.5.2 decision must be configuration missing.", run_dir)
    if gate.get("decision") != "REAL_PROVIDER_SMOKE_CONFIGURATION_MISSING_NO_EXECUTION":
        _add(findings, "v0_5_2_gate_decision_mismatch", "v0.5.2 gate decision mismatch.", run_dir)
    if responses:
        _add(findings, "v0_5_2_responses_without_execution", "v0.5.2 responses exist despite zero completed attempts.", run_dir)
    if any("mock" in json.dumps(row).lower() for row in responses):
        _add(findings, "real_execution_mock_fallback_response", "Real execution artifacts contain mock/synthetic fallback text.", run_dir)


def _check_secret_scan(config: ReleaseGateConfig, findings: list[ReleaseGateFinding]) -> None:
    roots = [
        *(config.resolve(path) for path in config.status_docs),
        config.resolve(config.v0_5_run_dir),
        config.resolve(config.v0_5_1_run_dir),
        config.resolve(config.v0_5_2_run_dir),
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.exists():
            files.extend(path for path in root.rglob("*") if path.is_file())
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in _secret_patterns():
            if pattern.search(text):
                _add(findings, "secret_like_content", "Secret-like content found in generated/docs artifact.", path)
                break


def _check_docs(config: ReleaseGateConfig, findings: list[ReleaseGateFinding]) -> None:
    required_phrases = [
        "diagnostic",
        "No statistical claim is authorized",
        "No provider superiority claim is authorized",
        "No Xendris superiority claim is authorized",
    ]
    forbidden_patterns = [
        re.compile(r"\b(statistically valid|statistical validity|statistically significant)\b", re.IGNORECASE),
        re.compile(r"\b(provider superiority demonstrated|Xendris superiority demonstrated)\b(?!(?:;|\.|,|-))", re.IGNORECASE),
        re.compile(r"\breal-provider performance result\b", re.IGNORECASE),
        re.compile(r"\bload(?:ing)? \.env automatically\b", re.IGNORECASE),
    ]
    for doc in config.status_docs:
        path = config.resolve(doc)
        if not path.exists():
            _add(findings, "missing_status_doc", "Required status document missing.", path)
            continue
        text = _read_text(path)
        for phrase in required_phrases:
            if phrase not in text:
                _add(findings, "documentation_missing_conservative_phrase", f"Document missing required phrase: {phrase}", path)
        for pattern in forbidden_patterns:
            if pattern.search(text):
                _add(findings, "documentation_overclaim", "Document contains forbidden overclaim wording.", path)


def _decision_from_findings(findings: list[ReleaseGateFinding]) -> str:
    codes = {finding.code for finding in findings}
    if "secret_like_content" in codes:
        return "BLOCKED_SECRET_RISK"
    if "dataset_hash_mismatch" in codes:
        return "BLOCKED_DATASET_HASH_MISMATCH"
    if "manifest_hash_mismatch" in codes:
        return "BLOCKED_MANIFEST_HASH_MISMATCH"
    if "missing_artifact" in codes or "missing_status_doc" in codes:
        return "BLOCKED_MISSING_ARTIFACTS"
    if any(code.startswith("documentation_") for code in codes):
        return "BLOCKED_DOCUMENTATION_OVERCLAIM"
    if "real_execution_mock_fallback_response" in codes:
        return "BLOCKED_REAL_EXECUTION_PATH_UNSAFE"
    if findings:
        return "BLOCKED_ARTIFACT_INCONSISTENCY"
    return APPROVED_DECISION


def evaluate_release_gate(config: ReleaseGateConfig = ReleaseGateConfig()) -> dict[str, Any]:
    findings: list[ReleaseGateFinding] = []
    dataset_info = _check_dataset(config, findings)
    _check_v0_5(config, findings)
    _check_v0_5_1(config, findings)
    _check_v0_5_2(config, findings)
    _check_secret_scan(config, findings)
    _check_docs(config, findings)
    decision = _decision_from_findings(findings)
    return {
        "gate_name": "Finitexo Code Matrix v0.5.2 Release Gate",
        "decision": decision,
        "dataset_hash": dataset_info["dataset_hash"],
        "manifest_hash": dataset_info["manifest_hash"],
        "frozen_task_count": dataset_info["frozen_task_count"],
        "real_providers_executed": False,
        "env_files_read": False,
        "secrets_found": decision == "BLOCKED_SECRET_RISK",
        "statistical_claim_authorized": False,
        "provider_superiority_claim_authorized": False,
        "xendris_superiority_claim_authorized": False,
        "finding_count": len(findings),
        "findings": [finding.to_dict() for finding in findings],
    }


def build_release_gate_report(summary: dict[str, Any]) -> str:
    findings = summary["findings"]
    finding_lines = [
        f"- `{finding['code']}`: {finding['message']} ({finding.get('path')})"
        for finding in findings
    ] or ["- None."]
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.5.2 Release Gate",
            "",
            "## Purpose",
            "",
            "Validate that v0.5.0, v0.5.1 and v0.5.2 provider-smoke infrastructure is internally consistent, safe and ready for explicit real-provider diagnostic execution.",
            "",
            "This gate does not execute real providers and does not authorize benchmark results.",
            "",
            "## Dataset",
            "",
            f"- Dataset hash: `{summary['dataset_hash']}`",
            f"- Manifest hash: `{summary['manifest_hash']}`",
            f"- Frozen task count: {summary['frozen_task_count']}",
            "",
            "## Safety",
            "",
            f"- Real providers executed: `{summary['real_providers_executed']}`",
            f"- `.env` files read: `{summary['env_files_read']}`",
            f"- Secrets found: `{summary['secrets_found']}`",
            "- Diagnostic-only: `true`",
            "- No statistical claim is authorized.",
            "- No provider superiority claim is authorized.",
            "- No Xendris superiority claim is authorized.",
            "",
            "## Findings",
            "",
            *finding_lines,
            "",
            "## Final Decision",
            "",
            "```txt",
            summary["decision"],
            "```",
            "",
        ]
    )


def write_release_gate_artifacts(config: ReleaseGateConfig = ReleaseGateConfig()) -> dict[str, Any]:
    summary = evaluate_release_gate(config)
    outdir = config.resolve(config.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "release_gate_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (outdir / "release_gate_report.md").write_text(build_release_gate_report(summary), encoding="utf-8")
    findings_text = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in summary["findings"])
    (outdir / "release_gate_findings.jsonl").write_text(findings_text + ("\n" if findings_text else ""), encoding="utf-8")
    return summary
