"""Blind scoring helpers for Finitexo Code Matrix v0.3.

The scorer intentionally rejects payloads that expose identity fields. It does
not validate broad programming ability and does not make provider calls.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Mapping

IDENTITY_FIELDS = {
    "variant",
    "provider",
    "model",
    "agent_name",
    "xendris_label",
    "baseline_label",
}

SCORING_WEIGHTS = {
    "hidden_tests_pass": 0.30,
    "visible_tests_pass": 0.15,
    "api_contract_preserved": 0.15,
    "minimal_patch": 0.10,
    "no_forbidden_files_touched": 0.10,
    "security_clean": 0.05,
    "no_false_success_claim": 0.10,
    "external_validity_integrity": 0.05,
}

MANDATORY_GATES = (
    "hidden_tests_pass",
    "api_contract_preserved",
    "no_forbidden_files_touched",
    "no_false_success_claim",
    "external_validity_integrity",
)


def _stable_hash(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _contains_identity_key(payload: Any) -> bool:
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            if key in IDENTITY_FIELDS:
                return True
            if _contains_identity_key(value):
                return True
    elif isinstance(payload, list):
        return any(_contains_identity_key(value) for value in payload)
    return False


def anonymize_submission(
    submission: Mapping[str, Any],
    *,
    salt: str = "finitexo-v0.3-blind",
) -> dict[str, Any]:
    """Remove scorer-forbidden identity fields and return map metadata.

    The anonymization map is separate from the scorer payload. The scorer should
    receive only `blind_payload`.
    """

    original = copy.deepcopy(dict(submission))
    metadata = {field: original.pop(field) for field in list(original) if field in IDENTITY_FIELDS}
    submission_id = str(submission.get("submission_id", _stable_hash(original)[:16]))
    anonymous_id = hashlib.sha256(f"{salt}:{submission_id}".encode("utf-8")).hexdigest()[:16]
    blind_payload = {
        "anonymous_submission_id": anonymous_id,
        "task_id": original.get("task_id"),
        "scoring_components": original.get("scoring_components", {}),
        "evidence_decision": original.get("evidence_decision", "UNKNOWN"),
        "limitations": original.get("limitations", []),
    }
    anonymization_map = {
        anonymous_id: {
            "submission_id": submission_id,
            "identity_metadata": metadata,
        }
    }
    return {
        "blind_payload": blind_payload,
        "anonymization_map": anonymization_map,
        "anonymization_map_hash": _stable_hash(anonymization_map),
    }


def score_anonymized_submission(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Score an anonymized submission conservatively.

    Unknown or missing mandatory values block verified success. Identity leaks
    fail blind scoring immediately.
    """

    if _contains_identity_key(payload):
        return {
            "raw_score": 0.0,
            "score": 0.0,
            "verified_success": False,
            "blind_scoring_decision": "FAILED",
            "blocking_reasons": ["identity_leak_detected"],
        }

    components = dict(payload.get("scoring_components") or {})
    raw_score = 0.0
    blocking_reasons: list[str] = []
    for name, weight in SCORING_WEIGHTS.items():
        value = components.get(name)
        if value is True:
            raw_score += weight
        elif value is None and name in MANDATORY_GATES:
            blocking_reasons.append(f"unknown_{name}")
        elif name in MANDATORY_GATES and value is not True:
            blocking_reasons.append(f"failed_{name}")

    evidence_decision = str(payload.get("evidence_decision", "UNKNOWN"))
    if evidence_decision != "INTERPRETABLE":
        blocking_reasons.append(f"evidence_{evidence_decision.lower()}")

    verified_success = (
        raw_score >= 0.85
        and evidence_decision == "INTERPRETABLE"
        and all(components.get(name) is True for name in MANDATORY_GATES)
    )
    return {
        "raw_score": round(raw_score, 6),
        "score": round(raw_score, 6),
        "verified_success": verified_success,
        "blind_scoring_decision": "PASSED",
        "blocking_reasons": [] if verified_success else blocking_reasons,
    }


def deanonymize_results(
    scored_results: list[Mapping[str, Any]],
    anonymization_map: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Join scored results with identity metadata outside the blind scorer."""

    joined: list[dict[str, Any]] = []
    for result in scored_results:
        anonymous_id = str(result.get("anonymous_submission_id", ""))
        identity = dict(anonymization_map.get(anonymous_id, {}))
        merged = dict(result)
        merged["deanonymized_metadata"] = identity
        joined.append(merged)
    return joined

