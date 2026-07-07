from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


PASS = "PASS"
WARNINGS_PRESENT = "WARNINGS_PRESENT"
BLOCKED = "BLOCKED"

LEAKAGE_PATTERNS = (
    "expected answer",
    "copy this solution",
    "xendris-only",
    "xendris must win",
)


@dataclass(frozen=True)
class AntiAdHocAssessment:
    anti_ad_hoc_decision: str
    warnings: tuple[str, ...]
    blocking_issues: tuple[str, ...]

    @property
    def has_blockers(self) -> bool:
        return bool(self.blocking_issues)

    def to_dict(self) -> dict[str, Any]:
        return {
            "anti_ad_hoc_decision": self.anti_ad_hoc_decision,
            "warnings": list(self.warnings),
            "blocking_issues": list(self.blocking_issues),
        }


def canonical_json_bytes(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def task_hash(task: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(task)).hexdigest()


def load_tasks(tasks_dir: str | Path) -> list[dict[str, Any]]:
    paths = sorted(Path(tasks_dir).glob("task_*.json"))
    tasks: list[dict[str, Any]] = []
    for path in paths:
        tasks.append(json.loads(path.read_text(encoding="utf-8")))
    return tasks


def task_hashes(tasks: list[Mapping[str, Any]]) -> dict[str, str]:
    return {str(task["task_id"]): task_hash(task) for task in tasks}


def dataset_hash_from_task_hashes(hashes: Mapping[str, str]) -> str:
    payload = {"task_hashes": dict(sorted(hashes.items()))}
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def load_manifest(root: str | Path) -> dict[str, Any]:
    return json.loads((Path(root) / "dataset_manifest.json").read_text(encoding="utf-8"))


def validate_dataset_manifest(root: str | Path) -> AntiAdHocAssessment:
    root_path = Path(root)
    manifest = load_manifest(root_path)
    tasks = load_tasks(root_path / "tasks")
    warnings: list[str] = []
    blockers: list[str] = []

    if not manifest.get("frozen"):
        blockers.append("dataset_not_frozen")

    expected_size = manifest.get("dataset_size")
    if expected_size != len(tasks):
        blockers.append(f"dataset_size_mismatch:{expected_size}!={len(tasks)}")

    current_task_hashes = task_hashes(tasks)
    if manifest.get("task_hashes") != current_task_hashes:
        blockers.append("task_hashes_mismatch")

    current_dataset_hash = dataset_hash_from_task_hashes(current_task_hashes)
    if manifest.get("dataset_hash") != current_dataset_hash:
        blockers.append("dataset_hash_mismatch")

    scoring_path = root_path / "scoring_contract.md"
    if manifest.get("scoring_contract_hash") != sha256_file(scoring_path):
        blockers.append("scoring_contract_hash_mismatch")

    for task in tasks:
        prompt = str(task.get("prompt", "")).lower()
        notes = str(task.get("anti_ad_hoc_notes", "")).lower()
        combined = f"{prompt}\n{notes}"
        if any(pattern in combined for pattern in LEAKAGE_PATTERNS):
            blockers.append(f"answer_or_xendris_leakage:{task.get('task_id')}")
        if re.search(r"\b(superior|production-ready|guaranteed)\b", combined):
            warnings.append(f"overclaiming_language:{task.get('task_id')}")

    decision = BLOCKED if blockers else WARNINGS_PRESENT if warnings else PASS
    return AntiAdHocAssessment(
        anti_ad_hoc_decision=decision,
        warnings=tuple(warnings),
        blocking_issues=tuple(blockers),
    )


def assess_run_interpretation(
    *,
    sample_count: int,
    report_text: str = "",
    manifest_assessment: AntiAdHocAssessment,
) -> AntiAdHocAssessment:
    warnings = list(manifest_assessment.warnings)
    blockers = list(manifest_assessment.blocking_issues)
    lower_report = report_text.lower()

    if sample_count < 20:
        warnings.append("sample_count_below_20_budget_validation_only")
        if any(term in lower_report for term in ("superior", "production-ready", "generalizes")):
            blockers.append("small_n_overclaim")

    decision = BLOCKED if blockers else WARNINGS_PRESENT if warnings else PASS
    return AntiAdHocAssessment(
        anti_ad_hoc_decision=decision,
        warnings=tuple(dict.fromkeys(warnings)),
        blocking_issues=tuple(dict.fromkeys(blockers)),
    )
