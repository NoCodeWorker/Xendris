"""Deterministic admissibility gate for real-provider diagnostic reports.

The gate is offline. It reads local run/report artifacts and rejects language
that promotes diagnostic evidence into statistical, provider-superiority,
Xendris-superiority, production-readiness, or universal benchmark claims.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


APPROVED = "REAL_PROVIDER_REPORT_ADMISSIBILITY_APPROVED_DIAGNOSTIC_ONLY"
BLOCKED = "REAL_PROVIDER_REPORT_ADMISSIBILITY_BLOCKED"
NEGATION_WINDOW = 180
TEXT_SUFFIXES = {".json", ".jsonl", ".md", ".txt"}


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    path: str
    excerpt: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "severity": self.severity,
            "path": self.path,
            "excerpt": self.excerpt,
            "message": self.message,
        }


@dataclass(frozen=True)
class ReportAdmissibilityConfig:
    input_paths: tuple[Path, ...] = (
        Path("runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized"),
        Path("runs/finitexo_code_matrix_v0_5_5_real_provider_evidence_integrity_gate"),
        Path("runs/finitexo_code_matrix_v0_5_6_real_provider_scoring_consistency_gate"),
    )
    optional_paths: tuple[Path, ...] = (
        Path("docs/status/FINITEXO_CODE_MATRIX_V0_5_4_REAL_PROVIDER_DIAGNOSTIC_AUTHORIZED.md"),
        Path("docs/status/FINITEXO_CODE_MATRIX_V0_5_5_REAL_PROVIDER_EVIDENCE_INTEGRITY_GATE.md"),
        Path("docs/status/FINITEXO_CODE_MATRIX_V0_5_6_REAL_PROVIDER_SCORING_CONSISTENCY_GATE.md"),
    )
    output_dir: Path = Path("runs/finitexo_code_matrix_v0_5_7_real_provider_report_admissibility_gate")


CLAIM_PATTERNS: dict[str, tuple[str, ...]] = {
    "statistical_overclaim": (
        "statistically significant",
        "significant result",
        "conclusive benchmark",
        "statistically proven",
        "statistically validated",
        "p-value",
        "confidence interval proves",
        "generalizes",
        "representative benchmark",
        "definitive benchmark",
    ),
    "provider_superiority_overclaim": (
        "deepseek is better than openai",
        "openai is better than deepseek",
        "provider superiority",
        "beats provider",
        "outperforms provider",
        "wins against provider",
        "superior provider",
        "provider winner",
    ),
    "xendris_superiority_overclaim": (
        "xendris is superior",
        "xendris beats",
        "xendris outperforms",
        "xendris wins",
        "xendris validated as better",
        "xendris superiority",
        "proves xendris",
    ),
    "production_readiness_overclaim": (
        "production ready",
        "production validated",
        "enterprise ready",
        "real-world superiority",
        "deployment approved",
    ),
    "universal_benchmark_overclaim": (
        "universal programming benchmark",
        "proves general programming ability",
        "general model quality",
        "universal superiority",
    ),
}

NEGATORS = (
    "no",
    "not",
    "never",
    "without",
    "does not",
    "do not",
    "non-authorized",
    "not authorized",
    "no claim",
    "claim not authorized",
    "not statistically conclusive",
    "diagnostic-only",
    "diagnostic only",
    "not approved",
    "false",
    "unauthorized",
    "blocked claim",
    "blocked claims",
    "forbidden",
    "must not",
)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _read_artifact(path: Path) -> str:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return json.dumps(data, ensure_ascii=False, sort_keys=True)
    return path.read_text(encoding="utf-8")


def _iter_artifact_files(paths: tuple[Path, ...]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
        elif path.is_dir():
            files.extend(
                sorted(
                    child
                    for child in path.rglob("*")
                    if child.is_file() and child.suffix.lower() in TEXT_SUFFIXES
                )
            )
    return sorted(files)


def _is_negated(normalized: str, start: int, end: int) -> bool:
    window_start = max(0, start - NEGATION_WINDOW)
    window_end = min(len(normalized), end + NEGATION_WINDOW)
    window = normalized[window_start:window_end]
    if any(negator in window for negator in NEGATORS):
        return True
    prefix = normalized[max(0, start - 600):start]
    return "does not:" in prefix or "do not:" in prefix or "must not:" in prefix


def _excerpt(original: str, normalized: str, start: int, end: int) -> str:
    # The normalized and original strings differ in whitespace/case, so use the
    # normalized excerpt for deterministic diagnostics.
    excerpt_start = max(0, start - 80)
    excerpt_end = min(len(normalized), end + 80)
    return normalized[excerpt_start:excerpt_end]


def _scan_text(path: Path, text: str) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    negated_allowed = 0
    normalized = _normalize(text)
    for code, patterns in CLAIM_PATTERNS.items():
        for phrase in patterns:
            search_at = 0
            while True:
                start = normalized.find(phrase, search_at)
                if start == -1:
                    break
                end = start + len(phrase)
                if _is_negated(normalized, start, end):
                    negated_allowed += 1
                else:
                    findings.append(
                        Finding(
                            code=code,
                            severity="BLOCKER",
                            path=str(path),
                            excerpt=_excerpt(text, normalized, start, end),
                            message=f"Unauthorized diagnostic-report claim detected: {phrase}",
                        )
                    )
                search_at = end
    return findings, negated_allowed


def _claim_flags(findings: list[Finding]) -> dict[str, bool]:
    return {
        "statistical_claim_authorized": any(f.code == "statistical_overclaim" for f in findings),
        "provider_superiority_claim_authorized": any(f.code == "provider_superiority_overclaim" for f in findings),
        "xendris_superiority_claim_authorized": any(f.code == "xendris_superiority_overclaim" for f in findings),
        "production_readiness_claim_authorized": any(f.code == "production_readiness_overclaim" for f in findings),
        "universal_benchmark_claim_authorized": any(f.code == "universal_benchmark_overclaim" for f in findings),
    }


def evaluate_report_admissibility(
    config: ReportAdmissibilityConfig = ReportAdmissibilityConfig(),
) -> dict[str, Any]:
    findings: list[Finding] = []
    negated_claims_allowed = 0
    missing_optional_artifacts = [
        str(path) for path in config.optional_paths if not path.exists()
    ]
    artifacts = _iter_artifact_files(config.input_paths + config.optional_paths)

    for path in artifacts:
        try:
            text = _read_artifact(path)
        except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            findings.append(
                Finding(
                    code="artifact_read_failure",
                    severity="BLOCKER",
                    path=str(path),
                    excerpt="",
                    message=f"Could not inspect artifact: {exc}",
                )
            )
            continue
        artifact_findings, artifact_negated = _scan_text(path, text)
        findings.extend(artifact_findings)
        negated_claims_allowed += artifact_negated

    finding_dicts = [finding.to_dict() for finding in findings]
    claim_flags = _claim_flags(findings)
    return {
        "gate": "finitexo_code_matrix_v0_5_7_real_provider_report_admissibility",
        "final_decision": APPROVED if not findings else BLOCKED,
        "diagnostic_only": True,
        "findings": finding_dicts,
        "findings_count": len(findings),
        "artifacts_inspected": len(artifacts),
        "artifacts_inspected_paths": [str(path) for path in artifacts],
        "forbidden_claims_detected": len(findings),
        "negated_claims_allowed": negated_claims_allowed,
        "missing_optional_artifacts": missing_optional_artifacts,
        **claim_flags,
        "strongest_allowed_interpretation": "diagnostic_only",
        "ready_for_v0_6_0_controlled_run": not findings,
    }


def build_report_admissibility_report(summary: dict[str, Any]) -> str:
    findings = summary["findings"] or [
        {"code": "none", "severity": "NOTE", "path": "", "excerpt": "", "message": "No findings."}
    ]
    finding_lines = [
        f"| `{finding['code']}` | `{finding['severity']}` | `{finding['path']}` | {finding['message']} |"
        for finding in findings
    ]
    missing = summary["missing_optional_artifacts"] or ["None"]
    missing_lines = [f"- `{path}`" for path in missing]
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.5.7 - Real Provider Report Admissibility Gate",
            "",
            "## Purpose",
            "",
            "Validate that real-provider diagnostic reports and summaries remain diagnostic-only and do not overstate authorized evidence.",
            "",
            "## Inputs Inspected",
            "",
            f"- Artifacts inspected: {summary['artifacts_inspected']}",
            "- v0.5.4 real-provider diagnostic run artifacts",
            "- v0.5.5 evidence integrity gate artifacts",
            "- v0.5.6 scoring consistency gate artifacts",
            "- related status documents when present",
            "",
            "## Claim Admissibility Policy",
            "",
            "Only diagnostic-only interpretation is allowed. The gate rejects unnegated statistical, provider-superiority, Xendris-superiority, production-readiness, and universal benchmark claims.",
            "",
            "## Allowed Diagnostic Language",
            "",
            "- diagnostic",
            "- diagnostic-only",
            "- controlled diagnostic",
            "- not statistically conclusive",
            "- no superiority claim authorized",
            "",
            "## Forbidden Overclaim Classes",
            "",
            "- statistical overclaims",
            "- provider superiority overclaims",
            "- Xendris superiority overclaims",
            "- production-readiness overclaims",
            "- universal benchmark overclaims",
            "",
            "## Findings",
            "",
            "| Code | Severity | Path | Message |",
            "|---|---|---|---|",
            *finding_lines,
            "",
            "## Missing Optional Artifacts",
            "",
            *missing_lines,
            "",
            "## Explicit Non-Authorization",
            "",
            "- No statistical claim is authorized.",
            "- No provider superiority claim is authorized.",
            "- No Xendris superiority claim is authorized.",
            "- No production readiness claim is authorized.",
            "- No universal benchmark claim is authorized.",
            "",
            "## Relation to v0.5.5 and v0.5.6",
            "",
            "v0.5.5 validates traceability. v0.5.6 validates score consistency. v0.5.7 validates report-language admissibility.",
            "",
            "## Next Recommended Phase",
            "",
            "v0.6.0 Real Provider Controlled Run n=30.",
            "",
            "## Final Decision",
            "",
            "```txt",
            summary["final_decision"],
            "```",
            "",
        ]
    )


def write_report_admissibility_artifacts(
    config: ReportAdmissibilityConfig = ReportAdmissibilityConfig(),
) -> dict[str, Any]:
    summary = evaluate_report_admissibility(config)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    (config.output_dir / "report_admissibility_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (config.output_dir / "report_admissibility_report.md").write_text(
        build_report_admissibility_report(summary),
        encoding="utf-8",
    )
    return summary
