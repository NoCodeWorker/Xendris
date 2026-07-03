# Phygn v3.1 — Reviewed Manifest Reporting & Loop Feedback

## 0. Purpose

This document defines reports and closed-loop feedback for v3.1.

---

## 1. Required reports

Generate:

```txt
reports/reviewed_manifest/phi_gradient_reviewed_manifest_v3_1.md
reports/reviewed_manifest/phi_gradient_manifest_validation_v3_1.md
reports/reviewed_manifest/phi_gradient_extract_pack_v3_1.md
reports/reviewed_manifest/phi_gradient_extract_validation_v3_1.md
reports/reviewed_manifest/phi_gradient_slot_coverage_v3_1.md
reports/reviewed_manifest/phi_gradient_negative_sources_v3_1.md
reports/reviewed_manifest/phi_gradient_benchmark_comparability_v3_1.md
reports/reviewed_manifest/phi_gradient_real_source_gate_v3_1.md
reports/reviewed_manifest/phi_gradient_loop_feedback_v3_1.md
reports/campaigns/PHI-GRADIENT-REVIEWED-LOCAL-MANIFEST-v3_1.md
```

---

## 2. Report requirements

Reports must include:

```txt
manifest id
entry count
traceable identifier coverage
fixture/test-double exclusions
source slot targeting
validated extract count
rejected analogy count
negative source count
benchmark comparable count
slot coverage matrix
canonical status
allowed claims
blocked claims
next actions
discipline note
```

---

## 3. Final statuses

Possible final statuses:

```txt
PHI_GRADIENT_REVIEWED_MANIFEST_CREATED
PHI_GRADIENT_REVIEWED_MANIFEST_LOADED
PHI_GRADIENT_REVIEWED_MANIFEST_INVALID
PHI_GRADIENT_REAL_EXTRACT_PACK_LOADED
PHI_GRADIENT_REAL_EXTRACTS_VALIDATED
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
PHI_GRADIENT_REVIEWED_MANIFEST_BLOCKED
```

---

## 4. Canonical mapping

For:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
```

map to:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
EvidenceLevel: SOURCE_BACKED_LIMITED
SupportLevel: SOURCE_LIMITED
BlockedReasons: MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA
```

For:

```txt
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
```

map to:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
EvidenceLevel: BENCHMARK_SUPPORTED
SupportLevel: BENCHMARK
BlockedReasons: MISSING_EXPERIMENTAL_DATA
```

For:

```txt
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
```

map to:

```txt
CanonicalPermission: CLAIM_BLOCKED
EvidenceLevel: SYNTHETIC_ONLY or NO_EVIDENCE
SupportLevel: SYNTHETIC or UNSUPPORTED
BlockedReasons: CONTRADICTION
```

For inconclusive or invalid manifest:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK
```

---

## 5. Loop feedback

If source-backed limited:

```txt
schedule benchmark comparison campaign
request more negative-source pressure
keep physical claims blocked
```

If benchmark data found:

```txt
schedule parameter alignment and numerical benchmark comparison
keep experimental validation blocked
```

If contradicted:

```txt
trigger post-mortem
down-rank PHI_GRADIENT or narrow its claim
select next phi family if needed
```

If inconclusive:

```txt
expand manifest
improve extract pack
target missing slots
```

Always blocked:

```txt
physical claim authorization
Frontera C validation
experimental confirmation
source requirement reduction
benchmark requirement reduction
claim gate relaxation
```

---

## 6. Final principle

```txt
Reviewed sources may raise pressure.
They still do not raise truth without experiment.
```
