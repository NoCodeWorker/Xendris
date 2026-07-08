from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def _try_read_json(path: Path) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _try_read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def load_run_artifacts(run_dir: Path) -> dict[str, Any]:
    artifacts: dict[str, Any] = {}

    artifacts["summary"] = _try_read_json(run_dir / "summary.json")
    artifacts["gate"] = _try_read_json(run_dir / "gate.json")
    artifacts["evidence_integrity"] = _try_read_json(run_dir / "evidence_integrity.json")
    artifacts["costs"] = _try_read_json(run_dir / "costs.json")
    artifacts["paired_lift"] = _try_read_json(run_dir / "paired_lift.json")
    artifacts["family_lift"] = _try_read_json(run_dir / "family_lift.json")

    artifacts["responses"] = _try_read_jsonl(run_dir / "responses.jsonl")
    artifacts["scores"] = _try_read_jsonl(run_dir / "scores.jsonl")
    artifacts["metadata"] = _try_read_jsonl(run_dir / "metadata.jsonl")
    artifacts["runtime_traces"] = _try_read_jsonl(run_dir / "runtime_traces.jsonl")
    artifacts["audit_decisions"] = _try_read_jsonl(run_dir / "audit_decisions.jsonl")
    artifacts["repair_attempts"] = _try_read_jsonl(run_dir / "repair_attempts.jsonl")
    artifacts["calibration_traces"] = _try_read_jsonl(run_dir / "calibration_traces.jsonl")
    artifacts["claim_status"] = _try_read_jsonl(run_dir / "claim_status.jsonl")
    artifacts["confidence_bands"] = _try_read_jsonl(run_dir / "confidence_bands.jsonl")
    artifacts["allowed_blocked_language"] = _try_read_jsonl(run_dir / "allowed_blocked_language.jsonl")
    artifacts["calibrated_final_responses"] = _try_read_jsonl(run_dir / "calibrated_final_responses.jsonl")
    artifacts["errors"] = _try_read_jsonl(run_dir / "errors.jsonl")

    return artifacts
