# I/K/R Claim Extraction Table

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Objective: extract conservative claim summaries from indexed source families.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Partial support: false.

## 1. Status

```yaml
ik_claim_extraction_status: CLAIMS_EXTRACTED_INITIAL
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
```

## 2. Claim Extraction

| Source ID | Extracted claim summary | Maps to | Redundancy implication | Decision |
|---|---|---|---|---|
| `SRC-AQFT-HAAG-KASTLER-LOCAL-ALGEBRAS` | Local algebras already attach observable structure to spacetime regions and encode locality/microcausality. | `D_LC`, `A_c`, `M`, weak `I_c` | Weak causal-observable versions of `D_CI` collapse into AQFT. | `PARTIALLY_COLLAPSES` |
| `SRC-HALVORSON-MUEGER-AQFT` | AQFT local-algebra structure strengthens redundancy pressure on region-to-observable mapping. | `M`, `D_CI`, weak `K` | Any finite-dimensional informal coherence/measurement layer must be defined against AQFT state/algebra restrictions. | `PARTIALLY_COLLAPSES` |
| `SRC-DETECTOR-QFT-MEASUREMENT` | Detector-based QFT measurement supplies admissible measurement structure through detector coupling and field-state updates. | `M`, partial `I_c` | Measurement possibility is not unique to Frontera C-Mayor. | `PARTIALLY_COLLAPSES` |
| `SRC-CAUSAL-MEASUREMENT-QFT-SPACETIME` | Causal QFT measurement work addresses spacetime-localized measurements without superluminal signaling. | `M`, partial `I_c`, `D_CI` | Relativistic measurement constraints absorb large parts of the local measurement layer. | `PARTIALLY_COLLAPSES` |
| `SRC-LOCAL-MEASUREMENT-FACTORISATION-QFT` | Local measurement factorisation provides criteria for causal admissibility of measurement operations. | `M`, partial `I_c` | `D_CI` cannot ignore existing local-measurement admissibility conditions. | `PARTIALLY_COLLAPSES` |
| `SRC-QUANTUM-RECOVERABILITY-NOISY-STATES` | Recoverability of noisy quantum states already formalizes when information can be recovered after noise. | `R`, partial `I_c`, partial `K` | `R` has strong known-framework coverage. | `COLLAPSES_TO_KNOWN_FRAMEWORK` |
| `SRC-PETZ-RECOVERY-MAP` | Petz recovery is a standard quantum recovery construction tied to information loss/data-processing contexts. | `R` | Generic recoverability collapses into Petz/recovery-map literature unless redefined. | `COLLAPSES_TO_KNOWN_FRAMEWORK` |
| `SRC-INFORMATION-CAUSALITY` | Information causality constrains possible information gain under communication limitations. | `I_c` | `I_c` terminology and causal-information constraints have known-framework pressure. | `PARTIALLY_COLLAPSES` |
| `SRC-COHERENT-INFORMATION-CAPACITY` | Coherent information and channel capacity already formalize quantum information transmissibility. | `I_c`, partial `R` | `I_c` as transmissible information strongly collapses into channel theory. | `COLLAPSES_TO_KNOWN_FRAMEWORK` |
| `SRC-DECOHERENCE-EINSELECTION` | Decoherence/einselection explains loss of accessible interference/coherence through environmental monitoring. | `K`, partial `R` | `K` as accessible coherence strongly collapses into decoherence theory. | `COLLAPSES_TO_KNOWN_FRAMEWORK` |
| `SRC-RESOURCE-THEORY-COHERENCE` | Resource theory defines coherence measures and constraints. | `K` | `K` needs a standard coherence measure or it remains redundant/vague. | `COLLAPSES_TO_KNOWN_FRAMEWORK` |
| `SRC-QUANTUM-ERROR-CORRECTION` | QEC studies recovery of encoded quantum information after errors. | `R`, partial `K` | `R` as recovery after noise is already standard. | `COLLAPSES_TO_KNOWN_FRAMEWORK` |
| `SRC-ENTANGLEMENT-WEDGE-PETZ` | Entanglement wedge reconstruction uses recovery maps to reconstruct subregion information. | `R`, `D_CI` same-family | Reconstructable-domain language already exists in quantum-gravity/QI contexts. | `PARTIALLY_COLLAPSES` |
| `SRC-UNIVERSAL-RECOVERY-ENTANGLEMENT-WEDGE` | Universal recovery-channel results strengthen the recovery/reconstruction overlap. | `R`, `D_CI` same-family | `D_CI` as recoverable subdomain needs expert review against this family. | `NEEDS_EXPERT_REVIEW` |

## 3. Extraction Summary

```yaml
ik_claim_extraction_status: CLAIMS_EXTRACTED_INITIAL
I_c_primary_threat: quantum_channel_capacity_and_information_causality
K_primary_threat: decoherence_and_resource_theory_of_coherence
R_primary_threat: Petz_recovery_QEC_and_reconstruction
joint_layer_primary_threat: conjunction_of_known_frameworks
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
```

