# Phygn v3.9 — Source Pressure Decision Rules

## 0. Purpose

This document defines how validation-ready extracts produce source-pressure decisions.

---

## 1. Extract pressure classes

Each extract must be classified as one of:

```txt
SUPPORTS_BASELINE_ONLY
SUPPORTS_OBSERVABLE_ONLY
SUPPORTS_BENCHMARK_ALIGNMENT
SUPPORTS_PARAMETER_CONSTRAINT
SUPPORTS_GRADIENT_COMPONENT
CONTRADICTS_COMPONENT
LIMITS_COMPONENT
ANALOGY_ONLY
INCONCLUSIVE
IRRELEVANT_AFTER_REVIEW
```

---

## 2. Slot-level pressure

For each slot:

```txt
SLOT_1_DECOHERENCE_BASELINE
SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE
SLOT_3_BENCHMARK_RANGES
SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS
SLOT_5_PARAMETER_CONSTRAINTS
SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS
SLOT_7_EXPERIMENTAL_CONTEXT
```

Compute:

```txt
extract_count
support_count
contradiction_count
limitation_count
analogy_only_count
inconclusive_count
pressure_score
pressure_status
```

---

## 3. Pressure status values

```txt
SLOT_SOURCE_BACKED_LIMITED
SLOT_BENCHMARK_RELEVANT
SLOT_CONTRADICTED
SLOT_LIMITED
SLOT_ANALOGY_ONLY
SLOT_INCONCLUSIVE
SLOT_NO_VALID_EXTRACTS
```

---

## 4. Global decision logic

### Limited source backing

Allowed only if:

```txt
baseline/observable extracts are clean
and at least one relevant source aligns with a PHI_GRADIENT component
and no direct contradiction dominates
```

Output:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
```

### Benchmark data found

Allowed if extracts include:

```txt
observable
mass/time/visibility/pressure/temperature/range
experimental regime
```

Output:

```txt
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
```

### Contradiction

Required if extracts show:

```txt
candidate mechanism incompatible with benchmark
environmental baseline dominates away candidate effect
gradient interpretation unsupported or contradicted
parameter constraints exclude required scale
```

Output:

```txt
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
```

### Analogy-only

Required if:

```txt
extracts are scientifically relevant
but do not support or constrain PHI_GRADIENT beyond analogy/context
```

Output:

```txt
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
```

### Inconclusive

Required if:

```txt
extracts are relevant but insufficient for support or contradiction
```

Output:

```txt
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
```

---

## 5. Gradient component rule

This is the strictest rule.

```txt
No SLOT_4 validation-ready extract
→ no gradient-component support.
```

If Pedernales SLOT_4 records were analogy-only, ambiguous, rejected or manual-review:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
```

must not be based on gradient-component support.

---

## 6. Negative evidence priority

If clean negative or limitation extracts exist, they must be considered before support-like extracts.

Reason:

```txt
A hypothesis survives what could have killed it.
```

---

## 7. Source weight

Suggested source weights:

```txt
Schrinski 2020 = 1.00
Nimmrichter 2011 = 0.95
Pedernales 2019 = 0.90
Hornberger 2003 = 0.85
Hackermueller 2004 = 0.85
```

But a lower-weight contradiction may dominate a higher-weight analogy.

---

## 8. Decision confidence

Use:

```txt
LOW
MEDIUM
HIGH
```

Default:

```txt
LOW
```

unless the extract alignment is direct and slot coverage is strong.

---

## 9. Final principle

```txt
A weak positive must lose to a clean contradiction.
```
