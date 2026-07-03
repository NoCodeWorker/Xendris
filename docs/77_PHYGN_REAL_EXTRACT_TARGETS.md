# Phygn v1.3 — Real Extract Targets

## 0. Purpose

This document defines what to extract from selected candidate sources.

Do not copy long text. Do not invent quotes. Use short excerpts or careful paraphrase with local references.

## 1. Target claims

### CLAIM-BASELINE-FORMULA-001

```txt
A visibility/coherence decay baseline can be represented phenomenologically by an exponential or monotonic decay form under explicit assumptions.
```

Support needed:

```txt
FORMULA_SUPPORT
```

### CLAIM-BASELINE-OBSERVABLE-001

```txt
Visibility/interference contrast is a valid observable in interferometric decoherence contexts.
```

Support needed:

```txt
OBSERVABLE_SUPPORT
```

### CLAIM-BASELINE-CONTEXT-001

```txt
Matter-wave or mesoscopic interferometry is an appropriate context for studying decoherence and visibility loss.
```

Support needed:

```txt
CONTEXT_SUPPORT
OBSERVABLE_SUPPORT
```

### CLAIM-BASELINE-LIMITATION-001

```txt
The exponential baseline is limited/phenomenological and not a universal physical model.
```

Support needed:

```txt
ASSUMPTION_SUPPORT
CONTEXT_SUPPORT
CONTRADICTION if source warns against simplification
```

## 2. Extract targets by source

### SRC-BASE-DECOH-001

Look for:

```txt
environment-induced decoherence
loss of coherence
limitations of decoherence for interpretation
decoherence program scope
```

Likely support:

```txt
CONTEXT_SUPPORT
ASSUMPTION_SUPPORT
```

Only tag FORMULA_SUPPORT if an explicit mathematical decay relation is present.

### SRC-BASE-MWI-001

Look for:

```txt
visibility depends on decoherence
scattering gas particles
blackbody radiation
matter-wave/macroscopic quantum experiment context
```

Likely support:

```txt
OBSERVABLE_SUPPORT
CONTEXT_SUPPORT
```

### SRC-BASE-VIS-001

Look for:

```txt
decoherence and dephasing lead to loss of contrast in visibility
visibility of matter-wave interferometer
```

Likely support:

```txt
OBSERVABLE_SUPPORT
CONTEXT_SUPPORT
```

### SRC-BASE-VIS-002

Look for:

```txt
exponential decrease of fringe visibility
background gas pressure
agreement with decoherence theory
```

Likely support:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
BENCHMARK_SUPPORT
```

## 3. Extract template

```md
# Extracts — SRC-BASE-XXX

## Source Metadata

- Title:
- Authors:
- Year:
- Source file:
- URL:
- Trust level:

## Extract 1

Support type: OBSERVABLE_SUPPORT  
Claim target: CLAIM-BASELINE-OBSERVABLE-001  
Local reference: page/section/paragraph if known  
Text:

> short excerpt or careful paraphrase

Audit notes:

- Why this supports the claim:
- What this does not support:
- Limitations:
```

## 4. Required limitation per extract

Every extract must say one of:

```txt
This does not validate Frontera C.
This does not validate the boundary-aware candidate.
This does not imply physical prediction.
This supports only the baseline.
```

## 5. Forbidden outcome

Even if all extracts pass, do not write:

```txt
Frontera C is supported by these sources.
```

Write only:

```txt
The baseline may be source-backed limited if audit passes.
```

## 6. Final principle

```txt
Extracts must strengthen the adversary before they strengthen the theory.
```
