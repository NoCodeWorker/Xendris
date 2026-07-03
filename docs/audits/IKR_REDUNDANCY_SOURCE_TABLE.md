# I/K/R Redundancy Source Table

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Purpose: initial source table for I/K/R redundancy review.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Partial support: false.

## 1. Table Status

This is an initial review table based on already identified sources and source families.

It is not a completed literature review. It is not evidence of validation or novelty.

## 2. Initial Sources

| Source ID | Source / family | Domain | URL / DOI / arXiv | Relation to `I_c` | Relation to `K` | Relation to `R` | Relation to `D_CI` | Redundancy threat | Trust level | Review status |
|---|---|---|---|---|---|---|---|---|---|---|
| `SRC-AQFT-HAAG-KASTLER-LOCAL-ALGEBRAS` | AQFT / Haag-Kastler / local algebras | `aqft` | https://en.wikipedia.org/wiki/Algebraic_quantum_field_theory plus primary follow-up required | `PARTIAL` | `PARTIAL` | `BACKGROUND` | `PARTIAL` | `PARTIAL_REDUNDANCY_THREAT` | `REFERENCE_OVERVIEW` | `NEEDS_DEEP_REVIEW` |
| `SRC-HALVORSON-AQFT-PDF` | Halvorson AQFT PDF | `aqft` | local PDF reviewed in `docs/audits/AQFT_HAAG_KASTLER_COMPARISON.md` | `PARTIAL` | `PARTIAL` | `BACKGROUND` | `PARTIAL` | `PARTIAL_REDUNDANCY_THREAT` | `LOCAL_PDF_UNVERIFIED_IDENTITY` | `NEEDS_EXPERT_REVIEW` |
| `SRC-DETECTOR-QFT-MEASUREMENT` | Detector-based QFT measurement | `relativistic_measurement` | https://arxiv.org/abs/2108.02793 | `PARTIAL` | `BACKGROUND` | `BACKGROUND` | `PARTIAL` | `PARTIAL_REDUNDANCY_THREAT` | `PRIMARY_PREPRINT` | `NEEDS_DEEP_REVIEW` |
| `SRC-CAUSAL-MEASUREMENT-QFT` | Causal measurement in QFT / local measurements | `relativistic_measurement` | https://arxiv.org/abs/2511.06566 | `PARTIAL` | `BACKGROUND` | `BACKGROUND` | `PARTIAL` | `PARTIAL_REDUNDANCY_THREAT` | `PRIMARY_PREPRINT` | `NEEDS_DEEP_REVIEW` |
| `SRC-LOCAL-MEASUREMENT-FACTORISATION-QFT` | Factorisation conditions and causality for local QFT measurements | `relativistic_measurement` | https://arxiv.org/abs/2511.21644 | `PARTIAL` | `BACKGROUND` | `BACKGROUND` | `PARTIAL` | `PARTIAL_REDUNDANCY_THREAT` | `PRIMARY_PREPRINT` | `NEEDS_DEEP_REVIEW` |
| `SRC-QUANTUM-RECOVERABILITY-NOISY-STATES` | Information recoverability of noisy quantum states | `recoverability` | https://arxiv.org/abs/2203.04862 | `PARTIAL` | `PARTIAL` | `DIRECT` | `PARTIAL` | `DIRECT_REDUNDANCY_THREAT` | `PRIMARY_PREPRINT` | `NEEDS_DEEP_REVIEW` |
| `SRC-PETZ-RECOVERY-MAP` | Petz recovery map | `petz_recovery` | https://en.wikipedia.org/wiki/Petz_recovery_map | `PARTIAL` | `BACKGROUND` | `DIRECT` | `PARTIAL` | `DIRECT_REDUNDANCY_THREAT` | `REFERENCE_OVERVIEW` | `NEEDS_PRIMARY_SOURCE_REVIEW` |
| `SRC-INFORMATION-CAUSALITY` | Information causality | `quantum_information` | https://en.wikipedia.org/wiki/Information_causality | `DIRECT` | `BACKGROUND` | `BACKGROUND` | `PARTIAL` | `PARTIAL_REDUNDANCY_THREAT` | `REFERENCE_OVERVIEW` | `NEEDS_PRIMARY_SOURCE_REVIEW` |
| `SRC-COHERENT-INFORMATION-CAPACITY` | Coherent information and quantum channel capacity | `quantum_information` | https://arxiv.org/abs/2107.00392 | `DIRECT` | `BACKGROUND` | `PARTIAL` | `PARTIAL` | `DIRECT_REDUNDANCY_THREAT` | `PRIMARY_PREPRINT` | `NEEDS_DEEP_REVIEW` |
| `SRC-DECOHERENCE-EINSELECTION` | Decoherence and einselection | `decoherence` | https://arxiv.org/abs/quant-ph/0105127 | `BACKGROUND` | `DIRECT` | `PARTIAL` | `PARTIAL` | `DIRECT_REDUNDANCY_THREAT` | `PRIMARY_PREPRINT` | `NEEDS_DEEP_REVIEW` |
| `SRC-RESOURCE-THEORY-COHERENCE` | Quantifying coherence / resource theory of coherence | `decoherence` | https://arxiv.org/abs/1311.0275 | `BACKGROUND` | `DIRECT` | `PARTIAL` | `PARTIAL` | `DIRECT_REDUNDANCY_THREAT` | `PRIMARY_PREPRINT` | `NEEDS_DEEP_REVIEW` |
| `SRC-ENTANGLEMENT-WEDGE-PETZ` | Entanglement wedge reconstruction using Petz map | `entanglement_wedge` | https://arxiv.org/abs/1902.02844 | `PARTIAL` | `PARTIAL` | `DIRECT` | `POSSIBLE_BRIDGE` | `PARTIAL_REDUNDANCY_THREAT` | `PRIMARY_PREPRINT` | `NEEDS_EXPERT_REVIEW` |
| `SRC-UNIVERSAL-RECOVERY-ENTANGLEMENT-WEDGE` | Entanglement wedge reconstruction via universal recovery channels | `entanglement_wedge` | https://arxiv.org/abs/1704.05839 | `PARTIAL` | `PARTIAL` | `DIRECT` | `POSSIBLE_BRIDGE` | `PARTIAL_REDUNDANCY_THREAT` | `PRIMARY_PREPRINT` | `NEEDS_EXPERT_REVIEW` |

