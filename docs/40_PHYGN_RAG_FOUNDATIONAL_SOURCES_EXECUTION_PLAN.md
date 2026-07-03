# Phygn v0.7 — RAG Foundational Sources Execution Plan

## 0. Propósito

Este documento convierte las ResearchTasks de v0.5/v0.6 en una campaña ejecutable de ingesta de fuentes.

La meta no es acumular PDFs.  
La meta es crear **permisos de claim**.

## 1. Principio

```txt
Una fuente no es decoración.
Una fuente es control de permiso.
```

## 2. Estados de una fuente

```txt
REQUIRED
SEARCH_PLANNED
CANDIDATE_FOUND
INGESTED
CHUNKED
LINKED_TO_CLAIM
AUDITED
REJECTED
```

## 3. SourceRequirement

```python
class SourceRequirement(BaseModel):
    requirement_id: str
    topic: str
    reason: str
    linked_claim_ids: list[str]
    linked_campaign_ids: list[str]
    required_trust_level: str
    required_source_types: list[str]
    suggested_queries: list[str]
    status: str
```

## 4. SourceIngestionResult

```python
class SourceIngestionResult(BaseModel):
    requirement_id: str
    source_id: str | None
    status: str
    action: str
    reason: str
    created_claim_links: list[str]
    blocked_claims: list[str]
    next_steps: list[str]
```

## 5. Fuente mínima por categoría

### REQ-SRC-001 — Reduced Compton wavelength

Usado para:

```txt
λC definition
quantum localization boundary language
```

Claims:

```txt
CLAIM-QB-001
CLAIM-QB-002
CLAIM-ATLAS-QUANTUM-BOUNDARY
```

### REQ-SRC-002 — Gravitational radius / Schwarzschild radius

Usado para:

```txt
rg definition
RS definition
horizon boundary interpretation
```

Claims:

```txt
CLAIM-GRAV-001
CLAIM-ATLAS-GRAV-BOUNDARY
```

### REQ-SRC-003 — Planck scale

Usado para:

```txt
ℓP
mP
Planck crossing
```

Claims:

```txt
CLAIM-PLANCK-001
CLAIM-ATLAS-PLANCK-CROSSING
```

### REQ-SRC-004 — Compton-Schwarzschild related work

Usado para:

```txt
novelty discipline
related work
avoid overclaim
```

Claims:

```txt
CLAIM-QB-RELATED-WORK
CLAIM-NOVELTY-LIMITATION
```

### REQ-SRC-005 — Mesoscopic matter-wave interferometry

Usado para:

```txt
mass ranges
length scales
visibility context
MAQRO-like language
```

Claims:

```txt
CLAIM-MESO-001
CLAIM-MESO-MAQRO-LIKE
```

### REQ-SRC-006 — Environmental decoherence models

Usado para:

```txt
M_base
visibility decay
gamma_env
standard decoherence comparison
```

Claims:

```txt
CLAIM-DECOH-BASELINE-001
CLAIM-CAMPAIGN-002-MODEL-BASE
```

### REQ-SRC-007 — Experimental visibility thresholds

Usado para:

```txt
epsilon_exp
detectability threshold
```

Claims:

```txt
CLAIM-DETECTABILITY-001
CLAIM-CAMPAIGN-002-EPSILON
```

### REQ-SRC-008 — Benchmark or data source

Usado para:

```txt
y_true
benchmark curve
error metric comparison
```

Claims:

```txt
CLAIM-GAIN-001
CLAIM-CAMPAIGN-002-PREDICTIVE-GAIN
```

## 6. Trust rule

```txt
Physical-core hard claims require PRIMARY or HIGH trust.
Toy model claims may use internal derivation but must remain marked TOY.
Benchmark claims require provenance.
```

## 7. Ingestion protocol

If source file exists:

```txt
1. create SourceRecord
2. extract metadata without invention
3. chunk or summarize with section markers
4. create ClaimSourceLinks
5. run citation audit
6. update claim statuses
7. generate source_claim_matrix
```

If source file does not exist:

```txt
1. create SourceRequirement
2. create ResearchTask
3. leave claims as REQUIRES_SOURCE or ALLOWED_LIMITED
```

## 8. No fake metadata rule

Never invent:

```txt
authors
year
DOI
journal
page
quote
experimental result
```

Use:

```txt
null
```

when unknown.

## 9. Claim status transitions

```txt
No source → REQUIRES_SOURCE
BACKGROUND only → REQUIRES_DIRECT_SUPPORT
LOW trust only for hard claim → REQUIRES_HIGHER_TRUST_SOURCE
CONTRADICTS → BLOCKED
DIRECT_SUPPORT + HIGH/PRIMARY → ALLOWED_LIMITED or ALLOWED
```

## 10. Reports

Generate:

```txt
reports/rag/source_requirements.md
reports/rag/foundational_source_ingestion.md
reports/rag/source_claim_matrix.md
reports/rag/claims_awaiting_sources.md
reports/rag/claims_unlocked_by_sources.md
```

## 11. Tests

```txt
tests/test_source_requirements.py
tests/test_source_ingestion_execution_plan.py
tests/test_source_claim_matrix.py
```

Cases:

```txt
test_source_requirement_created_for_missing_compton_source
test_no_fake_metadata_allowed
test_background_support_does_not_unlock_hard_claim
test_high_trust_direct_support_allows_limited_claim
test_contradictory_source_blocks_claim
test_reports_generated
```

## 12. Final rule

```txt
El RAG no está para recordar.
Está para decidir qué puede afirmarse.
```
