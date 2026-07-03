# Phygn v0.5 — RAG Source Plan for Invariant Boundary Campaign

## 0. Propósito

Este documento define qué fuentes necesita Phygn antes de permitir claims fuertes en CAMPAIGN-001 y el Boundary Atlas.

## 1. Regla

```txt
No source, no hard claim.
No primary/high source, no physical-core hard claim.
No source link, no paper claim.
```

## 2. Source categories

### SRC-CAT-001 — Compton wavelength

Necesario para:

```txt
λC definition
localization interpretation
quantum boundary claims
```

Suggested queries:

```txt
reduced Compton wavelength localization limit relativistic quantum mechanics
Compton wavelength localization quantum field theory
```

Required trust:

```txt
HIGH or PRIMARY
```

### SRC-CAT-002 — Gravitational / Schwarzschild radius

Necesario para:

```txt
rg definition
RS definition
horizon boundary claims
```

Suggested queries:

```txt
Schwarzschild radius gravitational radius definition general relativity
gravitational radius rg GM c^2
```

### SRC-CAT-003 — Planck scale

Necesario para:

```txt
ℓP
mP
Planck crossing
Compton-Schwarzschild intersection
```

Suggested queries:

```txt
Planck length Planck mass Compton Schwarzschild radius intersection
```

### SRC-CAT-004 — Compton-Schwarzschild diagram

Necesario para:

```txt
related work
not overclaiming novelty
```

Suggested queries:

```txt
Compton Schwarzschild diagram Adler Santiago
Generalized uncertainty principle Compton Schwarzschild
Maggiore generalized uncertainty principle Compton Schwarzschild
Scardigli generalized uncertainty principle black hole Compton wavelength
```

### SRC-CAT-005 — Mesoscopic interferometry / MAQRO-like systems

Necesario para:

```txt
system parameters
mass range
L scale
experimental context
```

Suggested queries:

```txt
MAQRO macroscopic quantum resonators space experiment nanoparticle mass 10^-17 kg
mesoscopic matter wave interferometry nanoparticle decoherence space
```

### SRC-CAT-006 — Decoherence models

Necesario para CAMPAIGN-002, no CAMPAIGN-001.

Suggested queries:

```txt
Caldeira Leggett decoherence model
Diosi Penrose gravitational decoherence
matter wave interferometry decoherence nanoparticle
```

### SRC-CAT-007 — Quantum information channel reliability

Necesario para futuros modelos de \(\mathcal{R}_{O,S}\).

Suggested queries:

```txt
quantum channel mutual information Holevo bound
depolarizing channel mutual information qubit
channel fidelity quantum information Nielsen Chuang
```

## 3. ResearchTask template

```json
{
  "task_id": "RT-CAMPAIGN-001-001",
  "question": "...",
  "reason": "...",
  "linked_claim_id": "...",
  "priority": "P1",
  "required_source_types": ["PAPER", "BOOK", "LECTURE_NOTES"],
  "suggested_queries": ["..."],
  "status": "AWAITING_SOURCE_INGESTION"
}
```

## 4. Claim-source matrix required rows

```txt
CLAIM-QB-001:
QB = (ℓP/L)^2 follows from definitions.

CLAIM-QB-002:
Q and B are not independent at fixed L.

CLAIM-MESO-001:
For m=1e-17 kg and L=1e-7 m, B is negligible.

CLAIM-MESO-002:
The selected system is MAQRO-like.

CLAIM-DECOH-001:
Phygn predicts new decoherence.

CLAIM-DECOH-001 must remain BLOCKED until model comparison exists.
```

## 5. Trust rules

```txt
CLAIM-QB-001:
Can be supported by mathematical derivation + constants sources.

CLAIM-QB-002:
Can be supported by internal derivation, but novelty claim needs literature scan.

CLAIM-MESO-001:
Needs calculation + accepted L.

CLAIM-MESO-002:
Needs source on experimental parameters.

CLAIM-DECOH-001:
Needs model, benchmark, source, gain.
```

## 6. Citation audit output

Generate:

```txt
reports/campaigns/CAMPAIGN-001_citation_audit.md
```

Columns:

```txt
claim_id
claim_text
status
required_source_category
source_ids
support_level
trust_level
action
```

## 7. Final rule

The RAG does not make Phygn smarter by remembering more.

It makes Phygn safer by refusing to claim what it cannot ground.
