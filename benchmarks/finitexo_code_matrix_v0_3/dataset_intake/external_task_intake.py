"""CLI and pure helpers for Finitexo Code Matrix v0.3.1 intake."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .intake_report_builder import build_intake_report
from .intake_validation import apply_candidate_pool_checks, validate_candidate
from .source_registry import validate_source_registry

BENCHMARK_DIR = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = BENCHMARK_DIR / "external_sources" / "source_registry.json"
DEFAULT_CANDIDATES = BENCHMARK_DIR / "tasks_external_candidates"


def load_source_registry(path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_candidate_tasks(path: Path = DEFAULT_CANDIDATES) -> list[dict[str, Any]]:
    return [
        json.loads(candidate_path.read_text(encoding="utf-8"))
        for candidate_path in sorted(path.glob("candidate_task_*.json"))
    ]


def validate_candidate_task(candidate: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    return validate_candidate(candidate, registry)


def summarize_intake(
    decisions: list[dict[str, Any]],
    registry_issues: list[str] | None = None,
    *,
    phase: str = "v0.3.1",
) -> dict[str, Any]:
    registry_issues = registry_issues or []
    accepted_count = sum(1 for item in decisions if item["intake_decision"] == "ACCEPTED")
    warnings_count = sum(1 for item in decisions if item["intake_decision"] == "WARNINGS_PRESENT")
    rejected_count = sum(1 for item in decisions if item["intake_decision"] == "REJECTED")
    origin_distribution = Counter(item["origin"] for item in decisions)
    mean_score = round(
        sum(float(item["externality_score"]) for item in decisions) / len(decisions),
        6,
    ) if decisions else 0.0
    if registry_issues or rejected_count:
        intake_decision = "REJECTED"
    elif warnings_count:
        intake_decision = "WARNINGS_PRESENT"
    else:
        intake_decision = "ACCEPTED"
    new_decisions = [item for item in decisions if str(item.get("task_id", "")).startswith("fcm_v0_3_2_")]
    new_mean = round(
        sum(float(item["externality_score"]) for item in new_decisions) / len(new_decisions),
        6,
    ) if new_decisions else 0.0
    target_mean = 0.60
    summary = {
        "benchmark_version": phase,
        "intake_run_id": datetime.now(timezone.utc).strftime(
            f"fcm-{phase.replace('.', '-')}-intake-%Y%m%dT%H%M%SZ"
        ),
        "candidate_count": len(decisions),
        "new_candidate_count": len(new_decisions),
        "accepted_count": accepted_count,
        "warnings_count": warnings_count,
        "rejected_count": rejected_count,
        "origin_distribution": dict(sorted(origin_distribution.items())),
        "mean_externality_score": mean_score,
        "mean_externality_score_new_candidates": new_mean,
        "target_mean_externality_score": target_mean,
        "target_met": new_mean >= target_mean if new_decisions else False,
        "new_external_adapted_count": sum(1 for item in new_decisions if item["origin"] == "EXTERNAL_ADAPTED"),
        "intake_decision": intake_decision,
        "claims_authorized": [],
        "providers_executed": False,
        "candidate_pool_modifies_seed_dataset": False,
        "source_registry_issues": registry_issues,
        "decisions": decisions,
    }
    if phase == "v0.3.2" and summary["target_met"] and summary["new_external_adapted_count"] >= 3 and intake_decision != "REJECTED":
        summary["phase_decision"] = "EXTERNAL_ADAPTED_TARGET_MET"
    elif phase == "v0.3.2" and summary["new_external_adapted_count"] > 0 and intake_decision != "REJECTED":
        summary["phase_decision"] = "EXTERNAL_ADAPTED_TARGET_PARTIALLY_MET"
    elif phase == "v0.3.2":
        summary["phase_decision"] = "IMPLEMENTED_SEMI_EXTERNAL_ONLY"
    else:
        summary["phase_decision"] = "IMPLEMENTED_SEMI_EXTERNAL_INTAKE_ONLY"
    return summary


def build_external_adapted_summary(summary: dict[str, Any]) -> dict[str, Any]:
    decisions = summary["decisions"]
    new_decisions = [item for item in decisions if str(item.get("task_id", "")).startswith("fcm_v0_3_2_")]
    return {
        "benchmark_version": "v0.3.2",
        "candidate_count_total": len(decisions),
        "new_candidate_count": len(new_decisions),
        "external_adapted_count": sum(1 for item in new_decisions if item["origin"] == "EXTERNAL_ADAPTED"),
        "mutated_fixture_count": sum(1 for item in new_decisions if item["origin"] == "MUTATED_FIXTURE"),
        "semi_external_synthetic_count": sum(1 for item in new_decisions if item["origin"] == "SEMI_EXTERNAL_SYNTHETIC"),
        "accepted_count": sum(1 for item in new_decisions if item["intake_decision"] == "ACCEPTED"),
        "warnings_count": sum(1 for item in new_decisions if item["intake_decision"] == "WARNINGS_PRESENT"),
        "rejected_count": sum(1 for item in new_decisions if item["intake_decision"] == "REJECTED"),
        "mean_externality_score_all_candidates": summary["mean_externality_score"],
        "mean_externality_score_new_candidates": summary["mean_externality_score_new_candidates"],
        "target_mean_externality_score": summary["target_mean_externality_score"],
        "target_met": summary["target_met"],
        "providers_executed": False,
        "claims_authorized": [],
        "phase_decision": summary["phase_decision"],
    }


def write_intake_artifacts(summary: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "intake_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "intake_report.md").write_text(
        build_intake_report(summary),
        encoding="utf-8",
    )
    if summary.get("benchmark_version") == "v0.3.2":
        (output_dir / "external_adapted_summary.json").write_text(
            json.dumps(build_external_adapted_summary(summary), indent=2, sort_keys=True),
            encoding="utf-8",
        )


def run_intake(output_dir: Path, *, phase: str = "v0.3.1") -> dict[str, Any]:
    registry = load_source_registry()
    candidates = load_candidate_tasks()
    registry_issues = validate_source_registry(registry)
    decisions = apply_candidate_pool_checks([validate_candidate_task(candidate, registry) for candidate in candidates])
    summary = summarize_intake(decisions, registry_issues, phase=phase)
    write_intake_artifacts(summary, output_dir)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="runs/finitexo_code_matrix_v0_3_1_intake")
    parser.add_argument("--phase", choices=["v0.3.1", "v0.3.2"], default="v0.3.1")
    args = parser.parse_args()
    summary = run_intake(Path(args.output_dir), phase=args.phase)
    return 1 if summary["intake_decision"] == "REJECTED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
