# Phygn v4.4 — Reporting & Next Gate

## 0. Purpose

This document defines v4.4 reports and transition logic.

---

## 1. Required reports

Generate:

```txt
reports/y_true_manual_extraction/phi_gradient_manual_extraction_review_records_v4_4.md
reports/y_true_manual_extraction/phi_gradient_manual_extraction_accepted_y_true_v4_4.md
reports/y_true_manual_extraction/phi_gradient_manual_extraction_rejected_v4_4.md
reports/y_true_manual_extraction/phi_gradient_manual_extraction_audit_trail_v4_4.md
reports/y_true_manual_extraction/phi_gradient_assembled_y_true_dataset_v4_4.md
reports/y_true_manual_extraction/phi_gradient_dataset_quality_report_v4_4.md
reports/y_true_manual_extraction/phi_gradient_next_predictive_gain_inputs_v4_4.md
reports/campaigns/PHI-GRADIENT-MANUAL-DATA-EXTRACTION-v4_4.md
```

---

## 2. Report requirements

Reports must include:

```txt
input manual queue count
reviewed count
accepted y_true count
rejected count
rerouted count
ready_for_predictive_gain
PredictiveGain status
matched prediction count
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
PHI_GRADIENT_MANUAL_EXTRACTION_COMPLETED
PHI_GRADIENT_MANUAL_EXTRACTION_PARTIAL
PHI_GRADIENT_MANUAL_EXTRACTION_NO_YTRUE_ACCEPTED
PHI_GRADIENT_MANUAL_EXTRACTION_READY_FOR_PREDICTIVE_GAIN
PHI_GRADIENT_MANUAL_EXTRACTION_REQUIRES_HUMAN_REVIEW
PHI_GRADIENT_MANUAL_EXTRACTION_BLOCKED_MISSING_QUEUE
```

Suggested mapping if no accepted y_true:

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
Manual data extraction was performed.
Accepted y_true records were added if QC passed.
PredictiveGain readiness was evaluated.
SLOT_4 debt remained blocking.
```

Blocked:

```txt
PHI_GRADIENT is predictively validated.
PHI_GRADIENT has PredictiveGain unless v4.5 computes it.
Gradient mechanism is supported.
SLOT_4 debt is resolved.
Frontera C is validated.
Invariant is empirically confirmed.
```

---

## 5. Possible next phases

If ready_for_predictive_gain:

```txt
v4.5 — PredictiveGain Smoke Test & Error Comparison
```

If no accepted y_true:

```txt
v4.5 — Public Dataset Acquisition & Table/Figure Review Continuation
```

If most items rerouted:

```txt
v4.5 — Figure/Supplementary/Public Data Extraction Sprint
```

Parallel:

```txt
v4.1-SLOT4 — Targeted SLOT_4 Source Acquisition & Manual Review
```

---

## 6. Final principle

```txt
A number can enter the dataset only if the claim system can audit it.
```
