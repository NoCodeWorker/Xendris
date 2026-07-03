# Phygn v3.8.3 — Priority Packet Review & Validation-Ready Extract Promotion Goal

## 0. Context

The latest confirmed document is:

```txt
D:\BIOCULTOR\PHYNG\docs\238_PHYGN_V3_8_2_SEMANTIC_TRIAGE_RESULTS.md
```

Therefore, v3.8.3 starts at:

```txt
239
```

v3.8.2 produced:

```txt
PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY
input_candidate_count = 548
priority_packet_count = 60
critical_count = 12
high_count = 47
ready_for_v3_9 = false
validation_ready_count = 0
```

v3.8.2 reduced review burden, but did not create validation-ready extracts.

v3.8.3 reviews the priority packet and promotes only clean, exact, traceable extracts to validation-ready status.

---

## 1. Core thesis

```txt
A prioritized passage is not evidence.
A reviewed exact extract is evidence-ready.
A validated extract is pressure.
```

v3.8.3 may create validation-ready extracts.

v3.8.3 must not grant source support.

v3.8.3 must not grant benchmark support.

v3.8.3 must not validate PHI_GRADIENT.

---

## 2. Goal

Convert:

```txt
60 priority review packet items
all Pedernales SLOT_4 candidates from triage map
```

into:

```txt
validation-ready exact extracts
rejected priority packet items
manual review items
analogy-only items
negative/limitation candidates
next v3.9 gate inputs
```

---

## 3. Hard rule

```txt
No promotion without exact source hash.
No promotion without page/location.
No promotion without exact text or clean extracted passage.
No promotion if role is ambiguous.
No promotion from garbage extraction.
No support granted in v3.8.3.
No physical claim.
```

---

## 4. Inputs

v3.8.3 must load:

```txt
data/real_sources/extracts/phi_gradient_semantic_triage_map_v3_8_2.json
data/real_sources/extracts/phi_gradient_priority_review_packet_v3_8_2.json
data/real_sources/extracts/phi_gradient_slot_review_queues_v3_8_2.json
data/real_sources/extracts/phi_gradient_v3_8_2_next_gate_readiness.json
data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
data/real_sources/source_hashes_v3_6.json
```

If missing:

```txt
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_BLOCKED_MISSING_INPUTS
```

---

## 5. Special Pedernales rule

Even if only one Pedernales SLOT_4 item entered the capped packet, v3.8.3 must additionally inspect:

```txt
all semantic triage records where:
source_id = SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING
assigned_slot = SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS
include_in_priority_packet = true OR priority in [CRITICAL, HIGH, MEDIUM]
```

Reason:

```txt
Pedernales is the highest-priority SLOT_4 gradient-component bottleneck.
```

---

## 6. Outputs

Create:

```txt
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json
data/real_sources/extracts/phi_gradient_priority_packet_review_decisions_v3_8_3.json
data/real_sources/extracts/phi_gradient_rejected_priority_items_v3_8_3.json
data/real_sources/extracts/phi_gradient_analogy_only_items_v3_8_3.json
data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8_3.json
data/real_sources/extracts/phi_gradient_v3_8_3_next_source_pressure_inputs.json
```

---

## 7. Statuses

```txt
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_COMPLETED
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_PARTIAL
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_READY_FOR_SOURCE_PRESSURE
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_MANUAL_REVIEW_REQUIRED
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_NO_VALIDATION_READY_EXTRACTS
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_BLOCKED_MISSING_INPUTS
```

---

## 8. v3.9 readiness rule

```txt
ready_for_v3_9 = true
```

only if:

```txt
validation_ready_count >= 1
```

But:

```txt
ready_for_v3_9 = true
```

means only:

```txt
ready for source-pressure decision
```

It does not mean:

```txt
positive source support
```

---

## 9. Acceptance criteria

v3.8.3 is complete when:

```txt
priority packet loaded
Pedernales SLOT_4 expanded inspection performed
promotion rules applied
validation-ready pack generated
rejected/analogy/manual-review files generated
next source-pressure inputs generated
reports generated
tests pass
physical claims remain blocked
```

---

## 10. Final principle

```txt
Promotion means ready to be judged, not judged.
```
