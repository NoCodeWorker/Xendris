# Phygn v1.3 — Baseline Real Source Candidates

## 0. Purpose

This document lists real source candidates for the baseline source pack. These are candidate sources, not ingested sources.

They must still be:

```txt
downloaded or stored locally
added to sources/baseline/
represented in source_manifest.json
validated
audited
linked to claims
```

## 1. Source candidate table

| Slot | Candidate | Intended Support | Status |
|---|---|---|---|
| `SRC-BASE-DECOH-001` | Schlosshauer, *Decoherence, the measurement problem, and interpretations of quantum mechanics* | decoherence foundations, assumptions | CANDIDATE |
| `SRC-BASE-DECOH-002` | Paz & Zurek, *Environment-Induced Decoherence, Classicality and Consistency of Quantum Histories* | decoherence time/context | CANDIDATE |
| `SRC-BASE-MWI-001` | Kaltenbaek et al., *Macroscopic quantum resonators (MAQRO)* | matter-wave/mesoscopic context, visibility/decoherence | CANDIDATE |
| `SRC-BASE-MWI-002` | Kaltenbaek et al., *MAQRO: 2015 update* | updated matter-wave/space proposal context | CANDIDATE |
| `SRC-BASE-VIS-001` | Schut et al., matter-wave interferometer visibility/decoherence/dephasing source | visibility loss/contrast | CANDIDATE |
| `SRC-BASE-VIS-002` | Decoherence in Talbot-Lau interferometry / C70 visibility source | exponential visibility decrease with gas/background | CANDIDATE |
| `SRC-BASE-EXP-001` | Arndt et al., *Experimental decoherence in molecule interferometry* | molecule interferometry/decoherence experiments | CANDIDATE |
| `SRC-BASE-NANO-001` | Pedalino et al., nanoparticle matter-wave interferometry | high-mass nanoparticle interference context | CANDIDATE |

## 2. Candidate slot mapping

### `SRC-BASE-DECOH-001`

Use for:

```txt
CONTEXT_SUPPORT
ASSUMPTION_SUPPORT
maybe FORMULA_SUPPORT if explicit decay relation is found
```

Do not use for direct visibility observable support unless the text explicitly discusses visibility/interference contrast. Do not use as Frontera C support.

### `SRC-BASE-MWI-001`

Use for:

```txt
MATTER_WAVE_INTERFEROMETRY
CONTEXT_SUPPORT
OBSERVABLE_SUPPORT if visibility is explicit
```

Possible key target:

```txt
MAQRO visibility depends on decoherence from gas particles and blackbody radiation.
```

### `SRC-BASE-VIS-001`

Use for:

```txt
OBSERVABLE_SUPPORT
visibility loss
decoherence/dephasing reduces contrast
```

### `SRC-BASE-VIS-002`

Use for:

```txt
FORMULA_SUPPORT or BENCHMARK_SUPPORT if the source explicitly reports exponential fringe visibility decrease
OBSERVABLE_SUPPORT
```

This may be the strongest candidate for LIMITED upgrade if verified.

## 3. Acquisition priority

```txt
1. SRC-BASE-VIS-002 — because exponential visibility decrease is directly relevant.
2. SRC-BASE-MWI-001 — because MAQRO links mesoscopic context and decoherence/visibility.
3. SRC-BASE-DECOH-001 — because it grounds decoherence foundations.
4. SRC-BASE-VIS-001 — because it distinguishes decoherence/dephasing and visibility loss.
5. SRC-BASE-EXP-001 — because it provides experimental decoherence context.
```

## 4. Minimum pack target

For a LIMITED baseline attempt:

```txt
SRC-BASE-VIS-002
SRC-BASE-MWI-001
SRC-BASE-DECOH-001
```

Expected support:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
CONTEXT_SUPPORT
```

## 5. No fake metadata rule

Even if candidate metadata is suggested here, the ingestion manifest should only include metadata verified from the local source file or reliable bibliographic record.

If uncertain:

```txt
title = null
authors = []
year = null
```

## 6. Final principle

```txt
Select sources for what they can constrain, not for what they can decorate.
```
