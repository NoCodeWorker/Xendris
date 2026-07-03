# Phygn v2.2 — Candidate Generation & Prioritization

## 0. Purpose

This document defines how Phygn generates and prioritizes candidate hypotheses using heuristics.

This layer is designed for search acceleration, not validation.

---

## 1. Candidate schema

```python
class HeuristicCandidate(BaseModel):
    candidate_id: str
    domain: str
    raw_idea: str
    proposed_hypothesis: str
    candidate_family: str | None
    suggested_observables: list[str]
    suggested_proxies: list[str]
    required_sources: list[str]
    required_benchmarks: list[str]
    failure_conditions: list[str]
    assumptions: list[str]
    heuristic_scores: dict[str, float]
    canonical_status: CanonicalStatusRecord
```

---

## 2. Candidate families for Frontera C

Candidate generator may propose:

```txt
B_SUPPRESSED
QB_STRUCTURAL
LOG_BOUNDARY
THRESHOLD_SATURATION
OBSERVABLE_DEPENDENT_BOUNDARY
DIMENSIONLESS_INVARIANT
REGIME_TRANSITION
NOISE_COUPLING_MODULATION
```

But every candidate must pass:

```txt
dimensional sanity
non-ad-hoc rule
observable definition
failure condition
detectability estimate
source-search path
benchmark path
```

---

## 3. Heuristic scorecard

Recommended scores:

```txt
detectability_potential: 0.0–1.0
non_ad_hoc_score: 0.0–1.0
dimensional_consistency: 0.0–1.0
falsifiability: 0.0–1.0
benchmarkability: 0.0–1.0
source_searchability: 0.0–1.0
simplicity: 0.0–1.0
novelty: 0.0–1.0
cost_to_test_inverse: 0.0–1.0
risk_penalty: 0.0–1.0
```

Total score:

```txt
priority_score =
  0.20 * detectability_potential
+ 0.15 * non_ad_hoc_score
+ 0.15 * dimensional_consistency
+ 0.15 * falsifiability
+ 0.10 * benchmarkability
+ 0.10 * source_searchability
+ 0.05 * simplicity
+ 0.05 * novelty
+ 0.05 * cost_to_test_inverse
- 0.10 * risk_penalty
```

Weights are heuristic and must be declared.

---

## 4. Candidate ranking result

```python
class HeuristicRankingResult(BaseModel):
    candidates: list[HeuristicCandidate]
    ranking_method: str
    weights: dict[str, float]
    top_candidate_id: str | None
    warnings: list[str]
    canonical_status: CanonicalStatusRecord
```

The ranking result itself must be:

```txt
support_level: HEURISTIC
evidence_level: HEURISTIC_ONLY
permission: EXPLORE_ALLOWED or TEST_DESIGN_ALLOWED
```

---

## 5. Negative-control learning

v1.5 showed that:

```txt
DeltaGamma_C = alpha × B
```

is likely too suppressed for ordinary mesoscopic systems unless alpha is extreme.

Heuristic prioritization should learn:

```txt
B_SUPPRESSED candidates are useful as controls
but should be down-ranked for positive prediction unless they improve detectability.
```

This is not proof of falsity.

It is prioritization.

---

## 6. Forbidden ranking behavior

The prioritizer must not:

```txt
rank candidates based on elegance alone
ignore dimensional inconsistency
ignore missing failure conditions
treat source absence as neutral for claim readiness
turn high score into evidence
```

---

## 7. Final principle

```txt
A high heuristic score means: test this first.
It does not mean: believe this first.
```
