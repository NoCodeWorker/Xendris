# Phygn v3.9 — Source Pressure Output Schemas

## 0. Purpose

This document defines the v3.9 source-pressure artifacts.

---

## 1. Extract pressure record

```python
class ExtractPressureRecord(BaseModel):
    extract_id: str
    source_id: str
    sha256: str
    page_number: int | None
    assigned_slot: str
    component_role: str
    exact_text: str
    pressure_class: str
    pressure_direction: str
    pressure_score: float
    confidence: str
    reasoning: str
    limitations: list[str]
    can_support_claim: bool
    can_contradict_claim: bool
```

---

## 2. Source pressure decision

Create:

```txt
data/real_sources/source_pressure/phi_gradient_source_pressure_decision_v3_9.json
```

Schema:

```python
class SourcePressureDecision(BaseModel):
    decision_id: str
    candidate_family: str
    phi_family: str
    created_at: str
    input_validation_pack: str
    validation_ready_count: int
    global_decisions: list[str]
    primary_decision: str
    confidence: str
    slot_pressure_summary_path: str
    benchmark_alignment_path: str
    contradiction_map_path: str
    physical_claim_permission: str
    allowed_claims: list[str]
    blocked_claims: list[str]
    next_recommendations: list[str]
    notes: list[str]
```

---

## 3. Slot pressure summary

Create:

```txt
data/real_sources/source_pressure/phi_gradient_slot_pressure_summary_v3_9.json
```

Each slot:

```txt
slot_id
extract_count
support_count
benchmark_count
contradiction_count
limitation_count
analogy_only_count
inconclusive_count
pressure_status
pressure_score
summary
```

---

## 4. Benchmark alignment

Create:

```txt
data/real_sources/source_pressure/phi_gradient_benchmark_alignment_v3_9.json
```

Fields:

```txt
benchmark_extracts
observable_alignment
range_alignment
missing_benchmark_fields
benchmark_decision
limitations
```

---

## 5. Contradiction and limitation map

Create:

```txt
data/real_sources/source_pressure/phi_gradient_contradiction_and_limitation_map_v3_9.json
```

Fields:

```txt
contradictions
limitations
dominant_risks
source_ids
affected_slots
required_model_changes
```

---

## 6. Next model update recommendations

Create:

```txt
data/real_sources/source_pressure/phi_gradient_next_model_update_recommendations_v3_9.json
```

Recommendations may include:

```txt
keep PHI_GRADIENT as analogy-only
restrict PHI_GRADIENT to observable/benchmark framing
revise gradient component
seek new SLOT_4 literature
seek exact Pedernales manual review
design benchmark-only model comparison
run negative-control source pressure
```

---

## 7. Final principle

```txt
The output of v3.9 is not belief.
It is permission, pressure or prohibition.
```
