# Phygn v1.6 — Dream-to-Claim Ladder

## 0. Purpose

This document defines the ladder by which an intuition becomes a testable hypothesis, then a claim, and only later an action.

The ladder prevents two opposite errors:

```txt
killing ideas too early
letting ideas masquerade as truth too early
```

---

## 1. Ladder levels

### Level 0 — DREAM

Description:

```txt
free intuition, metaphor, speculative association, aesthetic idea
```

Allowed:

```txt
wild hypotheses
analogies
unverified connections
poetic language
```

Blocked:

```txt
public factual claim
operational recommendation
scientific validation
financial action
```

Status:

```txt
IDEA_ALLOWED
INTUITION_LOGGED
```

---

### Level 1 — HYPOTHESIS_SEED

Description:

```txt
an idea stated as a possible relation
```

Requires:

```txt
candidate phenomenon
rough domain
uncertainty acknowledged
```

Example:

```txt
Frontera C may modulate visibility loss in boundary-sensitive systems.
```

Status:

```txt
HYPOTHESIS_SEED
CLAIM_NOT_ALLOWED
```

---

### Level 2 — FORMALIZING_HYPOTHESIS

Requires:

```txt
variables
candidate observable
rough mechanism
scope boundary
```

Status:

```txt
HYPOTHESIS_INCUBATING
NEEDS_OBSERVABLE
NEEDS_FAILURE_CONDITION
```

---

### Level 3 — TESTABLE_HYPOTHESIS

Requires:

```txt
observable
baseline
candidate model
failure condition
metric
detectability threshold
```

Status:

```txt
HYPOTHESIS_TESTABLE
READY_FOR_BENCHMARK_DESIGN
```

---

### Level 4 — SYNTHETIC_SUPPORT

Requires:

```txt
synthetic benchmark
delta computation
toy failure conditions
```

Allowed:

```txt
synthetic / toy claim only
```

Blocked:

```txt
physical prediction
real-world action
```

Status:

```txt
SYNTHETIC_SUPPORT_ONLY
```

---

### Level 5 — SOURCE_BACKED_LIMITED

Requires:

```txt
source audit
claim-source links
baseline/candidate source support
```

Status:

```txt
CLAIM_ALLOWED_LIMITED
```

---

### Level 6 — BENCHMARK_SUPPORTED

Requires:

```txt
real or literature-extracted y_true
baseline comparison
metric
uncertainty
out-of-sample or independent evaluation
```

Status:

```txt
BENCHMARK_SUPPORTED_CLAIM
```

---

### Level 7 — OPERATIONALLY_ACTIONABLE

Requires:

```txt
risk assessment
scope limits
failure protocol
monitoring
human review if needed
```

Status:

```txt
ACTION_ALLOWED_LIMITED
```

---

### Level 8 — AUTOMATED_EXECUTION_ALLOWED

Requires:

```txt
strong evidence
risk engine
logging
rollback
kill switch
compliance review
```

Status:

```txt
EXECUTION_ALLOWED_LIMITED
```

---

## 2. Core rule

```txt
A lower-level idea may exist.
It may not impersonate a higher-level claim.
```

---

## 3. Status examples

### Creative physics idea

```txt
Input:
"Maybe C is a causal seam that appears as decoherence."

Output:
Level 0/1
IDEA_ALLOWED
CLAIM_BLOCKED
NEXT: define observable
```

### Candidate formula

```txt
Input:
DeltaGamma_C = alpha * B

Output:
Level 3/4 if parameters are declared
HYPOTHESIS_TESTABLE
SYNTHETIC_SUPPORT_REQUIRED
```

### Public statement

```txt
Input:
"Phygn predicts gravitational decoherence."

Output:
CLAIM_BLOCKED
requires benchmark, source-backed candidate and predictive gain
```

---

## 4. Final principle

```txt
Phygn should be a ladder, not a guillotine.
```
