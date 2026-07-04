"""Trust Ledger package for Xendris."""

from __future__ import annotations

from typing import Any
from xendris.core.ledger.event_type import TrustEventType
from xendris.core.ledger.record import TrustLedgerRecord
from xendris.core.ledger.hashchain import TrustHashChain
from xendris.core.ledger.writer import TrustLedgerWriter
from xendris.core.ledger.reader import TrustLedgerReader
from xendris.core.ledger.export import TrustLedgerExporter
from xendris.core.ledger.ledger_audit import LedgerAudit


def record_boundary_decision(
    writer: TrustLedgerWriter,
    run_id: str,
    record_id: str,
    decision: Any,
    claim_id: str | None = None,
) -> TrustLedgerRecord:
    """Record a ContaminationGuard BoundaryDecision in the ledger."""
    dec_val = getattr(decision, "decision", "BLOCK")
    reason = getattr(decision, "reason", "UNKNOWN_BOUNDARY_DECISION")
    gates = getattr(decision, "required_evidence", ())
    return writer.append_event(
        record_id=record_id,
        run_id=run_id,
        event_type=TrustEventType.CLAIM_BOUNDARY_DECISION,
        source_component="ContaminationGuard",
        decision=dec_val,
        reason=reason,
        risk_level="MEDIUM",
        claim_id=claim_id,
        limitations=gates,
    )


def record_sector_transition_decision(
    writer: TrustLedgerWriter,
    run_id: str,
    record_id: str,
    decision: Any,
    claim_id: str | None = None,
) -> TrustLedgerRecord:
    """Record a SectorTransitionDecision in the ledger."""
    dec_val = getattr(decision, "decision", "BLOCK")
    reason = getattr(decision, "reason", "UNKNOWN_SECTOR_TRANSITION")
    limitations = getattr(decision, "limitations", ())
    evidence = getattr(decision, "required_evidence", ())
    risk = getattr(decision, "risk_level", "LOW")
    risk_str = risk.name if hasattr(risk, "name") else str(risk)
    
    # Retrieve claim_id if nested
    if not claim_id and hasattr(decision, "transition") and decision.transition is not None:
        claim_id = getattr(decision.transition, "claim_id", None)

    return writer.append_event(
        record_id=record_id,
        run_id=run_id,
        event_type=TrustEventType.SECTOR_TRANSITION_DECISION,
        source_component="SectorTransitionEngine",
        decision=dec_val,
        reason=reason,
        risk_level=risk_str,
        claim_id=claim_id,
        limitations=limitations,
        evidence_refs=evidence,
    )


def record_representation_consistency_decision(
    writer: TrustLedgerWriter,
    run_id: str,
    record_id: str,
    decision: Any,
    claim_id: str | None = None,
) -> TrustLedgerRecord:
    """Record a RepresentationConsistencyDecision in the ledger."""
    dec_val = getattr(decision, "decision", "BLOCK")
    reason = getattr(decision, "reason", "UNKNOWN_CONSISTENCY_GATE")
    limitations = getattr(decision, "limitations", ())
    evidence = getattr(decision, "required_evidence", ())

    if not claim_id and hasattr(decision, "recommended_claim") and decision.recommended_claim is not None:
        claim_id = getattr(decision.recommended_claim, "claim_id", None)

    return writer.append_event(
        record_id=record_id,
        run_id=run_id,
        event_type=TrustEventType.REPRESENTATION_CONSISTENCY_DECISION,
        source_component="RepresentationConsistencyGate",
        decision=dec_val,
        reason=reason,
        risk_level="MEDIUM",
        claim_id=claim_id,
        limitations=limitations,
        evidence_refs=evidence,
    )


def record_model_fingerprint(
    writer: TrustLedgerWriter,
    run_id: str,
    record_id: str,
    fingerprint: Any,
) -> TrustLedgerRecord:
    """Record a ModelEpistemicFingerprint summary in the ledger."""
    model_id = None
    provider = None
    if hasattr(fingerprint, "model_identity") and fingerprint.model_identity is not None:
        model_id = getattr(fingerprint.model_identity, "model_id", None)
        provider = getattr(fingerprint.model_identity, "provider", None)
        
    limitations = getattr(fingerprint, "limitations", ())

    return writer.append_event(
        record_id=record_id,
        run_id=run_id,
        event_type=TrustEventType.MODEL_FINGERPRINT_SUMMARY,
        source_component="EpistemicFingerprintAggregator",
        decision="ALLOW",
        reason="FINGERPRINT_SUMMARY_RECORDED",
        risk_level="LOW",
        model_id=model_id,
        provider=provider,
        limitations=limitations,
    )


def record_route_decision(
    writer: TrustLedgerWriter,
    run_id: str,
    record_id: str,
    decision: Any,
    request_id: str | None = None,
) -> TrustLedgerRecord:
    """Record a RouteDecision in the ledger."""
    dec_val = getattr(decision, "decision", "BLOCK")
    model_id = getattr(decision, "selected_model_id", None)
    provider = getattr(decision, "selected_provider", None)
    reason = getattr(decision, "reason", "UNKNOWN_ROUTE_DECISION")
    gates = getattr(decision, "required_gates", ())
    rejected = getattr(decision, "rejected_models", ())
    cost = getattr(decision, "estimated_cost", 0.0)
    latency = getattr(decision, "estimated_latency_ms", 0)
    limitations = getattr(decision, "limitations", ())

    return writer.append_event(
        record_id=record_id,
        run_id=run_id,
        event_type=TrustEventType.ROUTING_DECISION,
        source_component="MultiModelSelector",
        decision=dec_val,
        reason=reason,
        risk_level="MEDIUM",
        model_id=model_id,
        provider=provider,
        limitations=limitations,
        metadata={
            "request_id": request_id,
            "required_gates": list(gates),
            "rejected_models": list(rejected),
            "estimated_cost": cost,
            "estimated_latency_ms": latency,
        },
    )


__all__ = [
    "TrustEventType",
    "TrustLedgerRecord",
    "TrustHashChain",
    "TrustLedgerWriter",
    "TrustLedgerReader",
    "TrustLedgerExporter",
    "LedgerAudit",
    "record_boundary_decision",
    "record_sector_transition_decision",
    "record_representation_consistency_decision",
    "record_model_fingerprint",
    "record_route_decision",
]
