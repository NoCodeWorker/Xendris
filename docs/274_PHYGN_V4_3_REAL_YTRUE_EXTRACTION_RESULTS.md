# Phygn v4.3 — Real y_true Extraction, Source-Coverage Audit & Dataset Assembly Results

Date: 2026-07-01

Source prompt:
```txt
docs/273_PHYGN_CODEX_V4_3_REAL_YTRUE_EXTRACTION_PROMPT.md
```

Supporting specs:
```txt
docs/269_PHYGN_V4_3_REAL_YTRUE_EXTRACTION_docs/status/GOAL.md
docs/270_PHYGN_V4_3_SOURCE_COVERAGE_AUDIT_AND_EXTRACTION_RULES.md
docs/271_PHYGN_V4_3_YTRUE_DATASET_AND_QUALITY_SCHEMA.md
docs/272_PHYGN_V4_3_REPORTING_AND_NEXT_GATE.md
```

---

## 1. Completion Status
Status: **COMPLETE UNDER v4.3 PROMPT SPECIFICATIONS**

Final Campaign Status:
```txt
PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_MANUAL_TABLE_REVIEW
```

Predictive Gain Status:
```txt
UNDEFINED
```

SLOT_4 Debt Status:
```txt
OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

Tests run:
```txt
141 passed (all regression and unit tests pass) in 7.28s
```

---

## 2. Source Coverage Audit
We audited 28 targets against source hashes and PDF file presence.
- **`SOURCE_COVERAGE_NEEDS_TABLE_REVIEW`**: 5 targets (visibility and decoherence rate observables with local PDFs).
- **`SOURCE_COVERAGE_NEEDS_PUBLIC_DATA`**: 12 targets (regime bounds for mass, time, separation, temperature/pressure).
- **`SOURCE_COVERAGE_LOCAL_PDF_ONLY`**: 11 targets (parameter bounds and limitations).

No targets have missing hashes or missing local PDFs.

---

## 3. y_true Extraction Candidates
- **Total candidates evaluated**: 28
- **`can_enter_dataset`**: `False` for all 28 candidates.
- **Honest Extraction Summary**: No numeric measurements are extractable from the raw text extracts in `normalized_targets_v4_2.json` for base/observable classes (they contain qualitative/generic prose like *"and thus halve the interference visibility"*). Regime boundaries contain numeric values, but are rejected as y_true per rules.
- **QC Statuses**:
  - `FAIL_NO_NUMERIC_VALUE`: for visibility/decoherence rate targets with prose-only texts.
  - `FAIL_CONSTRAINT_ONLY`: for parameters/limitations/regimes.

---

## 4. Actionable Extraction Queues
Targets unable to enter the dataset were correctly distributed into 4 queues:
1. **`manual_table_extraction_queue`**: 5 items (critical/high priority visibility and decoherence rate targets).
2. **`figure_digitization_queue`**: 0 items.
3. **`public_dataset_lookup_queue`**: 12 items (medium priority mass/time/separation/temperature/pressure).
4. **`supplementary_lookup_queue`**: 11 items (low priority constraints and limits).

No targets were silently discarded.

---

## 5. Assembled y_true Dataset
- **`y_true_record_count`**: 0
- **`ready_for_predictive_gain`**: `False` (requires accepted count >= 3).
- **`PredictiveGain`**: Remains `null` (undefined).
- **`slot4_debt_status`**: `OPEN_BLOCKING_FOR_GRADIENT_CLAIMS`.
- **`physical_claim_permission`**: `BLOCKED`.

---

## 6. Dataset Quality Report
- **Readiness Status**: `YTRUE_DATASET_EMPTY_NEEDS_EXTRACTION`
- **Recommendations**:
  - Acquire additional y_true measurements to meet the minimum viable threshold (>= 3).
  - Execute manual table review sprint to extract values from local PDFs.
  - Search public repositories for regime bounds.

---

## 7. Next Gate Inputs
Created `data/y_true/phi_gradient_v4_3_next_predictive_gain_inputs.json`:
- **`ready_for_predictive_gain`**: `False`.
- **`minimum_viable_y_true_count`**: 3.
- **`recommended_next_phase`**: `"v4.4 — Manual Data Extraction Sprint"`.

---

## 8. Allowed and Blocked Claims

### Allowed Claims:
- `A y_true extraction attempt was performed.`
- `A source-coverage audit was generated.`
- `A y_true dataset was assembled if accepted records exist.`
- `PredictiveGain remains undefined unless the minimum viable y_true threshold is met.`

### Blocked Claims:
- `PHI_GRADIENT is predictively validated.`
- `PHI_GRADIENT has PredictiveGain.`
- `Gradient mechanism is supported.`
- `SLOT_4 debt is resolved.`
- `Frontera C is validated.`
- `Invariant is empirically confirmed.`

---

## 9. Generated Data Artifacts
Created:
- `data/y_true/phi_gradient_source_coverage_audit_v4_3.json`
- `data/y_true/phi_gradient_y_true_extraction_candidates_v4_3.json`
- `data/y_true/phi_gradient_manual_table_extraction_queue_v4_3.json`
- `data/y_true/phi_gradient_figure_digitization_queue_v4_3.json`
- `data/y_true/phi_gradient_public_dataset_lookup_queue_v4_3.json`
- `data/y_true/phi_gradient_supplementary_lookup_queue_v4_3.json`
- `data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json`
- `data/y_true/phi_gradient_blocked_y_true_targets_v4_3.json`
- `data/y_true/phi_gradient_dataset_quality_report_v4_3.json`
- `data/y_true/phi_gradient_v4_3_next_predictive_gain_inputs.json`

---

## 10. Generated Reports
Created:
- `reports/y_true/phi_gradient_source_coverage_audit_v4_3.md`
- `reports/y_true/phi_gradient_y_true_extraction_candidates_v4_3.md`
- `reports/y_true/phi_gradient_manual_table_extraction_queue_v4_3.md`
- `reports/y_true/phi_gradient_figure_digitization_queue_v4_3.md`
- `reports/y_true/phi_gradient_public_dataset_lookup_queue_v4_3.md`
- `reports/y_true/phi_gradient_supplementary_lookup_queue_v4_3.md`
- `reports/y_true/phi_gradient_assembled_y_true_dataset_v4_3.md`
- `reports/y_true/phi_gradient_blocked_y_true_targets_v4_3.md`
- `reports/y_true/phi_gradient_dataset_quality_report_v4_3.md`
- `reports/campaigns/PHI-GRADIENT-REAL-YTRUE-EXTRACTION-v4_3.md`