## 3. Initial Interpretation

Current table-level decision:

```yaml
direct_redundancy_threats:
  - quantum_recoverability
  - Petz_recovery
  - coherent_information_quantum_capacity
  - decoherence_einselection
  - resource_theory_of_coherence
partial_redundancy_threats:
  - AQFT_local_algebras
  - relativistic_QFT_measurement
  - information_causality
  - entanglement_wedge_reconstruction
possible_residue: ordered_I_K_R_bridge_layer_only
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
```

## 4. Required Next Review

Next review should not ask whether Frontera C-Mayor is validated.

It should ask:

```txt
Does any primary source already combine causal access, local measurement, information transfer, coherence access, and recoverability into a D_CI-like domain?
```

If yes, `D_CI` is likely redundant.

If no, the remaining result is still only a bridge-layer taxonomy unless a theorem or expert-reviewed operational residue is produced.

## 5. Populated Metadata Update

The source table has now been expanded by:

```txt
docs/audits/IKR_SOURCE_METADATA_TABLE.md
docs/audits/IKR_CLAIM_EXTRACTION_TABLE.md
docs/audits/IKR_REDUNDANCY_FINDINGS.md
```

Updated status:

```yaml
source_metadata_status: POPULATED_INITIAL_SOURCE_INDEX
ik_claim_extraction_status: CLAIMS_EXTRACTED_INITIAL
ik_r_collapse_risk: HIGH_TO_VERY_HIGH
joint_ikr_layer_status: SURVIVES_AS_BRIDGE_ONLY
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
next_gate: EXPERT_REVIEW_OR_PRIMARY_SOURCE_DEEP_REVIEW
```
