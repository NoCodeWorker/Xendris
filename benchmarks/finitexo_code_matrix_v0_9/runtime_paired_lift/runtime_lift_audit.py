"""Deterministic runtime audit engine for v0.9.0."""

from __future__ import annotations

import re
from typing import Any

from .runtime_lift_types import (
    AUDIT_COMPONENTS,
    RuntimeAuditDecision,
    RuntimeAuditResult,
)


SECRET_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9]{20,}", re.IGNORECASE),
    re.compile(r"Bearer\s+\S{20,}", re.IGNORECASE),
    re.compile(r"api[-_]?key[=:]\s*\S{10,}", re.IGNORECASE),
    re.compile(r"Authorization:\s*\S{10,}", re.IGNORECASE),
]

CONTRADICTION_PATTERNS = [
    re.compile(r"\b(no|not|don't|cannot|can't)\b.{0,80}\b(yes|can|will|do)\b", re.IGNORECASE),
]

FALSE_SUCCESS_SIGNALS = [
    "task complete",
    "successfully implemented",
    "fully working",
    "all tests pass",
    "done and tested",
    "works perfectly",
]

LIMITATION_SIGNALS = [
    "limitation",
    "note",
    "caveat",
    "disclaimer",
    "not guaranteed",
    "may not",
    "depending on",
    "assumption",
    "edge case",
    "not fully tested",
    "requires verification",
]


