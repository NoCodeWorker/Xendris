# Phygn v1.2 — Baseline Source Pack Canonical Selection

## 0. Purpose

This document defines the canonical source slots for the first real baseline source pack.

The goal is to support:

\[
V_{base}(t)=e^{-\Gamma t}
\]

as a **limited phenomenological baseline** for visibility/coherence decay.

---

## 1. Canonical source slots

### SRC-BASE-DECOH-001 — Decoherence / coherence decay source

Purpose:

```txt
support the idea that coherence can decay over time under environmental interaction.
```

Desired support:

```txt
FORMULA_SUPPORT
CONTEXT_SUPPORT
PARAMETER_SUPPORT
```

Allowed source types:

```txt
review paper
textbook/chapter
foundational decoherence paper
lecture notes from reputable institution
```

Forbidden use:

```txt
do not use this alone as OBSERVABLE_SUPPORT unless visibility/interference readout is explicit.
```

---

### SRC-BASE-VIS-001 — Visibility / interference contrast source

Purpose:

```txt
support visibility or interference contrast as an observable/readout.
```

Desired support:

```txt
OBSERVABLE_SUPPORT
FORMULA_SUPPORT if visibility equation exists
EXPERIMENTAL_CONTEXT
```

Forbidden use:

```txt
do not use general quantum measurement text as direct visibility support unless visibility/contrast is explicit.
```

---

### SRC-BASE-MWI-001 — Matter-wave / nanoparticle interferometry source

Purpose:

```txt
support relevance to matter-wave or mesoscopic interferometry.
```

Desired support:

```txt
CONTEXT_SUPPORT
OBSERVABLE_SUPPORT
EXPERIMENTAL_CONTEXT
```

Forbidden use:

```txt
does not validate Frontera C.
does not validate the boundary-aware candidate.
```

---

### SRC-BASE-THRESH-001 — Visibility uncertainty / threshold source

Purpose:

```txt
support epsilon_exp or measurement threshold in later detectability analysis.
```

Desired support:

```txt
BENCHMARK_SUPPORT
PARAMETER_SUPPORT
OBSERVABLE_SUPPORT
```

Forbidden use:

```txt
do not invent epsilon_exp if not directly provided.
```

---

### SRC-BASE-PARAM-001 — Gamma / parameter / timescale support

Purpose:

```txt
support interpretation of Gamma as effective rate/timescale.
```

Desired support:

```txt
PARAMETER_SUPPORT
ASSUMPTION_SUPPORT
FORMULA_SUPPORT
```

Forbidden use:

```txt
does not make arbitrary gamma values physical.
```

---

## 2. Minimum viable pack

Minimum viable pack for ingestion attempt:

```txt
SRC-BASE-DECOH-001
SRC-BASE-VIS-001
```

if together they provide:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
HIGH or PRIMARY trust
local files or validated extracts
```

---

## 3. Stronger pack

Recommended:

```txt
SRC-BASE-DECOH-001
SRC-BASE-VIS-001
SRC-BASE-MWI-001
SRC-BASE-THRESH-001
SRC-BASE-PARAM-001
```

This positions future phases for:

```txt
SOURCE_BACKED_READY
epsilon_exp grounding
benchmark selection
experimental comparison
```

---

## 4. Selection rules

Prefer sources that are:

```txt
peer-reviewed
well-cited
standard reviews
directly about decoherence/visibility/interferometry
specific enough to constrain claims
```

Avoid sources that are:

```txt
blogs
general pop science
AI summaries
URL-only records
papers unrelated to visibility/coherence
quantum gravity speculation with no baseline relevance
```

---

## 5. Support assignment discipline

A source may be:

```txt
excellent context
```

and still fail to provide:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
```

Do not overtag.

---

## 6. Expected result

The source selection should answer:

```txt
Can we prepare the baseline for limited source-backed status?
```

Not:

```txt
Is Frontera C true?
```

---

## 7. Final principle

```txt
Choose sources that constrain the baseline, not sources that flatter the theory.
```
