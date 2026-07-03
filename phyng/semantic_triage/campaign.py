"""Campaign orchestration for PHI_GRADIENT semantic triage v3.8.2."""

from __future__ import annotations

from pathlib import Path

from phyng.core.compatibility import normalize_status
from phyng.semantic_triage.loader import load_semantic_triage_inputs
from phyng.semantic_triage.packet_builder import (
    build_low_value_exclusions,
    build_next_gate_readiness,
    build_priority_packet,
    build_slot_review_queues,
    write_v3_8_2_outputs,
)
from phyng.semantic_triage.prioritizer import triage_candidates
from phyng.semantic_triage.reports import write_semantic_triage_reports
from phyng.semantic_triage.schemas import (
    NextGateReadiness,
    PhiGradientSemanticTriageCampaignResult,
    PhiGradientSemanticTriageGateResult,
)


def run_phi_gradient_semantic_triage_campaign(root: str | Path = ".") -> PhiGradientSemanticTriageCampaignResult:
    repo_root = Path(root)
    inputs = load_semantic_triage_inputs(repo_root)
    blocked_claims = _blocked_claims()
    if inputs.blocked_reason:
        readiness = NextGateReadiness(
            status=inputs.blocked_reason,
            reason="Required v3.8.2 input artifacts are missing.",
            recommended_next_action="Regenerate v3.7 and v3.8 artifacts before semantic triage.",
            blocked_claims=blocked_claims,
        )
        gate = PhiGradientSemanticTriageGateResult(
            status=inputs.blocked_reason,
            canonical_status=normalize_status(inputs.blocked_reason, domain="semantic_triage"),
            next_gate_readiness=readiness,
            allowed_claims=_allowed_claims(),
            blocked_claims=blocked_claims,
            next_actions=["Regenerate v3.7/v3.8 artifacts before v3.8.2."],
        )
        result = PhiGradientSemanticTriageCampaignResult(campaign_id="PHI-GRADIENT-SEMANTIC-TRIAGE-v3_8_2", status=inputs.blocked_reason, gate_result=gate)
        result.report_paths = write_semantic_triage_reports(result, repo_root / "reports")
        return result

    records = triage_candidates(inputs.candidates)
    packet = build_priority_packet(records)
    queues = build_slot_review_queues(packet)
    exclusions = build_low_value_exclusions(records)
    validation_ready_count = int(inputs.validation_ready_pack.get("validation_ready_count", 0) or 0)
    status = _status(packet, records, validation_ready_count)
    readiness = build_next_gate_readiness(status, packet, validation_ready_count, blocked_claims)
    output_paths = write_v3_8_2_outputs(repo_root, records, packet, queues, exclusions, readiness)
    gate = PhiGradientSemanticTriageGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="semantic_triage"),
        input_candidate_count=len(inputs.candidates),
        triaged_candidate_count=len(records),
        priority_packet_count=len(packet),
        critical_count=sum(1 for item in packet if item.priority == "CRITICAL"),
        high_count=sum(1 for item in packet if item.priority == "HIGH"),
        validation_ready_count=validation_ready_count,
        pedernales_slot4_count=sum(
            1
            for item in packet
            if item.source_id == "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING"
            and item.assigned_slot == "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS"
        ),
        slot_coverage=_slot_coverage(packet),
        source_coverage=_source_coverage(packet),
        triage_map=records,
        priority_packet=packet,
        slot_review_queues=queues,
        low_value_exclusions=exclusions,
        next_gate_readiness=readiness,
        output_paths=output_paths,
        allowed_claims=_allowed_claims(),
        blocked_claims=blocked_claims,
        next_actions=_next_actions(status),
    )
    result = PhiGradientSemanticTriageCampaignResult(campaign_id="PHI-GRADIENT-SEMANTIC-TRIAGE-v3_8_2", status=status, gate_result=gate)
    result.report_paths = write_semantic_triage_reports(result, repo_root / "reports")
    return result


def _status(packet: list, records: list, validation_ready_count: int) -> str:
    if packet and validation_ready_count == 0:
        return "PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY"
    if packet and validation_ready_count > 0:
        return "PHI_GRADIENT_SEMANTIC_TRIAGE_PARTIAL"
    if records:
        return "PHI_GRADIENT_SEMANTIC_TRIAGE_NO_USEFUL_CANDIDATES"
    return "PHI_GRADIENT_SEMANTIC_TRIAGE_COMPLETED"


def _slot_coverage(packet: list) -> dict[str, int]:
    coverage: dict[str, int] = {}
    for item in packet:
        coverage[item.assigned_slot] = coverage.get(item.assigned_slot, 0) + 1
    return coverage


def _source_coverage(packet: list) -> dict[str, int]:
    coverage: dict[str, int] = {}
    for item in packet:
        coverage[item.source_id] = coverage.get(item.source_id, 0) + 1
    return coverage


def _allowed_claims() -> list[str]:
    return [
        "Semantic triage was performed.",
        "A priority review packet was generated.",
        "Candidate review was reduced to a smaller set.",
        "Pedernales SLOT_4 was prioritized if candidate text exists.",
    ]


def _blocked_claims() -> list[str]:
    return [
        "Priority packet validates PHI_GRADIENT.",
        "High-priority candidate is source support.",
        "Critical candidate is evidence.",
        "Triage score is physical support.",
        "PHI_GRADIENT is physically validated.",
        "Frontera C is validated.",
    ]


def _next_actions(status: str) -> list[str]:
    if status == "PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY":
        return ["Perform v3.8.3 priority packet review before any positive v3.9 pressure gate."]
    if status == "PHI_GRADIENT_SEMANTIC_TRIAGE_BLOCKED_MISSING_INPUTS":
        return ["Regenerate v3.7 and v3.8 input artifacts."]
    return ["Inspect semantic triage output and decide whether extraction quality must improve."]
