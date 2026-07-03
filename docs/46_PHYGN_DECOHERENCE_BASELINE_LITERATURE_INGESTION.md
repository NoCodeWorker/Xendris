# Phygn v0.8 — Decoherence Baseline Literature Ingestion

## 0. Propósito

Este documento define cómo Phygn debe planificar e ingerir literatura para anclar un baseline de decoherencia/visibilidad.

El objetivo no es encontrar fuentes que favorezcan Frontera C.  
El objetivo es encontrar fuentes que definan correctamente el modelo base.

## 1. Source categories

### BASE-SRC-001 — Visibility decay / coherence loss

Necesario para:

```txt
observable = visibility_loss
coherence_decay
V(t)
```

Suggested queries:

```txt
matter wave interferometry visibility decoherence exponential decay
quantum decoherence visibility loss interferometry exponential model
```

### BASE-SRC-002 — Environmental decoherence

Necesario para:

```txt
Γ_env
environmental decoherence rate
baseline noise
```

Suggested queries:

```txt
environmental decoherence matter wave interferometry nanoparticle
decoherence rate matter wave interferometry visibility
```

### BASE-SRC-003 — Caldeira-Leggett / master equation context

Solo si se usa formalmente.

Suggested queries:

```txt
Caldeira Leggett quantum Brownian motion decoherence master equation
environment induced decoherence master equation
```

### BASE-SRC-004 — Mesoscopic / nanoparticle interferometry

Necesario para:

```txt
system mass range
visibility experiments
MAQRO-like context
```

Suggested queries:

```txt
macroscopic quantum resonators MAQRO nanoparticle interferometry decoherence
matter wave interferometry massive nanoparticles decoherence visibility
```

### BASE-SRC-005 — Experimental thresholds

Necesario para:

```txt
epsilon_exp
detectability
visibility uncertainty
```

Suggested queries:

```txt
matter wave interferometry visibility measurement uncertainty
nanoparticle interferometry decoherence experimental visibility threshold
```

## 2. SourceRequirement schema extension

```python
class BaselineSourceRequirement(BaseModel):
    requirement_id: str
    topic: str
    baseline_role: str
    reason: str
    required_for: list[str]
    linked_model_ids: list[str]
    linked_claim_ids: list[str]
    required_trust_level: str
    suggested_queries: list[str]
    status: str
```

## 3. Ingestion rules

If no source is available:

```txt
create BaselineSourceRequirement
create ResearchTask
baseline remains BASELINE_REQUIRES_SOURCE
```

If source is available:

```txt
create SourceRecord
create EvidenceRecord
create ClaimSourceLink
audit support level
update baseline readiness
```

## 4. Source support levels for baseline

```txt
FORMULA_SUPPORT:
supports formula form.

PARAMETER_SUPPORT:
supports parameter interpretation.

OBSERVABLE_SUPPORT:
supports observable.

CONTEXT_SUPPORT:
background only.

CONTRADICTS:
contradicts baseline use.
```

## 5. Minimum source-backed baseline

A baseline can become:

```txt
BASELINE_SOURCE_BACKED_LIMITED
```

if it has:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
HIGH or PRIMARY source
```

It can become:

```txt
BASELINE_SOURCE_BACKED_READY
```

only if it also has:

```txt
PARAMETER_SUPPORT
assumptions
allowed uses
forbidden uses
```

## 6. No cherry-picking rule

The RAG retrieval must return:

```txt
supporting evidence
limiting evidence
contradicting evidence
missing evidence
```

Not just favorable support.

## 7. Reports

Generate:

```txt
reports/rag/baseline_source_requirements.md
reports/rag/baseline_literature_ingestion.md
reports/rag/baseline_source_support_matrix.md
```

## 8. Tests

```txt
tests/test_baseline_literature_requirements.py
tests/test_baseline_source_support_matrix.py
```

Cases:

```txt
test_missing_visibility_source_creates_requirement
test_formula_support_without_observable_not_ready
test_background_only_does_not_source_back_baseline
test_high_trust_formula_and_observable_support_allows_limited_baseline
test_contradicting_source_blocks_baseline
```

## 9. Final principle

```txt
Una fuente no existe para confirmar Phygn.
Existe para limitarlo.
```
