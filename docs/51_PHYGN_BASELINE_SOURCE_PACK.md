# Phygn v0.9 — Baseline Source Pack

## 0. Propósito

Este documento define el paquete de fuentes que Phygn necesita para intentar subir el baseline de CAMPAIGN-002.

El objetivo no es completar una bibliografía exhaustiva.  
El objetivo es conseguir evidencia mínima suficiente para un baseline limitado.

## 1. Baseline objetivo

\[
V_{base}(t)=e^{-\Gamma t}
\]

Interpretación limitada:

```txt
phenomenological visibility/coherence decay baseline
```

No interpretación universal.

## 2. Source pack mínimo

### BSP-001 — Visibility/coherence decay formula support

Necesario para:

```txt
FORMULA_SUPPORT
V(t) decay model
```

### BSP-002 — Observable support

Necesario para:

```txt
OBSERVABLE_SUPPORT
visibility/coherence as measurable/readout quantity
```

### BSP-003 — Environmental decoherence support

Necesario para:

```txt
Γ_env as effective environmental decoherence/decay rate
```

### BSP-004 — Matter-wave / mesoscopic context

Necesario para:

```txt
CAMPAIGN-002 system relevance
nanoparticle or matter-wave interferometry context
```

### BSP-005 — Parameter discipline

Necesario para:

```txt
parameter limitations
gamma arbitrary vs fitted vs sourced
```

## 3. SourceCandidate

```python
class SourceCandidate(BaseModel):
    source_candidate_id: str
    requirement_id: str
    title: str | None
    authors: list[str]
    year: str | None
    source_type: str
    local_path: str | None
    url: str | None
    trust_level: str
    candidate_status: str
    notes: str | None
```

Statuses:

```txt
CANDIDATE_REGISTERED
LOCAL_FILE_AVAILABLE
METADATA_INCOMPLETE
READY_FOR_AUDIT
REJECTED
```

## 4. BaselineSourcePack

```python
class BaselineSourcePack(BaseModel):
    pack_id: str
    campaign_id: str
    source_candidates: list[SourceCandidate]
    minimum_requirements: list[str]
    coverage_status: str
    missing_requirements: list[str]
    ready_for_upgrade_attempt: bool
```

Coverage statuses:

```txt
EMPTY
PARTIAL
MINIMUM_COVERAGE
FULL_COVERAGE
CONTRADICTED
```

## 5. Manual source records

Allowed if:

```txt
metadata explicit
source_type clear
trust_level explicit
no invented fields
marked MANUAL_RECORD
```

Not allowed:

```txt
invented DOI
invented page number
invented quote
invented author/year
```

## 6. Local source files

Preferred path convention:

```txt
sources/baseline/
```

Examples:

```txt
sources/baseline/decoherence_visibility_decay_001.pdf
sources/baseline/matter_wave_decoherence_001.md
sources/baseline/citation_notes_001.md
```

## 7. If no source exists

Generate:

```txt
rag/research_tasks/RT-BSP-001.json
rag/research_tasks/RT-BSP-002.json
...
```

and keep:

```txt
BASELINE_REQUIRES_SOURCE
```

## 8. Reports

Generate:

```txt
reports/rag/baseline_source_pack.md
reports/rag/baseline_source_candidates.md
```

## 9. Tests

```txt
tests/test_baseline_source_pack.py
```

Cases:

```txt
test_empty_source_pack_not_ready
test_partial_source_pack_not_minimum_coverage
test_minimum_formula_observable_support_ready_for_attempt
test_no_fake_metadata_in_source_candidate
test_url_only_is_candidate_not_ingested
```

## 10. Final rule

```txt
Un source pack no es una lista.
Es una condición de entrada para subir un claim.
```
