# Phygn v4.6 — Reporting & Next Gate

## 0. Purpose

This document defines reporting and next-gate logic after candidate freeze review.

---

## 1. Required reports

Generate:

```txt
reports/candidate_decisions/phi_gradient_freeze_review_v4_6.md
reports/candidate_decisions/phi_gradient_final_claim_permissions_v4_6.md
reports/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.md
reports/candidate_decisions/phi_gradient_experiment_requirement_v4_6.md
reports/candidate_decisions/next_candidate_family_selection_matrix_v4_6.md
reports/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.md
reports/campaigns/PHI-GRADIENT-CANDIDATE-FREEZE-REVIEW-v4_6.md
```

---

## 2. Report requirements

Reports must include:

```txt
freeze status
accepted_y_true_count
PredictiveGain permission
physical claim permission
SLOT_4 debt status
method-only status
experiment requirement status
candidate family selection summary
pivot decision
allowed claims
blocked claims
required-to-unblock conditions
next recommended phase
canonical status
discipline note
```

---

## 3. Canonical statuses

Add:

```txt
PHI_GRADIENT_FREEZE_REVIEW_COMPLETED
PHI_GRADIENT_FREEZE_REVIEW_BLOCKED_MISSING_FREEZE_DECISION
PHI_GRADIENT_ARCHIVED_EMPIRICALLY_UNGROUNDED
PHI_GRADIENT_REDEFINED_AS_METHOD_ONLY
PHI_GRADIENT_REQUIRES_NEW_EXPERIMENT
PHI_GRADIENT_PIVOT_TO_NEXT_CANDIDATE
```

Suggested mapping for method-only:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: EMPIRICALLY_UNGROUNDED_METHOD_ONLY
Support Level: UNSUPPORTED_AS_PHYSICAL_MODEL
Risk Level: SCIENTIFIC_RISK
```

Suggested mapping for archive:

```txt
Canonical Permission: CLAIM_BLOCKED
Evidence Level: EMPIRICALLY_UNGROUNDED
Support Level: UNSUPPORTED
Risk Level: SCIENTIFIC_RISK
```

---

## 4. Possible next phases

If pivot candidate selected:

```txt
v4.7 — Next Candidate Source/y_true Accessibility Screen
```

If experiment required:

```txt
v4.7 — Experimental Observable Design & Feasibility Gate
```

If archived only:

```txt
v4.7 — Frontera C Candidate Family Reprioritization
```

If no candidate ready:

```txt
v4.7 — Research Program Pause / External Dataset Strategy
```

---

## 5. Allowed claims

Allowed:

```txt
PHI_GRADIENT was frozen as empirically ungrounded under current available artifacts.
PHI_GRADIENT was redefined as method-only if the decision says so.
A pivot or experiment requirement was selected according to v4.6 gate.
```

Blocked:

```txt
PHI_GRADIENT is validated.
PHI_GRADIENT has PredictiveGain.
PHI_GRADIENT is empirically supported.
PHI_GRADIENT validates Frontera C.
PHI_GRADIENT confirms the invariant.
```

---

## 6. Final principle

```txt
The pipeline must be able to convert failed evidence acquisition into better research direction.
```
