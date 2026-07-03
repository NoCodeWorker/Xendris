# Paper Source Schema

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Purpose: metadata schema for source-indexed redundancy review.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Partial support: false.

## 1. Source Record Schema

Each source record must use:

```json
{
  "source_id": "string",
  "title": "string",
  "authors": ["string"],
  "year": "string",
  "domain": "aqft|relativistic_measurement|quantum_information|decoherence|recoverability|petz_recovery|qec|entanglement_wedge|relativistic_quantum_information",
  "url": "string_or_null",
  "doi": "string_or_null",
  "arxiv": "string_or_null",
  "local_pdf_path": "string_or_null",
  "local_sha256": "string_or_null",
  "key_definitions": ["string"],
  "key_theorem_or_result": ["string"],
  "relation_to_I_c": "DIRECT|PARTIAL|BACKGROUND|NONE|UNCLEAR",
  "relation_to_K": "DIRECT|PARTIAL|BACKGROUND|NONE|UNCLEAR",
  "relation_to_R": "DIRECT|PARTIAL|BACKGROUND|NONE|UNCLEAR",
  "relation_to_D_CI": "DIRECT|PARTIAL|BACKGROUND|NONE|UNCLEAR",
  "redundancy_threat": "DIRECT_REDUNDANCY_THREAT|PARTIAL_REDUNDANCY_THREAT|BACKGROUND|POSSIBLE_BRIDGE|LOW_RELEVANCE|NEEDS_DEEP_REVIEW",
  "possible_residue": "string",
  "trust_level": "PRIMARY_PEER_REVIEWED|PRIMARY_PREPRINT|REFERENCE_OVERVIEW|SECONDARY_LOW_TRUST|LOCAL_PDF_UNVERIFIED_IDENTITY",
  "review_status": "PENDING_REVIEW|REVIEWED_BACKGROUND|REVIEWED_PARTIAL_THREAT|REVIEWED_DIRECT_THREAT|NEEDS_DEEP_REVIEW|NEEDS_EXPERT_REVIEW|REJECTED_LOW_RELEVANCE",
  "reviewer_notes": "string"
}
```

## 2. Required Fields

Required for every source:

- `source_id`
- `title`
- `authors`
- `year`
- `domain`
- at least one of `url`, `doi`, `arxiv`, `local_pdf_path`
- `relation_to_I_c`
- `relation_to_K`
- `relation_to_R`
- `relation_to_D_CI`
- `redundancy_threat`
- `trust_level`
- `review_status`

## 3. Key Definition Schema

Each key definition should be recorded as:

```json
{
  "definition_id": "string",
  "source_id": "string",
  "term": "string",
  "definition_text_or_summary": "string",
  "page_or_section": "string_or_null",
  "maps_to": ["I_c", "K", "R", "D_CI", "B_c", "M", "A_c", "D_LC"],
  "coverage_class": "COVERED|PARTIALLY_COVERED|UNCLEAR|POSSIBLE_RESIDUE|NOT_COVERED|REQUIRES_EXPERT_REVIEW"
}
```

## 4. Key Theorem / Result Schema

Each theorem or result should be recorded as:

```json
{
  "result_id": "string",
  "source_id": "string",
  "result_name": "string",
  "result_summary": "string",
  "page_or_section": "string_or_null",
  "relation_to_ikr": "DIRECT|PARTIAL|BACKGROUND|UNCLEAR",
  "redundancy_note": "string",
  "requires_expert_review": true
}
```

## 5. Relation Mapping Rules

### `I_c`

Map to `I_c` when the source defines or constrains information transfer, channel capacity, coherent information, mutual information through channels, causal communication, or observer-accessible records.

### `K`

Map to `K` when the source defines or constrains coherence, decoherence, phase information, entanglement degradation, resource theory of coherence, or state restriction affecting coherence access.

### `R`

Map to `R` when the source defines or constrains recoverability, reconstruction, Petz recovery, quantum error correction, entanglement wedge reconstruction, or inference from available records.

### `D_CI`

Map to `D_CI` when the source combines causal access, measurement/local observability, information transfer, coherence access, and recoverability/reconstruction.

## 6. Governance Rule

This schema supports redundancy review only.

```yaml
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
source_identity_is_not_evidence: true
rag_index_is_not_validation: true
```

