# Phygn v5.7.3 — Dataset Quality & Benchmark Readiness

## 0. Purpose

This document defines dataset quality and benchmark readiness after targeted y_true extraction.

---

## 1. Expanded dataset

Create:

```txt
data/frontera_c/targeted_ytrue/visibility_decoherence_expanded_ytrue_dataset_v5_7_3.json
```

It must include:

```txt
existing accepted y_true from v5.3
new accepted y_true from v5.7.3
deduplicated record list
source count
accepted y_true count
observable class distribution
condition distribution
QC distribution
limitation flags
```

---

## 2. Dataset quality

Create:

```txt
data/frontera_c/targeted_ytrue/visibility_decoherence_dataset_quality_v5_7_3.json
```

Schema:

```python
class DatasetQuality(BaseModel):
    dataset_id: str
    total_accepted_ytrue_count: int
    new_accepted_ytrue_count: int
    independent_source_count: int
    observable_class_distribution: dict
    qc_status_distribution: dict
    source_distribution: dict
    condition_key_distribution: dict
    limitation_flags: list[str]
    quality_status: str
    benchmark_readiness: str
    notes: list[str]
```

Quality statuses:

```txt
SINGLE_SOURCE_N_SMALL
MULTI_SOURCE_N_SMALL
MULTI_SOURCE_THRESHOLD_REACHED
REQUIRES_MORE_YTRUE
REQUIRES_MORE_SOURCES
REQUIRES_HUMAN_FIGURE_REVIEW
```

---

## 3. Benchmark readiness

Readiness states:

```txt
NOT_READY_NO_YTRUE
PARTIAL_SINGLE_SOURCE_ONLY
PARTIAL_MULTI_SOURCE_N_SMALL
READY_FOR_MULTI_SOURCE_BENCHMARK
READY_FOR_OUT_OF_SOURCE_CONTROL
```

Gate:

```txt
if total_accepted_ytrue_count >= 10 and independent_source_count >= 2:
    benchmark_readiness = READY_FOR_OUT_OF_SOURCE_CONTROL
else:
    benchmark_readiness = PARTIAL_MULTI_SOURCE_N_SMALL or PARTIAL_SINGLE_SOURCE_ONLY
```

---

## 4. Next gate decision

Create:

```txt
data/frontera_c/targeted_ytrue/v5_7_3_next_gate_decision.json
```

Fields:

```txt
final_status
new_accepted_ytrue_count
total_accepted_ytrue_count
independent_source_count
benchmark_readiness
allowed_next_phase
blocked_next_phases
rationale
```

---

## 5. Allowed next phases

If threshold reached:

```txt
v5.8 — Multi-Source Benchmark & Out-of-Source Control Gate
```

If partial:

```txt
v5.7.4 — Targeted Human Figure/Table Review
```

or:

```txt
v5.7.4 — Additional Source Download & y_true Expansion
```

If no y_true:

```txt
v5.7.4 — Human Figure Review or Supplementary Data Acquisition
```

---

## 6. Final principle

```txt
Benchmark readiness is a property of the dataset, not of the candidate.
```
