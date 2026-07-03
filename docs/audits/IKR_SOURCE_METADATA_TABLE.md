# I/K/R Source Metadata Table

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Objective: populate source metadata for I/K/R redundancy review.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Partial support: false.
- Benchmarks run: none.
- Auxiliary thermal/visibility/contrast work touched: no.
- Applications generated: no.

## 1. Status

```yaml
source_metadata_status: POPULATED_INITIAL_SOURCE_INDEX
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
```

This table indexes sources for redundancy review only. It does not create source support for Frontera C-Mayor.

## 2. Metadata Table

| Source ID | Title / family | Source type | URL / DOI / arXiv | Domain | Key definitions | Key theorem or result | Relation to `I_c` | Relation to `K` | Relation to `R` | Relation to `D_CI` | Threat | Possible residue | Review status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SRC-AQFT-HAAG-KASTLER-LOCAL-ALGEBRAS` | AQFT / Haag-Kastler local algebras | source family | https://en.wikipedia.org/wiki/Algebraic_quantum_field_theory; primary follow-up: Haag & Kastler, J. Math. Phys. 1964 | `aqft` | local observable algebra, isotony, microcausality | local spacetime regions are assigned observable algebras | `PARTIAL` | `PARTIAL` | `BACKGROUND` | `PARTIAL` | `PARTIAL` | I/K/R may survive only as post-AQFT operational gates | `NEEDS_EXPERT_REVIEW` |
| `SRC-HALVORSON-MUEGER-AQFT` | Algebraic Quantum Field Theory | arXiv survey / local PDF family | https://arxiv.org/abs/math-ph/0602036 | `aqft` | AQFT local algebras, foundational structure, nonlocality, superselection | survey-level AQFT structure for local observables | `PARTIAL` | `PARTIAL` | `BACKGROUND` | `PARTIAL` | `PARTIAL` | bridge layer may remain only if I/K/R are independently operational | `SOURCE_INDEXED` |
| `SRC-DETECTOR-QFT-MEASUREMENT` | A detector-based measurement theory for quantum field theory | arXiv / article | https://arxiv.org/abs/2108.02793; DOI 10.1103/PhysRevD.105.065003 | `relativistic_measurement` | detector-induced POVM, localized detector coupling | detector-based QFT measurement avoids impossible-measurement problems | `PARTIAL` | `BACKGROUND` | `BACKGROUND` | `PARTIAL` | `PARTIAL` | I/K/R conjunction may remain beyond detector measurement | `CLAIMS_EXTRACTED` |
| `SRC-CAUSAL-MEASUREMENT-QFT-SPACETIME` | Causal measurement in quantum field theory: spacetime | arXiv / article | https://arxiv.org/abs/2511.06566; DOI 10.1103/5gl8-3j6p | `relativistic_measurement` | spacetime-localized observables, causal transparency | regularized measurements avoid unphysical superluminal signaling | `PARTIAL` | `BACKGROUND` | `BACKGROUND` | `PARTIAL` | `PARTIAL` | I/K/R may remain after admissible measurement is fixed | `CLAIMS_EXTRACTED` |
| `SRC-LOCAL-MEASUREMENT-FACTORISATION-QFT` | Factorisation conditions and causality for local measurements in QFT | arXiv preprint | https://arxiv.org/abs/2511.21644 | `relativistic_measurement` | local S-matrix factorisation, causal Kraus operators | criteria for admissible local measurements under causality | `PARTIAL` | `BACKGROUND` | `BACKGROUND` | `PARTIAL` | `PARTIAL` | I/K/R bridge remains only after local-measurement criteria | `SOURCE_INDEXED` |
| `SRC-QUANTUM-RECOVERABILITY-NOISY-STATES` | Information recoverability of noisy quantum states | arXiv / article | https://arxiv.org/abs/2203.04862 | `recoverability` | noisy quantum states, recoverable information | recoverability framework for noisy quantum information | `PARTIAL` | `PARTIAL` | `DIRECT` | `PARTIAL` | `DIRECT` | R may be an ordering gate only | `SOURCE_INDEXED` |
| `SRC-PETZ-RECOVERY-MAP` | Petz recovery map | theorem family / reference overview | https://en.wikipedia.org/wiki/Petz_recovery_map; primary-source review required | `petz_recovery` | recovery channel, equality/saturation of data-processing contexts | standard quantum recovery map | `PARTIAL` | `BACKGROUND` | `DIRECT` | `PARTIAL` | `DIRECT` | R must be defined against Petz-style recovery | `NEEDS_SOURCE` |
| `SRC-INFORMATION-CAUSALITY` | Information causality | principle / reference overview | https://en.wikipedia.org/wiki/Information_causality; primary-source review required | `quantum_information` | information gain under communication limits | communication principle stronger than no-signalling in some settings | `DIRECT` | `BACKGROUND` | `BACKGROUND` | `PARTIAL` | `PARTIAL` | I_c may survive only as observer-target gate | `NEEDS_SOURCE` |
| `SRC-COHERENT-INFORMATION-CAPACITY` | Coherent information and quantum channel capacity | arXiv technical paper | https://arxiv.org/abs/2107.00392 | `quantum_information` | coherent information, quantum channel capacity | positive capacity detection is central to quantum information transmission | `DIRECT` | `BACKGROUND` | `PARTIAL` | `PARTIAL` | `DIRECT` | I_c may be only causal conditioning of known capacity | `CLAIMS_EXTRACTED` |
| `SRC-DECOHERENCE-EINSELECTION` | Decoherence and the transition from quantum to classical | arXiv review | https://arxiv.org/abs/quant-ph/0105127 | `decoherence` | decoherence, einselection, environment-induced superselection | environment-induced monitoring explains loss of interference | `BACKGROUND` | `DIRECT` | `PARTIAL` | `PARTIAL` | `DIRECT` | K may be only an observer-accessible coherence gate | `CLAIMS_EXTRACTED` |
| `SRC-RESOURCE-THEORY-COHERENCE` | Quantifying coherence | arXiv technical paper | https://arxiv.org/abs/1311.0275 | `decoherence` | coherence measure, resource theory of coherence | formal criteria for coherence as resource | `BACKGROUND` | `DIRECT` | `PARTIAL` | `PARTIAL` | `DIRECT` | K must specify a standard coherence measure | `CLAIMS_EXTRACTED` |
| `SRC-QUANTUM-ERROR-CORRECTION` | Quantum error correction | source family | Shor 1995 / primary-source review required | `qec` | encoded information, error correction, recovery operation | recoverability after noise/decoherence | `PARTIAL` | `PARTIAL` | `DIRECT` | `PARTIAL` | `DIRECT` | R collapses unless tied to causal-observer order | `NEEDS_SOURCE` |
| `SRC-ENTANGLEMENT-WEDGE-PETZ` | Entanglement wedge reconstruction using the Petz map | arXiv technical paper | https://arxiv.org/abs/1902.02844 | `entanglement_wedge` | Petz map, entanglement wedge reconstruction | reconstruction from boundary subregions using recovery ideas | `PARTIAL` | `PARTIAL` | `DIRECT` | `POSSIBLE_BRIDGE` | `PARTIAL` | same-family bridge for subdomain recoverability | `NEEDS_EXPERT_REVIEW` |
| `SRC-UNIVERSAL-RECOVERY-ENTANGLEMENT-WEDGE` | Entanglement wedge reconstruction via universal recovery channels | arXiv technical paper | https://arxiv.org/abs/1704.05839 | `entanglement_wedge` | universal recovery channel, wedge reconstruction | recovery-channel formulation of reconstruction | `PARTIAL` | `PARTIAL` | `DIRECT` | `POSSIBLE_BRIDGE` | `PARTIAL` | same-family bridge for reconstructable domains | `NEEDS_EXPERT_REVIEW` |

## 3. Metadata Summary

```yaml
source_metadata_status: POPULATED_INITIAL_SOURCE_INDEX
source_count: 14
direct_redundancy_threats:
  - recoverability
  - petz_recovery
  - coherent_information_channel_capacity
  - decoherence_einselection
  - resource_theory_of_coherence
  - quantum_error_correction
partial_redundancy_threats:
  - aqft_local_algebras
  - relativistic_qft_measurement
  - information_causality
  - entanglement_wedge_reconstruction
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
```

