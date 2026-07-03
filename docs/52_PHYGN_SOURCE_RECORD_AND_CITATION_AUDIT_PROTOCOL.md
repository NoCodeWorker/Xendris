# Phygn v0.9 — Source Record & Citation Audit Protocol

## 0. Propósito

Este documento define cómo Phygn decide si una fuente registrada puede afectar claims y readiness.

v0.9 no debe confundir:

```txt
source candidate
```

con:

```txt
audited source
```

## 1. SourceRecord v0.9

```python
class SourceRecordV09(BaseModel):
    source_id: str
    title: str | None
    authors: list[str]
    year: str | None
    source_type: str
    trust_level: str
    local_path: str | None
    url: str | None
    ingestion_status: str
    metadata_status: str
    citation_audit_status: str
    notes: str | None
```

## 2. Ingestion statuses

```txt
NOT_INGESTED
CANDIDATE_ONLY
INGESTED_METADATA_ONLY
INGESTED_LOCAL_TEXT
INGESTED_LOCAL_PDF_METADATA
INGESTED_WITH_EXTRACTS
REJECTED
```

## 3. Metadata statuses

```txt
COMPLETE
PARTIAL
UNKNOWN
CONFLICTING
```

## 4. CitationAuditResult

```python
class CitationAuditResult(BaseModel):
    source_id: str
    passed: bool
    audit_status: str
    missing_fields: list[str]
    trust_issues: list[str]
    extraction_issues: list[str]
    allowed_support_types: list[str]
    forbidden_support_types: list[str]
```

Audit statuses:

```txt
PASSED_LIMITED
PASSED_METADATA_ONLY
FAILED_MISSING_METADATA
FAILED_NO_LOCAL_CONTENT
FAILED_LOW_TRUST
FAILED_CONTRADICTORY
```

## 5. Support types

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
PARAMETER_SUPPORT
CONTEXT_SUPPORT
BACKGROUND_ONLY
CONTRADICTION
```

## 6. Permission table

| Audit status | Can unlock baseline? | Notes |
|---|---:|---|
| `PASSED_LIMITED` | yes, limited | if support type direct |
| `PASSED_METADATA_ONLY` | no | can support bibliography only |
| `FAILED_MISSING_METADATA` | no | create task |
| `FAILED_NO_LOCAL_CONTENT` | no | URL alone is not ingestion |
| `FAILED_LOW_TRUST` | no for hard claims | may be background |
| `FAILED_CONTRADICTORY` | no | blocks claim |

## 7. ClaimSourceLinkV09

```python
class ClaimSourceLinkV09(BaseModel):
    link_id: str
    claim_id: str
    source_id: str
    support_type: str
    support_strength: str
    quote_or_excerpt: str | None
    local_reference: str | None
    audit_status: str
```

## 8. Quote discipline

If an excerpt is stored:

```txt
must be short
must include local_reference
must not be invented
```

If no excerpt:

```txt
quote_or_excerpt = null
```

## 9. Report

Generate:

```txt
reports/rag/citation_audit_v0_9.md
reports/rag/claim_source_links_v0_9.md
```

## 10. Tests

```txt
tests/test_citation_audit_v0_9.py
tests/test_claim_source_links_v0_9.py
```

Cases:

```txt
test_url_only_fails_no_local_content
test_metadata_only_does_not_unlock_baseline
test_passed_limited_allows_direct_formula_support
test_low_trust_blocks_hard_claim
test_contradictory_source_blocks_claim
test_no_fake_excerpt_allowed
```

## 11. Final rule

```txt
Una cita no auditada no manda.
Una cita auditada limita.
```
