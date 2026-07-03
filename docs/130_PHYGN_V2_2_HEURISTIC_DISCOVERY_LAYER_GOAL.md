# Phygn v2.2 — Heuristic Discovery Layer & Candidate Prioritization Goal

## 0. Context

The latest confirmed document is:

```txt
129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

Therefore, v2.2 starts at:

```txt
130
```

v2.1 introduced the canonical status grammar:

```txt
CanonicalPermission
CanonicalBlockedReason
CanonicalEvidenceLevel
CanonicalSupportLevel
CanonicalRiskLevel
CanonicalStatusRecord
CanonicalReportContract
```

v2.2 introduces a heuristic discovery layer, but forces all heuristic outputs through the v2.1 canonical grammar.

---

## 1. Core thesis

```txt
Heuristics may guide search.
They may not grant truth.
```

Heuristics are valid as accelerators of discovery:

```txt
generate candidates
rank candidates
suggest observables
suggest proxies
suggest scales
identify likely dead ends
prioritize experiments
```

But heuristics cannot:

```txt
validate a physical claim
authorize public claims
replace source support
replace benchmark support
replace experimental data
invent alpha justification
convert elegance into evidence
```

---

## 2. Why v2.2 is needed

Phygn currently has:

```txt
candidate benchmarking
negative controls
hypothesis incubation
idea-to-hypothesis UX
truth-boundary copilot
business validation
canonical status mapping
```

The missing piece is a controlled discovery layer:

```txt
a system that can generate and prioritize candidate hypotheses
without confusing heuristic plausibility with evidence.
```

---

## 3. Heuristic output must be canonically typed

Every heuristic output must map to:

```txt
CanonicalPermission: EXPLORE_ALLOWED or TEST_DESIGN_ALLOWED at most
CanonicalEvidenceLevel: HEURISTIC_ONLY
CanonicalSupportLevel: HEURISTIC
BlockedReason: MISSING_SOURCE_SUPPORT / MISSING_BENCHMARK / MISSING_EXPERIMENTAL_DATA as applicable
```

No heuristic-only candidate may map to:

```txt
CLAIM_LIMITED_ALLOWED
ACTION_LIMITED_ALLOWED
EXECUTION_ALLOWED
SCALE_ALLOWED
BENCHMARK_SUPPORTED
EXPERIMENTAL_DATA_SUPPORTED
```

unless independent evidence exists outside the heuristic layer.

---

## 4. v2.2 scope

Implement:

```txt
Heuristic Discovery Layer
Candidate Generator
Candidate Prioritizer
Heuristic Scorecard
Heuristic Permission Gate
Heuristic-to-Testable-Hypothesis Pipeline
Reports
Campaign Runner
Tests
```

---

## 5. Heuristic domains

Support at minimum:

```txt
physical_candidate
business_hypothesis
copilot_question
source_search_prioritization
benchmark_selection
```

Domain-specific heuristics may differ, but all must output canonical interpretation.

---

## 6. Candidate prioritization criteria

Recommended criteria:

```txt
detectability_potential
non_ad_hoc_score
dimensional_consistency
source_searchability
benchmarkability
falsifiability
simplicity
novelty
risk_level
cost_to_test
```

---

## 7. Acceptance criteria

v2.2 is complete when:

```txt
heuristic candidate schemas exist
heuristic outputs are canonically mapped
heuristic candidates cannot authorize truth
candidate ranking works
heuristic-to-testable pipeline works
reports generated
tests pass
behavior of existing gates remains unchanged
```

---

## 8. Final principle

```txt
A heuristic seed is not evidence.
It is an invitation to design a better test.
```
