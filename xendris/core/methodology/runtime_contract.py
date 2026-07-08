"""Runtime contract constants for Xendris foundational methodology."""

from __future__ import annotations

from .methodology_types import ExecutionMethod

RUNTIME_CONTRACT_FINAL_DECISION = "FOUNDATIONAL_RUNTIME_CONTRACT_ESTABLISHED"

RUNTIME_REQUIRED_ARTIFACTS = [
    "runtime_traces.jsonl",
    "audit_decisions.jsonl",
    "repair_attempts.jsonl",
    "final_audits.jsonl",
]

CALIBRATED_RUNTIME_REQUIRED_ARTIFACTS = [
    "calibration_traces.jsonl",
    "claim_status.jsonl",
    "confidence_bands.jsonl",
    "allowed_blocked_language.jsonl",
    "calibrated_final_responses.jsonl",
]

FORBIDDEN_SUBSTITUTIONS = [
    "calling a prompt wrapper 'runtime'",
    "calling tone adjustment 'calibration'",
    "scoring initial response as runtime final response without audit",
    "reporting wrapper lift as runtime lift",
    "reporting calibrated runtime without calibration traces",
    "using runtime terminology in benchmark docs when runtime traces do not exist",
]


def get_methodology_doctrine_summary() -> dict[str, object]:
    return {
        "final_decision": RUNTIME_CONTRACT_FINAL_DECISION,
        "execution_methods": [m.value for m in ExecutionMethod],
        "runtime_required_artifacts": RUNTIME_REQUIRED_ARTIFACTS,
        "calibrated_runtime_required_artifacts": CALIBRATED_RUNTIME_REQUIRED_ARTIFACTS,
        "forbidden_substitutions": FORBIDDEN_SUBSTITUTIONS,
        "development_rule": (
            "Any future benchmark version touching Xendris runtime or calibrate "
            "must import and pass the methodology guard."
        ),
    }
