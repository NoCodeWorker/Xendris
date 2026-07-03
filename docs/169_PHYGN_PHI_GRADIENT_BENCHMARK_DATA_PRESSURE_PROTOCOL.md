# Phygn v2.8 — PHI_GRADIENT Benchmark-Data Pressure Protocol

## 0. Purpose

This document defines how PHI_GRADIENT is pressured against benchmark data.

Benchmark data may be published experimental data, published numerical benchmark ranges, or locally curated baseline datasets.

---

## 1. Benchmark pressure schema

```python
class BenchmarkPressureRecord(BaseModel):
    benchmark_id: str
    source_id: str | None
    observable: str
    parameter_ranges: dict[str, tuple[float, float]]
    data_type: str
    supports_baseline: bool
    supports_candidate_component: bool
    constrains_alpha: bool
    comparable_to_phi_gradient: bool
    limitations: list[str]
    status: str
```

---

## 2. Required benchmark fields

```txt
observable
mass range
length/separation range
time range
visibility or decoherence measure
environmental decoherence baseline
uncertainty or tolerance
source citation or local dataset path
```

---

## 3. Benchmark classifications

```txt
BENCHMARK_REJECTED_NOT_COMPARABLE
BENCHMARK_BASELINE_ONLY
BENCHMARK_CONSTRAINS_ALPHA
BENCHMARK_SUPPORTS_OBSERVABLE_ONLY
BENCHMARK_SUPPORTS_COMPONENT_LIMITED
BENCHMARK_SUPPORTS_CANDIDATE_LIMITED
BENCHMARK_CONTRADICTS_CANDIDATE
```

---

## 4. Parameter pressure

PHI_GRADIENT must be pressured against:

```txt
alpha constraints
Gamma_env plausibility
m_kg range
L_m range
t_grid/time horizon
visibility decay magnitude
```

If the candidate requires:

```txt
alpha too large
Gamma_env mismatch
unrealistic L
unobserved visibility decay
```

then classify:

```txt
BENCHMARK_CONTRADICTS_CANDIDATE
```

or:

```txt
PHI_GRADIENT_SOURCE_PRESSURE_INCONCLUSIVE
```

depending on evidence strength.

---

## 5. Benchmark-supported status requirements

To reach:

```txt
PHI_GRADIENT_BENCHMARK_DATA_FOUND
```

require:

```txt
at least one comparable benchmark record
observable match
parameter range match or justified transform
documented limitation
candidate component not contradicted
```

---

## 6. Final principle

```txt
A benchmark does not need to agree with PHI_GRADIENT.
It needs to be comparable enough to hurt it.
```
