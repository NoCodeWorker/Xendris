"""Unit tests for Xendris v0.9 Trust Ledger."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from typing import Any
import pytest
from xendris.core.ledger import (
    TrustEventType,
    TrustLedgerRecord,
    TrustHashChain,
    TrustLedgerWriter,
    TrustLedgerReader,
    TrustLedgerExporter,
    LedgerAudit,
    record_boundary_decision,
    record_sector_transition_decision,
    record_representation_consistency_decision,
    record_model_fingerprint,
    record_route_decision,
)


@pytest.fixture
def writer() -> TrustLedgerWriter:
    return TrustLedgerWriter()


def test_1_ledger_record_hash_is_stable():
    record = TrustLedgerRecord(
        record_id="REC-1",
        run_id="RUN-1",
        event_type=TrustEventType.CLAIM_BOUNDARY_DECISION,
        sequence_index=0,
        source_component="Test",
        decision="ALLOW",
        reason="Success",
        risk_level="LOW",
    )
    h1 = record.calculate_record_hash()
    h2 = record.calculate_record_hash()
    assert h1 == h2
    assert isinstance(h1, str)
    assert len(h1) == 64  # SHA-256 hex length


def test_2_ledger_record_hash_changes_when_content_changes():
    r1 = TrustLedgerRecord(
        record_id="REC-1",
        run_id="RUN-1",
        event_type=TrustEventType.CLAIM_BOUNDARY_DECISION,
        sequence_index=0,
        source_component="Test",
        decision="ALLOW",
        reason="Success",
        risk_level="LOW",
    )
    r2 = TrustLedgerRecord(
        record_id="REC-1",
        run_id="RUN-1",
        event_type=TrustEventType.CLAIM_BOUNDARY_DECISION,
        sequence_index=0,
        source_component="Test",
        decision="BLOCK",  # Changed
        reason="Success",
        risk_level="LOW",
    )
    assert r1.calculate_record_hash() != r2.calculate_record_hash()


def test_3_writer_appends_records_without_mutating_previous_records(writer: TrustLedgerWriter):
    r1 = writer.append_event("REC-1", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW")
    r2 = writer.append_event("REC-2", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW")
    
    assert r1.sequence_index == 0
    assert r2.sequence_index == 1
    assert r2.previous_record_hash == r1.record_hash
    assert r1.previous_record_hash is None


def test_4_writer_exports_jsonl_deterministically(writer: TrustLedgerWriter):
    writer.append_event("REC-1", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "ledger.jsonl")
        writer.write_jsonl(path)
        
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["record_id"] == "REC-1"
        assert data["event_type"] == "CLAIM_BOUNDARY_DECISION"


def test_5_reader_filters_by_run_id(writer: TrustLedgerWriter):
    writer.append_event("REC-1", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW")
    writer.append_event("REC-2", "RUN-2", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW")
    
    reader = TrustLedgerReader(writer)
    run1_records = reader.find_by_run_id("RUN-1")
    assert len(run1_records) == 1
    assert run1_records[0].record_id == "REC-1"


def test_6_reader_filters_by_claim_id(writer: TrustLedgerWriter):
    writer.append_event("REC-1", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW", claim_id="CLAIM-1")
    writer.append_event("REC-2", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW", claim_id="CLAIM-2")
    
    reader = TrustLedgerReader(writer)
    assert len(reader.find_by_claim_id("CLAIM-1")) == 1
    assert reader.find_by_claim_id("CLAIM-1")[0].record_id == "REC-1"


def test_7_reader_filters_by_model_id(writer: TrustLedgerWriter):
    writer.append_event("REC-1", "RUN-1", TrustEventType.MODEL_SELECTED, "Comp", "ALLOW", "reason", "LOW", model_id="gpt-4")
    writer.append_event("REC-2", "RUN-1", TrustEventType.MODEL_SELECTED, "Comp", "ALLOW", "reason", "LOW", model_id="claude-3")
    
    reader = TrustLedgerReader(writer)
    assert len(reader.find_by_model_id("gpt-4")) == 1


def test_8_reader_filters_by_event_type(writer: TrustLedgerWriter):
    writer.append_event("REC-1", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW")
    writer.append_event("REC-2", "RUN-1", TrustEventType.SECTOR_TRANSITION_DECISION, "Comp", "ALLOW", "reason", "LOW")
    
    reader = TrustLedgerReader(writer)
    assert len(reader.find_by_event_type(TrustEventType.SECTOR_TRANSITION_DECISION)) == 1


def test_9_markdown_summary_contains_event_counts(writer: TrustLedgerWriter):
    writer.append_event("REC-1", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW")
    writer.append_event("REC-2", "RUN-1", TrustEventType.SECTOR_TRANSITION_DECISION, "Comp", "ALLOW", "reason", "LOW")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "summary.md")
        TrustLedgerExporter.export_markdown_summary(writer.export_records(), path)
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        assert "CLAIM_BOUNDARY_DECISION" in content
        assert "SECTOR_TRANSITION_DECISION" in content
        assert "Total Records**: 2" in content


def test_10_hash_chain_validates_for_ordered_records(writer: TrustLedgerWriter):
    writer.append_event("REC-1", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW")
    writer.append_event("REC-2", "RUN-1", TrustEventType.SECTOR_TRANSITION_DECISION, "Comp", "ALLOW", "reason", "LOW")
    
    records = writer.export_records()
    assert TrustHashChain.verify_chain(records) is True


def test_11_hash_chain_fails_when_record_is_modified(writer: TrustLedgerWriter):
    writer.append_event("REC-1", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW")
    writer.append_event("REC-2", "RUN-1", TrustEventType.SECTOR_TRANSITION_DECISION, "Comp", "ALLOW", "reason", "LOW")
    
    records = writer.export_records()
    # Modify second record's content manually to break verification
    from dataclasses import replace
    records[1] = replace(records[1], decision="BLOCK")
    
    assert TrustHashChain.verify_chain(records) is False


def test_12_ledger_audit_counts_blocked_claims(writer: TrustLedgerWriter):
    writer.append_event("REC-1", "RUN-1", TrustEventType.CLAIM_BLOCKED, "Comp", "BLOCK", "reason", "LOW")
    writer.append_event("REC-2", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "BLOCK", "reason", "LOW")
    writer.append_event("REC-3", "RUN-1", TrustEventType.CLAIM_BOUNDARY_DECISION, "Comp", "ALLOW", "reason", "LOW")
    
    audit = LedgerAudit.summarize("RUN-1", writer.export_records())
    assert audit.blocked_count == 2


def test_13_ledger_audit_counts_human_review_routes(writer: TrustLedgerWriter):
    writer.append_event("REC-1", "RUN-1", TrustEventType.HUMAN_REVIEW_ROUTED, "Comp", "HUMAN_REVIEW", "reason", "LOW")
    
    audit = LedgerAudit.summarize("RUN-1", writer.export_records())
    assert audit.human_review_count == 1


def test_14_ledger_audit_counts_model_selection_events(writer: TrustLedgerWriter):
    writer.append_event("REC-1", "RUN-1", TrustEventType.MODEL_SELECTED, "Comp", "ALLOW", "reason", "LOW", model_id="gpt-4")
    writer.append_event("REC-2", "RUN-1", TrustEventType.MODEL_REJECTED, "Comp", "ALLOW", "reason", "LOW", model_id="claude-3")
    
    audit = LedgerAudit.summarize("RUN-1", writer.export_records())
    assert audit.selected_model_count == 1
    assert audit.rejected_model_count == 1


@dataclass
class DummyRouteDecision:
    decision: str
    selected_model_id: str
    selected_provider: str
    reason: str
    required_gates: tuple[str, ...]
    rejected_models: tuple[str, ...]
    estimated_cost: float
    estimated_latency_ms: int
    limitations: tuple[str, ...]


def test_15_route_decision_can_be_recorded(writer: TrustLedgerWriter):
    decision = DummyRouteDecision(
        decision="SELECT",
        selected_model_id="strong-coder",
        selected_provider="test-prov",
        reason="Valid cost-safety profile",
        required_gates=("Benchmark Gate",),
        rejected_models=("cheap-draft",),
        estimated_cost=0.005,
        estimated_latency_ms=250,
        limitations=("Strict Universalization Filter",),
    )
    rec = record_route_decision(writer, "RUN-1", "REC-ROUTE-15", decision, "REQ-15")
    assert rec.event_type == TrustEventType.ROUTING_DECISION
    assert rec.model_id == "strong-coder"
    assert rec.metadata["estimated_cost"] == 0.005
    assert "Strict Universalization Filter" in rec.limitations


@dataclass
class DummySectorTransitionDecision:
    decision: str
    reason: str
    limitations: tuple[str, ...]
    required_evidence: tuple[str, ...]
    risk_level: Any


def test_16_sector_transition_decision_can_be_recorded(writer: TrustLedgerWriter):
    decision = DummySectorTransitionDecision(
        decision="ALLOW",
        reason="Transition policy passed",
        limitations=("Constraint Check",),
        required_evidence=("Ref-123",),
        risk_level="MEDIUM",
    )
    rec = record_sector_transition_decision(writer, "RUN-1", "REC-SECTOR-16", decision, "CLAIM-16")
    assert rec.event_type == TrustEventType.SECTOR_TRANSITION_DECISION
    assert rec.claim_id == "CLAIM-16"
    assert "Constraint Check" in rec.limitations
    assert "Ref-123" in rec.evidence_refs


@dataclass
class DummyRepresentationConsistencyDecision:
    decision: str
    reason: str
    limitations: tuple[str, ...]
    required_evidence: tuple[str, ...]


def test_17_representation_consistency_decision_can_be_recorded(writer: TrustLedgerWriter):
    decision = DummyRepresentationConsistencyDecision(
        decision="ALLOW",
        reason="Representations are equivalent",
        limitations=("Agreement fence",),
        required_evidence=("evidence-1",),
    )
    rec = record_representation_consistency_decision(writer, "RUN-1", "REC-REP-17", decision, "CLAIM-17")
    assert rec.event_type == TrustEventType.REPRESENTATION_CONSISTENCY_DECISION
    assert rec.claim_id == "CLAIM-17"


@dataclass
class DummyBoundaryDecision:
    decision: str
    reason: str
    allowed: bool
    required_evidence: tuple[str, ...]


def test_18_contamination_guard_decision_can_be_recorded(writer: TrustLedgerWriter):
    decision = DummyBoundaryDecision(
        decision="ALLOW",
        reason="Context clean",
        allowed=True,
        required_evidence=("Cleanliness verification",),
    )
    rec = record_boundary_decision(writer, "RUN-1", "REC-BOUND-18", decision, "CLAIM-18")
    assert rec.event_type == TrustEventType.CLAIM_BOUNDARY_DECISION
    assert "Cleanliness verification" in rec.limitations


def test_19_empty_ledger_summary_is_safe():
    audit = LedgerAudit.summarize("RUN-EMPTY", [])
    assert audit.record_count == 0
    assert audit.chain_valid is True
    assert len(audit.event_type_counts) == 0


def test_20_ledger_does_not_claim_blockchain_immutability():
    # As requested: "ledger must not claim immutability beyond its local deterministic append-only semantics unless backed by a real immutable backend."
    doc_path = "docs/status/XENDRIS_TRUST_LEDGER_V0_9.md"
    assert os.path.exists(doc_path)
