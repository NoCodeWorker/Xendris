# Phygn v4.0 — Benchmark Dataset Schema

## 0. Purpose

This document defines the benchmark dataset created from v3.9 source-pressure outputs.

---

## 1. Benchmark dataset manifest

Create:

```txt
data/benchmarks/phi_gradient_benchmark_dataset_manifest_v4_0.json
```

Schema:

```python
class BenchmarkDatasetManifest(BaseModel):
    dataset_id: str
    candidate_family: str
    phi_family: str
    created_at: str
    source_pressure_ref: str
    validation_pack_ref: str
    debt_registry_ref: str
    benchmark_row_count: int
    observable_alignment_count: int
    negative_control_count: int
    excluded_claims: list[str]
    allowed_usage: list[str]
    blocked_usage: list[str]
    status: str
    notes: list[str]
```

---

## 2. Benchmark row

Create:

```txt
data/benchmarks/phi_gradient_benchmark_rows_v4_0.json
```

Schema:

```python
class BenchmarkRow(BaseModel):
    benchmark_id: str
    source_id: str
    extract_id: str
    sha256: str
    page_number: int | None
    observable_type: str
    observable_text: str
    regime_text: str
    mass_range: str | None
    time_range: str | None
    length_or_separation_range: str | None
    temperature_or_pressure: str | None
    parameter_constraints: list[str]
    limitations: list[str]
    benchmark_use: str
    allowed_model_comparison: bool
    gradient_claim_allowed: bool
```

---

## 3. Observable alignment

Create:

```txt
data/benchmarks/phi_gradient_observable_alignment_v4_0.json
```

Schema:

```python
class ObservableAlignmentRecord(BaseModel):
    alignment_id: str
    source_id: str
    extract_id: str
    observable: str
    source_observable_text: str
    phygn_observable_mapping: str
    baseline_model_mapping: str
    candidate_model_mapping: str
    alignment_status: str
    limitations: list[str]
```

Allowed alignment statuses:

```txt
OBSERVABLE_ALIGNED_LIMITED
OBSERVABLE_ALIGNED_FOR_BENCHMARK
OBSERVABLE_REQUIRES_MANUAL_REVIEW
OBSERVABLE_REJECTED
```

---

## 4. Negative-control plan

Create:

```txt
data/benchmarks/phi_gradient_negative_control_plan_v4_0.json
```

Each control:

```txt
control_id
source_id
slot_id
control_type
what_it_tests
failure_condition
expected_result_if_PHIGRADIENT_is_only_analogy
expected_result_if_candidate_has_signal
```

Control types:

```txt
BASELINE_ONLY_CONTROL
OBSERVABLE_ONLY_CONTROL
BENCHMARK_RANGE_CONTROL
PARAMETER_CONSTRAINT_CONTROL
LIMITATION_STRESS_CONTROL
NO_SLOT4_CONTROL
```

---

## 5. Blocked usage

The benchmark dataset must explicitly block:

```txt
gradient mechanism validation
physical validation
Frontera C validation
empirical confirmation of invariant
```

---

## 6. Final principle

```txt
A benchmark is allowed to compare.
It is not allowed to pretend the missing mechanism exists.
```
