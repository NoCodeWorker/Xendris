# Phygn v4.7 — Reporting & Next Gate

## 0. Purpose

This document defines reporting for PHI_CURVATURE accessibility screening.

---

## 1. Required reports

Generate:

```txt
reports/candidate_screening/phi_curvature_screening_inputs_v4_7.md
reports/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.md
reports/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.md
reports/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.md
reports/candidate_screening/phi_curvature_public_dataset_screen_v4_7.md
reports/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.md
reports/candidate_screening/phi_curvature_claim_risk_screen_v4_7.md
reports/candidate_screening/phi_curvature_screening_decision_v4_7.md
reports/campaigns/PHI-CURVATURE-SOURCE-YTRUE-ACCESSIBILITY-SCREEN-v4_7.md
```

---

## 2. Report requirements

Reports must include:

```txt
candidate family
v4.6 pivot reference
source accessibility result
observable accessibility result
y_true accessibility result
public dataset result
experimental feasibility result
SLOT_4 independence result
claim risk result
pass/fail criteria
allowed next phase
blocked next phases
guardrails
canonical status
discipline note
```

---

## 3. Canonical statuses

Add:

```txt
PHI_CURVATURE_ACCESSIBILITY_SCREEN_COMPLETED
PHI_CURVATURE_ACCESSIBILITY_BLOCKED_MISSING_PIVOT_DECISION
PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED
PHI_CURVATURE_ACCESSIBILITY_SCREEN_PARTIAL
PHI_CURVATURE_ACCESSIBILITY_SCREEN_FAILED
PHI_CURVATURE_REQUIRES_EXPERIMENT_BEFORE_PIPELINE
PHI_CURVATURE_REJECTED_NO_REALITY_CONTACT
```

Suggested mapping if passed/partial:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: ACCESSIBILITY_SCREEN_ONLY
Support Level: NOT_YET_SUPPORTED
Risk Level: SCIENTIFIC_RISK
```

Suggested mapping if failed:

```txt
Canonical Permission: CLAIM_BLOCKED
Evidence Level: ACCESSIBILITY_SCREEN_FAILED
Support Level: UNSUPPORTED
Risk Level: SCIENTIFIC_RISK
```

---

## 4. Allowed claims

Allowed:

```txt
PHI_CURVATURE was screened for source/y_true accessibility.
The screen passed/failed/was partial according to generated criteria.
A minimal next phase was allowed if screening criteria were met.
```

Blocked:

```txt
PHI_CURVATURE is validated.
PHI_CURVATURE has PredictiveGain.
PHI_CURVATURE is empirically supported.
PHI_CURVATURE validates Frontera C.
PHI_CURVATURE confirms the invariant.
```

---

## 5. Final principle

```txt
Accessibility is not evidence.
It is permission to look for evidence.
```
