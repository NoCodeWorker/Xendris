# Phygn v4.9 — Candidate Source Identity Preflight Gate Goal

## 0. Context

The latest confirmed result document is:

```txt
D:\BIOCULTOR\PHYNG\docs\315_PHYGN_V4_8_PHI_CURVATURE_MINIMAL_CAMPAIGN_RESULTS.md
```

Therefore, v4.9 starts at:

```txt
316
```

v4.8 produced:

```txt
PHI_CURVATURE_REJECTED_NO_RESOLVABLE_SOURCES
accepted_y_true_count = 0
rejected_y_true_count = 4
threshold_reached = false
PredictiveGain = UNDEFINED_NOT_COMPUTED_IN_MINIMAL_CAMPAIGN
physical_claim_permission = BLOCKED
```

The lesson from v4.8:

```txt
PHI_CURVATURE did not fail at y_true.
It failed earlier: source identity resolution.
```

The broader lesson:

```txt
Before y_true accessibility, source identity must be real.
```

---

## 1. Core thesis

```txt
No source identity, no science pipeline.
```

---

## 2. Hard rule

```txt
No candidate may pass accessibility screening from unresolved citation strings.
No resolvable source identity, no candidate screen pass.
```

---

## 3. Mission

Implement:

```txt
v4.9 — Candidate Source Identity Preflight Gate
```

This is a transversal gate before any new candidate-family screening or minimal source/y_true campaign.

It must evaluate candidate families using **resolvable source identity**, not synthetic score, intuition, or raw citation strings.

---

## 4. Candidate families to screen

At minimum:

```txt
PHI_CURVATURE
PHI_LOCALIZED_WINDOW
PHI_BANDPASS
PHI_GRADIENT
B_SUPPRESSED
QB_STRUCTURAL
LOG_BOUNDARY
THRESHOLD_SATURATION
```

PHI_GRADIENT must remain:

```txt
METHOD_ONLY_EMPIRICALLY_UNGROUNDED
```

PHI_CURVATURE must reflect v4.8:

```txt
REJECTED_NO_RESOLVABLE_SOURCES
```

---

## 5. Preflight pipeline

For each candidate family:

```txt
candidate_family
  -> raw_source_refs
  -> source_identity_resolution
  -> source_availability
  -> observable_identity
  -> y_true_path_plausibility
  -> candidate_preflight_decision
```

Do not allow:

```txt
raw_source_refs
  -> accessibility pass
```

---

## 6. Source identity minimum

A source identity is minimally resolvable only if it has at least:

```txt
source_id
title or exact citation identity
authors or publication authority
publication/year
DOI, arXiv, URL, or local PDF hash
```

A raw string such as:

```txt
Phys. Rev. A 102, 022101
Nature Physics 15, 890
```

is not sufficient unless resolved into identity fields.

---

## 7. Required outputs

Create:

```txt
data/preflight/source_identity/candidate_family_source_inventory_v4_9.json
data/preflight/source_identity/source_identity_resolution_matrix_v4_9.json
data/preflight/source_identity/source_availability_matrix_v4_9.json
data/preflight/source_identity/observable_identity_matrix_v4_9.json
data/preflight/source_identity/ytrue_path_plausibility_matrix_v4_9.json
data/preflight/source_identity/candidate_preflight_decision_matrix_v4_9.json
data/preflight/source_identity/source_identity_preflight_gate_v4_9.json
```

---

## 8. Statuses

Add:

```txt
PHYGN_SOURCE_IDENTITY_PREFLIGHT_COMPLETED
PHYGN_SOURCE_IDENTITY_PREFLIGHT_BLOCKED_MISSING_PRIOR_RESULTS
PHYGN_SOURCE_IDENTITY_PREFLIGHT_NO_CANDIDATE_PASSED
PHYGN_SOURCE_IDENTITY_PREFLIGHT_CANDIDATE_PASSED
PHYGN_SOURCE_IDENTITY_PREFLIGHT_REQUIRES_SOURCE_ACQUISITION
PHYGN_SOURCE_IDENTITY_PREFLIGHT_REQUIRES_HUMAN_LOOKUP
```

---

## 9. Pass criteria

A candidate may pass preflight only if:

```txt
at least 2 resolvable source identities exist
at least 1 source is locally available or has exact external identity
at least 1 observable class is source-locatable
y_true path plausibility is not NONE
claim risk is not CRITICAL
```

Optional stronger pass:

```txt
at least 3 resolvable source identities
at least 1 local PDF/hash
at least 1 candidate numeric observable location candidate
```

---

## 10. Fail criteria

A candidate fails if:

```txt
all source refs are unresolved
source refs are raw citation strings only
no source identity has DOI/arXiv/URL/local hash
no observable identity can be tied to a source
y_true path plausibility is NONE
candidate depends on unresolved SLOT_4 debt for physical claim
```

---

## 11. Acceptance criteria

v4.9 is complete when:

```txt
prior PHI_GRADIENT and PHI_CURVATURE outcomes loaded
candidate family source inventory generated
source identity matrix generated
availability matrix generated
observable identity matrix generated
y_true plausibility matrix generated
candidate preflight matrix generated
gate decision generated
reports generated
tests pass
no y_true created
no PredictiveGain created
no physical claim upgraded
PHI_GRADIENT remains method-only
PHI_CURVATURE remains blocked unless source identity is newly resolved
```

---

## 12. Final principle

```txt
A citation hint is not a source.
A source is not evidence.
Evidence begins only after identity and location.
```
