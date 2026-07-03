# Phygn v2.5 — LOG_BOUNDARY Synthetic Detectability Report Protocol

## 0. Purpose

This document defines how to report LOG_BOUNDARY synthetic execution results.

The report must be numerically explicit and epistemically conservative.

---

## 1. Required metrics

Report:

```txt
candidate_id
candidate_family
parameter grid size
best parameter record
best max_abs_delta
epsilon_exp
detectability status
parameter reasonableness
failure conditions
canonical permission
blocked claims
next actions
```

---

## 2. Best parameter record

Include:

```txt
alpha
k
k2
u0
w0
Gamma_env
m_kg
L_m
q
b
u
w
phi_log
DeltaGamma_log
max_abs_delta
```

---

## 3. Failure conditions

Possible failures:

```txt
FAIL_UNDETECTABLE_DELTA
FAIL_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS
FAIL_DETECTABLE_ONLY_WITH_POST_HOC_TUNING
FAIL_NO_SOURCE_SUPPORT
FAIL_NO_BENCHMARK
FAIL_NO_EXPERIMENTAL_DATA
FAIL_NUMERICAL_INSTABILITY
FAIL_EMPTY_SWEEP
FAIL_INVALID_VISIBILITY_RANGE
```

---

## 4. Allowed claims

If detectable synthetically:

```txt
LOG_BOUNDARY produced a detectable synthetic delta under declared toy parameters.
LOG_BOUNDARY may proceed to source/benchmark pressure.
Candidate priority may be updated.
```

If undetectable:

```txt
LOG_BOUNDARY did not produce a detectable synthetic delta under declared toy parameters.
LOG_BOUNDARY should be down-ranked or revised unless new justification appears.
```

---

## 5. Blocked claims

Always block:

```txt
LOG_BOUNDARY predicts physical decoherence.
LOG_BOUNDARY validates Frontera C.
Synthetic delta proves a physical effect.
Toy parameter sweep establishes real-world detectability.
```

---

## 6. Canonical report section

Use v2.1 `CanonicalReportContract`.

Minimum canonical fields:

```txt
Domain Status
Canonical Permission
Blocked Reasons
Evidence Level
Support Level
Risk Level
Allowed Uses
Blocked Uses
Next Actions
Discipline Note
```

---

## 7. Final principle

```txt
The report must make the number visible and the overclaim impossible.
```
