# Phygn Autonomous Roadmap — v5.7.4 to v6.4

## 0. Purpose

This document defines the autonomous roadmap from the current partial y_true dataset to a Frontera C validation decision.

---

# v5.7.4 — Targeted Human Figure/Table Review & Missing Source Completion

## Goal

Reach benchmark dataset threshold:

```txt
total_accepted_ytrue_count >= 10
independent_source_count >= 2
```

Current:

```txt
total_accepted_ytrue_count = 7
independent_source_count = 4
```

Need:

```txt
at least 3 additional accepted y_true
```

## Inputs

```txt
docs/356_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_RESULTS.md
data/frontera_c/targeted_ytrue/targeted_rejected_ytrue_v5_7_3.json
data/frontera_c/targeted_ytrue/targeted_ytrue_extraction_audit_trail_v5_7_3.json
data/frontera_c/source_download/source_download_failures_v5_7_2.json
data/frontera_c/observable_location/targeted_observed_measurement_candidates_v5_7_2.json
```

## Work

1. Review the 7 rejected candidates.
2. Prioritize candidates rejected for recoverable reasons:
   - REQUIRES_HUMAN_FIGURE_REVIEW
   - REQUIRES_UNIT_RESOLUTION
   - REQUIRES_CONDITION_MAPPING
   - NUMERIC_VALUE_MISSING but figure/table present
3. Complete missing source objects:
   - GERLICH_2011_LARGE_ORGANIC.pdf
   - ARNDT_1999_C60.pdf
4. Extract additional y_true only under strict provenance.

## Success

```txt
TARGETED_YTRUE_EXPANSION_THRESHOLD_REACHED
```

## Block

```txt
FRONTERA_C_BLOCKED_BY_INSUFFICIENT_DATA
FRONTERA_C_REQUIRES_NEW_EXPERIMENT
```

---

# v5.8 — Multi-Source Benchmark & Out-of-Source Control Gate

## Goal

Create a benchmark-ready dataset and validate that out-of-source evaluation is possible.

## Requirements

```txt
total_accepted_ytrue_count >= 10
independent_source_count >= 2
```

## Work

1. Build canonical DataFrame using Pandas.
2. Normalize units.
3. Define target variables.
4. Define feature columns.
5. Group records by source_id.
6. Create train/test strategies:
   - LeaveOneOut
   - GroupKFold by source_id
   - leave-one-source-out if possible
7. Define baseline models.
8. Assess leakage risk.

## Success

```txt
MULTI_SOURCE_BENCHMARK_READY
```

## Block

```txt
FRONTERA_C_BLOCKED_BY_BENCHMARK_FAILURE
```

---

# v5.9 — Candidate Family Reprioritization Against Expanded Dataset

## Goal

Select candidate families that may be tested against the expanded dataset.

## Candidate families

```txt
PHI_CURVATURE
PHI_LOCALIZED_WINDOW
PHI_BANDPASS
PHI_GRADIENT_AS_METHOD_ONLY
B_SUPPRESSED
QB_STRUCTURAL
THRESHOLD_SATURATION
NEW_DATA_DRIVEN_CANDIDATE_FAMILY
```

LOG_BOUNDARY remains archived as validation candidate.

## Rule

```txt
A candidate may be selected only if it can produce predictions without direct leakage from y_true.
```

## Success

```txt
CANDIDATE_FAMILY_SELECTED_FOR_PREDICTIVE_GATE
```

## Block

```txt
NO_CANDIDATE_WITH_REALITY_CONTACT
```

---

# v6.0 — Candidate Prediction Alignment & PredictiveGain Gate

## Goal

Compute model predictions and PredictiveGain against accepted y_true.

## Formula

```txt
PredictiveGain = (Error(M_base) - Error(M_C)) / Error(M_base)
```

Primary error:

```txt
RMSE
```

## Success

```txt
PREDICTIVE_GAIN_POSITIVE
```

## Block

```txt
FRONTERA_C_BLOCKED_BY_BENCHMARK_FAILURE
FRONTERA_C_BLOCKED_NO_PREDICTIVE_GAIN
```

---

# v6.1 — Negative Controls, Leakage and Simplicity Tests

## Goal

Try to destroy the positive PredictiveGain.

## Controls

```txt
mean baseline
median baseline
linear model
ridge/lasso
exponential model
monotonic interpolation
shuffled target
shuffled condition
random/null predictor
source leakage test
leave-one-source-out test
parameter-count fairness
```

## Success

```txt
NEGATIVE_CONTROLS_SURVIVED
```

## Block

```txt
FRONTERA_C_BLOCKED_BY_NEGATIVE_CONTROLS
```

---

# v6.2 — C-Structure Ablation Gate

## Goal

Test whether the predictive advantage depends on Frontera C structure.

## Required ablations

```txt
remove Q/B/u/w structure
replace C-coordinates with generic coordinates
shuffle C-features
remove invariant-derived features
candidate without C-structure
baseline with same parameter count
```

## Success

```txt
C_STRUCTURE_ABLATION_SURVIVED
```

## Block

```txt
FRONTERA_C_BLOCKED_BY_C_STRUCTURE_ABLATION_FAILURE
```

---

# v6.3 — Scientific Debt and Claim Permission Gate

## Goal

Check whether any unresolved debt blocks claims.

## Required checks

```txt
SLOT_4 debt
source provenance
dataset limits
single-domain limits
PASS_WITH_LIMITATIONS density
model fitting/leakage
negative controls
ablation status
claim scope
```

## Success

```txt
CLAIM_PERMISSION_LIMITED_VALIDATION_CANDIDATE
```

## Block

```txt
FRONTERA_C_BLOCKED_BY_SCIENTIFIC_DEBT
```

---

# v6.4 — Frontera C Validation Candidate Report or Terminal Block

## Goal

Create final decision report.

## If all gates pass

Emit:

```txt
FRONTERA_C_VALIDATION_CANDIDATE_READY
```

## If any gate fails

Emit exact blocker.

---

## Final principle

```txt
Validation is not a phase.
Validation is what remains after every permission gate has failed to kill the claim.
```
