# Phygn v0.6 — RAG Source Ingestion Campaign

## 0. Propósito

CAMPAIGN-002 no puede avanzar a interpretación física fuerte sin RAG.

Por tanto, v0.6 incluye una campaña paralela:

```txt
RAG-SRC-001 — Foundational Source Ingestion
```

Su misión es convertir:

```txt
AWAITING_SOURCE_INGESTION
```

en:

```txt
SOURCE_INGESTED
CLAIM_LINKED
CLAIM_AUDITED
```

## 1. Regla

```txt
El RAG no está para adornar.
El RAG decide qué claims pueden respirar.
```

## 2. Fuentes mínimas

### SRC-001 — Compton wavelength

Necesario para:

```txt
λC definition
reduced Compton wavelength
localization interpretation
```

### SRC-002 — Schwarzschild / gravitational radius

Necesario para:

```txt
rg = Gm/c²
RS = 2Gm/c²
horizon interpretation
```

### SRC-003 — Planck scale

Necesario para:

```txt
ℓP
mP
Planck crossing
```

### SRC-004 — Compton-Schwarzschild diagram / related work

Necesario para:

```txt
avoid false novelty
related work
```

### SRC-005 — Mesoscopic matter-wave interferometry

Necesario para:

```txt
m ranges
L ranges
visibility
experimental context
```

### SRC-006 — Environmental decoherence models

Necesario para CAMPAIGN-002.

### SRC-007 — Gravitational decoherence proposals

Solo si se habla de Diósi-Penrose o similares.

## 3. Trust levels

```txt
PRIMARY:
paper fundacional, libro técnico, documentación académica primaria.

HIGH:
review, lecture notes universitarias, libro estándar.

MEDIUM:
enciclopedia, artículo técnico secundario.

LOW:
blog, foro, texto no verificable.
```

## 4. Required SourceRecord

```python
class SourceRecord(BaseModel):
    source_id: str
    title: str
    authors: list[str]
    year: str | None
    url: str | None
    local_path: str | None
    source_type: str
    trust_level: str
    relevance: str
    topics: list[str]
    used_for: list[str]
    notes: str | None
```

## 5. No invention rule

No inventar:

```txt
authors
year
DOI
page
quote
result
```

Si no se sabe:

```txt
null
```

## 6. Claim linking

Cada fuente ingerida debe conectar con claims:

```txt
DIRECT_SUPPORT
INDIRECT_SUPPORT
BACKGROUND
CONTRADICTS
INSUFFICIENT
```

## 7. Minimum claims to audit

```txt
CLAIM-QB-001:
QB = (ℓP/L)^2 follows from definitions.

CLAIM-QB-002:
At fixed L, Q and B are not independent.

CLAIM-MESO-001:
For m=1e-17 kg and L=1e-7 m, B is negligible.

CLAIM-MESO-002:
The selected system is MAQRO-like.

CLAIM-DECOH-001:
Phygn predicts gravitational decoherence.

CLAIM-DECOH-001 must remain BLOCKED.
```

## 8. Reports

Generate:

```txt
reports/rag/foundational_source_ingestion.md
reports/rag/source_claim_matrix.md
reports/rag/claims_awaiting_sources.md
```

## 9. Tests

```txt
tests/test_rag_source_ingestion_campaign.py
tests/test_source_claim_matrix.py
```

Cases:

```txt
test_source_record_no_fake_metadata
test_source_links_claim
test_background_support_not_enough_for_hard_claim
test_direct_support_updates_allowed_limited
test_contradiction_blocks_claim
test_claim_decoherence_remains_blocked_without_model
```

## 10. Deep research integration

If IDE has browsing:

```txt
perform source search
create SourceRecord
save notes
link claims
audit claim status
```

If IDE has no browsing:

```txt
create research tasks
do not fake ingestion
```

## 11. Acceptance criteria

```txt
source registry updated or research tasks created
claim-source matrix generated
no invented citations
hard claims remain blocked unless fully supported
tests pass
```

## 12. Final phrase

```txt
A source is not decoration.
A source is permission control.
```
