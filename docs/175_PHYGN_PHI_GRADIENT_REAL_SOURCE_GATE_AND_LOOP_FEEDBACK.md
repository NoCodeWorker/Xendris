# Phygn v2.9 — PHI_GRADIENT Real Source Gate & Loop Feedback

## 0. Purpose

This document defines how validated real extracts determine PHI_GRADIENT source status and how the result feeds the closed loop.

---

## 1. Real source gate inputs

```txt
real_source_manifest
validated_extracts
benchmark_records
negative_extracts
fixture_separation_report
```

---

## 2. Minimum status rules

To reach:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
```

require:

```txt
at least one valid observable/baseline extract
at least one valid gradient/transition/component extract
fixture sources excluded
no unaddressed contradiction
```

To reach:

```txt
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
```

require:

```txt
at least one comparable benchmark extract or record
observable match
parameter range match or justified transform
limitations recorded
fixture sources excluded
```

To classify:

```txt
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
```

when:

```txt
sources exist but all accepted content is analogy-only
no component support exists
```

To classify:

```txt
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
```

when:

```txt
negative extract contradicts candidate and contradiction is unaddressed
```

---

## 3. Loop feedback rules

If real source-backed limited:

```txt
increase real-source pressure confidence
schedule benchmark data acquisition
keep physical claims blocked
```

If real benchmark data found:

```txt
schedule benchmark comparison campaign
prepare parameter alignment protocol
keep experimental claims blocked
```

If analogy only:

```txt
block source upgrade
record analogy failure
search more precise sources
```

If contradicted:

```txt
block candidate promotion
record contradiction
trigger post-mortem
consider down-ranking PHI_GRADIENT
```

If acquisition failed:

```txt
record acquisition failure
do not infer unsupported status as contradiction
retry with improved search terms
```

---

## 4. Always blocked updates

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

## 5. Report requirements

```txt
manifest summary
extract summary
slot coverage
accepted support
rejected analogy
negative sources
benchmark comparability
canonical status
allowed updates
blocked updates
next actions
discipline note
```

---

## 6. Final principle

```txt
Real sources may raise pressure.
Only experiments can raise physical truth.
```
