# Phygn v5.7.1 — Targeted Visibility/Decoherence Literature Acquisition Goal

## 0. Context

The latest confirmed result document is:

```txt
D:\BIOCULTOR\PHYNG\docs\338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md
```

Therefore v5.7.1 starts at:

```txt
339
```

v5.7 status:

```txt
VISIBILITY_DECOHERENCE_DATASET_EXPANSION_PARTIAL
accepted_y_true_total = 4
independent_source_count = 1
```

Current limitations:

```txt
MISSING_EXPERIMENTAL_DATA
MISSING_BENCHMARK
SOURCE_LIMITED
```

LOG_BOUNDARY remains:

```txt
ARCHIVED_AS_VALIDATION_CANDIDATE
```

---

## 1. Core rule

```txt
More literature is not more evidence.
Only source-located observables can become y_true.
```

---

## 2. Mission

Implement:

```txt
v5.7.1 — Targeted Visibility/Decoherence Literature Acquisition
```

The mission is to identify, resolve and prioritize additional independent literature sources likely to contain extractable visibility/decoherence observables.

This phase does not extract y_true.

This phase creates a high-quality acquisition queue for the next dataset expansion attempt.

---

## 3. Primary objective

Create a targeted source acquisition packet for visibility/decoherence observables.

The packet must prioritize sources that can plausibly provide:

```txt
observed visibility values
fringe contrast values
decoherence rates
contrast decay curves
visibility vs pressure/temperature/time/heating power/separation/mass
```

---

## 4. Target outcomes

Minimum success:

```txt
at least 3 candidate sources with resolvable identity
```

Useful success:

```txt
at least 3 candidate sources with resolvable identity
at least 1 candidate source with likely source-locatable observable
```

Strong success:

```txt
at least 5 candidate sources with resolvable identity
at least 2 independent candidate sources with likely source-locatable observables
```

---

## 5. What this phase is NOT

This phase is not:

```txt
y_true extraction
PredictiveGain computation
benchmark construction
LOG_BOUNDARY rescue
C-structure ablation
Frontera C validation
physical claim creation
```

---

## 6. Required inputs

Load:

```txt
docs/338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md
docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md
data/frontera_c/dataset_expansion/visibility_decoherence_dataset_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_dataset_quality_v5_7.json
data/frontera_c/dataset_expansion/visibility_decoherence_benchmark_readiness_v5_7.json
data/frontera_c/dataset_expansion/v5_7_next_gate_decision.json
data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json
data/preflight/source_identity/source_identity_resolution_integrated_v5_1.json
data/real_sources/source_hashes_v3_6.json
```

---

## 7. Search domains

The acquisition queue should target sources in:

```txt
matter-wave interferometry
molecular interferometry
decoherence in atom interferometry
thermal emission decoherence
collisional decoherence
interference visibility loss
decoherence rate measurement
CSL/macroscopicity experimental tests with visibility/contrast data
```

---

## 8. Seed source families

Prioritize sources related to or citing:

```txt
Hackermüller 2004 thermal emission decoherence
Hornberger collisional decoherence
Arndt/Zeilinger molecular interferometry
Nimmrichter macroscopicity tests
matter-wave interference visibility experiments
decoherence by gas collisions
decoherence by thermal radiation
Talbot-Lau interferometry visibility measurements
KDTLI molecular interference visibility
```

---

## 9. Required outputs

Create:

```txt
data/frontera_c/source_acquisition/visibility_decoherence_source_acquisition_queue_v5_7_1.json
data/frontera_c/source_acquisition/visibility_decoherence_candidate_source_identity_matrix_v5_7_1.json
data/frontera_c/source_acquisition/visibility_decoherence_observable_target_matrix_v5_7_1.json
data/frontera_c/source_acquisition/visibility_decoherence_download_priority_queue_v5_7_1.json
data/frontera_c/source_acquisition/visibility_decoherence_source_rejection_log_v5_7_1.json
data/frontera_c/source_acquisition/v5_7_1_next_gate_decision.json
```

---

## 10. Final statuses

Emit exactly one:

```txt
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_COMPLETED
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_PARTIAL
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_REQUIRES_HUMAN_LOOKUP
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_REQUIRES_DOWNLOAD
TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_BLOCKED_NO_CANDIDATE_SOURCES
FRONTERA_C_REQUIRES_TARGETED_DATASET_EXPANSION
```

---

## 11. Next-gate logic

If at least 3 candidate sources have resolvable identity:

```txt
permit v5.7.2 — Targeted Source Download & Observable Location Review
```

If fewer than 3 sources are resolvable:

```txt
continue human literature lookup
```

If no candidate sources are found:

```txt
stop with TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_BLOCKED_NO_CANDIDATE_SOURCES
```

---

## 12. Final principle

```txt
The next advance will not come from a better curve.
It will come from more independent observed truth.
```
