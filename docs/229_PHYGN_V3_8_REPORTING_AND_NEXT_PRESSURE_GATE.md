# Phygn v3.8 — Reporting & Next Pressure Gate

## 0. Purpose

This document defines v3.8 reports and the next source-pressure decision gate.

---

## 1. Required reports

Generate:

```txt
reports/extract_candidate_review/phi_gradient_candidate_review_summary_v3_8.md
reports/extract_candidate_review/phi_gradient_validation_ready_pack_v3_8.md
reports/extract_candidate_review/phi_gradient_rejected_candidates_v3_8.md
reports/extract_candidate_review/phi_gradient_manual_review_queue_v3_8.md
reports/extract_candidate_review/phi_gradient_component_role_map_v3_8.md
reports/extract_candidate_review/phi_gradient_next_pressure_gate_v3_8.md
reports/campaigns/PHI-GRADIENT-EXTRACT-CANDIDATE-REVIEW-v3_8.md
```

---

## 2. Report requirements

Reports must include:

```txt
input candidate count
accepted validation-ready count
rejected candidate count
manual review queue count
component role counts
source coverage
Pedernales blocked status
canonical status
blocked claims
next actions
discipline note
```

---

## 3. Canonical status

If no validation-ready extracts:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons:
  REVIEW_PENDING
  MISSING_VALIDATION_READY_EXTRACTS
  MISSING_VALIDATED_SOURCE_SUPPORT
  MISSING_BENCHMARK
```

If validation-ready extracts exist:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons:
  VALIDATION_PENDING
  MISSING_VALIDATED_SOURCE_SUPPORT
  MISSING_EXPERIMENTAL_DATA
```

---

## 4. Allowed claims

Allowed:

```txt
Extraction candidates were reviewed.
A validation-ready extract pack was assembled.
Some candidates were rejected or queued for manual review.
```

Blocked:

```txt
Reviewed extract pack validates PHI_GRADIENT.
Validation-ready extract equals source support.
Reviewed equation equals physical support.
Benchmark candidate equals benchmark support.
Frontera C validated.
```

---

## 5. Next phase

Recommended next phase:

```txt
v3.9 — Validation-Ready Extract Gate & First Source-Pressure Decision
```

v3.9 must decide whether reviewed extracts allow:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
```

---

## 6. Optional pre-v3.9 improvement

If Pedernales remains blocked, install a PDF reader and rerun v3.7 before v3.8/v3.9:

```txt
pypdf
pdfplumber
```

Reason:

```txt
Pedernales is the highest-priority SLOT_4 gradient-component bottleneck.
```

---

## 7. Final principle

```txt
v3.8 prepares the witness.
v3.9 cross-examines it.
```
