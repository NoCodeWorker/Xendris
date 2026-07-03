# Phygn v3.8.2 — Reporting & Next Review Gate

## 0. Purpose

This document defines reports and transition rules after semantic triage.

---

## 1. Required reports

Generate:

```txt
reports/semantic_triage/phi_gradient_semantic_triage_summary_v3_8_2.md
reports/semantic_triage/phi_gradient_priority_review_packet_v3_8_2.md
reports/semantic_triage/phi_gradient_slot_review_queues_v3_8_2.md
reports/semantic_triage/phi_gradient_low_value_exclusions_v3_8_2.md
reports/semantic_triage/phi_gradient_next_gate_readiness_v3_8_2.md
reports/campaigns/PHI-GRADIENT-SEMANTIC-TRIAGE-v3_8_2.md
```

---

## 2. Report requirements

Reports must include:

```txt
input candidate count
triaged candidate count
priority packet count
critical item count
high item count
slot coverage
source coverage
Pedernales SLOT_4 coverage
validation_ready_count inherited from v3.8
ready_for_v3_9 status
blocked claims
canonical status
discipline note
```

---

## 3. Canonical status mapping

Add conservative statuses:

```txt
PHI_GRADIENT_SEMANTIC_TRIAGE_COMPLETED
PHI_GRADIENT_SEMANTIC_TRIAGE_PARTIAL
PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY
PHI_GRADIENT_SEMANTIC_TRIAGE_MANUAL_REVIEW_REQUIRED
PHI_GRADIENT_SEMANTIC_TRIAGE_NO_USEFUL_CANDIDATES
PHI_GRADIENT_SEMANTIC_TRIAGE_BLOCKED_MISSING_INPUTS
```

Recommended active status if a packet is created but no validation-ready extracts exist:

```txt
PHI_GRADIENT_SEMANTIC_TRIAGE_PACKET_READY
```

Canonical mapping:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: SYNTHETIC_ONLY
Support Level: SYNTHETIC
Risk Level: TECHNICAL_RISK
Blocked Reasons:
  HUMAN_REVIEW_REQUIRED
  VALIDATION_PENDING
  MISSING_VALIDATED_SOURCE_SUPPORT
  MISSING_BENCHMARK
```

---

## 4. Allowed claims

Allowed:

```txt
Semantic triage was performed.
A priority review packet was generated.
Candidate review was reduced to a smaller set.
Pedernales SLOT_4 was prioritized if candidate text exists.
```

Blocked:

```txt
Priority packet validates PHI_GRADIENT.
High-priority candidate is source support.
Critical candidate is evidence.
Triage score is physical support.
Frontera C is validated.
```

---

## 5. Next action

If packet count > 0 and validation_ready_count = 0:

```txt
Perform manual/AI-assisted review of priority packet.
Do not run v3.9 as positive pressure gate yet.
```

Recommended next phase:

```txt
v3.8.3 — Priority Packet Review & Validation-Ready Extract Promotion
```

Only after v3.8.3 produces validation-ready extracts should v3.9 decide source pressure.

---

## 6. Final principle

```txt
v3.8.2 chooses what deserves attention.
v3.8.3 reviews it.
v3.9 judges it.
```
