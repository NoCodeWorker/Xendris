"""Leakage controls for adapted candidate text."""

from __future__ import annotations

from .adaptation_types import LeakageRisk

BLOCKING_TERMS = (
    "xendris",
    "finitexo code matrix",
    "benchmark gate",
    "trust gate",
    "previous benchmark run",
    "hidden_tests_pass",
    "visible_tests_pass",
    "api_contract_preserved",
    "raw_score",
    "scoring formula",
    "expected hidden tests",
)

HIGH_RISK_TERMS = (
    "deepseek",
    "openai",
    "provider-specific",
    "candidate_task_",
    "external_task_",
)


def assess_leakage(text: str) -> dict[str, object]:
    normalized = text.lower()
    flags = [term for term in BLOCKING_TERMS if term in normalized]
    high_flags = [term for term in HIGH_RISK_TERMS if term in normalized]
    if flags:
        return {"leakage_risk": LeakageRisk.BLOCKED, "flags": flags}
    if high_flags:
        return {"leakage_risk": LeakageRisk.HIGH, "flags": high_flags}
    return {"leakage_risk": LeakageRisk.LOW, "flags": []}

