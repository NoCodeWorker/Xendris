# Phygn v4.0 — Reporting & Next Gate

## 0. Purpose

This document defines reports and post-v4.0 transition logic.

---

## 1. Required reports

Generate:

```txt
reports/benchmark_construction/phi_gradient_benchmark_dataset_manifest_v4_0.md
reports/benchmark_construction/phi_gradient_observable_alignment_v4_0.md
reports/benchmark_construction/phi_gradient_benchmark_rows_v4_0.md
reports/benchmark_construction/phi_gradient_negative_control_plan_v4_0.md
reports/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.md
reports/debts/slot4_resolution_plan_v4_0.md
reports/campaigns/PHI-GRADIENT-DEBT-AWARE-BENCHMARK-v4_0.md
```

---

## 2. Report requirements

Reports must include:

```txt
source-pressure basis
benchmark row count
observable alignment count
negative-control count
SLOT_4 debt status
claims blocked by debt
work allowed despite debt
next recommended phase
canonical status
discipline note
```

---

## 3. Canonical status mappings

Add statuses:

```txt
PHI_GRADIENT_DEBT_AWARE_BENCHMARK_READY
PHI_GRADIENT_DEBT_AWARE_BENCHMARK_PARTIAL
PHI_GRADIENT_SLOT4_DEBT_OPEN_BLOCKING
PHI_GRADIENT_BENCHMARK_BLOCKED_MISSING_SOURCE_PRESSURE
PHI_GRADIENT_BENCHMARK_BLOCKED_NO_OBSERVABLE_ALIGNMENT
```

Expected mapping for benchmark ready:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: REAL_SOURCE_PRESSURE_LIMITED
Support Level: LIMITED
Risk Level: SCIENTIFIC_RISK
```

Expected mapping for SLOT_4 debt:

```txt
Canonical Permission: CLAIM_BLOCKED
Evidence Level: REAL_SOURCE_PRESSURE_LIMITED
Support Level: UNSUPPORTED_FOR_GRADIENT_MECHANISM
Risk Level: SCIENTIFIC_RISK
```

---

## 4. Allowed claims

Allowed:

```txt
A debt-aware benchmark dataset was constructed.
Observable alignment was created from source-pressure-limited extracts.
SLOT_4 gradient-component debt remains open and blocking for mechanism claims.
```

Blocked:

```txt
PHI_GRADIENT is validated.
Frontera C is validated.
The gradient mechanism is source-backed.
The invariant has empirical confirmation.
Benchmark construction proves physics.
```

---

## 5. Possible next phases

Recommended:

```txt
v4.1 — Benchmark Model Comparison Without Gradient Claim
```

Parallel:

```txt
v4.1-SLOT4 — Targeted SLOT_4 Source Acquisition & Manual Review
```

Alternative if the team wants to resolve debt first:

```txt
v4.1 — SLOT_4 Resolution Sprint Before Benchmark Execution
```

---

## 6. Final principle

```txt
Do not let benchmark progress launder mechanism debt.
```
