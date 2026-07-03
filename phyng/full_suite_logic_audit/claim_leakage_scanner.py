"""Claim leakage scanner for forbidden epistemic upgrades."""

from __future__ import annotations

import re
from pathlib import Path

from phyng.full_suite_logic_audit.schemas import ArtifactScanResult, AuditIssue


BLOCKING_CONTEXT = (
    "blocked",
    "blocks",
    "do not",
    "don't",
    "never",
    "forbidden",
    "prohibited",
    "not write",
    "not claim",
    "no physical claim",
    "must not",
    "claims remain blocked",
    "blocked claims",
    "blocked uses",
    "blocked=[",
    "contradicted",
    "constrained",
    "not evidence",
    "not support",
    "no:",
    "not allowed",
    "no ",
    "ningún",
    "ningun",
    "qué debe seguir bloqueado",
    "que debe seguir bloqueado",
    "excluded claims",
    "excluded_claims",
    "blocking conditions",
    "audit rule",
    "mark as blocker",
    "implying",
    "minimum tests",
    "cannot be computed",
    "remains undefined",
    "no predictivegain",
    "candidate_not_validated",
    "requires_manual_review",
    "validated=0",
    "unresolved evidence gap",
)

POSITIVE_VALIDATION_PATTERNS = [
    (re.compile(r"\bphi_gradient\b.{0,80}\b(is|was|has been)\b.{0,40}\b(validated|confirmed|proved|proven)\b", re.I), "PHI_GRADIENT_VALIDATION_CLAIM"),
    (re.compile(r"\bfrontera c\b.{0,80}\b(is|was|has been)\b.{0,40}\b(validated|confirmed|proved|proven)\b", re.I), "FRONTERA_C_VALIDATION_CLAIM"),
    (re.compile(r"\bsource pressure\b.{0,80}\b(experimental proof|physical proof|validates)\b", re.I), "SOURCE_PRESSURE_AS_PROOF"),
    (re.compile(r"\bextraction candidate\b.{0,80}\b(source support|evidence support)\b", re.I), "EXTRACTION_CANDIDATE_AS_SUPPORT"),
]


def scan_claim_leakage(root: str | Path, artifact_scan: ArtifactScanResult) -> list[AuditIssue]:
    repo_root = Path(root)
    issues: list[AuditIssue] = []
    for artifact in artifact_scan.artifacts:
        if artifact.path.startswith("tests/"):
            continue
        path = repo_root / artifact.path
        text = _read_text(path)
        if not text:
            continue
        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            context = _context_window(lines, line_number)
            if _is_blocking_context(context):
                continue
            lowered = line.lower()
            for pattern, category in POSITIVE_VALIDATION_PATTERNS:
                if pattern.search(line):
                    issues.append(_issue(category, artifact.path, line_number, line, "Remove or downgrade the unsupported validation/support claim."))
            if "predictivegain" in lowered and _positive_existence_claim(lowered) and not _mentions_ytrue_support(lowered):
                issues.append(_issue("PREDICTIVE_GAIN_WITHOUT_YTRUE", artifact.path, line_number, line, "Gate PredictiveGain behind accepted y_true and matched predictions."))
            if "gradient" in lowered and "support" in lowered and ("slot_4" in lowered or "slot4" in lowered) and "open" in lowered:
                issues.append(_issue("GRADIENT_SUPPORT_WITH_OPEN_SLOT4_DEBT", artifact.path, line_number, line, "Keep gradient support blocked while SLOT_4 debt is open."))
            if "benchmark score" in lowered and any(term in lowered for term in ("predictive truth", "predictivegain", "predictive gain")):
                issues.append(_issue("BENCHMARK_SCORE_AS_PREDICTIVE_TRUTH", artifact.path, line_number, line, "Separate benchmark scoring from predictive truth claims."))
    return issues


def detects_claim_leakage(text: str) -> list[AuditIssue]:
    temp_scan = ArtifactScanResult(artifacts=[])
    issues: list[AuditIssue] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if _is_blocking_context(line):
            continue
        lowered = line.lower()
        if "predictivegain" in lowered and _positive_existence_claim(lowered) and not _mentions_ytrue_support(lowered):
            issues.append(_issue("PREDICTIVE_GAIN_WITHOUT_YTRUE", "inline", line_number, line, "Gate PredictiveGain behind accepted y_true and matched predictions."))
        if "gradient mechanism" in lowered and "supported" in lowered and ("slot4" in lowered or "slot_4" in lowered) and "open" in lowered:
            issues.append(_issue("GRADIENT_SUPPORT_WITH_OPEN_SLOT4_DEBT", "inline", line_number, line, "Keep gradient support blocked while SLOT_4 debt is open."))
    return issues


def _issue(category: str, path: str, line_number: int, line: str, remediation: str) -> AuditIssue:
    return AuditIssue(
        issue_id=f"{category}-{abs(hash((path, line_number, line))) % 100000}",
        severity="BLOCKER",
        category=category,
        path=path,
        message=f"Unsupported positive claim detected at line {line_number}.",
        evidence=line.strip()[:300],
        remediation=remediation,
    )


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def _is_blocking_context(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in BLOCKING_CONTEXT)


def _context_window(lines: list[str], line_number: int, radius: int = 8) -> str:
    start = max(0, line_number - radius - 1)
    end = min(len(lines), line_number + radius)
    return "\n".join(lines[start:end])


def _positive_existence_claim(lowered: str) -> bool:
    return any(term in lowered for term in (" exists", " exists.", " achieved", " computed", " positive", " validated"))


def _mentions_ytrue_support(lowered: str) -> bool:
    return "y_true" in lowered and any(term in lowered for term in ("accepted", "matched", "sufficient", "provenance"))
