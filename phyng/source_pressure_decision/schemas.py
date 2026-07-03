"""Schemas for v3.9 source pressure decision gate."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


# --- Extract-level pressure ---

class ExtractPressureRecord(BaseModel):
    extract_id: str
    source_id: str
    sha256: str
    page_number: int | None = None
    assigned_slot: str
    component_role: str
    exact_text: str
    pressure_class: str
    pressure_direction: str
    pressure_score: float
    confidence: str
    reasoning: str
    limitations: list[str] = Field(default_factory=list)
    can_support_claim: bool = False
    can_contradict_claim: bool = False


PRESSURE_CLASSES = [
    "SUPPORTS_BASELINE_ONLY",
    "SUPPORTS_OBSERVABLE_ONLY",
    "SUPPORTS_BENCHMARK_ALIGNMENT",
    "SUPPORTS_PARAMETER_CONSTRAINT",
    "SUPPORTS_GRADIENT_COMPONENT",
    "CONTRADICTS_COMPONENT",
    "LIMITS_COMPONENT",
    "ANALOGY_ONLY",
    "INCONCLUSIVE",
    "IRRELEVANT_AFTER_REVIEW",
]

SLOTS = [
    "SLOT_1_DECOHERENCE_BASELINE",
    "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE",
    "SLOT_3_BENCHMARK_RANGES",
    "SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS",
    "SLOT_5_PARAMETER_CONSTRAINTS",
    "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS",
    "SLOT_7_EXPERIMENTAL_CONTEXT",
]

SLOT_PRESSURE_STATUSES = [
    "SLOT_SOURCE_BACKED_LIMITED",
    "SLOT_BENCHMARK_RELEVANT",
    "SLOT_CONTRADICTED",
    "SLOT_LIMITED",
    "SLOT_ANALOGY_ONLY",
    "SLOT_INCONCLUSIVE",
    "SLOT_NO_VALID_EXTRACTS",
]

SOURCE_WEIGHTS: dict[str, float] = {
    "SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS": 1.00,
    "SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST": 0.95,
    "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING": 0.90,
    "SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE": 0.85,
    "SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE": 0.85,
}

GLOBAL_DECISIONS = [
    "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED",
    "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND",
    "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED",
    "PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY",
    "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE",
    "PHI_GRADIENT_REAL_SOURCE_PRESSURE_BLOCKED",
]


# --- Slot-level summary ---

class SlotPressureSummary(BaseModel):
    slot_id: str
    extract_count: int = 0
    support_count: int = 0
    benchmark_count: int = 0
    contradiction_count: int = 0
    limitation_count: int = 0
    analogy_only_count: int = 0
    inconclusive_count: int = 0
    pressure_status: str = "SLOT_NO_VALID_EXTRACTS"
    pressure_score: float = 0.0
    summary: str = ""


# --- Benchmark alignment ---

class BenchmarkAlignmentRecord(BaseModel):
    benchmark_extracts: list[str] = Field(default_factory=list)
    observable_alignment: list[str] = Field(default_factory=list)
    range_alignment: list[str] = Field(default_factory=list)
    missing_benchmark_fields: list[str] = Field(default_factory=list)
    benchmark_decision: str = "NO_BENCHMARK_EXTRACTS"
    limitations: list[str] = Field(default_factory=list)


# --- Contradiction map ---

class ContradictionLimitationMap(BaseModel):
    contradictions: list[dict] = Field(default_factory=list)
    limitations: list[dict] = Field(default_factory=list)
    dominant_risks: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    affected_slots: list[str] = Field(default_factory=list)
    required_model_changes: list[str] = Field(default_factory=list)


# --- Global decision ---

class SourcePressureDecision(BaseModel):
    decision_id: str = "PHI-GRADIENT-SOURCE-PRESSURE-DECISION-v3_9"
    candidate_family: str = "LOG_BOUNDARY"
    phi_family: str = "PHI_GRADIENT"
    created_at: str = "2026-07-01"
    input_validation_pack: str = "data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json"
    validation_ready_count: int = 0
    global_decisions: list[str] = Field(default_factory=list)
    primary_decision: str = "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"
    confidence: str = "LOW"
    gradient_component_support: bool = False
    slot_pressure_summary_path: str = "data/real_sources/source_pressure/phi_gradient_slot_pressure_summary_v3_9.json"
    benchmark_alignment_path: str = "data/real_sources/source_pressure/phi_gradient_benchmark_alignment_v3_9.json"
    contradiction_map_path: str = "data/real_sources/source_pressure/phi_gradient_contradiction_and_limitation_map_v3_9.json"
    physical_claim_permission: str = "BLOCKED"
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_recommendations: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


# --- Gate result ---

class SourcePressureGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    validation_ready_count: int = 0
    extract_pressure_records: list[ExtractPressureRecord] = Field(default_factory=list)
    slot_pressure_summary: list[SlotPressureSummary] = Field(default_factory=list)
    benchmark_alignment: BenchmarkAlignmentRecord = Field(default_factory=BenchmarkAlignmentRecord)
    contradiction_map: ContradictionLimitationMap = Field(default_factory=ContradictionLimitationMap)
    decision: SourcePressureDecision = Field(default_factory=SourcePressureDecision)
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_recommendations: list[str] = Field(default_factory=list)


# --- Campaign result ---

class SourcePressureCampaignResult(BaseModel):
    campaign_id: str = "PHI-GRADIENT-SOURCE-PRESSURE-DECISION-v3_9"
    status: str
    gate_result: SourcePressureGateResult
    report_paths: dict[str, str] = Field(default_factory=dict)


# --- Loader inputs ---

class SourcePressureInputs(BaseModel):
    validation_ready_pack: dict = Field(default_factory=dict)
    review_decisions: dict = Field(default_factory=dict)
    analogy_only_items: dict = Field(default_factory=dict)
    manual_review_queue: dict = Field(default_factory=dict)
    next_source_pressure_inputs: dict = Field(default_factory=dict)
    source_hashes: dict = Field(default_factory=dict)
    blocked_reason: str | None = None
