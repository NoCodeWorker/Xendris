"""Deterministic scoring consistency gate for v0.5.4/v0.5.5 artifacts."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPECTED_DATASET_HASH = "a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4"
EXPECTED_MANIFEST_HASH = "6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e"
APPROVED = "REAL_PROVIDER_SCORING_CONSISTENCY_APPROVED_DIAGNOSTIC_ONLY"
BLOCKED = "REAL_PROVIDER_SCORING_CONSISTENCY_BLOCKED"
EPSILON = 1e-4


@dataclass(frozen=True)
class ScoringConsistencyConfig:
    run_dir: Path = Path("runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized")
    evidence_integrity_summary_path: Path = Path(
        "runs/finitexo_code_matrix_v0_5_5_real_provider_evidence_integrity_gate/evidence_integrity_summary.json"
    )
    output_dir: Path = Path("runs/finitexo_code_matrix_v0_5_6_real_provider_scoring_consistency_gate")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _jsonl(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return []
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def _finding(code: str, message: str, identity: str | None = None) -> dict[str, Any]:
    return {"code": code, "message": message, "identity": identity}


def _identity(row: dict[str, Any]) -> tuple[str, str]:
    provider = row.get("provider_name") or row.get("provider") or row.get("system_name")
    task_id = row.get("task_id") or row.get("sample_id") or row.get("task")
    if not provider or not task_id:
        return ("", "")
    return (str(provider), str(task_id))


def _identity_text(identity: tuple[str, str]) -> str:
    return f"{identity[0]}::{identity[1]}"


def _is_finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def _in_unit_interval(value: Any) -> bool:
    return _is_finite_number(value) and 0.0 <= float(value) <= 1.0


def _required_paths(run_dir: Path) -> dict[str, Path]:
    return {
        "summary": run_dir / "real_provider_diagnostic_summary.json",
        "responses": run_dir / "real_provider_responses.jsonl",
        "scores": run_dir / "real_provider_scores.jsonl",
        "metadata": run_dir / "provider_request_metadata.jsonl",
        "report": run_dir / "real_provider_diagnostic_report.md",
    }


def _check_formula(score: dict[str, Any], findings: list[dict[str, Any]], identity: tuple[str, str]) -> bool:
    formula = score.get("scoring_formula")
    if formula is None:
        return True
    weighted = formula.get("weighted_components")
    if not isinstance(weighted, dict) or not weighted:
        findings.append(_finding("invalid_scoring_formula", "weighted_components missing or invalid.", _identity_text(identity)))
        return False
    weights = []
    for component, weight in weighted.items():
        if not _is_finite_number(weight) or float(weight) < 0:
            findings.append(_finding("invalid_scoring_formula_weight", f"Invalid weight for {component}.", _identity_text(identity)))
            return False
        weights.append(float(weight))
    if abs(sum(weights) - 1.0) > 1e-9:
        findings.append(_finding("invalid_scoring_formula_weight_sum", "Formula weights do not sum to 1.0.", _identity_text(identity)))
        return False
    penalties = formula.get("hard_penalties", [])
    if penalties is not None and not isinstance(penalties, list):
        findings.append(_finding("invalid_hard_penalty_structure", "hard_penalties must be a list when present.", _identity_text(identity)))
        return False
    return True


def _recompute_score(score: dict[str, Any]) -> tuple[bool, float | None]:
    formula = score.get("scoring_formula")
    components = score.get("score_components")
    if isinstance(formula, dict) and isinstance(formula.get("weighted_components"), dict) and isinstance(components, dict):
        total = 0.0
        for component, weight in formula["weighted_components"].items():
            if component not in components:
                return True, None
            total += float(components[component]) * float(weight)
        return True, max(0.0, min(1.0, total))
    if isinstance(components, dict) and components:
        numeric = [float(value) for value in components.values() if _is_finite_number(value)]
        if len(numeric) != len(components):
            return True, None
        return True, sum(numeric) / len(numeric)
    return False, None


def _check_false_success(score: dict[str, Any], response: dict[str, Any] | None, findings: list[dict[str, Any]], identity: tuple[str, str]) -> bool:
    success = score.get("success") or score.get("verified_success")
    if success is True:
        for field in ("hidden_tests_pass", "visible_tests_pass", "tests_passed"):
            if score.get(field) is False:
                findings.append(_finding("false_success_contradiction", f"success=true contradicts {field}=false.", _identity_text(identity)))
                return False
    components = score.get("score_components", {})
    no_false_success = components.get("no_false_success_claim") if isinstance(components, dict) else None
    response_text = ""
    if response is not None:
        response_text = str(response.get("response_text") or response.get("normalized_response_text") or "")
    if no_false_success is False or no_false_success == 0:
        if "success" in response_text.lower() or "all tests pass" in response_text.lower():
            findings.append(_finding("false_success_text_contradiction", "no_false_success_claim is false while response implies success.", _identity_text(identity)))
            return False
    return True


def _decision(findings: list[dict[str, Any]]) -> str:
    return APPROVED if not findings else BLOCKED


def evaluate_scoring_consistency(config: ScoringConsistencyConfig = ScoringConsistencyConfig()) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    paths = _required_paths(config.run_dir)
    for path in paths.values():
        if not path.exists():
            findings.append(_finding("missing_artifact", f"Missing artifact: {path}"))
    if findings:
        return _summary(findings, {}, [], [], [], False, 0, 0, False, False, 0)

    source_summary = _load_json(paths["summary"])
    responses = _jsonl(paths["responses"])
    scores = _jsonl(paths["scores"])
    metadata = _jsonl(paths["metadata"])
    report = paths["report"].read_text(encoding="utf-8")

    if config.evidence_integrity_summary_path.exists():
        evidence = _load_json(config.evidence_integrity_summary_path)
        if evidence.get("decision") != "REAL_PROVIDER_EVIDENCE_INTEGRITY_APPROVED_DIAGNOSTIC_ONLY":
            findings.append(_finding("evidence_integrity_not_approved", "v0.5.5 evidence integrity gate is not approved."))

    dataset_hash_verified = source_summary.get("dataset_hash") == EXPECTED_DATASET_HASH
    manifest_hash_verified = source_summary.get("manifest_hash") == EXPECTED_MANIFEST_HASH
    if not dataset_hash_verified:
        findings.append(_finding("dataset_hash_mismatch", "Dataset hash mismatch."))
    if not manifest_hash_verified:
        findings.append(_finding("manifest_hash_mismatch", "Manifest hash mismatch."))

    response_ids = [_identity(row) for row in responses]
    score_ids = [_identity(row) for row in scores]
    metadata_ids = [_identity(row) for row in metadata]
    if any(identity == ("", "") for identity in score_ids):
        findings.append(_finding("missing_score_identity", "At least one score row lacks provider/task identity."))
    if len(score_ids) != len(set(score_ids)):
        findings.append(_finding("duplicate_score_identity", "Duplicate score identity rows detected."))
    if len(scores) != len(responses):
        findings.append(_finding("score_response_cardinality_mismatch", "Score row count does not match response row count."))
    if len(scores) != len(metadata):
        findings.append(_finding("score_metadata_cardinality_mismatch", "Score row count does not match metadata row count."))
    if len(scores) != 20:
        findings.append(_finding("unexpected_score_total", "Expected 20 score rows for frozen n=10 x 2 providers."))
    if set(score_ids) != set(response_ids):
        findings.append(_finding("score_response_traceability_failure", "Score identities do not match response identities."))
    if set(score_ids) != set(metadata_ids):
        findings.append(_finding("score_metadata_traceability_failure", "Score identities do not match metadata identities."))

    provider_score_counts: dict[str, int] = {}
    provider_task_ids: dict[str, set[str]] = {}
    for provider, task_id in score_ids:
        provider_score_counts[provider] = provider_score_counts.get(provider, 0) + 1
        provider_task_ids.setdefault(provider, set()).add(task_id)
    if provider_score_counts.get("deepseek") != 10 or provider_score_counts.get("openai") != 10:
        findings.append(_finding("provider_symmetry_count_failure", "Expected 10 score rows for deepseek and 10 for openai."))
    if provider_task_ids.get("deepseek", set()) != provider_task_ids.get("openai", set()):
        findings.append(_finding("provider_symmetry_task_failure", "Providers do not cover the same task IDs."))

    score_range_valid = True
    formula_valid = True
    recomputation_attempted = False
    recomputation_failures = 0
    false_success_claims_detected = 0
    response_by_id = {_identity(row): row for row in responses}
    for score in scores:
        identity = _identity(score)
        final_score = score.get("score_total")
        if not _in_unit_interval(final_score):
            score_range_valid = False
            findings.append(_finding("score_out_of_range", "score_total must be finite and within [0, 1].", _identity_text(identity)))
        components = score.get("score_components", {})
        if isinstance(components, dict):
            for name, value in components.items():
                if not _in_unit_interval(value):
                    score_range_valid = False
                    findings.append(_finding("component_score_out_of_range", f"Component {name} is outside [0, 1].", _identity_text(identity)))
        else:
            findings.append(_finding("invalid_score_components", "score_components must be an object.", _identity_text(identity)))
            score_range_valid = False
        if not _check_formula(score, findings, identity):
            formula_valid = False
        attempted, recomputed = _recompute_score(score)
        recomputation_attempted = recomputation_attempted or attempted
        if recomputed is not None and _is_finite_number(final_score):
            if abs(float(final_score) - recomputed) > EPSILON:
                recomputation_failures += 1
                findings.append(_finding("score_recomputation_mismatch", "Recorded score differs from deterministic recomputation.", _identity_text(identity)))
        if not _check_false_success(score, response_by_id.get(identity), findings, identity):
            false_success_claims_detected += 1

    report_lower = report.lower()
    forbidden = [
        "statistical claim authorized: true",
        "provider superiority claim authorized: true",
        "xendris superiority claim authorized: true",
        "production readiness claim authorized: true",
        "universal programming benchmark claim authorized: true",
    ]
    if any(text in report_lower for text in forbidden):
        findings.append(_finding("decision_exceeds_diagnostic_only", "Report authorizes a forbidden claim."))

    return _summary(
        findings,
        source_summary,
        responses,
        scores,
        metadata,
        score_range_valid,
        recomputation_failures,
        false_success_claims_detected,
        formula_valid,
        recomputation_attempted,
        provider_score_counts,
        dataset_hash_verified,
        manifest_hash_verified,
    )


def _summary(
    findings: list[dict[str, Any]],
    source_summary: dict[str, Any],
    responses: list[dict[str, Any]],
    scores: list[dict[str, Any]],
    metadata: list[dict[str, Any]],
    score_range_valid: bool,
    recomputation_failures: int,
    false_success_claims_detected: int,
    formula_valid: bool,
    recomputation_attempted: bool,
    provider_score_counts: dict[str, int] | bool = False,
    dataset_hash_verified: bool = False,
    manifest_hash_verified: bool = False,
) -> dict[str, Any]:
    if not isinstance(provider_score_counts, dict):
        provider_score_counts = {}
    providers = sorted(provider_score_counts)
    return {
        "gate": "finitexo_code_matrix_v0_5_6_real_provider_scoring_consistency",
        "final_decision": _decision(findings),
        "diagnostic_only": True,
        "findings_count": len(findings),
        "findings": findings,
        "scores_checked": len(scores),
        "responses_checked": len(responses),
        "metadata_rows_checked": len(metadata),
        "providers": providers,
        "provider_score_counts": provider_score_counts,
        "score_range_valid": score_range_valid,
        "formula_valid": formula_valid,
        "recomputation_attempted": recomputation_attempted,
        "recomputation_failures": recomputation_failures,
        "provider_symmetry_valid": not any(f["code"].startswith("provider_symmetry") for f in findings),
        "false_success_claims_detected": false_success_claims_detected,
        "statistical_claim_authorized": False,
        "provider_superiority_claim_authorized": False,
        "xendris_superiority_claim_authorized": False,
        "dataset_hash_verified": dataset_hash_verified,
        "manifest_hash_verified": manifest_hash_verified,
        "source_final_decision": source_summary.get("final_decision"),
    }


def build_scoring_consistency_report(summary: dict[str, Any]) -> str:
    findings = summary["findings"] or [{"code": "none", "message": "No findings.", "identity": None}]
    finding_lines = [
        f"| `{finding['code']}` | {finding['message']} | `{finding.get('identity')}` |"
        for finding in findings
    ]
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.5.6 - Real Provider Scoring Consistency Gate",
            "",
            "## Purpose",
            "",
            "Validate the structural consistency and admissibility of diagnostic score artifacts from v0.5.4/v0.5.5.",
            "",
            "## Inputs Inspected",
            "",
            "- `real_provider_responses.jsonl`",
            "- `real_provider_scores.jsonl`",
            "- `provider_request_metadata.jsonl`",
            "- `real_provider_diagnostic_summary.json`",
            "- v0.5.5 evidence integrity summary",
            "",
            "## Checks Performed",
            "",
            "- score cardinality and duplicate identities;",
            "- score range and component range validation;",
            "- formula structure and deterministic recomputation where possible;",
            "- explicit false-success contradictions;",
            "- provider symmetry across DeepSeek and OpenAI;",
            "- diagnostic-only decision admissibility.",
            "",
            "## Findings",
            "",
            "| Code | Message | Identity |",
            "|---|---|---|",
            *finding_lines,
            "",
            "## Non-Authorization",
            "",
            "- No statistical claim is authorized.",
            "- No provider superiority claim is authorized.",
            "- No Xendris superiority claim is authorized.",
            "- No benchmark generalization is authorized.",
            "",
            "## Relation to v0.5.5",
            "",
            "v0.5.5 validates evidence traceability. v0.5.6 validates score structure and diagnostic admissibility.",
            "",
            "## Next Recommended Phase",
            "",
            "Add an external reviewer/audit layer before any public benchmark-performance interpretation.",
            "",
            "## Final Decision",
            "",
            "```txt",
            summary["final_decision"],
            "```",
            "",
        ]
    )


def write_scoring_consistency_artifacts(config: ScoringConsistencyConfig = ScoringConsistencyConfig()) -> dict[str, Any]:
    summary = evaluate_scoring_consistency(config)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    (config.output_dir / "scoring_consistency_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (config.output_dir / "scoring_consistency_report.md").write_text(
        build_scoring_consistency_report(summary),
        encoding="utf-8",
    )
    return summary
