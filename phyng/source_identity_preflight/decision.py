"""Decision matrix and gate for v4.9 source identity preflight."""

from __future__ import annotations

from collections import Counter

from phyng.source_identity_preflight.schemas import (
    CandidateFamilySourceInventory,
    CandidatePreflightDecisionRecord,
    ObservableIdentityRecord,
    SourceAvailabilityMatrixRecord,
    SourceIdentityPreflightGate,
    SourceIdentityResolutionRecord,
    YTruePathPlausibilityRecord,
)


BLOCKED_CLAIMS = [
    "Any candidate is validated.",
    "Any candidate has PredictiveGain.",
    "Any candidate is empirically supported.",
    "Source identity preflight creates y_true.",
    "Source identity preflight creates physical validation.",
]

ALLOWED_CLAIMS = [
    "Candidate families were screened for resolvable source identity.",
    "A candidate passed, failed, or was partial according to source identity preflight.",
    "A next source acquisition or minimal campaign was permitted by gate.",
]


def build_candidate_preflight_decision_matrix(
    inventory: list[CandidateFamilySourceInventory],
    identities: list[SourceIdentityResolutionRecord],
    availability: list[SourceAvailabilityMatrixRecord],
    observables: list[ObservableIdentityRecord],
    ytrue_paths: list[YTruePathPlausibilityRecord],
) -> list[CandidatePreflightDecisionRecord]:
    decisions: list[CandidatePreflightDecisionRecord] = []
    for item in inventory:
        fam_id = item.family_id
        fam_identities = [record for record in identities if record.family_id == fam_id]
        fam_availability = [record for record in availability if record.family_id == fam_id]
        fam_observables = [record for record in observables if record.family_id == fam_id]
        fam_ytrue = [record for record in ytrue_paths if record.family_id == fam_id]
        resolvable = sum(1 for record in fam_identities if record.identity_complete)
        local_or_exact = sum(1 for record in fam_availability if record.local_pdf_available or record.availability_status == "IDENTITY_ONLY_REQUIRES_DOWNLOAD")
        locatable = sum(1 for record in fam_observables if record.source_locatable)
        plausible = sum(1 for record in fam_ytrue if record.plausibility_level in {"HIGH", "MEDIUM"})
        slot4 = _slot4_dependency(item)
        claim_risk = _claim_risk(item)
        status = _preflight_status(resolvable, local_or_exact, locatable, plausible, slot4, claim_risk, item)
        decisions.append(
            CandidatePreflightDecisionRecord(
                family_id=fam_id,
                resolvable_source_count=resolvable,
                local_or_exact_source_count=local_or_exact,
                source_locatable_observable_count=locatable,
                plausible_ytrue_path_count=plausible,
                slot4_dependency=slot4,
                claim_risk=claim_risk,
                preflight_status=status,
                allowed_next_phase=_allowed_next_phase(status),
                blocked_next_phases=["PredictiveGain evaluation", "Physical validation", "y_true acceptance in v4.9"],
                required_next_action=_required_next_action(status),
                notes=_decision_notes(item, status),
            )
        )
    return decisions


