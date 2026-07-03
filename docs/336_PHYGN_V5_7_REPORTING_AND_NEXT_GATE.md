# Phygn v5.7 — Reporting & Next Gate

## 0. Purpose

This document defines v5.7 reporting, statuses and next-gate decisions.

---

## 1. Required reports

Generate:

```txt
reports/frontera_c/dataset_expansion/visibility_decoherence_source_pool_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_observable_location_candidates_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_ytrue_candidates_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_accepted_ytrue_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_rejected_ytrue_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_dataset_quality_v5_7.md
reports/frontera_c/dataset_expansion/visibility_decoherence_benchmark_readiness_v5_7.md
reports/campaigns/FRONTERA-C-VISIBILITY-DECOHERENCE-DATASET-EXPANSION-v5_7.md
```

---

## 2. Final result doc

Create:

```txt
docs/338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md
```

Note: the spec pack occupies 333-337. The campaign result should occupy 338.

---

## 3. Canonical statuses

Add:

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

## 4. Benchmark readiness

Create:

```txt
data/frontera_c/dataset_expansion/visibility_decoherence_benchmark_readiness_v5_7.json
```

Readiness states:

```txt
NOT_READY_NO_YTRUE
PARTIAL_SINGLE_SOURCE_ONLY
PARTIAL_N_SMALL
READY_FOR_SINGLE_SOURCE_BENCHMARK
READY_FOR_MULTI_SOURCE_BENCHMARK
READY_FOR_OUT_OF_SOURCE_CONTROL
```

Gate logic:

```txt
if independent_source_count >= 2 and accepted_ytrue_count_total >= 10:
    readiness = READY_FOR_OUT_OF_SOURCE_CONTROL
    next_phase = v5.8 — Multi-Source Benchmark & Out-of-Source Control Gate
elif accepted_ytrue_count_total > 0:
    readiness = PARTIAL_N_SMALL or READY_FOR_SINGLE_SOURCE_BENCHMARK
    next_phase = targeted dataset expansion
else:
    readiness = NOT_READY_NO_YTRUE
    next_phase = source/figure review
```

---

## 5. Blocked claims

Blocked in all cases:

```txt
Frontera C is validated
LOG_BOUNDARY is restored as active validation candidate
The invariant is empirically confirmed
Dataset expansion equals PredictiveGain
Dataset expansion equals validation
Single-source or in-source benchmark generalizes
```

---

## 6. Allowed claims

Allowed if true:

```txt
visibility/decoherence source pool was expanded
additional observable locations were found
additional y_true records were accepted
dataset quality was assessed
benchmarking stack was hardened
multi-source benchmark is ready or not ready
```

---

## 7. Final principle

```txt
Build the benchmark field before judging candidates again.
```
