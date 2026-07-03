# Phygn v4.2 — Observable Dataset Normalization & y_true Plan Results

Date: 2026-07-01

Source prompt:
```txt
docs/267_PHYGN_CODEX_V4_2_OBSERVABLE_YTRUE_PLAN_PROMPT.md
```

Supporting specs:
```txt
docs/263_PHYGN_V4_2_OBSERVABLE_DATASET_NORMALIZATION_docs/status/GOAL.md
docs/264_PHYGN_V4_2_OBSERVABLE_SCHEMA_AND_NORMALIZATION_RULES.md
docs/265_PHYGN_V4_2_YTRUE_ACQUISITION_PLAN_SCHEMA.md
docs/266_PHYGN_V4_2_REPORTING_AND_NEXT_GATE.md
```

---

## 1. Completion Status
Status: **COMPLETE UNDER v4.2 PROMPT SPECIFICATIONS**

Final Campaign Status:
```txt
PHI_GRADIENT_YTRUE_ACQUISITION_PLAN_READY
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
68 passed (27 v3.9 tests + 14 v4.0 tests + 12 v4.1 tests + 15 v4.2 tests) in 3.10s
```

---

## 2. Observable Schema Coverage
We mapped and standardized 11 observable classes:
- **VISIBILITY** (canonical: fringe visibility, expected: float, range: [0, 1])
- **COHERENCE_LOSS** (canonical: loss of coherence, expected: float, range: >= 0)
- **DECOHERENCE_RATE** (canonical: decoherence rate, expected: float, range: >= 0)
- **CONTRAST_DECAY** (canonical: contrast decay, expected: float, range: >= 0)
- **MASS_REGIME** (canonical: mass regime, expected: float, range: > 0)
- **TIME_REGIME** (canonical: time regime, expected: float, range: > 0)
- **SEPARATION_REGIME** (canonical: separation regime, expected: float, range: > 0)
- **TEMPERATURE_PRESSURE_REGIME** (canonical: temperature and pressure regime, expected: float, range: >= 0)
- **PARAMETER_BOUND** (canonical: parameter bound, expected: float)
- **LIMITATION_FLAG** (canonical: limitation flag, expected: string)
- **EXPERIMENTAL_CONTEXT** (canonical: experimental context, expected: string)

---

## 3. Normalized Targets
- **Normalized targets count**: 28
- **y_true_required**: `True` for all targets.
- **predictive_gain_allowed**: `False` for all targets (no observed numeric outcomes yet).
- **slot4_debt_status**: `OPEN_BLOCKING_FOR_GRADIENT_CLAIMS` (enforced across all targets).

---

## 4. y_true Acquisition Plan
We mapped 28 target items into the plan. Priority allocation:
- **CRITICAL**: Visibility / Contrast Decay targets.
- **HIGH**: Decoherence Rate and Coherence Loss targets.
- **MEDIUM**: Mass/Time/Separation/Temperature/Pressure regime targets.
- **LOW**: Experimental Context targets.

Acquisition methods utilized:
- **MANUAL_TABLE_EXTRACTION** (for visibility, coherence loss, and decoherence rate).
- **PUBLIC_DATASET_LOOKUP** (for regimes).
- **NEW_EXPERIMENT_REQUIRED** (where direct measurement is unavailable).
- **NOT_ACQUIRABLE_FROM_CURRENT_SOURCES** (for bounds, limits, and contexts).

No outcomes are marked as `Y_TRUE_AVAILABLE` since no real observed numeric values exist in input files.

---

## 5. Dataset Source Registry
- **Registered source count**: 1 unique source (`SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS` or standard test references).
- **Type classification**: classified as `ARTICLE_TABLE` or `PUBLIC_REPOSITORY` based on classes.
- **Access status**: `KNOWN_LOCAL_PDF` or `NEEDS_PUBLIC_LOOKUP`.

---

