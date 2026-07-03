# Source-Indexed RAG Plan: I/K/R Redundancy

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Objective: source-indexed workflow for I/K/R redundancy review.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Partial support: false.
- Benchmarks run: none.
- Auxiliary thermal/visibility/contrast work touched: no.
- Applications generated: no.

## 1. Purpose

This plan defines a source-indexed RAG workflow to test whether the remaining Frontera C-Mayor bridge residue:

```txt
I_c(O <- e)
K(O,e)
R(O,e)
```

already exists in known frameworks under another name.

This workflow is review infrastructure only. It does not create validation, novelty, partial support, or evidence.

## 2. Corpus Folders

Target folder structure:

```txt
papers/
  aqft/
  relativistic_measurement/
  quantum_information/
  decoherence/
  recoverability/
  petz_recovery/
  qec/
  entanglement_wedge/
  relativistic_quantum_information/
```

Recommended metadata and review structure:

```txt
rag/
  frontera_c_mayor/
    metadata/
      paper_sources.jsonl
      source_claims.jsonl
      ikr_redundancy_links.jsonl
      review_queue.jsonl
    reviews/
      ikr_source_reviews/
      deep_review_required/
      expert_review_packets/
```

## 3. Workflow

1. Register source identity.
2. Record source availability and exact external identity.
3. Attach local PDF path and SHA256 only if locally available.
4. Extract or manually register key definitions.
5. Extract or manually register key theorem/result.
6. Map each source against `I_c`, `K`, `R`, and `D_CI`.
7. Classify redundancy threat.
8. Mark review status.
9. Queue unresolved sources for expert review.

## 4. Source Trust Levels

| Trust level | Meaning |
|---|---|
| `PRIMARY_PEER_REVIEWED` | Journal, proceedings, monograph, or official preprint by domain experts. |
| `PRIMARY_PREPRINT` | arXiv or equivalent author-controlled technical paper. |
| `REFERENCE_OVERVIEW` | Encyclopedia, lecture note, or survey used only for orientation. |
| `SECONDARY_LOW_TRUST` | Article or commentary that requires verification against primary sources. |
| `LOCAL_PDF_UNVERIFIED_IDENTITY` | Local file exists but bibliographic authority still requires review. |

## 5. Review Statuses

```txt
PENDING_REVIEW
REVIEWED_BACKGROUND
REVIEWED_PARTIAL_THREAT
REVIEWED_DIRECT_THREAT
NEEDS_DEEP_REVIEW
NEEDS_EXPERT_REVIEW
REJECTED_LOW_RELEVANCE
```

## 6. Redundancy Classes

```txt
DIRECT_REDUNDANCY_THREAT
PARTIAL_REDUNDANCY_THREAT
BACKGROUND
POSSIBLE_BRIDGE
LOW_RELEVANCE
NEEDS_DEEP_REVIEW
```

## 7. Required Review Questions

Each source must answer:

1. Does this source already define observer-relative information transfer?
2. Does it already define accessible coherence?
3. Does it already define recoverability or reconstruction?
4. Does it combine I/K/R under causal constraints?
5. Does it imply `D_CI`-like subdomains?
6. Does it make `B_c(O)` redundant?
7. Does it only cover one component, or the ordered bridge conjunction?
8. Does it require AQFT, QFT measurement, QI, decoherence, or QEC expert review?

## 8. Claim-Control Rules

- A source match is not validation.
- A missing exact phrase is not novelty.
- A near match is not proof of redundancy.
- A direct match is a threat requiring review, not a final decision.
- RAG output is an index for human and expert review.
- Physical claims remain blocked.

## 9. Initial Source Families

Initial source families to index:

1. AQFT / Haag-Kastler / local algebras.
2. Halvorson AQFT PDF.
3. Detector-based QFT measurement.
4. Causal measurement in QFT.
5. Quantum recoverability.
6. Petz recovery map.
7. Information causality.
8. Quantum channel capacity / coherent information.
9. Decoherence / einselection.
10. Resource theory of coherence.
11. Quantum error correction.
12. Entanglement wedge reconstruction.

## 10. Status

```yaml
source_indexed_rag_plan_status: CREATED
classification: CORE_BRIDGE
target_relations:
  - I_c
  - K
  - R
  - D_CI
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
allowed_use: redundancy_review_and_expert_review_preparation
forbidden_use: validation_or_novelty_claim
```

