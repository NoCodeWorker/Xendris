# Phygn v4.7 — Decision Gate & Guardrails

## 0. Purpose

This document defines how PHI_CURVATURE may or may not enter a new pipeline.

---

## 1. Allowed next phases

If screen passes:

```txt
v4.8 — PHI_CURVATURE Minimal Source/y_true Campaign
```

If partial:

```txt
v4.8 — PHI_CURVATURE Targeted Source Discovery Before Pipeline
```

If experiment required:

```txt
v4.8 — PHI_CURVATURE Experimental Feasibility Gate
```

If failed:

```txt
v4.8 — Candidate Family Reprioritization
```

---

## 2. Guardrails if PHI_CURVATURE proceeds

Required guardrails:

```txt
no PredictiveGain until accepted y_true exists
no physical claim until source-pressure and y_true gates pass
no benchmark construction before source/y_true accessibility is confirmed
no SLOT_4 dependency unless explicitly resolved or scoped out
no synthetic score as selection authority
no full pipeline if public/manual/experimental paths remain UNKNOWN
```

---

## 3. Minimum campaign if passed

If passed, v4.8 must be minimal:

```txt
source discovery
exact source-location search
observable extraction
y_true availability check
stop/go decision
```

It must not immediately recreate the full PHI_GRADIENT pipeline.

---

## 4. PHI_GRADIENT preservation

PHI_GRADIENT remains:

```txt
METHOD_ONLY_EMPIRICALLY_UNGROUNDED
```

Allowed use:

```txt
negative control
regression fixture
claim-gate test case
pipeline stress-test
```

Blocked use:

```txt
physical candidate
predictive candidate
Frontera C evidence
invariant confirmation
```

---

## 5. SLOT_4 debt handling

SLOT_4 remains:

```txt
OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

For PHI_CURVATURE, determine:

```txt
SLOT4_INDEPENDENT
SLOT4_RELATED_BUT_SCOPED_OUT
SLOT4_DEPENDENT_BLOCKING
UNKNOWN
```

If `SLOT4_DEPENDENT_BLOCKING`, PHI_CURVATURE cannot proceed as physical candidate.

---

## 6. Final principle

```txt
A pivot is only progress if it lowers contact-with-reality risk.
```
