# Phygn v2.8 — PHI_GRADIENT Source-Support & Benchmark-Data Pressure Goal

## 0. Context

The latest confirmed document is:

```txt
165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
```

Therefore, v2.8 starts at:

```txt
166
```

v2.7 found synthetic phi alternatives that do better than the saturated v2.6 formulation under control-resistance checks.

Best surviving candidate:

```txt
PHI_GRADIENT
```

v2.7 status:

```txt
PHI_CANDIDATE_SURVIVES_CONTROLS
```

Canonical interpretation:

```txt
Evidence Level: SYNTHETIC_ONLY
Support Level: SYNTHETIC
Blocked Reasons:
  MISSING_SOURCE_SUPPORT
  MISSING_BENCHMARK
  MISSING_EXPERIMENTAL_DATA
```

v2.8 applies source-support and benchmark-data pressure to PHI_GRADIENT.

---

## 1. Core thesis

```txt
A surviving synthetic form must now face the world outside the toy model.
```

v2.8 does not attempt to prove PHI_GRADIENT physically.

It asks whether external sources, baseline models, benchmarks or negative evidence constrain the candidate enough to move beyond pure synthetic survival.

---

## 2. Hard rule

```txt
Analogies are not support.
Sources must constrain the candidate, not decorate it.
```

A source is not sufficient merely because it mentions:

```txt
gradients
boundaries
decoherence
logarithms
scale
mesoscopic physics
```

A source must support or constrain at least one concrete component:

```txt
observable
baseline equation
candidate equation component
transition/boundary operator
effective rate contribution
mesoscopic benchmark
parameter range
alpha-like coupling constraint
negative/conflicting evidence
```

---

## 3. Target candidate

```txt
candidate_family: LOG_BOUNDARY
phi_family: PHI_GRADIENT
candidate_status: PHI_CANDIDATE_SURVIVES_CONTROLS
```

Key conceptual claim:

```txt
A boundary-like synthetic contribution should be represented by transition/gradient structure, not saturated amplitude.
```

This remains synthetic until source/benchmark pressure says otherwise.

---

## 4. Evidence slots

v2.8 must define and fill source/benchmark slots:

```txt
SLOT_1_DECOHERENCE_BASELINE_MODELS
SLOT_2_GRAVITATIONAL_DECOHERENCE_MODELS
SLOT_3_LOG_OR_SCALE_SPACE_FORMULATIONS
SLOT_4_GRADIENT_TRANSITION_OPERATORS
SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS
SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS
SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES
SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT
```

---

## 5. Possible outcomes

```txt
PHI_GRADIENT_SOURCE_UNSUPPORTED
PHI_GRADIENT_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_SOURCE_BACKED_LIMITED
PHI_GRADIENT_BENCHMARK_DATA_FOUND
PHI_GRADIENT_CONTRADICTED_BY_SOURCE
PHI_GRADIENT_SOURCE_PRESSURE_INCONCLUSIVE
PHI_GRADIENT_SOURCE_AUDIT_BLOCKED
```

---

## 6. Canonical interpretation

If source-backed limited:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
Evidence: SOURCE_BACKED_LIMITED
Support: SOURCE_LIMITED
Blocked: MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA
```

If benchmark data found but not experimentally validated:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
Evidence: BENCHMARK_SUPPORTED
Support: BENCHMARK
Blocked: MISSING_EXPERIMENTAL_DATA
```

If analogy only:

```txt
CanonicalPermission: REVIEW_REQUIRED or CLAIM_BLOCKED
Evidence: HEURISTIC_ONLY or SYNTHETIC_ONLY
Support: HEURISTIC or SYNTHETIC
Blocked: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK
```

If contradicted:

```txt
CanonicalPermission: CLAIM_BLOCKED
Evidence: NO_EVIDENCE
Support: UNSUPPORTED
Blocked: CONTRADICTION
```

---

## 7. Acceptance criteria

v2.8 is complete when:

```txt
source evidence schemas exist
benchmark evidence schemas exist
slot registry exists
source-support audit works
analogy-vs-support gate works
negative source handling works
benchmark-data pressure works
alpha constraint requirement exists
canonical reports generated
loop feedback generated
tests pass
physical claims remain blocked unless external evidence explicitly supports limited claims
```

---

## 8. Final principle

```txt
External pressure is not confirmation.
It is the first chance for the toy model to be constrained by reality.
```
