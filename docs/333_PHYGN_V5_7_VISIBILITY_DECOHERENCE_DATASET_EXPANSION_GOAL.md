# Phygn v5.7 — Visibility/Decoherence Dataset Expansion Goal

## 0. Context

The latest occupied result document is:

```txt
docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md
```

Therefore v5.7 starts at:

```txt
333
```

v5.6 disposition:

```txt
LOG_BOUNDARY_ARCHIVED_AS_VALIDATION_CANDIDATE
```

Allowed next phase:

```txt
v5.7 - Visibility/Decoherence Dataset Expansion
```

---

## 1. Non-negotiable interpretation

LOG_BOUNDARY is archived as a validation candidate.

It may be retained only as:

```txt
benchmark fixture
negative-control fixture
pipeline regression fixture
```

It must not be restored as an active candidate during v5.7.

---

## 2. Core rule

```txt
Dataset expansion is not candidate rescue.
```

The purpose of v5.7 is to build a stronger empirical testing domain, not to save LOG_BOUNDARY.

---

## 3. Mission

Implement:

```txt
v5.7 — Visibility/Decoherence Dataset Expansion
```

The mission is to expand the accepted y_true dataset beyond the single-source N=4 Hackermueller FIG. 2 dataset by identifying, locating, extracting and normalizing additional visibility/decoherence observables from resolved and/or newly resolved sources.

---

## 4. Primary objective

Create a multi-source visibility/decoherence y_true expansion pipeline that can produce:

```txt
accepted_ytrue_count_total
independent_source_count
observable_class_distribution
source_provenance_matrix
dataset_quality_flags
benchmark_readiness_decision
```

---

## 5. Required scientific boundary

Do not validate Frontera C.

Do not validate LOG_BOUNDARY.

Do not compute a Frontera C PredictiveGain claim.

Do not run C-structure ablation.

Do not create physical claims.

Do not claim invariant confirmation.

---

## 6. Target observable classes

Allowed observable classes:

```txt
VISIBILITY
FRINGE_VISIBILITY
INTERFERENCE_CONTRAST
CONTRAST_DECAY
COHERENCE_LOSS
DECOHERENCE_RATE
PHASE_DECAY
THERMAL_DECOHERENCE_VISIBILITY
MATTER_WAVE_VISIBILITY
COLLISIONAL_DECOHERENCE_RATE
```

Context-only classes:

```txt
MASS_REGIME
TIME_REGIME
SEPARATION_REGIME
TEMPERATURE_REGIME
PRESSURE_REGIME
HEATING_POWER
VELOCITY_REGIME
MATERIAL_REGIME
```

Context-only classes may be conditions, not y_true.

---

## 7. Minimum useful success

Minimal success:

```txt
accepted_ytrue_count_total >= 5
independent_source_count >= 1
```

Strong success:

```txt
accepted_ytrue_count_total >= 10
independent_source_count >= 2
```

Benchmark expansion success:

```txt
accepted_ytrue_count_total >= 10
independent_source_count >= 2
at least one out-of-source split possible
```

---

## 8. Inputs

Load:

```txt
docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md
data/frontera_c/disposition/log_boundary_candidate_disposition_v5_6.json
data/frontera_c/disposition/v5_6_next_research_direction.json
data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json
data/frontera_c/ytrue/log_boundary_ytrue_dataset_v5_3.json
data/frontera_c/ytrue/log_boundary_ytrue_extraction_audit_trail_v5_3.json
data/preflight/source_identity/source_identity_resolution_integrated_v5_1.json
data/frontera_c/source_availability_matrix_v5_2.json
data/real_sources/source_hashes_v3_6.json
```

Local PDFs:

```txt
data/real_sources/pdfs/
```

---

## 9. Target source pool

Start with already resolved sources:

```txt
Hackermueller 2004
Hornberger 2003
Nimmrichter 2011
Pedernales 2019
Schrinski 2020
```

Also prepare optional lookup queue for additional sources if current local PDFs cannot produce enough new observables.

---

## 10. Benchmarking stack requirement

v5.7 must introduce or harden the official benchmark stack:

```txt
pandas
numpy
scikit-learn
scipy
pydantic
pytest
matplotlib
```

Core modules to create or update:

```txt
phyng/benchmarking/
  __init__.py
  datasets.py
  metrics.py
  baselines.py
  controls.py
  cross_validation.py
  leakage.py
  reports.py
```

Philosophy:

```txt
Pandas/NumPy prepare the evidence.
Scikit-Learn tries to destroy the predictive illusion.
```

---

## 11. Required outputs

Create:

```txt
data/frontera_c/dataset_expansion/visibility_decoherence_source_pool_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_observable_location_candidates_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_ytrue_candidates_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_accepted_ytrue_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_rejected_ytrue_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_dataset_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_dataset_quality_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_benchmark_readiness_v5_7.json
data/frontera_c/dataset_expansion/v5_7_next_gate_decision.json
```

---

## 12. Final statuses

Emit exactly one:

```txt
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_COMPLETED
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_THRESHOLD_REACHED
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_PARTIAL
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_BLOCKED_NO_NEW_OBSERVABLES
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_BLOCKED_NO_ACCEPTED_YTRUE
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_REQUIRES_HUMAN_FIGURE_REVIEW
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_REQUIRES_SOURCE_LOOKUP
FRONTERA_C_REQUIRES_DATASET_EXPANSION
```

---

## 13. Next-gate logic

If:

```txt
accepted_ytrue_count_total >= 10
independent_source_count >= 2
```

then permit:

```txt
v5.8 — Multi-Source Benchmark & Out-of-Source Control Gate
```

If:

```txt
0 < accepted_ytrue_count_total < 10
```

then continue only to:

```txt
Targeted visibility/decoherence expansion
```

If:

```txt
accepted_ytrue_count_total == 0
```

then stop with:

```txt
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_BLOCKED_NO_ACCEPTED_YTRUE
```

---

## 14. Final principle

```txt
No more single-source smoke-test authority.
Build the benchmark field before judging candidates again.
```
