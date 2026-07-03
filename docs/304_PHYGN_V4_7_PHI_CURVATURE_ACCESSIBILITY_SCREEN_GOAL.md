# Phygn v4.7 — PHI_CURVATURE Source/y_true Accessibility Screen Goal

## 0. Context

The latest confirmed result document is:

```txt
docs/303_PHYGN_V4_6_CANDIDATE_FREEZE_REVIEW_RESULTS.md
```

Therefore, v4.7 starts at:

```txt
304
```

v4.6 produced:

```txt
PHI_GRADIENT_FREEZE_REVIEW_COMPLETED
PHI_GRADIENT_PIVOT_TO_NEXT_CANDIDATE
PHI_GRADIENT_REDEFINED_AS_METHOD_ONLY
required_label = METHOD_ONLY_EMPIRICALLY_UNGROUNDED
```

v4.6 selected:

```txt
PHI_CURVATURE
```

as the next candidate family because it appeared to have:

```txt
medium y_true accessibility
high experimental feasibility
plausible public dataset availability
better contact-with-reality potential than PHI_GRADIENT
```

v4.7 must screen that claim before starting a full pipeline.

---

## 1. Core thesis

```txt
Select the next candidate for contact with reality, not elegance in isolation.
```

---

## 2. Hard rule

```txt
Do not rebuild the full pipeline for the next candidate until y_true accessibility survives screening.
```

This means:

```txt
No full source-pressure campaign yet.
No full benchmark construction yet.
No model comparison yet.
No PredictiveGain.
No physical claim.
```

---

## 3. Mission

Implement:

```txt
v4.7 — PHI_CURVATURE Source/y_true Accessibility Screen
```

The screen must answer:

```txt
Does PHI_CURVATURE have realistic access to source-backed observables and y_true?
```

The decision outputs must be one of:

```txt
PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED
PHI_CURVATURE_ACCESSIBILITY_SCREEN_PARTIAL
PHI_CURVATURE_ACCESSIBILITY_SCREEN_FAILED
PHI_CURVATURE_REQUIRES_EXPERIMENT_BEFORE_PIPELINE
PHI_CURVATURE_REJECTED_NO_REALITY_CONTACT
```

---

## 4. Screening dimensions

Evaluate PHI_CURVATURE across:

```txt
source-locatable literature
observable clarity
y_true accessibility
public dataset availability
supplementary data plausibility
SLOT_4 independence
experimental feasibility
required apparatus
measurement sensitivity
claim risk
pipeline reuse value
```

---

## 5. Required inputs

Load:

```txt
data/candidate_decisions/next_candidate_family_selection_matrix_v4_6.json
data/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.json
data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json
data/candidate_decisions/phi_gradient_final_claim_permissions_v4_6.json
data/candidate_decisions/phi_gradient_experiment_requirement_v4_6.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
```

Optionally inspect historical PHI_CURVATURE artifacts from:

```txt
data/synthetic_benchmark_design/
data/closed_loop/
data/source_pressure/
data/benchmarks/
reports/
docs/
```

If v4.6 pivot decision is missing:

```txt
PHI_CURVATURE_ACCESSIBILITY_BLOCKED_MISSING_PIVOT_DECISION
```

---

## 6. Outputs

Create:

```txt
data/candidate_screening/phi_curvature_screening_inputs_v4_7.json
data/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_public_dataset_screen_v4_7.json
data/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.json
data/candidate_screening/phi_curvature_claim_risk_screen_v4_7.json
data/candidate_screening/phi_curvature_screening_decision_v4_7.json
```

---

## 7. Statuses

```txt
PHI_CURVATURE_ACCESSIBILITY_SCREEN_COMPLETED
PHI_CURVATURE_ACCESSIBILITY_BLOCKED_MISSING_PIVOT_DECISION
PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED
PHI_CURVATURE_ACCESSIBILITY_SCREEN_PARTIAL
PHI_CURVATURE_ACCESSIBILITY_SCREEN_FAILED
PHI_CURVATURE_REQUIRES_EXPERIMENT_BEFORE_PIPELINE
PHI_CURVATURE_REJECTED_NO_REALITY_CONTACT
```

Expected conservative status:

```txt
PHI_CURVATURE_ACCESSIBILITY_SCREEN_PARTIAL
```

unless explicit accessibility evidence exists.

---

## 8. Pass criteria

PHI_CURVATURE may pass only if at least two of the following are true:

```txt
source_accessibility >= MEDIUM
observable_clarity >= MEDIUM
y_true_accessibility >= MEDIUM
public_dataset_availability >= PLAUSIBLE
experimental_feasibility >= MEDIUM
slot4_independence = TRUE
```

Additionally:

```txt
claim_risk must not be HIGH unless screen result is PARTIAL or EXPERIMENT_REQUIRED
```

---

## 9. Fail criteria

Fail or reject if:

```txt
no source-locatable literature
no measurable observable
no plausible y_true path
no public or experimental path
SLOT_4 dependency remains unresolved
claim risk HIGH with no mitigation
```

---

## 10. Acceptance criteria

v4.7 is complete when:

```txt
v4.6 pivot decision loaded
PHI_CURVATURE screening inputs generated
source accessibility screen generated
observable accessibility screen generated
y_true accessibility screen generated
public dataset screen generated
experimental feasibility screen generated
claim risk screen generated
screening decision generated
reports generated
tests pass
no PredictiveGain created
no y_true claimed
no physical claim upgraded
PHI_GRADIENT remains method-only
SLOT_4 debt remains open and scoped
```

---

## 11. Final principle

```txt
A candidate is worth a pipeline only if it has a path to observed truth.
```
