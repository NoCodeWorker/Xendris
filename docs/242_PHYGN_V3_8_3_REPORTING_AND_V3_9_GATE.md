# Phygn v3.8.3 — Reporting & v3.9 Gate

## 0. Purpose

This document defines v3.8.3 reports and when v3.9 may run.

---

## 1. Required reports

Generate:

```txt
reports/priority_packet_review/phi_gradient_priority_packet_review_summary_v3_8_3.md
reports/priority_packet_review/phi_gradient_validation_ready_extract_pack_v3_8_3.md
reports/priority_packet_review/phi_gradient_review_decisions_v3_8_3.md
reports/priority_packet_review/phi_gradient_rejected_priority_items_v3_8_3.md
reports/priority_packet_review/phi_gradient_analogy_only_items_v3_8_3.md
reports/priority_packet_review/phi_gradient_manual_review_queue_v3_8_3.md
reports/priority_packet_review/phi_gradient_next_source_pressure_gate_v3_8_3.md
reports/campaigns/PHI-GRADIENT-PRIORITY-PACKET-REVIEW-v3_8_3.md
```

---

## 2. Report requirements

Reports must include:

```txt
input priority packet count
expanded Pedernales SLOT_4 count
promoted validation-ready count
rejected count
manual review count
analogy-only count
slot coverage
source coverage
ready_for_v3_9
canonical status
blocked claims
discipline note
```

---

## 3. Canonical statuses

Add:

```txt
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_COMPLETED
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_PARTIAL
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_READY_FOR_SOURCE_PRESSURE
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_MANUAL_REVIEW_REQUIRED
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_NO_VALIDATION_READY_EXTRACTS
PHI_GRADIENT_PRIORITY_PACKET_REVIEW_BLOCKED_MISSING_INPUTS
```

If validation-ready extracts exist:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: REAL_SOURCE_EXTRACTS_UNVALIDATED
Support Level: UNSUPPORTED
Risk Level: SCIENTIFIC_RISK
Blocked Reasons:
  SOURCE_PRESSURE_DECISION_PENDING
  MISSING_VALIDATED_SOURCE_SUPPORT
  MISSING_BENCHMARK_DECISION
```

If no validation-ready extracts exist:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: SYNTHETIC_ONLY
Support Level: SYNTHETIC
Risk Level: TECHNICAL_RISK
Blocked Reasons:
  MISSING_VALIDATION_READY_EXTRACTS
  HUMAN_REVIEW_REQUIRED
  MISSING_VALIDATED_SOURCE_SUPPORT
```

---

## 4. Allowed claims

Allowed:

```txt
Priority packet items were reviewed.
Some extracts were promoted to validation-ready status.
v3.9 may run as a decision gate if validation-ready extracts exist.
```

Blocked:

```txt
Validation-ready extract supports PHI_GRADIENT.
v3.8.3 proves a physical mechanism.
v3.8.3 grants benchmark support.
PHI_GRADIENT is validated.
Frontera C is validated.
```

---

## 5. v3.9 readiness

v3.9 may run if:

```txt
ready_for_v3_9 = true
validation_ready_count >= 1
```

But v3.9 must decide among:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
```

v3.9 must be allowed to hurt or block PHI_GRADIENT.

---

## 6. Final principle

```txt
v3.8.3 prepares judgment.
v3.9 performs judgment.
```
