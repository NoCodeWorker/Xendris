"""Permission gate for heuristic candidates."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.core.permissions import CanonicalPermission
from phyng.heuristic_discovery.schemas import (
    HeuristicCandidate,
    HeuristicPermissionGateResult,
    HeuristicStatus,
)


def heuristic_status_record(status: HeuristicStatus):
    return normalize_status(status, domain="heuristic_discovery")


def evaluate_heuristic_permission(candidate: HeuristicCandidate) -> HeuristicPermissionGateResult:
    missing_fields = _missing_fields(candidate)
    notes = ["Heuristic-only output cannot authorize truth or public claims."]
    status: HeuristicStatus

    dimensional = candidate.heuristic_scores.get("dimensional_consistency", 1.0)
    non_ad_hoc = candidate.heuristic_scores.get("non_ad_hoc_score", 1.0)

    if dimensional < 0.5 or _contains(candidate.assumptions, "dimensional inconsistency"):
        status = "HEURISTIC_REJECTED_DIMENSIONAL_INCONSISTENCY"
        notes.append("Dimensional inconsistency blocks claim readiness.")
    elif non_ad_hoc < 0.5 or _contains(candidate.assumptions, "ad hoc"):
        status = "HEURISTIC_REJECTED_AD_HOC"
        notes.append("Ad-hoc candidate requires human review before promotion.")
    elif "suggested_observables" in missing_fields:
        status = "HEURISTIC_REJECTED_NO_OBSERVABLE"
        notes.append("Missing observable blocks test design.")
    elif "failure_conditions" in missing_fields:
        status = "HEURISTIC_REVIEW_REQUIRED"
        notes.append("Missing failure condition blocks test design.")
    elif "required_benchmarks" in missing_fields:
        status = "HEURISTIC_SEED"
        notes.append("Missing benchmark keeps candidate exploratory.")
    else:
        status = "HEURISTIC_TEST_DESIGN_READY"
        notes.append("Candidate is ready for test design, not claim authorization.")

    canonical = heuristic_status_record(status)
    return HeuristicPermissionGateResult(
        candidate_id=candidate.candidate_id,
        domain_status=status,
        is_claim_authorized=False,
        is_test_design_allowed=canonical.canonical_permission == CanonicalPermission.TEST_DESIGN_ALLOWED,
        missing_fields=missing_fields,
        blocked_reasons=[reason.value for reason in canonical.blocked_reasons],
        canonical_status=canonical,
        notes=notes,
    )


def _missing_fields(candidate: HeuristicCandidate) -> list[str]:
    missing: list[str] = []
    if not candidate.suggested_observables:
        missing.append("suggested_observables")
    if not candidate.suggested_proxies:
        missing.append("suggested_proxies")
    if not candidate.required_sources:
        missing.append("required_sources")
    if not candidate.required_benchmarks:
        missing.append("required_benchmarks")
    if not candidate.failure_conditions:
        missing.append("failure_conditions")
    return missing


def _contains(values: list[str], needle: str) -> bool:
    lowered = needle.lower()
    return any(lowered in value.lower() for value in values)
