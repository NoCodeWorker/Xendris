# Phygn v3.8 — Review Decision Rules

## 0. Purpose

This document defines how raw v3.7 extraction candidates become reviewed exact extracts, rejected candidates or manual-review items.

---

## 1. Review statuses

```txt
REVIEWED_CANDIDATE_ACCEPTED_VALIDATION_READY
REVIEWED_CANDIDATE_ACCEPTED_WITH_LIMITATIONS
REVIEWED_CANDIDATE_REQUIRES_MANUAL_REVIEW
REVIEWED_CANDIDATE_REJECTED_GARBAGE
REVIEWED_CANDIDATE_REJECTED_TOO_LONG
REVIEWED_CANDIDATE_REJECTED_NO_LOCATION
REVIEWED_CANDIDATE_REJECTED_NO_COMPONENT_ROLE
REVIEWED_CANDIDATE_REJECTED_DUPLICATE
```

---

## 2. Garbage rejection

Reject a candidate if:

```txt
text is empty
text is pure encoding noise
text is only page header/footer
text is only references/bibliography noise
text lacks scientific content
text cannot be linked to any role
```

Status:

```txt
REVIEWED_CANDIDATE_REJECTED_GARBAGE
```

---

## 3. Manual review queue

Send to manual review if:

```txt
candidate is promising but formatting is damaged
equation formatting is ambiguous
table row is incomplete
caption lacks nearby values
candidate appears relevant but role is uncertain
source is Pedernales and extraction failed
```

Status:

```txt
REVIEWED_CANDIDATE_REQUIRES_MANUAL_REVIEW
```

---

## 4. Accepted validation-ready rules

A candidate may be validation-ready only if it has:

```txt
source_id
sha256
page_number or exact location
short extracted text
candidate_type
component_role
limitations
```

And if:

```txt
requires_manual_review = false
```

or a reviewer marks:

```txt
manual_review_resolved = true
```

---

## 5. Role assignment rules

### Decoherence baseline

Assign:

```txt
DECOHERENCE_BASELINE
```

if candidate mentions:

```txt
decoherence rate
environmental decoherence
collisional decoherence
thermal emission decoherence
scattering
visibility decay caused by environment
```

### Visibility decay observable

Assign:

```txt
VISIBILITY_DECAY_OBSERVABLE
```

if candidate mentions:

```txt
fringe visibility
contrast
interference visibility
loss of coherence
observed decoherence
```

### Benchmark model

Assign:

```txt
BENCHMARK_MODEL
```

if candidate includes:

```txt
mass range
time range
separation
experimental regime
matter-wave interferometry constraints
macroscopic matter-wave test
```

### Parameter constraint

Assign:

```txt
PARAMETER_CONSTRAINT
```

if candidate includes:

```txt
CSL
collapse parameter
bound
constraint
exclusion
lambda
r_C
Bayesian hypothesis test
```

### Gradient component

Assign:

```txt
GRADIENT_COMPONENT
```

only if the candidate links gradient/transition/effective operator to:

```txt
decoherence
rate
visibility
interferometry dynamics
effective dynamics
```

If it is only a physical field gradient without PHI_GRADIENT relevance, assign:

```txt
ANALOGY_ONLY
```

### Negative constraint

Assign:

```txt
NEGATIVE_CONSTRAINT
```

if candidate implies:

```txt
environmental baseline dominates
candidate-like effect negligible
parameter regime excluded
observable mismatch
benchmark mismatch
```

---

## 6. Duplicate handling

Candidates with same:

```txt
source_id
page_number
candidate_type
normalized_text
```

should be deduplicated.

Record duplicates in:

```txt
phi_gradient_rejected_extraction_candidates_v3_8.json
```

---

## 7. Final principle

```txt
Review is the act of refusing to confuse extracted text with extracted meaning.
```
