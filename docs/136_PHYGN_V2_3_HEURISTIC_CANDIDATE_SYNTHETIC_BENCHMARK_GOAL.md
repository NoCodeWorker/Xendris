# Phygn v2.3 — Heuristic Candidate to Synthetic Benchmark Design Goal

## 0. Context

The latest confirmed document is:

```txt
135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
```

Therefore, v2.3 starts at:

```txt
136
```

v2.2 introduced the controlled heuristic discovery layer.

The highest-ranked physical heuristic candidate was:

```txt
HEUR-PHY-003 / LOG_BOUNDARY
```

with canonical status:

```txt
HEURISTIC_TEST_DESIGN_READY
CanonicalPermission: TEST_DESIGN_ALLOWED
Evidence: HEURISTIC_ONLY
Support: HEURISTIC
```

v2.3 converts that heuristic candidate into an explicit synthetic benchmark design.

---

## 1. Core thesis

```txt
A heuristic candidate must pay mathematical rent before it can enter synthetic benchmarking.
```

The purpose is not to validate LOG_BOUNDARY physically.

The purpose is to force it into:

```txt
explicit equation
dimensionless variables
observable
baseline
candidate model
parameter sweep
detectability threshold
failure conditions
report contract
tests
```

---

## 2. Hard rule

```txt
No equation, no benchmark.
No benchmark, no synthetic support.
No source/data, no physical claim.
```

---

## 3. v2.3 target candidate

Target:

```txt
candidate_id: HEUR-PHY-003
candidate_family: LOG_BOUNDARY
domain: physical_candidate
```

The candidate is only allowed to move from:

```txt
HEURISTIC_TEST_DESIGN_READY
```

to:

```txt
SYNTHETIC_BENCHMARK_DESIGNED
```

or:

```txt
SYNTHETIC_BENCHMARK_BLOCKED
```

It must not move to physical claim support.

---

## 4. Required canonical mapping

v2.3 must use the v2.1 canonical grammar.

Allowed synthetic benchmark design status:

```txt
SYNTHETIC_BENCHMARK_DESIGNED
→ CanonicalPermission: TEST_DESIGN_ALLOWED
→ Evidence: HEURISTIC_ONLY or SYNTHETIC_ONLY depending on execution state
→ Support: HEURISTIC or SYNTHETIC
→ BlockedReasons: MISSING_SOURCE_SUPPORT, MISSING_EXPERIMENTAL_DATA
```

Blocked design status:

```txt
SYNTHETIC_BENCHMARK_BLOCKED
→ CanonicalPermission: CLAIM_BLOCKED
→ Evidence: HEURISTIC_ONLY
→ Support: HEURISTIC
→ BlockedReasons: MISSING_OBSERVABLE or MISSING_FAILURE_CONDITION or UNPHYSICAL_PARAMETER
```

---

## 5. v2.3 scope

Implement:

```txt
LOG_BOUNDARY candidate formalization
synthetic benchmark design schemas
equation admissibility check
dimensionless variable check
no-ad-hoc scale check
detectability protocol
failure protocol
benchmark design report
campaign runner
tests
```

---

## 6. Acceptance criteria

v2.3 is complete when:

```txt
LOG_BOUNDARY candidate formalization exists
candidate equation is explicit
dimensionless variables are checked
observable is defined
baseline model is defined
candidate model is defined
delta metric is defined
parameter sweep design exists
failure conditions exist
canonical report exists
tests pass
heuristic candidate remains non-claim-authorizing
```

---

## 7. Final principle

```txt
The heuristic layer may open the door.
The benchmark design decides whether the candidate can enter the lab.
```
