# Phygn v1.5 — Delta & Detectability Protocol

## 0. Purpose

This protocol defines how Phygn evaluates whether a candidate differs detectably from a baseline.

---

## 1. Delta definition

For a shared observable:

\[
\Delta(t)=V_C(t)-V_{base}(t)
\]

Magnitude:

\[
|\Delta(t)|
\]

Maximum:

\[
\Delta_{max}=\max_t |\Delta(t)|
\]

---

## 2. Detectability rule

Given:

```txt
epsilon_exp
```

then:

```txt
if Delta_max > epsilon_exp:
    DETECTABLE_SYNTHETIC_DELTA
else:
    UNDETECTABLE_SYNTHETIC_DELTA
```

If no threshold:

```txt
NO_THRESHOLD_DECLARED
```

---

## 3. Important interpretation

Detectability is not correctness.

```txt
detectable delta != true model
undetectable delta != false theory
```

Detectability only means:

```txt
the candidate produces a difference large enough to be seen under the declared threshold.
```

---

## 4. Synthetic vs physical

If benchmark provenance is:

```txt
SYNTHETIC
```

then detectable status is:

```txt
toy/synthetic only
```

It cannot unlock:

```txt
physical prediction
PredictiveGain
theory validation
```

---

## 5. Alpha sweep protocol

For each alpha:

```txt
compute DeltaGamma_C
compute Delta_max
classify detectability
classify alpha scale
record failure conditions
```

Recommended alpha classifications:

```txt
alpha <= 1e6:
    ALPHA_REASONABLE_TOY

1e6 < alpha <= 1e20:
    ALPHA_LARGE

1e20 < alpha <= 1e35:
    ALPHA_EXTREME

alpha > 1e35:
    ALPHA_UNPHYSICAL_OR_UNCONSTRAINED
```

These thresholds are heuristic and must be labeled as toy classification.

---

## 6. Failure modes

### FAIL_UNDETECTABLE_DELTA

Triggered when:

```txt
Delta_max <= epsilon_exp
```

### REQUIRES_UNPHYSICAL_ALPHA

Triggered when detectability appears only at:

```txt
ALPHA_UNPHYSICAL_OR_UNCONSTRAINED
```

### FAIL_NO_BENCHMARK

Triggered when:

```txt
y_true is None
```

### FAIL_NO_SOURCE_SUPPORT

Triggered when:

```txt
source_ids = []
```

### FAIL_PARAMETER_UNDERIDENTIFIED

Triggered when:

```txt
alpha is free and not source-backed/pre-registered
```

---

## 7. Allowed report language

Allowed:

```txt
The candidate is synthetically undetectable under default alpha.
The candidate requires extreme alpha for synthetic detectability.
The candidate remains physically blocked.
```

Blocked:

```txt
The candidate predicts decoherence.
Frontera C is validated.
Synthetic detectability proves physical effect.
```

---

## 8. Final principle

```txt
A visible delta is only an invitation to test, not a proof.
```
