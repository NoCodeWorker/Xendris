# Phygn v3.2 — Source Pack Validation & Next Gate

## 0. Purpose

This document defines how the v3.2 seed pack feeds the next validation campaign.

v3.2 populates.

v3.3 must validate.

---

## 1. v3.2 output state

If seed files are created and structurally valid:

```txt
PHI_GRADIENT_SOURCE_PACK_POPULATED
```

Canonical interpretation:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons: MISSING_VALIDATED_SOURCE_SUPPORT, MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA
```

Allowed claim:

```txt
A reviewed source candidate pack was populated.
```

Blocked claims:

```txt
PHI_GRADIENT has real source support.
PHI_GRADIENT has benchmark support.
PHI_GRADIENT is physically validated.
PHI_GRADIENT validates Frontera C.
```

---

## 2. v3.3 next gate

Recommended next phase:

```txt
v3.3 — Source Pack Extract Validation & Slot Coverage Scoring
```

v3.3 must:

```txt
load v3.2 seed manifest
load v3.2 seed extract pack
validate extracts with v2.9 rules
score slot coverage
identify analogy-only sources
identify negative pressure
determine whether limited source-backed status is allowed
determine whether benchmark-data status is allowed
keep physical claims blocked
```

---

## 3. Positive outcomes that are possible after validation

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
```

---

## 4. Final principle

```txt
Population is not validation.
Validation is where the source pack earns or loses pressure.
```