def build_source_identity_preflight_gate(decisions: list[CandidatePreflightDecisionRecord]) -> SourceIdentityPreflightGate:
    counts = Counter(record.preflight_status for record in decisions)
    passed = counts.get("PREFLIGHT_PASSED", 0)
    partial = counts.get("PREFLIGHT_PARTIAL_REQUIRES_SOURCE_ACQUISITION", 0) + counts.get("PREFLIGHT_REQUIRES_HUMAN_LOOKUP", 0)
    failed = len(decisions) - passed - partial
    if passed:
        status = "PHYGN_SOURCE_IDENTITY_PREFLIGHT_CANDIDATE_PASSED"
        selected = next(record.family_id for record in decisions if record.preflight_status == "PREFLIGHT_PASSED")
        allowed_next = "v5.0 - Selected Candidate Minimal Source/y_true Campaign"
    elif partial:
        status = "PHYGN_SOURCE_IDENTITY_PREFLIGHT_REQUIRES_HUMAN_LOOKUP"
        selected = None
        allowed_next = "v5.0 - Targeted Source Acquisition and Human Lookup Sprint"
    else:
        status = "PHYGN_SOURCE_IDENTITY_PREFLIGHT_NO_CANDIDATE_PASSED"
        selected = None
        allowed_next = "v5.0 - Candidate Family Reprioritization / External Source Strategy"
    return SourceIdentityPreflightGate(
        final_status=status,
        candidate_count=len(decisions),
        passed_candidate_count=passed,
        partial_candidate_count=partial,
        failed_candidate_count=failed,
        selected_candidate_family=selected,
        allowed_next_phase=allowed_next,
        blocked_next_phases=["PredictiveGain evaluation", "Physical validation", "y_true creation"],
        required_before_next_pipeline=[
            "Resolve candidate source identity.",
            "Register DOI/arXiv/URL or local source hash.",
            "Tie observable classes to source locations.",
        ],
        blocked_claims=BLOCKED_CLAIMS,
        allowed_claims=ALLOWED_CLAIMS,
        notes=["No y_true, PredictiveGain, or physical validation is created by v4.9."],
    )


def _preflight_status(
    resolvable: int,
    local_or_exact: int,
    locatable: int,
    plausible: int,
    slot4: str,
    claim_risk: str,
    item: CandidateFamilySourceInventory,
) -> str:
    if item.family_id == "PHI_GRADIENT" or slot4 == "DEPENDENT":
        return "PREFLIGHT_BLOCKED_SLOT4_DEPENDENCY"
    if resolvable >= 2 and local_or_exact >= 1 and locatable >= 1 and plausible >= 1 and claim_risk != "CRITICAL":
        return "PREFLIGHT_PASSED"
    if item.raw_source_refs and resolvable == 0:
        return "PREFLIGHT_FAILED_NO_RESOLVABLE_SOURCES"
    if item.inventory_status in {"NO_SOURCE_REFS", "HAS_LOCAL_ARTIFACTS"}:
        return "PREFLIGHT_REQUIRES_HUMAN_LOOKUP"
    if plausible == 0:
        return "PREFLIGHT_FAILED_NO_YTRUE_PATH"
    return "PREFLIGHT_PARTIAL_REQUIRES_SOURCE_ACQUISITION"


def _slot4_dependency(item: CandidateFamilySourceInventory) -> str:
    if item.family_id in {"PHI_GRADIENT", "QB_STRUCTURAL"}:
        return "DEPENDENT"
    return "INDEPENDENT"


def _claim_risk(item: CandidateFamilySourceInventory) -> str:
    if item.family_id in {"PHI_GRADIENT", "B_SUPPRESSED", "QB_STRUCTURAL"}:
        return "HIGH"
    return "MEDIUM"


def _allowed_next_phase(status: str) -> str | None:
    if status == "PREFLIGHT_PASSED":
        return "v5.0 - Selected Candidate Minimal Source/y_true Campaign"
    if status in {"PREFLIGHT_PARTIAL_REQUIRES_SOURCE_ACQUISITION", "PREFLIGHT_REQUIRES_HUMAN_LOOKUP"}:
        return "v5.0 - Targeted Source Acquisition and Human Lookup Sprint"
    return None


def _required_next_action(status: str) -> str:
    if status == "PREFLIGHT_PASSED":
        return "Proceed to minimal source/y_true campaign without claim upgrade."
    if status == "PREFLIGHT_BLOCKED_SLOT4_DEPENDENCY":
        return "Resolve or preserve SLOT_4 claim block before physical interpretation."
    if status == "PREFLIGHT_FAILED_NO_RESOLVABLE_SOURCES":
        return "Resolve source title, year, and DOI/arXiv/URL/local hash."
    return "Perform targeted human source lookup and acquisition."


def _decision_notes(item: CandidateFamilySourceInventory, status: str) -> list[str]:
    notes = list(item.notes)
    if item.family_id == "PHI_CURVATURE":
        notes.append("Reflects v4.8 unresolved source identity result.")
    notes.append(f"Decision: {status}.")
    return notes
