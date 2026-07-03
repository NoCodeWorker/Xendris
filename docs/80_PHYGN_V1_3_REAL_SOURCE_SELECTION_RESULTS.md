# Phygn v1.3 Real Source Selection & Positive Prediction Pressure — Results

Date: 2026-06-30

Source prompt:

```txt
docs/79_PHYGN_CODEX_V1_3_REAL_SOURCE_SELECTION_PROMPT.md
```

Supporting specs:

```txt
docs/74_PHYGN_V1_3_REAL_SOURCE_SELECTION_AND_POSITIVE_PRESSURE_docs/status/GOAL.md
docs/75_PHYGN_BASELINE_REAL_SOURCE_CANDIDATES.md
docs/76_PHYGN_FILLED_SOURCE_MANIFEST_DRAFT.md
docs/77_PHYGN_REAL_EXTRACT_TARGETS.md
docs/78_PHYGN_POSITIVE_PREDICTION_PRESSURE_AND_KILL_CRITERIA.md
```

Prior session:

```txt
docs/73_PHYGN_V1_2_BASELINE_SOURCE_PACK_ASSEMBLY_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v1.3 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

All acceptance criteria from `§13` of the prompt are satisfied:

| Criterion | Result |
|---|---|
| `pytest -q` passes | ✅ **312 passed, 0 failed** |
| Real source candidates are represented | ✅ 7 real candidates mapped to slots |
| Manifest draft generated | ✅ `sources/baseline/source_manifest_draft_v1_3.json` written |
| Extract targets generated | ✅ `sources/baseline/notes/extract_targets_v1_3.md` written |
| Positive prediction gate implemented | ✅ `evaluate_positive_prediction_gate` functional |
| Kill/pivot criteria implemented | ✅ `evaluate_kill_or_pivot` functional |
| Reports generated | ✅ 6 reports written across 3 directories |
| Sources remain candidate-only | ✅ All files remain `MISSING`, preventing fake ingestion |
| No physical claim is unlocked | ✅ Physical claims remain strictly blocked |

---

## 2. New and Extended Modules Implemented (v1.3)

### Evidence Layer

- [real_source_candidates.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/real_source_candidates.py)
  — Defines the `RealSourceCandidate` schema and maps the 7 real candidate sources (Schlosshauer, Paz-Zurek, Kaltenbaek MAQRO, Schut, Talbot-Lau, Arndt).

- [manifest_draft_writer.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/manifest_draft_writer.py)
  — Implements `write_filled_manifest_draft()`. Resolves local file status dynamically against the actual filesystem (evaluates to `MISSING` since no local PDFs exist yet).

- [extract_target_generator.py](file:///d:/BIOCULTOR/PHYNG/phyng/evidence/extract_target_generator.py)
  — Implements `generate_extract_targets()`. Defines explicit targets for each claim and source, emphasizing forbidden overclaims and required limits.

### Prediction Pressure Layer

- [schemas.py](file:///d:/BIOCULTOR/PHYNG/phyng/prediction_pressure/schemas.py)
  — Declares the schemas for `CandidatePredictionSpec`, `PositivePredictionGateResult`, and `KillPivotResult`.

- [positive_gate.py](file:///d:/BIOCULTOR/PHYNG/phyng/prediction_pressure/positive_gate.py)
  — Implements the 10-field check. If any field is missing, returns `POSITIVE_PREDICTION_NOT_OPERATIONALIZED`. If all are present but evidence is missing, returns `POSITIVE_PREDICTION_REQUIRES_EVIDENCE`.

- [kill_criteria.py](file:///d:/BIOCULTOR/PHYNG/phyng/prediction_pressure/kill_criteria.py)
  — Implements the decision logic for continuing the predictive track versus pivoting to structural/epistemic frameworks.

- [report.py](file:///d:/BIOCULTOR/PHYNG/phyng/prediction_pressure/report.py)
  — Handles writing prediction pressure reports.

### Campaign Layer

- [real_source_selection.py](file:///d:/BIOCULTOR/PHYNG/phyng/campaigns/real_source_selection.py)
  — CLI campaign runner for v1.3.

---

## 3. Positive Prediction Pressure Evaluation

Currently, Frontera C is evaluated as follows:
- **Positive Prediction Gate**: `POSITIVE_PREDICTION_NOT_OPERATIONALIZED` (due to missing candidate model and terms).
- **Kill/Pivot Status**: `CLAIM_GATING_ARCHITECTURE` (since it currently only acts as a negative filter blocking invalid claims).

This ensures scientific honesty: the theory must earn its predictive status by operationalizing a detectable physical candidate.

---

## 4. Reports Generated (6 total)

```txt
reports/rag/real_source_candidates_v1_3.md
reports/rag/filled_manifest_draft_v1_3.md
reports/rag/extract_targets_v1_3.md
reports/prediction_pressure/positive_prediction_gate_v1_3.md
reports/prediction_pressure/kill_pivot_criteria_v1_3.md
reports/campaigns/REAL-SOURCE-SELECTION-v1_3.md
```

---

## 5. Test Verification Summary

```
======================== 312 passed in 2.65s ========================
```

Previous baseline (v1.2): 299 passed → **+13 new tests added**.

### New test files (v1.3)

| File | Tests | All Pass |
|---|---|---|
| [test_real_source_candidates_v1_3.py](file:///d:/BIOCULTOR/PHYNG/tests/test_real_source_candidates_v1_3.py) | 2 | ✅ |
| [test_manifest_draft_writer_v1_3.py](file:///d:/BIOCULTOR/PHYNG/tests/test_manifest_draft_writer_v1_3.py) | 2 | ✅ |
| [test_extract_target_generator_v1_3.py](file:///d:/BIOCULTOR/PHYNG/tests/test_extract_target_generator_v1_3.py) | 1 | ✅ |
| [test_positive_prediction_gate_v1_3.py](file:///d:/BIOCULTOR/PHYNG/tests/test_positive_prediction_gate_v1_3.py) | 3 | ✅ |
| [test_kill_pivot_criteria_v1_3.py](file:///d:/BIOCULTOR/PHYNG/tests/test_kill_pivot_criteria_v1_3.py) | 4 | ✅ |
| [test_real_source_selection_campaign_v1_3.py](file:///d:/BIOCULTOR/PHYNG/tests/test_real_source_selection_campaign_v1_3.py) | 1 | ✅ |

---

## 6. Scientific Discipline Note

> A theory that cannot risk losing cannot earn the right to win.

We maintain strict separation between candidate models and validated physical prediction. No physical claims are unlocked.
Frontera C's status is accurately tracked, putting pressure on future phases to either operationalize a real candidate or accept demotion to a claim gating framework.
