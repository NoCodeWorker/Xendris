# Phygn v3.3 — Source Pack Extract Validation & Slot Coverage Scoring Goal

## 0. Context

The latest confirmed document is:

```txt
195_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_RESULTS.md
```

Therefore, v3.3 starts at:

```txt
196
```

v3.2 populated a reviewed real source candidate pack for PHI_GRADIENT.

v3.2 final status:

```txt
PHI_GRADIENT_SOURCE_PACK_POPULATED
```

v3.2 created:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json
```

Seed pack summary:

```txt
manifest_entries = 13
traceable_entries = 13
valid_slot_targeted_entries = 13
benchmark_candidate_sources = 5
negative_candidate_sources = 3
extract_candidates = 8
manual_review_extracts = 8
validated_support_extracts = 0
```

v3.3 validates the seed extract pack and scores slot coverage.

---

## 1. Core thesis

```txt
A candidate source becomes evidence pressure only when its extract survives the gate.
```

v3.3 is the first campaign allowed to turn candidate sources into limited source pressure, benchmark pressure, contradiction, analogy rejection, or inconclusive status.

---

## 2. Hard rule

```txt
No extract validation, no source support.
No slot coverage without a validated component.
No benchmark status without comparable ranges.
No source-backed status with an unaddressed contradiction.
No physical claim.
```

---

## 3. Target candidate

```txt
candidate_family: LOG_BOUNDARY
phi_family: PHI_GRADIENT
previous_status: PHI_GRADIENT_SOURCE_PACK_POPULATED
current_evidence: SYNTHETIC_ONLY
```

---

## 4. Required validation inputs

v3.3 must load:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json
```

It may optionally output reviewed/validated versions:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_3.validated.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_3.validated.json
```

---

## 5. Possible final statuses

```txt
PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
PHI_GRADIENT_SOURCE_PACK_VALIDATION_BLOCKED
```

---

## 6. Minimum positive paths

### Source-backed limited

To reach:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
```

require:

```txt
at least one validated observable/baseline extract from SLOT_1 or SLOT_8
at least one validated gradient/transition/component extract from SLOT_4
no unaddressed validated contradiction from SLOT_7
fixture/test-double excluded
```

### Benchmark-data found

To reach:

```txt
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
```

require:

```txt
at least one validated benchmark extract from SLOT_5
observable match
mass/length/time/visibility comparability
limitations recorded
fixture/test-double excluded
```

### Contradicted

To reach:

```txt
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
```

require:

```txt
at least one validated contradiction affecting candidate mechanism, alpha, observable, benchmark comparability, or environmental dominance
```

---

## 7. Canonical interpretation

For real source-backed limited:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
EvidenceLevel: SOURCE_BACKED_LIMITED
SupportLevel: SOURCE_LIMITED
BlockedReasons: MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA
```

For real benchmark data found:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
EvidenceLevel: BENCHMARK_SUPPORTED
SupportLevel: BENCHMARK
BlockedReasons: MISSING_EXPERIMENTAL_DATA
```

For contradiction:

```txt
CanonicalPermission: CLAIM_BLOCKED
EvidenceLevel: SYNTHETIC_ONLY or NO_EVIDENCE
SupportLevel: SYNTHETIC or UNSUPPORTED
BlockedReasons: CONTRADICTION
```

For inconclusive:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK
```

---

## 8. Acceptance criteria

v3.3 is complete when:

```txt
seed manifest loaded
seed extract pack loaded
extracts validated through strict v2.9/v3.1 rules
slot coverage scored
analogy-only sources identified
negative pressure identified
benchmark comparability scored
final canonical status produced
reports generated
loop feedback generated
tests pass
physical claims remain blocked
```

---

## 9. Final principle

```txt
Validation is the moment where a source stops being a name and becomes pressure.
```
