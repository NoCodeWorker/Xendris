# Phygn v1.4 Candidate Model Operationalization — Results

Date: 2026-06-30

Source prompt:

```txt
docs/85_PHYGN_CODEX_V1_4_CANDIDATE_MODEL_OPERATIONALIZATION_PROMPT.md
```

Supporting specs:

```txt
docs/81_PHYGN_V1_4_CANDIDATE_MODEL_OPERATIONALIZATION_docs/status/GOAL.md
docs/82_PHYGN_FRONTERA_C_CANDIDATE_TERM_DESIGN.md
docs/83_PHYGN_CANDIDATE_MODEL_FAILURE_CONDITIONS.md
docs/84_PHYGN_CANDIDATE_OBSERVABLE_AND_PARAMETER_PROTOCOL.md
```

Prior session:

```txt
docs/80_PHYGN_V1_3_REAL_SOURCE_SELECTION_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v1.4 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

All acceptance criteria from `§13` of the prompt are satisfied:

| Criterion | Result |
|---|---|
| `pytest -q` passes | ✅ **324 passed, 0 failed** |
| Candidate families exist | ✅ B_SUPPRESSED, QB_STRUCTURAL, LOG_BOUNDARY, THRESHOLD_SATURATION |
| Default candidate is generated | ✅ `CAND-FC-B-NEGCTRL-001` initialized |
| Admissibility classifier works | ✅ Dimensional unit checks, parameter constraints, and controls handled |
| Failure conditions are explicit | ✅ 7 failure modes evaluated including nonpositive gain and undetectable delta |
| Positive prediction gate updates | ✅ Transitioned to `POSITIVE_PREDICTION_REQUIRES_EVIDENCE` for the default candidate |
| Reports generated | ✅ 5 reports written |
| Physical claims remain blocked | ✅ All physical decoherence predictions remain strictly blocked |

---

## 2. New and Extended Modules Implemented (v1.4)

### Candidate Model Layer

- [schemas.py](file:///d:/BIOCULTOR/PHYNG/phyng/candidates/schemas.py)
  — Defines `CandidatePredictionSpec` containing all required parameter, unit, and verification metadata, as well as `ParameterStatus` and `AdmissibilityStatus`. Backward compatibility is preserved with flexible types.

- [term_families.py](file:///d:/BIOCULTOR/PHYNG/phyng/candidates/term_families.py)
  — Implements registry of the 4 candidate families for Frontera C (`B_SUPPRESSED`, `QB_STRUCTURAL`, `LOG_BOUNDARY`, `THRESHOLD_SATURATION`).

- [admissibility.py](file:///d:/BIOCULTOR/PHYNG/phyng/candidates/admissibility.py)
  — Implements `classify_candidate_admissibility()`. Rejects candidates missing units (`BLOCKED_DIMENSIONAL_INCOMPLETE`) or having ad hoc parameters, while admitting pre-registered controls.

- [failure_conditions.py](file:///d:/BIOCULTOR/PHYNG/phyng/candidates/failure_conditions.py)
  — Implements `evaluate_candidate_failure_conditions()`. Explicitly checks for all 7 failure states.

- [readiness.py](file:///d:/BIOCULTOR/PHYNG/phyng/candidates/readiness.py)
  — Implements `evaluate_candidate_readiness()`. Handles the state machine from `CANDIDATE_NOT_OPERATIONALIZED` to `CANDIDATE_READY_FOR_SOURCE_BACKED_BENCHMARK`.

- [report.py](file:///d:/BIOCULTOR/PHYNG/phyng/candidates/report.py)
  — Implements report writing functions for candidate characteristics.

### Campaign Layer

- [candidate_model_operationalization.py](file:///d:/BIOCULTOR/PHYNG/phyng/campaigns/candidate_model_operationalization.py)
  — CLI campaign runner for v1.4.

---

## 3. Positive Prediction Pressure Progress

Frontera C has transitioned from:
`POSITIVE_PREDICTION_NOT_OPERATIONALIZED` (v1.3)
to:
`POSITIVE_PREDICTION_REQUIRES_EVIDENCE` (v1.4)

This represents a major milestone: a concrete physical candidate (`CAND-FC-B-NEGCTRL-001`) has been formally defined. However, because source-backing and benchmark validation are missing, it remains blocked from physical claim status, maintaining complete epistemic rigor.

---

## 4. Reports Generated (5 total)

```txt
reports/candidates/candidate_term_families_v1_4.md
reports/candidates/candidate_admissibility_v1_4.md
reports/prediction_pressure/candidate_failure_conditions_v1_4.md
reports/prediction_pressure/candidate_model_readiness_v1_4.md
reports/campaigns/CANDIDATE-MODEL-OPERATIONALIZATION-v1_4.md
```

---

## 5. Test Verification Summary

```
======================== 324 passed in 2.43s ========================
```

Previous baseline (v1.3): 312 passed → **+12 new tests added**.

### New test files (v1.4)

| File | Tests | All Pass |
|---|---|---|
| [test_candidate_term_families_v1_4.py](file:///d:/BIOCULTOR/PHYNG/tests/test_candidate_term_families_v1_4.py) | 3 | ✅ |
| [test_candidate_admissibility_v1_4.py](file:///d:/BIOCULTOR/PHYNG/tests/test_candidate_admissibility_v1_4.py) | 4 | ✅ |
| [test_candidate_failure_conditions_v1_4.py](file:///d:/BIOCULTOR/PHYNG/tests/test_candidate_failure_conditions_v1_4.py) | 3 | ✅ |
| [test_candidate_model_readiness_v1_4.py](file:///d:/BIOCULTOR/PHYNG/tests/test_candidate_model_readiness_v1_4.py) | 1 | ✅ |
| [test_candidate_model_operationalization_campaign_v1_4.py](file:///d:/BIOCULTOR/PHYNG/tests/test_candidate_model_operationalization_campaign_v1_4.py) | 1 | ✅ |

---

## 6. Scientific Discipline Note

> Frontera C has not predicted yet. But now it has something that can be tested.

Physical claims remain blocked. Frontera C is now held to strict testing: it has declared its failure criteria, its required parameters, and its dimensional units. In future phases, it must face the benchmark data to compute `PredictiveGain`.
