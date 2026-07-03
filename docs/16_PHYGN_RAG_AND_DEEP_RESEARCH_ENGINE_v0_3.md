# Phygn v0.3 — RAG & Auto Deep Research Engine

## 0. Propósito

Phygn necesita una memoria científica propia.

El RAG no debe servir para adornar respuestas.  
Debe servir para impedir alucinaciones, anclar claims y retroalimentar el desarrollo del Lab.

## 1. Principio

```txt
Todo claim fuerte debe estar conectado a:
fuente → chunk → claim → test/benchmark → decisión.
```

Si falta cualquiera de esos enlaces, el claim queda degradado o bloqueado.

## 2. Arquitectura RAG

Estructura propuesta:

```txt
rag/
  source_manifest.json
  sources/
    papers/
    books/
    notes/
    web_snapshots/
  chunks/
    chunks.jsonl
  indexes/
    lexical/
    vector/
  claims/
    claim_registry.json
    claim_source_links.json
  citations/
    citation_audit.json
  research_tasks/
    research_backlog.json
    completed_research.json
```

Módulos Python:

```txt
phyng/rag/
  __init__.py
  schemas.py
  source_registry.py
  ingestion.py
  chunking.py
  retrieval.py
  claim_linker.py
  citation_audit.py
  research_planner.py
  deep_research.py
  rag_report.py
```

## 3. Source Registry

Cada fuente debe registrarse antes de usarse.

Modelo:

```python
class SourceRecord(BaseModel):
    source_id: str
    title: str
    authors: list[str] = []
    year: str | None = None
    url: str | None = None
    local_path: str | None = None
    source_type: Literal[
        "PAPER",
        "BOOK",
        "LECTURE_NOTES",
        "OFFICIAL_DOC",
        "ENCYCLOPEDIC",
        "WEB_ARTICLE",
        "OTHER"
    ]
    trust_level: Literal["PRIMARY", "HIGH", "MEDIUM", "LOW"]
    relevance: Literal["HIGH", "MEDIUM", "LOW"]
    topics: list[str]
    used_for: list[str]
    notes: str | None = None
```

## 4. Claim Registry

Cada claim importante debe registrarse.

```python
class ClaimRecord(BaseModel):
    claim_id: str
    text: str
    claim_type: ClaimType
    layer: Layer
    trace_type: TraceType | None
    status: Literal[
        "ALLOWED",
        "ALLOWED_LIMITED",
        "REQUIRES_SOURCE",
        "REQUIRES_MODEL",
        "REQUIRES_TRACE",
        "BLOCKED"
    ]
    source_ids: list[str]
    test_ids: list[str]
    benchmark_ids: list[str]
    safe_rewrite: str | None = None
    forbidden_interpretations: list[str]
```

## 5. Claim-source link

Ningún claim fuerte debe depender de memoria suelta.

```python
class ClaimSourceLink(BaseModel):
    claim_id: str
    source_id: str
    support_level: Literal[
        "DIRECT_SUPPORT",
        "INDIRECT_SUPPORT",
        "BACKGROUND",
        "CONTRADICTS",
        "INSUFFICIENT"
    ]
    quote_or_note: str
    page_or_section: str | None = None
```

## 6. Deep Research Trigger

La IA debe iniciar deep research si detecta:

```txt
claim sin fuente
claim de originalidad
claim sobre literatura existente
claim sobre física estándar
claim sobre comparación con escuela/campo existente
claim sobre experimental feasibility
claim sobre benchmark contra modelo base
```

No iniciar deep research para:

```txt
cambios de estilo
nombres de componentes UI
refactors internos sin claim científico
```

## 7. Research Task

```python
class ResearchTask(BaseModel):
    task_id: str
    question: str
    reason: str
    linked_gap_id: str
    required_source_types: list[str]
    priority: Literal["P0", "P1", "P2", "P3"]
    expected_output: Literal[
        "SOURCE_RECORDS",
        "CLAIM_AUDIT",
        "LITERATURE_MAP",
        "BENCHMARK_BASELINE",
        "MODEL_COMPARISON"
    ]
    status: Literal["TODO", "IN_PROGRESS", "DONE", "BLOCKED"]
```

## 8. Research quality rules

### Fuentes preferidas

```txt
papers revisados
preprints técnicos con autores reconocibles
libros académicos
lecture notes universitarias
documentación oficial
```

### Fuentes secundarias

```txt
Wikipedia solo como orientación inicial
blogs solo para contexto, no para claim duro
foros nunca como autoridad
```

## 9. RAG ingestion pipeline

```txt
source file/url
→ SourceRecord
→ extraction
→ chunking
→ chunk metadata
→ optional embeddings
→ claim linking
→ citation audit
→ report
```

## 10. Chunk schema

```python
class RagChunk(BaseModel):
    chunk_id: str
    source_id: str
    text: str
    section: str | None = None
    page: int | None = None
    topics: list[str]
    supports_claims: list[str]
    contradicts_claims: list[str]
```

## 11. Retrieval protocol

Cuando el Lab necesite soporte:

```txt
query
→ retrieve chunks
→ rank
→ filter trust level
→ return supporting and contradicting evidence
→ update claim audit
```

Nunca devolver solo fuentes favorables.

Debe haber campo:

```txt
contradicting_evidence
```

## 12. Anti-alucinación

Reglas duras:

```txt
No inventar autores.
No inventar citas.
No inventar DOI.
No inventar páginas.
No inventar resultados experimentales.
No afirmar que un paper dice algo sin chunk asociado.
No usar "se sabe que" para claims técnicos sin fuente.
```

Si falta soporte:

```txt
REQUIRES_SOURCE
```

## 13. Integración con agentes

Agente responsable:

```txt
Literature & Citation Auditor
```

Flujo:

```txt
claim
→ citation audit
→ source retrieval
→ support/contradiction map
→ claim status
```

## 14. RAG reports

Generar:

```txt
reports/rag_status.md
reports/source_manifest.md
reports/claim_source_matrix.md
reports/research_backlog.md
```

## 15. MVP v0.3

No es obligatorio implementar embeddings vectoriales en v0.3.

MVP aceptable:

```txt
source registry
claim registry
claim-source links
research task registry
markdown reports
lexical retrieval simple
citation audit
```

## 16. v0.4

Añadir:

```txt
ChromaDB o LanceDB
sentence-transformers
PDF ingestion
semantic retrieval
source confidence scoring
automatic claim contradiction detection
```

## 17. Endpoints futuros

```txt
GET /rag/sources
POST /rag/sources
GET /rag/claims
POST /rag/claims
POST /rag/retrieve
POST /rag/audit-claim
GET /rag/report
```

## 18. Tests

Tests mínimos:

```txt
test_source_record_validation
test_claim_requires_source
test_claim_source_link_support
test_retrieval_returns_support_and_contradiction
test_research_task_created_for_unsourced_claim
test_low_trust_source_cannot_support_hard_claim
test_rag_report_generation
```

## 19. RAG operating principle

```txt
The RAG is not memory.
The RAG is evidence infrastructure.
```
