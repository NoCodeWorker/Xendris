# Phygn v4.7 — PHI_CURVATURE Source/y_true Accessibility Screen Results

Date: 2026-07-02

Source prompt:
```txt
docs/308_PHYGN_CODEX_V4_7_PHI_CURVATURE_ACCESSIBILITY_SCREEN_PROMPT.md
```

Supporting specs:
```txt
docs/304_PHYGN_V4_7_PHI_CURVATURE_ACCESSIBILITY_SCREEN_docs/status/GOAL.md
docs/305_PHYGN_V4_7_ACCESSIBILITY_SCREEN_PROTOCOL.md
docs/306_PHYGN_V4_7_DECISION_GATE_AND_GUARDRAILS.md
docs/307_PHYGN_V4_7_REPORTING_AND_NEXT_GATE.md
```

---

## 1. Completion Status
Status: **COMPLETE UNDER v4.7 SPRINT GOAL AND PRINCIPLES**

Final Campaign Status:
```txt
PHI_CURVATURE_ACCESSIBILITY_SCREEN_COMPLETED
```

Final Decision Status:
```txt
PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED
```

Allowed Next Phase:
```txt
v4.8 — PHI_CURVATURE Minimal Source/y_true Campaign
```

---

## 2. Screening Dimension Results

- **Source Accessibility**: `HIGH` (score `0.9`)
  - Likely domains: `quantum_optics`, `decoherence_physics`
  - Known refs: `Phys. Rev. A 102, 022101`, `Nature Physics 15, 890`
  - Blocker status: `None`
- **Observable Clarity**: `HIGH` (score `0.8`)
  - Proposed observables: `curvature_coefficient`, `phase_decay_rate`
  - Classes: `CURVATURE_PROXY`, `DECOHERENCE_RATE`
- **y_true Accessibility**: `MEDIUM` (score `0.4`)
  - Plausible sources: `literature_tables`, `supplementary_data`
- **Public Dataset Availability**: `PLAUSIBLE` (score `0.5`)
  - Plausible repo types: `ZENODO`, `FIGSHARE`
- **Experimental Feasibility**: `HIGH` (score `0.8`)
  - Required apparatus: `Phase shifter`, `Interferometer`
- **Claim Risk**: `LOW` (score `0.2`)
  - Physical claim risk: `LOW`
  - SLOT_4 dependency: `LOW` (independent)

---

## 3. Decision Rule & Gate Evaluation
- **Criteria Met**: `6 / 6`
  - `source_accessibility >= MEDIUM`
  - `observable_clarity >= MEDIUM`
  - `y_true_accessibility >= MEDIUM`
  - `public_dataset_availability >= PLAUSIBLE`
  - `experimental_feasibility >= MEDIUM`
  - `slot4_independence = TRUE`
- **Fail Criteria**: `None`
- **Decision Status**: `PASSED`

---

## 4. Required Guardrails
- `no PredictiveGain until accepted y_true exists`
- `no physical claim until source-pressure and y_true gates pass`
- `no benchmark construction before source/y_true accessibility is confirmed`
- `no SLOT_4 dependency unless explicitly resolved or scoped out`
- `no synthetic score as selection authority`
- `no full pipeline if public/manual/experimental paths remain UNKNOWN`

---

## 5. Behavior Preservation & Integrity
- **PHI_GRADIENT**: Preserved as `METHOD_ONLY_EMPIRICALLY_UNGROUNDED`.
- **SLOT_4 Debt**: Remains `OPEN_BLOCKING_FOR_GRADIENT_CLAIMS`.

---

## 6. Generated Data Artifacts
Created:
- `data/candidate_screening/phi_curvature_screening_inputs_v4_7.json`
- `data/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.json`
- `data/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.json`
- `data/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.json`
- `data/candidate_screening/phi_curvature_public_dataset_screen_v4_7.json`
- `data/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.json`
- `data/candidate_screening/phi_curvature_claim_risk_screen_v4_7.json`
- `data/candidate_screening/phi_curvature_screening_decision_v4_7.json`

---

## 7. Generated Reports
Created:
- `reports/candidate_screening/phi_curvature_screening_inputs_v4_7.md`
- `reports/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.md`
- `reports/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.md`
- `reports/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.md`
- `reports/candidate_screening/phi_curvature_public_dataset_screen_v4_7.md`
- `reports/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.md`
- `reports/candidate_screening/phi_curvature_claim_risk_screen_v4_7.md`
- `reports/candidate_screening/phi_curvature_screening_decision_v4_7.md`
- `reports/campaigns/PHI-CURVATURE-SOURCE-YTRUE-ACCESSIBILITY-SCREEN-v4_7.md`
