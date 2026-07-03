# Phygn v2.9 — Real Literature Acquisition & Source Extract Ingestion for PHI_GRADIENT Goal

## 0. Context

The latest confirmed document is:

```txt
171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
```

Therefore, v2.9 starts at:

```txt
172
```

v2.8 created the source-support and benchmark-pressure infrastructure for:

```txt
candidate_family: LOG_BOUNDARY
phi_family: PHI_GRADIENT
previous_status: PHI_CANDIDATE_SURVIVES_CONTROLS
```

v2.8 used deterministic fixtures.

Important limitation:

```txt
Fixture-backed benchmark pressure is not physical validation.
Real literature acquisition is still required.
```

v2.9 replaces fixture-based source pressure with real literature acquisition and source extract ingestion.

---

## 1. Core thesis

```txt
A fixture proves the gate works.
Only real sources can pressure the claim.
```

v2.9 must not treat fixture support as real support.

The goal is to acquire, ingest, extract and classify real sources relevant to PHI_GRADIENT.

---

## 2. Hard rule

```txt
No real source-backed status without a real extract.
No benchmark-supported status without comparable real benchmark data.
No analogy can fill a source slot.
No physical claim without experimental evidence.
```

---

## 3. Target candidate

```txt
candidate_family: LOG_BOUNDARY
phi_family: PHI_GRADIENT
candidate_status: PHI_CANDIDATE_SURVIVES_CONTROLS
previous_pressure_status: PHI_GRADIENT_BENCHMARK_DATA_FOUND fixture-based only
```

The fixture status must be treated as infrastructure validation, not evidence.

---

## 4. Required source slots

v2.9 must attempt real-source acquisition for:

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

## 5. Real-source statuses

Possible campaign statuses:

```txt
PHI_GRADIENT_REAL_SOURCES_ACQUIRED
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
PHI_GRADIENT_REAL_SOURCE_ACQUISITION_FAILED
PHI_GRADIENT_REAL_SOURCE_INGESTION_BLOCKED
```

---

## 6. Canonical interpretation

If real source-backed limited:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
Evidence: SOURCE_BACKED_LIMITED
Support: SOURCE_LIMITED
Blocked: MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA
```

If real benchmark data found:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
Evidence: BENCHMARK_SUPPORTED
Support: BENCHMARK
Blocked: MISSING_EXPERIMENTAL_DATA
```

If analogy only:

```txt
CanonicalPermission: CLAIM_BLOCKED or REVIEW_REQUIRED
Evidence: SYNTHETIC_ONLY
Support: SYNTHETIC
Blocked: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK
```

If contradicted:

```txt
CanonicalPermission: CLAIM_BLOCKED
Evidence: NO_EVIDENCE or SYNTHETIC_ONLY
Support: UNSUPPORTED or SYNTHETIC
Blocked: CONTRADICTION
```

---

## 7. Acceptance criteria

v2.9 is complete when:

```txt
real source acquisition schema exists
source manifest exists
source extract model exists
extract validation works
slot filling from real extracts works
analogy-only real sources are blocked
negative sources are recorded
benchmark comparability works with real or local records
fixture support is explicitly separated from real support
reports generated
loop feedback generated
tests pass
physical claims remain blocked
```

---

## 8. Final principle

```txt
The first real source is not confirmation.
It is the first external constraint.
```
