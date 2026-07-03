# Phygn v4.3 — Real y_true Extraction, Source-Coverage Audit & Dataset Assembly Goal

## 0. Context

The latest confirmed document is:

```txt
D:\BIOCULTOR\PHYNG\docs\268_PHYGN_V4_2_OBSERVABLE_YTRUE_PLAN_RESULTS.md
```

Therefore, v4.3 starts at:

```txt
269
```

v4.2 produced:

```txt
PHI_GRADIENT_YTRUE_ACQUISITION_PLAN_READY
normalized_targets_count = 28
y_true_available = 0
PredictiveGain = UNDEFINED
SLOT_4 debt = OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

v4.2 identified:

```txt
VISIBILITY: manual extraction required
DECOHERENCE_RATE: manual extraction required
MASS/TIME/SEPARATION/TEMPERATURE/PRESSURE: public data search required
PARAMETER_BOUND and LIMITATION_FLAG: blocked as constraints/limits
```

v4.3 must attempt real `y_true` extraction and assemble a provenance-checked observed dataset.

---

## 1. Core thesis

```txt
No provenance, no y_true.
No y_true, no PredictiveGain.
```

v4.3 is a data-acquisition and dataset-assembly phase.

v4.3 does not validate PHI_GRADIENT by itself.

v4.3 does not relax SLOT_4 debt.

---

## 2. Hard rule

```txt
A number without provenance is not y_true.
A range without measurement is not y_true.
A figure without digitization status is not y_true.
A table value without table/page/source hash is not y_true.
A value inferred from prose is not y_true unless explicitly quantitative and traceable.
```

---

## 3. Goal

Convert:

```txt
28 normalized observable targets
y_true acquisition plan
dataset source registry
measurement readiness matrix
quality-control rules
```

into:

```txt
source coverage audit
y_true extraction candidates
manual table extraction queue
figure digitization queue
public dataset lookup queue
supplementary material lookup queue
assembled y_true dataset
blocked y_true targets
dataset quality report
next PredictiveGain gate inputs
```

---

## 4. Inputs

Load:

```txt
data/observables/phi_gradient_observable_schema_v4_2.json
data/observables/phi_gradient_normalized_observable_targets_v4_2.json
data/observables/phi_gradient_y_true_acquisition_plan_v4_2.json
data/observables/phi_gradient_dataset_source_registry_v4_2.json
data/observables/phi_gradient_measurement_readiness_matrix_v4_2.json
data/observables/phi_gradient_quality_control_rules_v4_2.json
data/observables/phi_gradient_v4_2_next_gate_inputs.json
data/benchmarks/phi_gradient_benchmark_rows_v4_0.json
data/real_sources/source_hashes_v3_6.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
```

Optionally inspect local source PDFs and supplementary-data directories:

```txt
data/real_sources/pdfs/
data/real_sources/supplementary/
data/external_datasets/
```

If required inputs are missing:

```txt
PHI_GRADIENT_YTRUE_EXTRACTION_BLOCKED_MISSING_PLAN
```

---

## 5. Outputs

Create:

```txt
data/y_true/phi_gradient_source_coverage_audit_v4_3.json
data/y_true/phi_gradient_y_true_extraction_candidates_v4_3.json
data/y_true/phi_gradient_manual_table_extraction_queue_v4_3.json
data/y_true/phi_gradient_figure_digitization_queue_v4_3.json
data/y_true/phi_gradient_public_dataset_lookup_queue_v4_3.json
data/y_true/phi_gradient_supplementary_lookup_queue_v4_3.json
data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json
data/y_true/phi_gradient_blocked_y_true_targets_v4_3.json
data/y_true/phi_gradient_dataset_quality_report_v4_3.json
data/y_true/phi_gradient_v4_3_next_predictive_gain_inputs.json
```

---

## 6. Statuses

```txt
PHI_GRADIENT_YTRUE_EXTRACTION_COMPLETED
PHI_GRADIENT_YTRUE_EXTRACTION_PARTIAL
PHI_GRADIENT_YTRUE_EXTRACTION_NO_VALUES_FOUND
PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_MANUAL_TABLE_REVIEW
PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_FIGURE_DIGITIZATION
PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_PUBLIC_DATA_LOOKUP
PHI_GRADIENT_YTRUE_EXTRACTION_BLOCKED_MISSING_PLAN
PHI_GRADIENT_YTRUE_DATASET_READY_FOR_PREDICTIVE_GAIN
```

Expected conservative status:

```txt
PHI_GRADIENT_YTRUE_EXTRACTION_PARTIAL
```

unless enough high-quality y_true values exist.

---

## 7. PredictiveGain readiness

Only set:

```txt
ready_for_predictive_gain = true
```

if:

```txt
y_true_record_count >= 1
and at least one model prediction can be matched to the same target
and units are normalized
and source provenance is complete
and QC status is PASS or PASS_WITH_LIMITATIONS
```

Otherwise:

```txt
PredictiveGain remains undefined.
```

---

## 8. SLOT_4 debt interaction

SLOT_4 remains:

```txt
OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

v4.3 must not close or weaken debt.

If y_true exists for non-SLOT_4 observables, it may support predictive evaluation only for benchmark/observable claims.

---

## 9. Acceptance criteria

v4.3 is complete when:

```txt
v4.2 observable plan loaded
source coverage audit generated
extraction queues generated
assembled y_true dataset generated, even if empty
blocked target list generated
quality report generated
next predictive-gain inputs generated
reports generated
tests pass
physical claims remain blocked
SLOT_4 debt remains open
```

---

## 10. Final principle

```txt
The first honest dataset may be mostly empty.
That is better than a full dataset of guesses.
```
