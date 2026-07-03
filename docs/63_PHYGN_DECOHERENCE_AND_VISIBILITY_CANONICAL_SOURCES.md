# Phygn v1.1 — Decoherence & Visibility Canonical Sources

## 0. Purpose

This document defines the source categories Phygn should acquire for the baseline literature pack.

It is not a claim that these sources have already been ingested.  
It is a structured acquisition target list.

---

## 1. Baseline target

The baseline being supported is:

\[
V_{base}(t)=e^{-\Gamma t}
\]

as a limited phenomenological visibility/coherence decay reference.

Allowed interpretation:

```txt
limited source-backed baseline candidate
```

Forbidden interpretation:

```txt
universal decoherence law
validation of Frontera C
validation of the boundary-aware candidate
```

---

## 2. Canonical source category A — Decoherence foundations

Purpose:

```txt
environment-induced decoherence
loss of coherence
decoherence rate or timescale
```

Desired support:

```txt
CONTEXT_SUPPORT
FORMULA_SUPPORT if explicit
PARAMETER_SUPPORT if rates/timescales are discussed
```

Preferred source types:

```txt
academic review
book chapter
foundational paper
lecture notes from reputable institution
```

Suggested query themes:

```txt
environment induced decoherence review
decoherence timescale quantum systems review
quantum decoherence exponential decay coherence
```

---

## 3. Canonical source category B — Interferometric visibility

Purpose:

```txt
visibility as measured observable
loss of interference contrast
visibility decay
```

Desired support:

```txt
OBSERVABLE_SUPPORT
FORMULA_SUPPORT
EXPERIMENTAL_CONTEXT
```

Suggested query themes:

```txt
interferometric visibility decoherence matter wave
matter wave interferometry visibility loss decoherence
visibility contrast decoherence interference experiment
```

---

## 4. Canonical source category C — Matter-wave / nanoparticle interferometry

Purpose:

```txt
CAMPAIGN-002 mesoscopic system context
nanoparticle interference
mass and length scale realism
visibility readout
```

Desired support:

```txt
OBSERVABLE_SUPPORT
CONTEXT_SUPPORT
EXPERIMENTAL_CONTEXT
```

Suggested query themes:

```txt
matter wave interferometry massive particles decoherence
nanoparticle matter wave interferometry visibility decoherence
macroscopic quantum resonators MAQRO decoherence interferometry
```

---

## 5. Canonical source category D — Experimental visibility thresholds

Purpose:

```txt
epsilon_exp
detectability threshold
visibility uncertainty
```

Desired support:

```txt
BENCHMARK_SUPPORT
PARAMETER_SUPPORT
OBSERVABLE_SUPPORT
```

Suggested query themes:

```txt
matter wave interferometry visibility uncertainty
nanoparticle interferometry visibility measurement error
interferometric visibility experimental uncertainty decoherence
```

---

## 6. Canonical source category E — Effective exponential decay models

Purpose:

```txt
support for exponential decay as phenomenological model
```

Desired support:

```txt
FORMULA_SUPPORT
PARAMETER_SUPPORT
ASSUMPTION_SUPPORT
```

Suggested query themes:

```txt
coherence exponential decay decoherence rate
visibility exponential decay decoherence rate
phenomenological decoherence exponential model
```

---

## 7. Source scoring

Each candidate source must be scored:

```txt
trust_level: PRIMARY | HIGH | MEDIUM | LOW
source_relevance: DIRECT | INDIRECT | BACKGROUND | CONTRADICTORY
support_types: FORMULA_SUPPORT | OBSERVABLE_SUPPORT | PARAMETER_SUPPORT | CONTEXT_SUPPORT | BENCHMARK_SUPPORT | CONTRADICTION
ingestion_status
citation_audit_status
```

---

## 8. Minimum pack for v1.1 ingestion attempt

Minimum target:

```txt
1 source with FORMULA_SUPPORT
1 source with OBSERVABLE_SUPPORT
HIGH or PRIMARY trust
local file or local extract
citation audit passed
```

The same source may provide both support types if explicit.

---

## 9. Stronger pack

A stronger source pack includes:

```txt
1 decoherence review
1 matter-wave interferometry paper
1 visibility/contrast source
1 experimental uncertainty or threshold source
```

This may support future phases:

```txt
baseline SOURCE_BACKED_READY
epsilon_exp grounding
benchmark selection
```

---

## 10. Red flags

Reject or downgrade if:

```txt
source is only a URL
source is only metadata
source is AI-generated summary
source is low trust
source supports only context but is used as formula support
source discusses decoherence but not visibility/coherence observable
```

---

## 11. Final principle

```txt
A source is useful only to the extent that it constrains a claim.
```
