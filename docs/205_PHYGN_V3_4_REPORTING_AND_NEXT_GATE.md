# Phygn v3.4 — Reporting & Next Gate

## 0. Purpose

This document defines v3.4 reports and the next validation gate.

---

## 1. Required reports

Generate:

```txt
reports/exact_extract_review/phi_gradient_exact_extracts_v3_4.md
reports/exact_extract_review/phi_gradient_exact_extract_locations_v3_4.md
reports/exact_extract_review/phi_gradient_equation_observable_map_v3_4.md
reports/exact_extract_review/phi_gradient_parameter_ranges_v3_4.md
reports/exact_extract_review/phi_gradient_manual_review_resolution_v3_4.md
reports/exact_extract_review/phi_gradient_next_gate_v3_4.md
reports/campaigns/PHI-GRADIENT-EXACT-EXTRACT-REVIEW-v3_4.md
```

---

## 2. Report requirements

Reports must include:

```txt
input manifest count
input seed extract count
manual review debt before
exact extracts acquired
validation-ready extracts
unresolved extracts
equation map count
observable map count
parameter range count
benchmark range count
negative constraint count
blocked claims
next actions
canonical status
discipline note
```

---

## 3. v3.4 canonical interpretation

Default if exact extracts are acquired but not validated:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons:
  MISSING_VALIDATED_SOURCE_SUPPORT
  MISSING_BENCHMARK
  MISSING_EXPERIMENTAL_DATA
```

If no exact extracts acquired:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons:
  MANUAL_REVIEW_DEBT_UNRESOLVED
  MISSING_SOURCE_SUPPORT
  MISSING_BENCHMARK
```

---

## 4. Allowed claims

Allowed:

```txt
Exact source review was performed.
Some extracts may be validation-ready.
Manual-review debt was reduced or measured.
```

Blocked:

```txt
PHI_GRADIENT has real source support.
PHI_GRADIENT has benchmark support.
PHI_GRADIENT is physically validated.
PHI_GRADIENT validates Frontera C.
Exact extract existence alone proves the candidate.
```

---

## 5. Next gate

Recommended next phase:

```txt
v3.5 — Exact Extract Validation & Limited Source-Pressure Gate
```

v3.5 must:

```txt
load v3.4 reviewed extract pack
run strict extract validation
score slot coverage
determine if source-backed limited is allowed
determine if benchmark data found is allowed
detect contradiction
keep physical claims blocked
```

---

## 6. Final principle

```txt
v3.4 prepares evidence pressure.
v3.5 decides whether that pressure counts.
```
