# Phygn v1.5 — Synthetic Benchmark Design for Candidate

## 0. Purpose

This document defines the synthetic benchmark for:

```txt
CAND-FC-B-NEGCTRL-001
```

against:

```txt
V_base(t)=exp(-Gamma_env * t)
```

---

## 1. Benchmark ID

```txt
BENCH-CAND-FC-B-NEGCTRL-001-SYNTH-001
```

Campaign:

```txt
CANDIDATE-vs-BASELINE-SYNTH-v1_5
```

---

## 2. Model equations

Baseline:

\[
V_{base}(t)=e^{-\Gamma_{env}t}
\]

Candidate:

\[
V_C(t)=e^{-(\Gamma_{env}+\Delta\Gamma_C)t}
\]

Candidate term:

\[
\Delta\Gamma_C=\alpha B
\]

where:

```txt
B = r_g/L
```

---

## 3. Default physical input

Use CAMPAIGN-001 / CAMPAIGN-002 mesoscopic default:

```txt
m_kg = 1e-17
L_value_m = 1e-7
B = 7.426160269118667e-38
QB = 2.612280302374279e-56
```

Default synthetic environment:

```txt
Gamma_env = 0.05
t_grid = linspace(0, 10, 101)
epsilon_exp = 1e-6
```

Default alpha values:

```txt
alpha = 1.0
alpha_sweep = [1e0, 1e10, 1e20, 1e30, 1e35, 1e38, 1e40]
```

---

## 4. Computed quantities

For each alpha:

```txt
DeltaGamma_C = alpha * B
V_base(t)
V_C(t)
delta(t)=V_C(t)-V_base(t)
abs_delta(t)
max_abs_delta
detectability_status
```

---

## 5. Error metric

If `y_true` is absent:

```txt
PredictiveGain = undefined
SyntheticGain may be computed only against synthetic y_true or declared reference.
```

Default:

```txt
synthetic_gain_status = NOT_COMPUTABLE_WITHOUT_Y_TRUE
```

---

## 6. Alpha required for detectability

Approximate condition for small extra rate:

\[
|V_C(t)-V_{base}(t)| \approx V_{base}(t)\,t\,\alpha B
\]

Therefore roughly:

\[
\alpha_{min} \approx \frac{\epsilon_{exp}}{B \cdot \max_t(t V_{base}(t))}
\]

v1.5 should compute this estimate and report:

```txt
alpha_min_for_detectability
alpha_reasonableness_status
```

Statuses:

```txt
ALPHA_REASONABLE_TOY
ALPHA_LARGE
ALPHA_EXTREME
ALPHA_UNPHYSICAL_OR_UNCONSTRAINED
```

---

## 7. Required failure checks

```txt
FAIL_UNDETECTABLE_DELTA
FAIL_NO_BENCHMARK
FAIL_NO_SOURCE_SUPPORT
FAIL_PARAMETER_UNDERIDENTIFIED
REQUIRES_UNPHYSICAL_ALPHA
```

---

## 8. Benchmark provenance

```txt
benchmark_provenance = SYNTHETIC
```

Consequences:

```txt
no physical PredictiveGain
no physical validation
no claim above toy/synthetic level
```

---

## 9. Report

Generate:

```txt
reports/benchmarks/BENCH-CAND-FC-B-NEGCTRL-001-SYNTH-001.md
reports/candidates/CAND-FC-B-NEGCTRL-001_synthetic_benchmark_v1_5.md
```

---

## 10. Final principle

```txt
The synthetic benchmark is a wind tunnel, not the sky.
```
