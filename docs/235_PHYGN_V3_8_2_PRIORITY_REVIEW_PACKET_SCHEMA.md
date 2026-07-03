# Phygn v3.8.2 — Priority Review Packet Schema

## 0. Purpose

This document defines the compact human/AI-assisted review packet.

---

## 1. Semantic triage map

Create:

```txt
data/real_sources/extracts/phi_gradient_semantic_triage_map_v3_8_2.json
```

Schema:

```python
class SemanticTriageRecord(BaseModel):
    candidate_id: str
    source_id: str
    sha256: str | None
    page_number: int | None
    candidate_type: str
    extracted_text: str
    normalized_text: str | None
    assigned_slot: str
    semantic_score: float
    source_priority_score: float
    slot_relevance_score: float
    cleanliness_score: float
    specificity_score: float
    risk_score: float
    triage_score: float
    priority: str
    include_in_priority_packet: bool
    review_question: str
    decision_needed: str
    notes: list[str]
```

---

## 2. Priority review packet

Create:

```txt
data/real_sources/extracts/phi_gradient_priority_review_packet_v3_8_2.json
```

Schema:

```python
class PriorityReviewItem(BaseModel):
    review_item_id: str
    candidate_id: str
    source_id: str
    page_number: int | None
    assigned_slot: str
    priority: str
    exact_text_or_preview: str
    why_relevant: str
    review_question: str
    decision_needed: str
    possible_outcomes: list[str]
    next_gate_impact: str
```

Possible outcomes:

```txt
VALIDATION_READY_EXTRACT
MANUAL_REVIEW_REQUIRED
REJECT_AS_GARBAGE
ANALOGY_ONLY
NEGATIVE_CONSTRAINT
BENCHMARK_RELEVANT
BASELINE_RELEVANT
PARAMETER_CONSTRAINT_RELEVANT
GRADIENT_COMPONENT_RELEVANT
```

---

## 3. Slot review queues

Create:

```txt
data/real_sources/extracts/phi_gradient_slot_review_queues_v3_8_2.json
```

Fields:

```txt
slot_id
items
critical_count
high_count
medium_count
low_count
source_coverage
```

---

## 4. Low-value exclusion file

Create:

```txt
data/real_sources/extracts/phi_gradient_triage_rejected_low_value_v3_8_2.json
```

Each record:

```txt
candidate_id
source_id
reason
triage_score
text_preview
```

---

## 5. Next gate readiness

Create:

```txt
data/real_sources/extracts/phi_gradient_v3_8_2_next_gate_readiness.json
```

Fields:

```txt
status
priority_packet_count
critical_count
high_count
manual_review_required
ready_for_v3_9
reason
recommended_next_action
blocked_claims
```

Rule:

```txt
ready_for_v3_9 = false
```

unless there is at least one reviewed validation-ready extract.

v3.8.2 may prepare a packet for review but does not itself create source support.

---

## 6. Final principle

```txt
The packet is a map of where judgment should happen.
It is not the judgment.
```
