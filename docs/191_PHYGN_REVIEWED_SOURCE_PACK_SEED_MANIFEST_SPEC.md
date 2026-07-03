# Phygn v3.2 — Reviewed Source Pack Seed Manifest Spec

## 0. Purpose

This document defines the seed manifest used to populate PHI_GRADIENT real source review.

The seed manifest is not evidence.

It is a curated queue of candidate sources that must be extracted and validated.

---

## 1. Manifest file

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json
```

---

## 2. Manifest status

Seed manifest entries must start as:

```txt
REVIEWED_SOURCE_CANDIDATE
```

or:

```txt
REVIEWED_SOURCE_REQUIRES_MANUAL_REVIEW
```

No seed entry may start as evidence-supported.

---

## 3. Required fields

Each entry must contain:

```txt
source_id
title
authors
year
doi OR arxiv_id OR url OR local_path
source_type
target_slots
expected_components
review_status
reviewer_notes
risk_flags
evidence_status
```

---

## 4. Evidence status rule

Every v3.2 seed source must initially have:

```txt
evidence_status: CANDIDATE_NOT_VALIDATED
```

Possible later statuses:

```txt
EXTRACT_VALIDATED_SUPPORT
EXTRACT_VALIDATED_BENCHMARK
EXTRACT_VALIDATED_CONTRADICTION
EXTRACT_REJECTED_ANALOGY
EXTRACT_REJECTED_NOT_COMPARABLE
```

---

## 5. Recommended seed composition

Target 10–15 initial sources:

```txt
3 decoherence baseline / visibility decay sources
3 benchmark or matter-wave interferometry sources
2 gravitational decoherence or collapse-model sources
2 gradient/transition/effective-operator sources
1–2 scale/log-coordinate sources
2 negative or exclusion pressure sources
```

---

## 6. Risk flags

Use risk flags:

```txt
RISK_ANALOGY_ONLY
RISK_BENCHMARK_NOT_COMPARABLE
RISK_NO_ALPHA_CONSTRAINT
RISK_REVIEW_REQUIRED
RISK_SOURCE_MAY_BE_NEGATIVE
RISK_OBSERVABLE_MISMATCH
RISK_NOT_DIRECTLY_PHI_GRADIENT
```

---

## 7. Final principle

```txt
A source candidate becomes useful only when it can fill or wound a slot.
```
