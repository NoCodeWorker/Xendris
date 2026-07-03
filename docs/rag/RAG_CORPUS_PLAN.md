# RAG Corpus Plan

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Purpose: source-indexed redundancy and formal comparison support.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Forbidden use: evidence inflation, benchmark support, or validation claim.

## 1. Corpus Purpose

The corpus should support conservative review of whether Frontera C-Mayor's bridge objects are redundant with known physics.

It should answer:

- What does known physics already formalize?
- Which Frontera C-Mayor objects collapse into known concepts?
- Which objects survive only as bridge organization?
- Which claims require expert review?

## 2. Folder Structure

```txt
rag/
  frontera_c_mayor/
    corpus/
      aqft/
      relativity_causal_structure/
      relativistic_measurement/
      quantum_information/
      decoherence/
      recoverability_qec/
      horizons_information/
      foundations_measurement/
    metadata/
      sources.jsonl
      chunks.jsonl
      claims.jsonl
      redundancy_links.jsonl
    indexes/
      lexical/
      vector/
    reviews/
      exact_match_checks.jsonl
      near_match_checks.jsonl
      expert_review_queue.jsonl
```

## 3. Metadata Schema

Each source record should use:

```json
{
  "source_id": "string",
  "title": "string",
  "authors_or_authority": "string",
  "year": "string",
  "doi": "string_or_null",
  "arxiv": "string_or_null",
  "url": "string_or_null",
  "local_path": "string_or_null",
  "sha256": "string_or_null",
  "domain": "aqft|relativity|measurement|quantum_information|decoherence|recoverability|horizons|foundations",
  "availability_status": "LOCAL_HASHED|EXTERNAL_EXACT|PARTIAL|UNAVAILABLE",
  "review_status": "PENDING|REVIEWED|REQUIRES_EXPERT_REVIEW",
  "notes": "string"
}
```

## 4. Chunk Schema

Each chunk should use:

```json
{
  "chunk_id": "string",
  "source_id": "string",
  "page": "integer_or_null",
  "section": "string_or_null",
  "text_hash": "string",
  "text_excerpt": "short_string",
  "concept_tags": ["string"],
  "frontera_objects": ["D_LC", "A_c", "M", "I_c", "K", "R", "B_c", "D_CI"],
  "relevance_status": "BACKGROUND|OVERLAP|NEAR_MATCH|EXACT_MATCH|LOW_RELEVANCE"
}
```

## 5. Claim Extraction Schema

Each claim record should use:

```json
{
  "claim_id": "string",
  "source_id": "string",
  "chunk_id": "string",
  "claim_text": "string",
  "known_framework": "string",
  "frontera_object": "string",
  "coverage_class": "COVERED|PARTIALLY_COVERED|UNCLEAR|POSSIBLE_RESIDUE|NOT_COVERED|REQUIRES_EXPERT_REVIEW",
  "redundancy_note": "string",
  "requires_human_review": true
}
```

## 6. Paper Ingestion Workflow

1. Register source identity.
2. Store local source only if available and hashable.
3. Extract text with page/section provenance.
4. Chunk by section and concept.
5. Tag against Frontera C-Mayor objects.
6. Extract claims conservatively.
7. Link claims to redundancy categories.
8. Add uncertain cases to expert review queue.

## 7. Redundancy Search Questions

For each source, ask:

1. Does it already define causal accessibility inside a light cone?
2. Does it already connect causal regions to local observables?
3. Does it already define observer-relative measurement availability?
4. Does it already define information transfer limits constrained by `c`?
5. Does it already define coherence access or coherence degradation?
6. Does it already define recoverability or reconstruction maps?
7. Does it define a composite boundary equivalent to `D_CI(O)`?
8. Does it make `B_c(O)` redundant?

## 8. Governance Rules

- No source chunk is evidence for Frontera C-Mayor validation.
- No near match proves novelty.
- No absence of exact match proves originality.
- RAG output is a review aid only.
- External expert review remains required.

## 9. Plan Status

```yaml
rag_corpus_plan_status: CREATED
classification: CORE_BRIDGE
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
allowed_use: redundancy_review_and_formal_comparison
forbidden_use: validation_or_novelty_claim
```

