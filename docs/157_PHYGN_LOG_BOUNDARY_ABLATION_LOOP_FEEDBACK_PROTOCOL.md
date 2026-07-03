# Phygn v2.6 — LOG_BOUNDARY Ablation Loop Feedback Protocol

## 0. Purpose

This document defines how v2.6 feeds ablation results into the v2.4 closed-loop system.

---

## 1. Loop feedback input

After ablation, send:

```txt
input_type: SYNTHETIC_ABLATION_RESULT
domain: physical_candidate
candidate_id: HEUR-PHY-003
candidate_family: LOG_BOUNDARY
previous_status: LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA
result_status: <ablation_status>
metrics: <sensitivity metrics>
failure_conditions: <list>
warnings: <list>
```

---

## 2. Feedback rules

If:

```txt
LOG_BOUNDARY_SURVIVES_ABLATION
```

Then propose:

```txt
increase source-search priority
increase benchmark-pressure priority
schedule source support audit
schedule benchmark data search
keep physical claims blocked
```

If:

```txt
LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT
```

Then propose:

```txt
block source-pressure upgrade
down-rank current phi formulation
create simpler control report
search alternative non-saturating phi functions
```

If:

```txt
LOG_BOUNDARY_FAILS_CONSTANT_CONTROL
```

Then propose:

```txt
do not increase LOG_BOUNDARY priority
record control failure
compare next candidate family
```

If:

```txt
LOG_BOUNDARY_SIGNAL_REQUIRES_ALPHA_EXTREME
```

Then propose:

```txt
require alpha justification
block priority upgrade
search source constraints on alpha
```

If:

```txt
LOG_BOUNDARY_SIGNAL_REQUIRES_THRESHOLD_TUNING
```

Then propose:

```txt
require pre-registered thresholds
block post-hoc threshold tuning
rerun with threshold robustness test
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
```

---

## 4. Report requirements

The loop feedback report must include:

```txt
ablation_status
canonical_status
metrics
warnings
allowed updates
blocked updates
next actions
discipline note
```

---

## 5. Final principle

```txt
Ablation does not decide truth.
It decides whether a synthetic signal deserves the next pressure.
```
