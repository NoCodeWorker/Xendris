# Phygn v2.3 — LOG_BOUNDARY Detectability & Failure Protocol

## 0. Purpose

This document defines how LOG_BOUNDARY candidates are tested synthetically.

The benchmark is allowed to report synthetic detectability.

It is not allowed to report physical validation.

---

## 1. Synthetic benchmark equations

Baseline:

```txt
V_base(t) = exp(-Gamma_env * t)
```

Candidate:

```txt
V_log(t) = exp(-(Gamma_env + DeltaGamma_log) * t)
```

Delta:

```txt
delta(t) = V_log(t) - V_base(t)
```

Detectability metric:

```txt
max_abs_delta = max_t |delta(t)|
```

Detectability status:

```txt
if max_abs_delta > epsilon_exp:
    DETECTABLE_SYNTHETIC_DELTA
else:
    UNDETECTABLE_SYNTHETIC_DELTA
```

---

## 2. Required parameter sweep

At minimum:

```txt
alpha_values
k_values
u0_values
w0_values
m_values
L_values
Gamma_env_values
```

The sweep must mark:

```txt
pre_registered_range
out_of_range
extreme_parameter
unphysical_or_unjustified_parameter
```

---

## 3. Alpha and parameter discipline

A detectable result is not enough.

Phygn must ask:

```txt
Was detectability achieved with pre-registered parameters?
Was the scale L justified?
Was the parameter chosen to maximize effect after the fact?
Is alpha constrained by source or only toy?
```

---

## 4. Failure conditions

Required failure conditions:

```txt
FAIL_NO_EXPLICIT_EQUATION
FAIL_DIMENSIONAL_INCONSISTENCY
FAIL_NO_OBSERVABLE
FAIL_NO_FAILURE_CONDITION
FAIL_AD_HOC_SCALE
FAIL_UNDETECTABLE_DELTA
FAIL_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS
FAIL_NO_SOURCE_SUPPORT
FAIL_NO_BENCHMARK
FAIL_NO_EXPERIMENTAL_DATA
```

---

## 5. Candidate survival statuses

```txt
SURVIVES_AS_SYNTHETIC_TOY_CANDIDATE
SURVIVES_AS_NEGATIVE_CONTROL
BLOCKED_FORMALIZATION_FAILURE
BLOCKED_DIMENSIONAL_FAILURE
BLOCKED_AD_HOC_PARAMETERIZATION
BLOCKED_NO_DETECTABLE_SYNTHETIC_DELTA
```

No survival status may imply physical validation.

---

## 6. Canonical interpretation

If synthetic detectable:

```txt
domain_status: DETECTABLE_SYNTHETIC_DELTA
canonical_permission: CLAIM_LIMITED_ALLOWED
evidence_level: SYNTHETIC_ONLY
support_level: SYNTHETIC
blocked_reasons:
  - MISSING_SOURCE_SUPPORT
  - MISSING_EXPERIMENTAL_DATA
```

If synthetic undetectable:

```txt
domain_status: UNDETECTABLE_SYNTHETIC_DELTA
canonical_permission: CLAIM_BLOCKED
evidence_level: SYNTHETIC_ONLY
support_level: SYNTHETIC
blocked_reasons:
  - UNDETECTABLE_DELTA
  - MISSING_EXPERIMENTAL_DATA
```

If formalization blocked:

```txt
domain_status: SYNTHETIC_BENCHMARK_BLOCKED
canonical_permission: CLAIM_BLOCKED
evidence_level: HEURISTIC_ONLY
support_level: HEURISTIC
```

---

## 7. Report language

Allowed:

```txt
The LOG_BOUNDARY candidate produced a detectable synthetic delta under declared toy parameters.
The LOG_BOUNDARY candidate is ready for source/benchmark pressure.
The LOG_BOUNDARY candidate failed synthetic detectability under declared ranges.
```

Blocked:

```txt
LOG_BOUNDARY predicts physical decoherence.
Frontera C is validated.
Synthetic detectability proves the physical effect.
```

---

## 8. Final principle

```txt
Synthetic detectability is a door to pressure testing, not a proof of nature.
```
