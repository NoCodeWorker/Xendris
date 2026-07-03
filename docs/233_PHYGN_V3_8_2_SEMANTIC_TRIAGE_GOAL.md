# Phygn v3.8.2 — Semantic Triage & Priority Review Packet Goal

## 0. Context

The latest confirmed document is:

```txt
docs/232_PHYGN_V3_8_1_PDF_READER_INTEGRATION_FIX_RESULTS.md
```

Therefore, v3.8.2 starts at:

```txt
233
```

v3.8.1 fixed PDF reader integration.

v3.7 after the fix:

```txt
PHI_GRADIENT_PDF_EXTRACTION_COMPLETED
hashed_sources_seen = 5
sources_extracted = 5
sources_blocked = 0
total_pages_extracted = 44
total_candidates = 548
Pedernales blocked = false
```

v3.8 after rerun:

```txt
PHI_GRADIENT_EXTRACT_REVIEW_MANUAL_REVIEW_REQUIRED
input_candidate_count = 548
validation_ready_count = 0
rejected_count = 227
manual_review_count = 321
pedernales_blocked = false
```

The technical PDF reading bottleneck is resolved.

The new bottleneck is semantic review overload.

---

## 1. Core thesis

```txt
More extraction is not more evidence.
Priority is the bridge between reading and judgment.
```

v3.8.2 does not validate PHI_GRADIENT.

v3.8.2 reduces raw candidate volume into a prioritized review packet.

---

## 2. Goal

Convert:

```txt
548 raw extracted candidates
321 manual-review items
0 validation-ready extracts
```

into:

```txt
a prioritized semantic triage map
a compact priority review packet
slot-based review queues
source/slot coverage summaries
recommended exact review questions
next v3.9 readiness assessment
```

---

## 3. Hard rule

```txt
Triage is not support.
Priority is not evidence.
Review packet is not validation.
No candidate becomes source support in v3.8.2.
No benchmark support is granted.
No physical claim is upgraded.
```

---

## 4. Inputs

v3.8.2 must load:

```txt
data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_quote_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_equation_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_table_range_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_negative_constraint_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8.json
data/real_sources/extracts/phi_gradient_rejected_extraction_candidates_v3_8.json
data/real_sources/extracts/phi_gradient_reviewed_candidate_map_v3_8.json
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8.json
data/real_sources/source_hashes_v3_6.json
```

---

## 5. Outputs

Create:

```txt
data/real_sources/extracts/phi_gradient_semantic_triage_map_v3_8_2.json
data/real_sources/extracts/phi_gradient_priority_review_packet_v3_8_2.json
data/real_sources/extracts/phi_gradient_slot_review_queues_v3_8_2.json
data/real_sources/extracts/phi_gradient_triage_rejected_low_value_v3_8_2.json
data/real_sources/extracts/phi_gradient_v3_8_2_next_gate_readiness.json
```

---

## 6. Target packet size

The packet should be compact:

```txt
target priority review items: 30 to 60
critical items: 5 to 15
high items: 10 to 25
medium items: remaining useful items
low/noise: excluded from packet
```

If fewer than 30 meaningful items exist, include fewer.

If more than 60 look useful, cap by score and slot coverage.

---

## 7. Slot taxonomy

Use these slots:

```txt
SLOT_1_DECOHERENCE_BASELINE
SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE
SLOT_3_BENCHMARK_RANGES
SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS
SLOT_5_PARAMETER_CONSTRAINTS
SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS
SLOT_7_EXPERIMENTAL_CONTEXT
SLOT_8_ANALOGY_ONLY_OR_BACKGROUND
```

---

## 8. Priority classes

```txt
CRITICAL
HIGH
MEDIUM
LOW
EXCLUDE
```

v3.8.2 should prefer:

```txt
Pedernales gradient/transition/effective dynamics
Schrinski MMM/coherence loss/hypothesis testing
Nimmrichter CSL bounds/parameter constraints
Hornberger collisional decoherence baseline
Hackermueller thermal emission decoherence baseline
visibility/contrast observables
negative constraints and limitations
```

---

## 9. Statuses

```txt
PHI_GRADIENT_SEMANTIC_TRIAGE_COMPLETED
PHI_GRADIENT_SEMANTIC_TRIAGE_PARTIAL
PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY
PHI_GRADIENT_SEMANTIC_TRIAGE_MANUAL_REVIEW_REQUIRED
PHI_GRADIENT_SEMANTIC_TRIAGE_NO_USEFUL_CANDIDATES
PHI_GRADIENT_SEMANTIC_TRIAGE_BLOCKED_MISSING_INPUTS
```

---

## 10. Acceptance criteria

v3.8.2 is complete when:

```txt
candidate inputs loaded
semantic triage rules applied
priority review packet generated
slot review queues generated
low-value/noise candidates excluded
Pedernales SLOT_4 candidates prioritized if present
reports generated
tests pass
physical claims remain blocked
```

---

## 11. Final principle

```txt
Phygn must not drown the reviewer.
It must hand them the few passages that can change the state.
```
