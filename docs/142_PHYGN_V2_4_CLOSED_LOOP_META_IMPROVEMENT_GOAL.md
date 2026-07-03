# Phygn v2.4 — Closed Loop Learning & Meta-Improvement Engine Goal

## 0. Context

The latest confirmed document is:

```txt
141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
```

Therefore, v2.4 starts at:

```txt
142
```

v2.3 converted the top heuristic candidate:

```txt
HEUR-PHY-003 / LOG_BOUNDARY
```

into an explicit synthetic benchmark design with:

```txt
explicit equation
dimensionless variables
observable
baseline model
candidate model
parameter ranges
delta metric
detectability threshold
failure conditions
canonical report contract
tests
```

v2.3 did not execute physical validation.

The safe next step is to formalize the loop that connects:

```txt
heuristic discovery
candidate formalization
synthetic benchmark design
synthetic execution
source/benchmark pressure
prediction ledger
post-mortem
heuristic update
meta-improvement
```

---

## 1. Core thesis

```txt
Phygn may learn priorities.
Phygn may not self-authorize truth.
```

v2.4 introduces two loops:

```txt
Candidate Learning Loop
Meta-Improvement Loop
```

The first loop learns which candidates deserve more pressure.

The second loop learns how Phygn's own process can improve.

Neither loop can grant physical truth, public claim permission, financial action permission, or execution permission without the existing gates.

---

## 2. Why this is needed

The earlier loop was useful but underspecified.

Now Phygn has:

```txt
Prediction Ledger
Post-Mortem Loop
Canonical Status Mapping
Heuristic Discovery
Heuristic Candidate to Synthetic Benchmark Design
Business Validation Gates
Copilot Truth Boundary
```

v2.4 must integrate these into a coherent closed-loop engine.

---

## 3. Outer Loop: Candidate Learning Loop

```txt
Input idea/result
→ heuristic discovery
→ candidate ranking
→ formalization gate
→ synthetic benchmark design
→ synthetic execution or source pressure
→ result classification
→ prediction ledger entry
→ post-mortem
→ candidate family update proposal
→ next candidate selection
```

This loop may update:

```txt
candidate family priorities
heuristic score weights
next-best-question priorities
benchmark design suggestions
source search priorities
```

It may not update:

```txt
truth permissions
claim gates
source support requirements
experimental evidence requirements
financial action rules
canonical permission semantics
```

---

## 4. Inner Loop: Meta-Improvement Loop

The meta-loop observes Phygn's own behavior:

```txt
gate strictness
heuristic usefulness
report completeness
test coverage
model backend reliability
canonical mapping coverage
post-mortem patterns
```

It proposes internal improvements.

It must use shadow mode before applying any non-trivial change.

---

## 5. Meta-change lifecycle

```txt
META_CHANGE_PROPOSED
META_CHANGE_SHADOW_TESTING
META_CHANGE_BENCHMARKED
META_CHANGE_APPROVED_LOW_RISK
META_CHANGE_REQUIRES_HUMAN_REVIEW
META_CHANGE_BLOCKED_REGRESSION
META_CHANGE_REJECTED
META_CHANGE_APPLIED_VERSIONED
```

No critical meta-change may skip shadow testing and regression tests.

---

## 6. Safety rule

```txt
The system can change how it searches.
It cannot change what counts as evidence without review.
```

---

## 7. Acceptance criteria

v2.4 is complete when:

```txt
candidate learning loop state machine exists
meta-improvement loop state machine exists
post-mortem-to-update proposal pipeline exists
shadow mode exists
risk classification for meta-changes exists
regression/behavior-preservation guards exist
canonical status integration exists
reports are generated
tests pass
no existing gate behavior is changed
```

---

## 8. Final principle

```txt
Phygn can improve itself.
It cannot give itself permission to be right.
```
