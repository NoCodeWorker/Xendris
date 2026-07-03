# Phygn v5.7.3 — Reporting & Next Gate

## 0. Purpose

This document defines reports and final gate decisions for v5.7.3.

---

## 1. Required reports

Generate:

```txt
reports/frontera_c/targeted_ytrue/targeted_ytrue_candidates_v5_7_3.md
reports/frontera_c/targeted_ytrue/targeted_accepted_ytrue_v5_7_3.md
reports/frontera_c/targeted_ytrue/targeted_rejected_ytrue_v5_7_3.md
reports/frontera_c/targeted_ytrue/targeted_ytrue_extraction_audit_trail_v5_7_3.md
reports/frontera_c/targeted_ytrue/visibility_decoherence_expanded_ytrue_dataset_v5_7_3.md
reports/frontera_c/targeted_ytrue/visibility_decoherence_dataset_quality_v5_7_3.md
reports/frontera_c/targeted_ytrue/v5_7_3_next_gate_decision.md
reports/campaigns/FRONTERA-C-TARGETED-YTRUE-EXTRACTION-v5_7_3.md
```

---

## 2. Final result document

Create:

```txt
docs/356_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_RESULTS.md
```

Note:

```txt
Spec pack occupies 351-355.
Campaign result should occupy 356.
```

---

## 3. Final statuses

Emit exactly one:

```txt
TARGETED_YTRUE_EXTRACTION_COMPLETED
TARGETED_YTRUE_EXTRACTION_THRESHOLD_REACHED
TARGETED_YTRUE_EXTRACTION_PARTIAL
TARGETED_YTRUE_EXTRACTION_BLOCKED_NO_ACCEPTED_YTRUE
TARGETED_YTRUE_EXTRACTION_REQUIRES_HUMAN_FIGURE_REVIEW
TARGETED_YTRUE_EXTRACTION_REQUIRES_SUPPLEMENTARY_DATA
TARGETED_YTRUE_EXTRACTION_BLOCKED_PROVENANCE_FAILURE
FRONTERA_C_REQUIRES_DATASET_EXPANSION
```

---

## 4. Gate rules

If:

```txt
total_accepted_ytrue_count >= 10
independent_source_count >= 2
```

then:

```txt
final_status = TARGETED_YTRUE_EXTRACTION_THRESHOLD_REACHED
allowed_next_phase = v5.8 — Multi-Source Benchmark & Out-of-Source Control Gate
```

If:

```txt
new_accepted_ytrue_count > 0
```

but threshold not reached:

```txt
final_status = TARGETED_YTRUE_EXTRACTION_PARTIAL
allowed_next_phase = targeted dataset expansion
```

If:

```txt
new_accepted_ytrue_count == 0
```

then use the exact blocker:

```txt
TARGETED_YTRUE_EXTRACTION_BLOCKED_NO_ACCEPTED_YTRUE
TARGETED_YTRUE_EXTRACTION_REQUIRES_HUMAN_FIGURE_REVIEW
TARGETED_YTRUE_EXTRACTION_REQUIRES_SUPPLEMENTARY_DATA
TARGETED_YTRUE_EXTRACTION_BLOCKED_PROVENANCE_FAILURE
```

---

## 5. Blocked claims

Always blocked:

```txt
Frontera C is validated
LOG_BOUNDARY is reactivated
accepted y_true equals PredictiveGain
dataset expansion equals validation
physical claim
invariant confirmation
```

---

## 6. Allowed claims

Allowed if true:

```txt
targeted y_true extraction was attempted
new y_true records were accepted
candidate records were rejected under QC
dataset quality was assessed
v5.8 is permitted only if threshold reached
```

---

## 7. Final principle

```txt
Accepted y_true expands the field.
It does not yet judge the theory.
```