## 6. Measurement Readiness Matrix
| Observable Class | Targets | y_true Available | Public Data Acquirable | Manual Extraction | Experiment Required | Blocked | Status | Next Action |
|---|---:|---:|---:|---:|---:|---:|---|---|
| `DECOHERENCE_RATE` | 2 | 0 | 0 | 2 | 0 | 0 | **MANUAL_EXTRACTION_REQUIRED** | Perform manual data extraction from source papers. |
| `VISIBILITY` | 5 | 0 | 0 | 5 | 0 | 0 | **MANUAL_EXTRACTION_REQUIRED** | Perform manual data extraction from source papers. |
| `MASS_REGIME` | 3 | 0 | 3 | 0 | 0 | 0 | **PUBLIC_DATA_SEARCH_REQUIRED** | Search public repositories for datasets. |
| `TIME_REGIME` | 3 | 0 | 3 | 0 | 0 | 0 | **PUBLIC_DATA_SEARCH_REQUIRED** | Search public repositories for datasets. |
| `SEPARATION_REGIME` | 3 | 0 | 3 | 0 | 0 | 0 | **PUBLIC_DATA_SEARCH_REQUIRED** | Search public repositories for datasets. |
| `TEMPERATURE_PRESSURE_REGIME` | 3 | 0 | 3 | 0 | 0 | 0 | **PUBLIC_DATA_SEARCH_REQUIRED** | Search public repositories for datasets. |
| `PARAMETER_BOUND` | 6 | 0 | 0 | 0 | 0 | 6 | **BLOCKED** | Observable class serves only as constraints or limits. |
| `LIMITATION_FLAG` | 3 | 0 | 0 | 0 | 0 | 3 | **BLOCKED** | Observable class serves only as constraints or limits. |
| `EXPERIMENTAL_CONTEXT` | 0 | 0 | 0 | 0 | 0 | 0 | **BLOCKED** | No targets classified in this class. |
| `COHERENCE_LOSS` | 0 | 0 | 0 | 0 | 0 | 0 | **BLOCKED** | No targets classified in this class. |
| `CONTRAST_DECAY` | 0 | 0 | 0 | 0 | 0 | 0 | **BLOCKED** | No targets classified in this class. |

---

## 7. Quality-Control Rules
Formulated 8 rules for y_true validation:
1. Unit normalization required.
2. Source hash traceability required.
3. Page/table/figure reference required.
4. Numeric uncertainty required when available.
5. Do not infer data from prose unless explicitly quantitative.
6. Figure digitization must be marked as approximate.
7. Supplementary files must be hashed.
8. Author-provided data must be provenance-tagged.

---

## 8. Allowed and Blocked Claims

### Allowed Claims:
- `Observable targets were normalized.`
- `A y_true acquisition plan was generated.`
- `PredictiveGain remains undefined until observed truth exists.`
- `SLOT_4 debt remains blocking for mechanism claims.`

### Blocked Claims:
- `PHI_GRADIENT is predictively validated.`
- `PHI_GRADIENT has PredictiveGain.`
- `Gradient mechanism is supported.`
- `Frontera C is validated.`
- `Invariant is empirically confirmed.`

---

## 9. Generated Data Artifacts
Created:
- `data/observables/phi_gradient_observable_schema_v4_2.json`
- `data/observables/phi_gradient_normalized_observable_targets_v4_2.json`
- `data/observables/phi_gradient_y_true_acquisition_plan_v4_2.json`
- `data/observables/phi_gradient_dataset_source_registry_v4_2.json`
- `data/observables/phi_gradient_measurement_readiness_matrix_v4_2.json`
- `data/observables/phi_gradient_quality_control_rules_v4_2.json`
- `data/observables/phi_gradient_v4_2_next_gate_inputs.json`

---

## 10. Generated Reports
Created:
- `reports/observables/phi_gradient_observable_schema_v4_2.md`
- `reports/observables/phi_gradient_normalized_observable_targets_v4_2.md`
- `reports/observables/phi_gradient_y_true_acquisition_plan_v4_2.md`
- `reports/observables/phi_gradient_dataset_source_registry_v4_2.md`
- `reports/observables/phi_gradient_measurement_readiness_matrix_v4_2.md`
- `reports/observables/phi_gradient_quality_control_rules_v4_2.md`
- `reports/campaigns/PHI-GRADIENT-OBSERVABLE-DATASET-YTRUE-PLAN-v4_2.md`

---

## 11. Next Phase Recommendation
- **Acquisition Plan Execution**: `v4.3 — Real y_true Extraction & Dataset Assembly`
- **Parallel Track**: `v4.1-SLOT4 — Targeted SLOT_4 Source Acquisition & Manual Review`
