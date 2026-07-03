# Phygn v4.8 — PHI_CURVATURE Minimal Source/y_true Campaign Goal

## 0. Context

The latest confirmed result document is:

```txt
D:\BIOCULTOR\PHYNG\docs\309_PHYGN_V4_7_PHI_CURVATURE_ACCESSIBILITY_SCREEN_RESULTS.md
```

Therefore, v4.8 starts at:

```txt
310
```

v4.7 produced:

```txt
PHI_CURVATURE_ACCESSIBILITY_SCREEN_COMPLETED
PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED
allowed_next_phase = v4.8 — PHI_CURVATURE Minimal Source/y_true Campaign
```

Screening result:

```txt
source_accessibility = HIGH
observable_clarity = HIGH
y_true_accessibility = MEDIUM
public_dataset_availability = PLAUSIBLE
experimental_feasibility = HIGH
slot4_independence = TRUE
claim_risk = LOW
```

Known promising refs from v4.7:

```txt
Phys. Rev. A 102, 022101
Nature Physics 15, 890
```

v4.8 must transform promising references into resolvable evidence objects or reject them.

---

## 1. Core thesis

```txt
Accessibility is not evidence.
It is permission to look for evidence.
```

v4.8 is the looking phase.

---

## 2. Hard rule

```txt
No source reference without resolvable identity.
No y_true without page/table/figure/value/unit/provenance.
No PredictiveGain from accessibility.
```

---

## 3. Mission

Implement:

```txt
v4.8 — PHI_CURVATURE Minimal Source/y_true Campaign
```

Minimal means:

```txt
resolve source identities
check local/public/supplementary availability
extract candidate observables
accept/reject y_true under strict QC
produce stop/go decision
```

It does not mean:

```txt
full benchmark construction
PredictiveGain
physical validation
Frontera C validation
new theory embellishment
```

---

## 4. Required decision outputs

Final status must be one of:

```txt
PHI_CURVATURE_MINIMAL_CAMPAIGN_COMPLETED
PHI_CURVATURE_MINIMAL_CAMPAIGN_BLOCKED_MISSING_SCREEN
PHI_CURVATURE_MINIMAL_YTRUE_FOUND
PHI_CURVATURE_MINIMAL_YTRUE_THRESHOLD_REACHED
PHI_CURVATURE_NO_ACCEPTED_YTRUE_IN_MINIMAL_CAMPAIGN
PHI_CURVATURE_REQUIRES_TARGETED_SOURCE_DOWNLOAD
PHI_CURVATURE_REQUIRES_HUMAN_TABLE_REVIEW
PHI_CURVATURE_REJECTED_NO_RESOLVABLE_SOURCES
```

Threshold rule:

```txt
accepted_y_true_count >= 3 => PHI_CURVATURE_MINIMAL_YTRUE_THRESHOLD_REACHED
0 < accepted_y_true_count < 3 => PHI_CURVATURE_MINIMAL_YTRUE_FOUND
accepted_y_true_count = 0 => PHI_CURVATURE_NO_ACCEPTED_YTRUE_IN_MINIMAL_CAMPAIGN
```

---

## 5. Inputs

Load:

```txt
data/candidate_screening/phi_curvature_screening_decision_v4_7.json
data/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.json
data/candidate_screening/phi_curvature_public_dataset_screen_v4_7.json
data/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.json
data/candidate_screening/phi_curvature_claim_risk_screen_v4_7.json
data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
```

Inspect:

```txt
data/real_sources/pdfs/
data/real_sources/supplementary/
data/external_datasets/
data/phi_curvature/
reports/
docs/
```

If v4.7 passed decision is missing:

```txt
PHI_CURVATURE_MINIMAL_CAMPAIGN_BLOCKED_MISSING_SCREEN
```

---

## 6. Required outputs

Create:

```txt
data/phi_curvature/sources/phi_curvature_source_resolution_v4_8.json
data/phi_curvature/sources/phi_curvature_source_availability_v4_8.json
data/phi_curvature/evidence/phi_curvature_candidate_observables_v4_8.json
data/phi_curvature/evidence/phi_curvature_ytrue_candidates_v4_8.json
data/phi_curvature/evidence/phi_curvature_accepted_ytrue_v4_8.json
data/phi_curvature/evidence/phi_curvature_rejected_ytrue_v4_8.json
data/phi_curvature/evidence/phi_curvature_evidence_audit_trail_v4_8.json
data/phi_curvature/datasets/phi_curvature_minimal_ytrue_dataset_v4_8.json
data/phi_curvature/next/phi_curvature_v4_8_next_gate_decision.json
```

---

## 7. Acceptance criteria

v4.8 is complete when:

```txt
v4.7 screen loaded
source identities resolved or rejected
source availability assessed
candidate observables generated
y_true candidates generated
accepted/rejected y_true generated
minimal dataset generated
next gate decision generated
reports generated
tests pass
no PredictiveGain created
no physical claim upgraded
PHI_GRADIENT remains method-only
SLOT_4 remains open and scoped
```

---

## 8. Final principle

```txt
The first real victory is not a prediction.
It is one accepted observed truth.
```
