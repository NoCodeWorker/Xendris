# Phygn v4.5 — Reporting & Next Gate

## 0. Purpose

This document defines reports and next gates after external evidence acquisition.

---

## 1. Required reports

Generate:

```txt
reports/external_evidence/phi_gradient_table_review_results_v4_5.md
reports/external_evidence/phi_gradient_supplementary_search_results_v4_5.md
reports/external_evidence/phi_gradient_public_dataset_search_results_v4_5.md
reports/external_evidence/phi_gradient_external_y_true_candidates_v4_5.md
reports/external_evidence/phi_gradient_external_y_true_accepted_v4_5.md
reports/external_evidence/phi_gradient_external_y_true_rejected_v4_5.md
reports/external_evidence/phi_gradient_external_evidence_audit_trail_v4_5.md
reports/external_evidence/phi_gradient_candidate_freeze_decision_v4_5.md
reports/y_true/phi_gradient_assembled_y_true_dataset_v4_5.md
reports/y_true/phi_gradient_next_predictive_gain_inputs_v4_5.md
reports/campaigns/PHI-GRADIENT-EXTERNAL-EVIDENCE-SPRINT-v4_5.md
```

---

## 2. Report requirements

Reports must include:

```txt
table review count
supplementary search count
public dataset search count
external candidate count
accepted y_true count
rejected y_true count
matched prediction count
ready_for_predictive_gain
freeze status
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
PHI_GRADIENT_EXTERNAL_EVIDENCE_SPRINT_COMPLETED
PHI_GRADIENT_EXTERNAL_EVIDENCE_SPRINT_PARTIAL
PHI_GRADIENT_EXTERNAL_EVIDENCE_BLOCKED_MISSING_PRIOR_ARTIFACTS
PHI_GRADIENT_EXTERNAL_EVIDENCE_NO_YTRUE_FOUND
PHI_GRADIENT_EXTERNAL_EVIDENCE_YTRUE_THRESHOLD_REACHED
PHI_GRADIENT_EXTERNAL_EVIDENCE_REQUIRES_NEW_EXPERIMENT
PHI_GRADIENT_EMPIRICALLY_UNGROUNDED_FREEZE
```

Suggested mapping if no y_true found:

```txt
Canonical Permission: CLAIM_BLOCKED
Evidence Level: REAL_SOURCE_PRESSURE_LIMITED
Support Level: UNSUPPORTED
Risk Level: SCIENTIFIC_RISK
```

Suggested mapping if threshold reached:

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
External evidence acquisition was attempted.
Accepted external y_true records were added if QC passed.
Candidate was frozen if the y_true threshold was not reached.
PredictiveGain remains undefined until computed by a later gate.
```

Blocked:

```txt
PHI_GRADIENT is validated.
PHI_GRADIENT has PredictiveGain before v4.6.
Gradient mechanism is supported.
SLOT_4 debt is resolved.
Frontera C is validated.
Invariant is empirically confirmed.
```

---

## 5. Next gates

If threshold reached:

```txt
v4.6 — PredictiveGain Smoke Test & Error Comparison
```

If frozen due no data:

```txt
v4.6 — Candidate Freeze Review & Experiment Design Decision
```

If human review needed:

```txt
v4.6 — Human Table/Figure Review Execution
```

If new experiment needed:

```txt
v4.6 — Experimental Observable Design & Feasibility Gate
```

---

## 6. Final principle

```txt
The pipeline must be able to stop without calling it failure.
```
