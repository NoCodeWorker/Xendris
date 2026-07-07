"""Report builder for the v0.3.2 source acquisition gate."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Iterable

from .acquisition_types import ContaminationRisk
from .acquisition_validation import evaluate_promotion_eligibility
from .source_acquisition_record import SourceAcquisitionRecord

EXAMPLE_RECORD_DIR = Path(__file__).resolve().parents[1] / "external_sources" / "source_acquisition_examples"


def load_acquisition_records(path: Path = EXAMPLE_RECORD_DIR) -> list[SourceAcquisitionRecord]:
    return [
        SourceAcquisitionRecord.from_dict(json.loads(record_path.read_text(encoding="utf-8")))
        for record_path in sorted(path.glob("*.json"))
    ]


def build_acquisition_summary(records: Iterable[SourceAcquisitionRecord]) -> dict[str, object]:
    records = list(records)
    decisions = [
        {"record": record.to_dict(), "promotion_decision": evaluate_promotion_eligibility(record).to_dict()}
        for record in records
    ]
    eligible = [item for item in decisions if item["promotion_decision"]["promotion_allowed"]]
    blocked = [
        item
        for item in decisions
        if item["record"]["contamination_risk"] in {ContaminationRisk.HIGH.value, ContaminationRisk.BLOCKED.value}
    ]
    rejected = [item for item in decisions if not item["promotion_decision"]["promotion_allowed"]]
    return {
        "benchmark_version": "v0.3.2",
        "total_records": len(records),
        "eligible_for_future_promotion": len(eligible),
        "rejected": len(rejected),
        "blocked": len(blocked),
        "counts_by_source_type": dict(sorted(Counter(record.source_type.value for record in records).items())),
        "counts_by_origin_candidate": dict(sorted(Counter(record.origin_candidate.value for record in records).items())),
        "counts_by_contamination_risk": dict(sorted(Counter(record.contamination_risk.value for record in records).items())),
        "providers_executed": False,
        "frozen_dataset_modified": False,
        "claims_authorized": [],
        "final_decision": "SOURCE_ACQUISITION_GATE_IMPLEMENTED_NO_DATASET_PROMOTION",
        "decisions": decisions,
    }


def build_acquisition_report(summary: dict[str, object]) -> str:
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.3.2 - External Source Acquisition Gate",
            "",
            "## Scope",
            "",
            "This report validates local fixture source-acquisition records. It does not fetch external sources, execute providers, or promote benchmark tasks.",
            "",
            "## Summary",
            "",
            f"- total_records: `{summary['total_records']}`",
            f"- eligible_for_future_promotion: `{summary['eligible_for_future_promotion']}`",
            f"- rejected: `{summary['rejected']}`",
            f"- blocked: `{summary['blocked']}`",
            "",
            "## Counts By Source Type",
            "",
            f"`{summary['counts_by_source_type']}`",
            "",
            "## Counts By Origin Candidate",
            "",
            f"`{summary['counts_by_origin_candidate']}`",
            "",
            "## Counts By Contamination Risk",
            "",
            f"`{summary['counts_by_contamination_risk']}`",
            "",
            "## Dataset Boundary",
            "",
            "Acquisition records are not benchmark tasks. Acquisition eligibility does not equal dataset promotion.",
            "",
            "The frozen v0.3 seed dataset was not modified.",
            "",
            "## Provider Execution",
            "",
            "No provider execution occurred.",
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


def write_acquisition_artifacts(output_dir: Path, records: list[SourceAcquisitionRecord] | None = None) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = build_acquisition_summary(records if records is not None else load_acquisition_records())
    (output_dir / "source_acquisition_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "source_acquisition_report.md").write_text(
        build_acquisition_report(summary),
        encoding="utf-8",
    )
    return summary


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="runs/finitexo_code_matrix_v0_3_2_source_acquisition")
    args = parser.parse_args()
    write_acquisition_artifacts(Path(args.output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

