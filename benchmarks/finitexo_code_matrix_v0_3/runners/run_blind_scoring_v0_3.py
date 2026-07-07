"""Dry-run blind scoring runner for Finitexo Code Matrix v0.3."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_3.evaluators.blind_score_result_v0_3 import (
    anonymize_submission,
    score_anonymized_submission,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="runs/finitexo_code_matrix_v0_3_blind_scoring")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    submission = {
        "submission_id": "dry-run-001",
        "variant": "strong_non_xendris_agent",
        "task_id": "FCM-V03-001",
        "evidence_decision": "INTERPRETABLE",
        "scoring_components": {
            "hidden_tests_pass": True,
            "visible_tests_pass": True,
            "api_contract_preserved": True,
            "minimal_patch": True,
            "no_forbidden_files_touched": True,
            "security_clean": True,
            "no_false_success_claim": True,
            "external_validity_integrity": True,
        },
    }
    anonymized = anonymize_submission(submission)
    score = score_anonymized_submission(anonymized["blind_payload"])
    (output_dir / "blind_score_summary.json").write_text(
        json.dumps({"anonymized": anonymized, "score": score}, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

