# Phygn v3.3 — Reporting & Loop Feedback

## 0. Purpose

This document defines the reports and closed-loop feedback for source-pack extract validation.

---

## 1. Required reports

Generate:

```txt
reports/source_pack_validation/phi_gradient_extract_validation_v3_3.md
reports/source_pack_validation/phi_gradient_slot_coverage_v3_3.md
reports/source_pack_validation/phi_gradient_analogy_rejections_v3_3.md
reports/source_pack_validation/phi_gradient_negative_pressure_v3_3.md
reports/source_pack_validation/phi_gradient_benchmark_comparability_v3_3.md
reports/source_pack_validation/phi_gradient_final_gate_v3_3.md
reports/source_pack_validation/phi_gradient_loop_feedback_v3_3.md
reports/campaigns/PHI-GRADIENT-SOURCE-PACK-VALIDATION-v3_3.md
```

---

## 2. Report requirements

Reports must include:

```txt
manifest source count
extract candidate count
validated support count
manual-review count
analogy rejection count
negative pressure count
benchmark comparable count
slot coverage matrix
source pressure score
benchmark score
canonical status section
allowed claims
blocked claims
next actions
discipline note
```

---

## 3. Allowed claims by final status

### PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED

Allowed:

```txt
PHI_GRADIENT has limited real source pressure for specific validated components.
```

Blocked:

```txt
benchmark-supported claim unless benchmark status is met
physical prediction
Frontera C validation
experimental confirmation
```

### PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND

Allowed:

```txt
PHI_GRADIENT has a comparable benchmark pressure candidate.
```

Blocked:

```txt
experimental validation
physical prediction
Frontera C validation
```

### PHI_GRADIENT_REAL_SOURCE_CONTRADICTED

Allowed:

```txt
PHI_GRADIENT is contradicted or constrained by validated source pressure.
Post-mortem is required.
```

Blocked:

```txt
claim promotion
source-backed upgrade
benchmark-supported upgrade
```

### PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE

Allowed:

```txt
Source pack validation completed or partially completed.
More exact extracts are required.
```

Blocked:

```txt
source-backed claim
benchmark-supported claim
physical claim
```

---

## 4. Loop feedback

If source-backed limited:

```txt
schedule benchmark comparison
increase real-source confidence
target missing alpha constraints
search negative sources
```

If benchmark data found:

```txt
schedule parameter alignment and numerical benchmark comparison
```

If contradicted:

```txt
trigger PHI_GRADIENT post-mortem
down-rank candidate or narrow claim
select next phi family if needed
```

If inconclusive/manual-review heavy:

```txt
create exact-extract acquisition task
prioritize high-value sources
reject analogy-only paths
```

Always blocked:

```txt
physical claim authorization
Frontera C validation
experimental confirmation
claim gate relaxation
```

---

## 5. Final principle

```txt
Validated pressure changes next actions, not truth.
```
