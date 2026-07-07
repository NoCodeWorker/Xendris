"""Evidence contract for Finitexo Code Matrix v0.3 submissions."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

FORBIDDEN_BLIND_FIELDS = {
    "variant",
    "provider",
    "model",
    "agent_name",
    "xendris_label",
    "baseline_label",
}


def create_evidence_contract(
    *,
    run_id: str,
    task_id: str,
    submission_id: str,
    dataset_hash: str,
    task_hash: str,
    scoring_contract_hash: str,
    anonymization_map_hash: str,
    origin: str,
    raw_output_path: str,
    patch_path: str,
    score_result_path: str,
    evidence_decision: str = "INTERPRETABLE",
    limitations: list[str] | None = None,
    blind_payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a conservative per-submission evidence contract."""

    sanitized_blind_payload = dict(blind_payload or {})
    for field in FORBIDDEN_BLIND_FIELDS:
        sanitized_blind_payload.pop(field, None)

    return {
        "benchmark_name": "Finitexo Code Matrix",
        "benchmark_version": "0.3",
        "run_id": run_id,
        "task_id": task_id,
        "submission_id": submission_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "dataset_hash": dataset_hash,
        "task_hash": task_hash,
        "scoring_contract_hash": scoring_contract_hash,
        "blind_scoring": True,
        "anonymization_map_hash": anonymization_map_hash,
        "origin": origin,
        "raw_output_path": raw_output_path,
        "patch_path": patch_path,
        "score_result_path": score_result_path,
        "evidence_decision": evidence_decision,
        "limitations": limitations or [],
        "blind_scorer_payload": sanitized_blind_payload,
    }