def run_audit(response_text: str, task: dict[str, Any] | None = None) -> RuntimeAuditResult:
    component_scores: dict[str, float] = {}
    reasons: list[str] = []
    blocked_claims: list[str] = []
    repair_reasons: list[str] = []
    text = response_text or ""
    normalized = " ".join(text.split())

    # response_present
    if text.strip():
        component_scores["response_present"] = 1.0
    else:
        component_scores["response_present"] = 0.0
        reasons.append("no response text")
        return RuntimeAuditResult(
            decision=RuntimeAuditDecision.BLOCK,
            score=0.0,
            reasons=reasons,
            component_scores=component_scores,
            blocked_claims=["empty response"],
            is_repairable=False,
        )

    # follows_task_format
    if task and "format" in task.get("constraints", []):
        format_hints = [c for c in task.get("constraints", []) if isinstance(c, str) and "format" in c.lower()]
        format_ok = any(hint.lower().replace("format", "").strip() in normalized.lower() for hint in format_hints) if format_hints else True
    else:
        format_ok = True
    component_scores["follows_task_format"] = 1.0 if format_ok else 0.0
    if not format_ok:
        reasons.append("does not follow required task format")
        repair_reasons.append("missing format")

    # preserves_api_contract_claim
    api_ok = True
    if task and "public_contract" in task:
        contract_hints = task["public_contract"]
        if isinstance(contract_hints, str) and contract_hints not in normalized and len(contract_hints) > 10:
            api_ok = False
        elif isinstance(contract_hints, list):
            api_ok = any(hint in normalized for hint in contract_hints)
    component_scores["preserves_api_contract_claim"] = 1.0 if api_ok else 0.0
    if not api_ok:
        reasons.append("API contract not preserved")
        repair_reasons.append("API contract ambiguity")

    # task_completion_signal
    has_completion = bool(re.search(r"(return|result|output|response|answer)", normalized, re.IGNORECASE))
    component_scores["task_completion_signal"] = 1.0 if has_completion else 0.0
    if not has_completion:
        reasons.append("no task completion signal")
        repair_reasons.append("incomplete answer")

    # no_false_success_claim
    false_success = any(s in normalized.lower() for s in FALSE_SUCCESS_SIGNALS)
    component_scores["no_false_success_claim"] = 0.0 if false_success else 1.0
    if false_success:
        reasons.append("false success claim detected")
        blocked_claims.append("unsupported success claim")
        repair_reasons.append("unsupported success claim that cannot be corrected safely")

    # mentions_limitations_when_needed
    mentions_limitations = any(s in normalized.lower() for s in LIMITATION_SIGNALS)
    task_complex = task and len(task.get("prompt", "")) > 200
    if task_complex and not mentions_limitations:
        component_scores["mentions_limitations_when_needed"] = 0.5
    else:
        component_scores["mentions_limitations_when_needed"] = 1.0 if mentions_limitations else 0.0
    if task_complex and not mentions_limitations:
        reasons.append("missing limitations for complex task")
        repair_reasons.append("missing limitations")

    # deterministic_structure
    has_structure = bool(re.search(r"(1\.|\- |\* |\n\n)", normalized))
    component_scores["deterministic_structure"] = 1.0 if has_structure else 0.0
    if not has_structure:
        reasons.append("lacks deterministic structure")
        repair_reasons.append("unclear deterministic structure")

    # no_runtime_error
    error_signals = ["internal error", "runtime error", "exception occurred", "traceback", "could not process"]
    has_error = any(s in normalized.lower() for s in error_signals)
    component_scores["no_runtime_error"] = 0.0 if has_error else 1.0
    if has_error:
        reasons.append("runtime error detected")
        blocked_claims.append("runtime error")

    # security_clean
    has_security_issue = bool(re.search(r"(password|secret|credential|certificate|private.key)", normalized, re.IGNORECASE))
    component_scores["security_clean"] = 0.0 if has_security_issue else 1.0
    if has_security_issue:
        reasons.append("potential security issue")
        blocked_claims.append("security risk")

    # no_secret_exposure
    secret_exposed = any(p.search(text) for p in SECRET_PATTERNS)
    component_scores["no_secret_exposure"] = 0.0 if secret_exposed else 1.0
    if secret_exposed:
        reasons.append("secret/key exposure detected")
        blocked_claims.append("secret exposure")
        repair_reasons.append("secrets exposure")

    # minimal_unnecessary_verbosity
    word_count = len(normalized.split())
    verbosity_ok = word_count <= 500
    component_scores["minimal_unnecessary_verbosity"] = 1.0 if verbosity_ok else 0.0
    if not verbosity_ok:
        reasons.append("excessive verbosity")
        repair_reasons.append("excessive verbosity")

    # actionable_answer
    has_action = bool(re.search(r"(fix|implement|create|write|return|use|apply|call|define|set|configure)", normalized, re.IGNORECASE))
    component_scores["actionable_answer"] = 1.0 if has_action else 0.0
    if not has_action:
        reasons.append("not actionable")
        repair_reasons.append("weak actionable answer")

    # Repair policy: only repairable if the failure is:
    # - missing format, incomplete answer, weak actionable answer, missing limitations,
    #   API contract ambiguity, excessive verbosity, unclear deterministic structure
    UNREPAIRABLE_REASONS = {"secrets exposure", "security risk", "empty response", "runtime error", "unsupported success claim that cannot be corrected safely"}
    has_unrepairable = any(r in UNREPAIRABLE_REASONS for r in repair_reasons)
    is_repairable = len(repair_reasons) > 0 and not has_unrepairable

    # Decision
    score = sum(component_scores.values()) / len(component_scores) if component_scores else 0.0

    if secret_exposed or has_error or has_security_issue or false_success:
        decision = RuntimeAuditDecision.BLOCK
    elif not has_completion or not text.strip():
        decision = RuntimeAuditDecision.BLOCK
    elif is_repairable and score < 0.7:
        decision = RuntimeAuditDecision.REPAIR_REQUIRED
    elif score < 0.5:
        decision = RuntimeAuditDecision.BLOCK
    elif not mentions_limitations and task_complex:
        decision = RuntimeAuditDecision.ALLOW_WITH_LIMITATIONS
    elif score >= 0.8:
        decision = RuntimeAuditDecision.ALLOW
    elif 0.5 <= score < 0.8:
        decision = RuntimeAuditDecision.ALLOW_WITH_LIMITATIONS
    else:
        decision = RuntimeAuditDecision.ALLOW

    return RuntimeAuditResult(
        decision=decision,
        score=round(score, 4),
        reasons=reasons,
        blocked_claims=blocked_claims,
        repair_reasons=repair_reasons,
        component_scores=component_scores,
        is_repairable=is_repairable,
    )


def build_repair_prompt(
    task_prompt: str,
    initial_response: str,
    audit_result: RuntimeAuditResult,
) -> str:
    repair_instructions = (
        "The previous response has the following issues that need repair:\n"
    )
    for reason in audit_result.repair_reasons:
        repair_instructions += f"- {reason}\n"

    if audit_result.reasons:
        repair_instructions += "\nFull audit reasons:\n"
        for r in audit_result.reasons:
            repair_instructions += f"- {r}\n"

    repair_instructions += (
        "\nPlease provide a corrected response that:\n"
        "- Addresses each issue listed above\n"
        "- Preserves the API contract\n"
        "- Is deterministic and structured\n"
        "- Includes limitations when relevant\n"
        "- Is actionable and complete\n"
    )

    return task_prompt + "\n\n" + repair_instructions
