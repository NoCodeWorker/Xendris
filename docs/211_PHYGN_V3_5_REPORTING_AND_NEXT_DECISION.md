# Phygn v3.5 — Reporting & Next Decision

## 0. Purpose

This document defines v3.5 reports and the next decision gate.

---

## 1. Required reports

Generate:

```txt
reports/priority_exact_fill/phi_gradient_priority_source_review_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_exact_extracts_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_locations_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_equation_observable_map_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_parameter_ranges_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_risk_and_negative_pressure_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_next_gate_v3_5.md
reports/campaigns/PHI-GRADIENT-PRIORITY-EXACT-FILL-v3_5.md
```

---

## 2. Report requirements

Reports must include:

```txt
priority source count
source text availability count
exact fill records
validation-ready count
unresolved count
equation map count
observable map count
parameter range count
benchmark range count
negative candidate count
analogy-only risk count
manual review debt before
manual review debt after
canonical status
blocked claims
next actions
discipline note
```

---

## 3. Canonical status

If source text unavailable or no exact fills ready:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons:
  MANUAL_REVIEW_DEBT_UNRESOLVED
  MISSING_VALIDATED_SOURCE_SUPPORT
  MISSING_BENCHMARK
```

If exact fills are validation-ready:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons:
  VALIDATION_PENDING
  MISSING_EXPERIMENTAL_DATA
```

---

## 4. Campaign statuses

```txt
PHI_GRADIENT_PRIORITY_EXTRACT_FILL_COMPLETED
PHI_GRADIENT_PRIORITY_EXTRACTS_PARTIAL
PHI_GRADIENT_PRIORITY_EXTRACTS_ACQUIRED
PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT
PHI_GRADIENT_PRIORITY_EXTRACTS_NO_VALIDATABLE_CONTENT
PHI_GRADIENT_PRIORITY_EXTRACT_FILL_BLOCKED
```

---

## 5. Next phase

Recommended next phase:

```txt
v3.6 — Priority Exact Extract Validation & First Source-Pressure Decision
```

v3.6 must decide whether the filled exact extracts allow:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
```

---

## 6. Final principle

```txt
v3.5 loads the weapon.
v3.6 pulls the epistemic trigger.
```
