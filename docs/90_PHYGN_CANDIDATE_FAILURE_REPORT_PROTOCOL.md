# Phygn v1.5 — Candidate Failure Report Protocol

## 0. Purpose

This document defines how v1.5 reports candidate failure or survival.

The report must be honest even if the result is disappointing.

---

## 1. Report path

```txt
reports/prediction_pressure/CAND-FC-B-NEGCTRL-001_failure_report_v1_5.md
```

---

## 2. Required sections

```txt
candidate summary
benchmark summary
baseline equation
candidate equation
parameter table
delta results
alpha sweep
detectability result
failure conditions triggered
allowed claims
blocked claims
next action
```

---

## 3. Candidate summary

Must include:

```txt
candidate_id
candidate_family
candidate_term
observable
parameter_status
source_support_status
benchmark_status
```

---

## 4. Failure condition mapping

### Undetectable default

If default alpha gives:

```txt
Delta_max <= epsilon_exp
```

then:

```txt
FAIL_UNDETECTABLE_DELTA
```

Allowed language:

```txt
The default candidate is synthetically undetectable under the declared threshold.
```

---

### Alpha too large

If detectability requires huge alpha:

```txt
REQUIRES_UNPHYSICAL_ALPHA
```

Allowed language:

```txt
The B-suppressed candidate requires an unconstrained/extreme alpha to become visible.
```

---

### No y_true

If no benchmark data:

```txt
FAIL_NO_BENCHMARK
```

Allowed language:

```txt
PredictiveGain cannot be computed.
```

---

### No sources

If no source support:

```txt
FAIL_NO_SOURCE_SUPPORT
```

Allowed language:

```txt
The candidate remains toy-level and cannot claim physical interpretation.
```

---

## 5. Candidate survival statuses

```txt
SURVIVES_AS_TOY_NEGATIVE_CONTROL
SURVIVES_PENDING_BENCHMARK
FAILS_DEFAULT_DETECTABILITY
FAILS_PARAMETER_REASONABLENESS
BLOCKED_PHYSICAL_INTERPRETATION
```

---

## 6. Recommended default conclusion

For B-suppressed candidate:

```txt
CAND-FC-B-NEGCTRL-001 is expected to survive mainly as a negative control unless an independently justified alpha exists.
```

This is valuable because:

```txt
negative controls calibrate the system
```

but it is not:

```txt
positive physical prediction
```

---

## 7. Final principle

```txt
Failure is information.
A hidden failure is corruption.
```
