# Phygn v2.7 — Phi Search Loop Feedback & Report Contract

## 0. Purpose

This document defines how v2.7 reports phi search results and feeds them back into the v2.4 closed loop.

---

## 1. Required report sections

Every v2.7 report must include:

```txt
Candidate Family
Phi Formula
Synthetic Delta
Control Deltas
Saturation Ratio
Control Gain
Coordinate Contribution
Threshold Robustness
Alpha Sensitivity
Classification
Canonical Status
Allowed Uses
Blocked Uses
Loop Feedback
Next Actions
Discipline Note
```

---

## 2. Loop feedback rules

If:

```txt
PHI_CANDIDATE_SURVIVES_CONTROLS
```

Then propose:

```txt
increase source-search priority for surviving phi formulation
increase benchmark-pressure priority
schedule source-support audit
schedule benchmark-data search
keep physical claims blocked
```

If:

```txt
PHI_CANDIDATE_FAILS_CONSTANT_CONTROL
```

Then propose:

```txt
reject formulation
record control failure
do not increase source pressure
```

If:

```txt
PHI_CANDIDATE_SATURATES
```

Then propose:

```txt
reject or down-rank formulation
add saturation warning
search non-saturating alternatives
```

If:

```txt
PHI_SEARCH_NO_SURVIVOR
```

Then propose:

```txt
down-rank LOG_BOUNDARY family
select next heuristic family
retain results as negative control
```

---

## 3. Blocked updates

Always block:

```txt
physical claim authorization
Frontera C validation
experimental confirmation
source requirement reduction
benchmark requirement reduction
canonical permission semantic change
claim gate relaxation
```

---

## 4. Canonical section

Use v2.1 `CanonicalReportContract`.

Fields:

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

## 5. Final discipline note

```txt
A surviving phi earns pressure.
A failing phi earns memory.
Neither earns truth.
```
