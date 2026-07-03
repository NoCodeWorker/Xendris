# Phygn v4.3 — Reporting & Next Gate

## 0. Purpose

This document defines reports and transition logic after y_true extraction.

---

## 1. Required reports

Generate:

```txt
reports/y_true/phi_gradient_source_coverage_audit_v4_3.md
reports/y_true/phi_gradient_y_true_extraction_candidates_v4_3.md
reports/y_true/phi_gradient_manual_table_extraction_queue_v4_3.md
reports/y_true/phi_gradient_figure_digitization_queue_v4_3.md
reports/y_true/phi_gradient_public_dataset_lookup_queue_v4_3.md
reports/y_true/phi_gradient_supplementary_lookup_queue_v4_3.md
reports/y_true/phi_gradient_assembled_y_true_dataset_v4_3.md
reports/y_true/phi_gradient_blocked_y_true_targets_v4_3.md
reports/y_true/phi_gradient_dataset_quality_report_v4_3.md
reports/campaigns/PHI-GRADIENT-REAL-YTRUE-EXTRACTION-v4_3.md
```

---

## 2. Report requirements

Reports must include:

```txt
target count
source coverage summary
candidate count
accepted y_true count
blocked target count
queue counts
QC summary
ready_for_predictive_gain
PredictiveGain status
SLOT_4 debt status
physical claim permission
allowed claims
blocked claims
next recommended phase
canonical status
discipline note
```

---

## 3. Canonical statuses

Add:

```txt
PHI_GRADIENT_YTRUE_EXTRACTION_COMPLETED
PHI_GRADIENT_YTRUE_EXTRACTION_PARTIAL
PHI_GRADIENT_YTRUE_EXTRACTION_NO_VALUES_FOUND
PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_MANUAL_TABLE_REVIEW
PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_FIGURE_DIGITIZATION
PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_PUBLIC_DATA_LOOKUP
PHI_GRADIENT_YTRUE_EXTRACTION_BLOCKED_MISSING_PLAN
PHI_GRADIENT_YTRUE_DATASET_READY_FOR_PREDICTIVE_GAIN
```

Suggested mapping if dataset not ready:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: REAL_SOURCE_PRESSURE_LIMITED
Support Level: LIMITED
Risk Level: SCIENTIFIC_RISK
```

Suggested mapping if ready for predictive gain:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: REAL_OBSERVED_YTRUE_PARTIAL
Support Level: LIMITED
Risk Level: SCIENTIFIC_RISK
```

---

## 4. Allowed claims

Allowed:

```txt
A y_true extraction attempt was performed.
A source-coverage audit was generated.
A y_true dataset was assembled if accepted records exist.
PredictiveGain remains undefined unless the minimum viable y_true threshold is met.
```

Blocked:

```txt
PHI_GRADIENT is predictively validated.
PHI_GRADIENT has PredictiveGain unless the gate says so.
Gradient mechanism is supported.
SLOT_4 debt is resolved.
Frontera C is validated.
Invariant is empirically confirmed.
```

---

## 5. Possible next phases

If enough y_true exists:

```txt
v4.4 — PredictiveGain Smoke Test & Error Comparison
```

If manual table/figure extraction dominates:

```txt
v4.4 — Manual Data Extraction Sprint
```

If public data lookup dominates:

```txt
v4.4 — Public Dataset Acquisition & Provenance Hashing
```

If no values found:

```txt
v4.4 — Experimental Feasibility or Candidate Pivot Gate
```

Parallel:

```txt
v4.1-SLOT4 — Targeted SLOT_4 Source Acquisition & Manual Review
```

---

## 6. Final principle

```txt
The next gate must not ask whether the theory is beautiful.
It must ask whether the numbers exist.
```
