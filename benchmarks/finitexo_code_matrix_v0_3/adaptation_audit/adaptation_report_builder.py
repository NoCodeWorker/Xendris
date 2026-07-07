"""Report builder for v0.3.3 adaptation audit examples."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Iterable

from .adaptation_record import AdaptationRecord
from .adaptation_validation import evaluate_adaptation_candidate

EXAMPLE_DIR = Path(__file__).resolve().parent / "examples"


def load_adaptation_records(path: Path = EXAMPLE_DIR) -> list[AdaptationRecord]:
    return [
        AdaptationRecord.from_dict(json.loads(record_path.read_text(encoding="utf-8")))
        for record_path in sorted(path.glob("*.json"))
    ]


def build_adaptation_audit_summary(records: Iterable[AdaptationRecord]) -> dict[str, object]:
    records = list(records)
    decisions = [
        {"record": record.to_dict(), "audit_decision": evaluate_adaptation_candidate(record).to_dict()}
        for record in records
    ]
    recommendations = [item["audit_decision"]["recommendation"] for item in decisions]
    return {
        "benchmark_version": "v0.3.3",
        "total_adaptation_records": len(records),
        "recommended_for_future_freeze": recommendations.count("RECOMMEND_FOR_FUTURE_FREEZE"),
        "recommended_with_human_review": recommendations.count("RECOMMEND_WITH_HUMAN_REVIEW"),
        "do_not_promote": recommendations.count("DO_NOT_PROMOTE"),
        "blocked": recommendations.count("BLOCKED"),
        "counts_by_adaptation_type": dict(sorted(Counter(record.adaptation_type.value for record in records).items())),
        "counts_by_contamination_risk": dict(sorted(Counter(record.contamination_risk.value for record in records).items())),
        "counts_by_leakage_risk": dict(sorted(Counter(record.leakage_risk.value for record in records).items())),
        "counts_by_task_validity_status": dict(sorted(Counter(record.task_validity_status.value for record in records).items())),
        "counts_by_benchmark_fit_status": dict(sorted(Counter(record.benchmark_fit_status.value for record in records).items())),
        "providers_executed": False,
        "network_required": False,
        "env_read": False,
        "secrets_printed": False,
        "frozen_dataset_modified": False,
        "examples_are_benchmark_tasks": False,
        "claims_authorized": [],
        "final_decision": "EXTERNAL_ADAPTATION_AUDIT_IMPLEMENTED_NO_FROZEN_DATASET_CHANGE",
        "decisions": decisions,
    }


def build_adaptation_audit_report(summary: dict[str, object]) -> str:
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.3.3 - External Adaptation + Contamination Audit",
            "",
            "## Scope",
            "",
            "This report audits local fixture adaptation records. It does not execute providers, fetch network resources, or promote benchmark tasks.",
            "",
            "## Boundary",
            "",
            "acquisition_record != benchmark_task",
            "",
            "adapted_candidate != frozen_benchmark_task",
            "",
            "audit_pass != dataset_promotion",
            "",
            "## Summary",
            "",
            f"- total_adaptation_records: `{summary['total_adaptation_records']}`",
            f"- recommended_for_future_freeze: `{summary['recommended_for_future_freeze']}`",
            f"- recommended_with_human_review: `{summary['recommended_with_human_review']}`",
            f"- do_not_promote: `{summary['do_not_promote']}`",
            f"- blocked: `{summary['blocked']}`",
            "",
            "## Counts",
            "",
            f"- by adaptation type: `{summary['counts_by_adaptation_type']}`",
            f"- by contamination risk: `{summary['counts_by_contamination_risk']}`",
            f"- by leakage risk: `{summary['counts_by_leakage_risk']}`",
            f"- by task validity: `{summary['counts_by_task_validity_status']}`",
            f"- by benchmark fit: `{summary['counts_by_benchmark_fit_status']}`",
            "",
            "## Dataset Boundary",
            "",
            "The frozen v0.3 seed dataset was not modified.",
            "",
            "The examples are not benchmark tasks.",
            "",
            "## Provider Execution",
            "",
            "No providers were executed.",
            "",
            "No network access was required.",
            "",
            "No `.env` file was read.",
            "",
            "No secrets were printed.",
            "",
            "## Claims",
            "",
            "No external superiority claim is authorized.",
            "",
            "## Final Decision",
            "",
            f"`{summary['final_decision']}`",
            "",
        ]
    )


def write_adaptation_audit_artifacts(output_dir: Path, records: list[AdaptationRecord] | None = None) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = build_adaptation_audit_summary(records if records is not None else load_adaptation_records())
    (output_dir / "adaptation_audit_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "adaptation_audit_report.md").write_text(
        build_adaptation_audit_report(summary),
        encoding="utf-8",
    )
    return summary


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="runs/finitexo_code_matrix_v0_3_3_adaptation_audit")
    args = parser.parse_args()
    write_adaptation_audit_artifacts(Path(args.output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

