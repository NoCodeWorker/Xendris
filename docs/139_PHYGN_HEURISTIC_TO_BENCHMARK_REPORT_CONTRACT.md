# Phygn v2.3 — Heuristic-to-Benchmark Report Contract

## 0. Purpose

This document defines the required report contract for converting a heuristic candidate into a synthetic benchmark design.

v2.3 reports must use the v2.1 `CanonicalReportContract`.

---

## 1. Required report sections

Every v2.3 report must include:

```txt
Title
Date
Candidate ID
Candidate Family
Heuristic Origin
Canonical Status
Observable
Baseline Equation
Candidate Equation
Dimensionless Variables
Parameter Ranges
Detectability Metric
Failure Conditions
Synthetic Benchmark Design
Allowed Claims
Blocked Claims
Next Actions
Tests
Discipline Note
```

---

## 2. Canonical status section

Must include:

```txt
Domain Status
Canonical Permission
Blocked Reasons
Evidence Level
Support Level
Risk Level
Allowed Uses
Blocked Uses
Next Actions
Discipline Note
```

---

## 3. Report types

Generate:

```txt
log_boundary_candidate_formalization_v2_3.md
log_boundary_synthetic_benchmark_design_v2_3.md
log_boundary_detectability_failure_protocol_v2_3.md
heuristic_to_benchmark_canonical_contract_v2_3.md
campaign report
```

---

## 4. Allowed claims section

For synthetic benchmark design:

```txt
Allowed:
- Candidate has explicit toy equation.
- Candidate has declared parameter ranges.
- Candidate has synthetic benchmark design.
- Candidate may proceed to synthetic execution.

Blocked:
- Physical prediction.
- Experimental validation.
- Source-backed claim.
- Benchmark-supported claim unless benchmark data exists.
```

---

## 5. Next actions

Typical next actions:

```txt
execute synthetic benchmark
run parameter sweep
compute max_abs_delta
classify detectability
record failure conditions
search source support
search benchmark data
```

---

## 6. Final principle

```txt
A benchmark report must show both what the candidate can claim and what it cannot.
```
