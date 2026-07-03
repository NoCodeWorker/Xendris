# Phygn v1.4 — Candidate Model Failure Conditions

## 0. Purpose

Every Frontera C candidate must declare how it can fail.

A theory that cannot fail cannot gain predictive status.

---

## 1. Required failure conditions

Every candidate must declare:

```txt
FAIL_GAIN_NONPOSITIVE
FAIL_UNDETECTABLE_DELTA
FAIL_PARAMETER_UNDERIDENTIFIED
FAIL_AD_HOC_TERM
FAIL_DIMENSIONAL_INVALID
FAIL_NO_SOURCE_SUPPORT
FAIL_NO_BENCHMARK
```

---

## 2. Gain failure

If admissible benchmark exists:

\[
Gain_C = \frac{Error(M_{base})-Error(M_C)}{Error(M_{base})}
\]

If:

```txt
Gain_C <= 0
```

then:

```txt
FAIL_GAIN_NONPOSITIVE
```

Allowed conclusion:

```txt
The candidate does not improve the baseline under this benchmark.
```

---

## 3. Detectability failure

If:

```txt
max_abs_delta <= epsilon_exp
```

then:

```txt
FAIL_UNDETECTABLE_DELTA
```

Allowed conclusion:

```txt
The candidate is not detectable under the selected threshold.
```

---

## 4. Parameter failure

If candidate requires unconstrained parameters:

```txt
alpha free
threshold arbitrary
a,b,c fitted without prior
```

then:

```txt
FAIL_PARAMETER_UNDERIDENTIFIED
```

Allowed conclusion:

```txt
The candidate is too flexible to be predictive.
```

---

## 5. Ad hoc failure

If candidate term is chosen after seeing benchmark data without pre-registration:

```txt
FAIL_AD_HOC_TERM
```

Allowed conclusion:

```txt
The candidate is not admissible as a predictive hypothesis.
```

---

## 6. Dimensional failure

If units are inconsistent or undeclared:

```txt
FAIL_DIMENSIONAL_INVALID
```

Allowed conclusion:

```txt
The candidate is mathematically incomplete.
```

---

## 7. Source failure

If candidate physical interpretation lacks sources:

```txt
FAIL_NO_SOURCE_SUPPORT
```

Allowed conclusion:

```txt
The candidate may remain toy but cannot claim physical interpretation.
```

---

## 8. Benchmark failure

If no y_true or benchmark target:

```txt
FAIL_NO_BENCHMARK
```

Allowed conclusion:

```txt
The candidate cannot compute Predictive Gain.
```

---

## 9. Candidate failure report

Generate:

```txt
reports/prediction_pressure/candidate_failure_conditions_v1_4.md
```

Must include:

```txt
candidate id
failure modes
current triggered failures
allowed claims
blocked claims
next required actions
```

---

## 10. Final principle

```txt
A real candidate brings its own death certificate.
```
