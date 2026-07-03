# I/K/R Operational Residue Review — Frontera C-Mayor

## FOCUS CHECK

- Current objective: test the remaining `I_c/K/R` bridge residue against quantum information, decoherence, and recoverability.
- Classification: CORE / BRIDGE
- Current accepted status: BRIDGE_FORMAL_FRAMEWORK_CREATED
- Current validation status: NOT_VALIDATED
- Current novelty status: UNRESOLVED
- Current redundancy risk: MEDIUM_HIGH
- Drift risk: LOW
- Allowed action: operational redundancy review only.

## 1. Purpose and Scope

After the AQFT / Haag-Kastler comparison, the following Frontera C-Mayor components are strongly absorbed:

```yaml
D_LC(O): strongly_absorbed_by_AQFT
A_c(O,e): strongly_absorbed_by_AQFT
M(O,e): largely_absorbed_by_AQFT
```

The remaining possible bridge residue is:

```txt
I_c(O <- e)
K(O,e)
R(O,e)
```

This review asks whether those relations have any non-redundant operational role or whether they collapse into existing quantum information, decoherence, and recoverability frameworks.

This document does not validate Frontera C-Mayor. It does not claim novelty or partial support.

## 2. Current Post-AQFT Status

```yaml
post_aqft_status:
  D_LC_O: strongly_absorbed_by_AQFT
  A_c_O_e: strongly_absorbed_by_AQFT
  M_O_e: largely_absorbed_by_AQFT
  I_c_K_R: unresolved_surviving_bridge_layer
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
```

The AQFT review concluded:

```txt
AQFT absorbs much of the causal-observable structure.
Only the bridge layer remains live.
```

The question now is whether that bridge layer is more than a bundle of already-standard tools.

## 3. Review of `I_c(O <- e)`

### Possible Meaning

`I_c(O <- e)` means physically transmissible information from event/domain `e` to observer `O`, through channels allowed by causal structure.

Candidate formalization from `docs/frontera_c/RELATION_FORMALIZATION.md`:

```txt
I_c(O <- e) > 0 iff there exists a c-supported physical channel Ch_{e->O}
such that I(X_e; Y_O | Ch_{e->O}, A_c(O,e)=1) > 0.
```

### Relation to Classical / Quantum Channel Capacity

This relation overlaps strongly with classical and quantum channel theory.

Quantum information theory already treats quantum channels as completely positive trace-preserving maps and studies their capacity to transmit classical or quantum information. Coherent information and quantum channel capacity already formalize whether quantum information can be transmitted through a noisy channel.

The reviewed source on coherent information states that detecting positive quantum capacity is a central open problem and gives the standard relation between quantum capacity and coherent information. This is a direct overlap with any definition of `I_c` as quantum-transmissible information.

Classification:

```txt
SAME_FAMILY / STRONG_COLLAPSE_RISK
```

### Relation to Causal Communication

The causal part of `I_c` is not independent after AQFT and relativity:

```txt
allowed channel support is already constrained by causal structure, locality, and no-signalling.
```

Thus:

```txt
I_c = channel information + causal support
```

is a bridge synthesis, not a new relation.

### Relation to Information Causality

Information causality is a known information-theoretic principle constraining information gain under communication limitations. It is not identical to `I_c(O <- e)`, but it makes the terminology and conceptual space non-empty before Frontera C-Mayor.

Classification:

```txt
NEAR_MATCH
```

### Relation to AQFT Local Observables

If `I_c(O <- e)` means only that a local algebra contains an observable whose statistics depend on `e`, it collapses into AQFT/local observable structure.

If it means channel capacity, mutual information, or coherent information through an explicitly defined operational channel, it collapses into standard information theory unless a new causal-informational theorem is produced.

### Collapse Risk

```yaml
collapse_risk: HIGH
collapses_into:
  - quantum_channel_capacity
  - coherent_information
  - mutual_information
  - AQFT_local_observable_dependence
  - no_signalling_causal_support
```

### Possible Operational Residue

The possible residue is narrow:

```txt
I_c could act as a project-specific gate requiring information transfer to be explicitly tied to an observer, a target event variable, and causal support.
```

This is useful as bridge discipline but does not currently define a new formal object.

Decision:

```txt
I_c_SURVIVES_AS_BRIDGE_GATE_ONLY
```

## 4. Review of `K(O,e)`

### Possible Meaning

`K(O,e)` means observer-accessible coherence from `e` above a declared threshold.

Candidate formalization:

```txt
K(O,e) = C(rho_{O,e})
K(O,e) >= theta_K
```

where `C` is a declared coherence measure.

### Relation to Decoherence Theory

Decoherence theory already explains loss of interference and emergence of effectively classical mixtures through environmental interaction. Zurek's decoherence/einselection framework treats the environment as monitoring certain observables and destroying interference between pointer-state alternatives.

This strongly overlaps `K(O,e)` as accessible coherence.

Classification:

```txt
BACKGROUND_KNOWN_PHYSICS / STRONG_COLLAPSE_RISK
```

### Relation to Phase Coherence

If `K` measures phase-information accessibility, it overlaps with ordinary coherence measures, off-diagonal terms in a preferred basis, interference visibility in general formal settings, and resource theories of coherence.

The resource-theory literature already provides formal criteria for coherence measures and treats coherence as an operational resource.

Classification:

```txt
SAME_FAMILY
```

### Relation to Entanglement Degradation

If coherence loss is modeled through entanglement with an environment, decoherence and open quantum systems already cover the mechanism. If recoverable entanglement is the target, the issue moves toward quantum error correction and recoverability.

### Relation to Algebraic States / Restrictions

AQFT local algebras and state restrictions already complicate coherence access. The Halvorson AQFT PDF strengthens this issue through type III local algebras and Reeh-Schlieder consequences. Therefore `K` cannot be treated as a simple local finite-dimensional coherence measure unless a domain-specific reduction is justified.

### Collapse Risk

```yaml
collapse_risk: HIGH
collapses_into:
  - decoherence_theory
  - einselection
  - quantum_coherence_resource_theory
  - open_quantum_systems
  - AQFT_state_restriction_issues
```

### Possible Operational Residue

The possible residue is:

```txt
K could serve as a threshold gate requiring the project to state which coherence measure is accessible to O for target event variable e.
```

This is useful as bridge discipline but not a new physical principle.

Decision:

```txt
K_SURVIVES_AS_BRIDGE_GATE_ONLY
```

## 5. Review of `R(O,e)`

### Possible Meaning

`R(O,e)` means recoverability or reconstructability of relevant event information from records available to observer `O`.

Candidate formalization:

```txt
R(O,e) >= theta_R iff there exists a reconstruction map g(Y_O)
such that expected reconstruction error L(g(Y_O), X_e) <= epsilon_R.
```

### Relation to Petz Recovery

The Petz recovery map already formalizes recovery of an input state from a channel output relative to a reference state. It is used in quantum information theory, quantum retrodiction, error correction, and entanglement wedge reconstruction.

Therefore `R(O,e)` overlaps very strongly with known recoverability theory if it is cast as reconstruction from records or channel outputs.

Classification:

```txt
SAME_FAMILY / STRONG_COLLAPSE_RISK
```

### Relation to Quantum Error Correction

Quantum error correction already studies conditions under which encoded quantum information can be recovered after noise, decoherence, or other channel errors. If `R` means recoverability after noise, then QEC is a direct known framework.

Classification:

```txt
SAME_FAMILY
```

### Relation to Reconstruction Maps

Generic reconstruction maps, posterior inference, fidelity thresholds, and loss functions are already standard in classical/quantum inference and information theory.

Thus:

```txt
R = existence of reconstruction map above threshold
```

is not novel without a theorem tying it to causal-informational membrane structure in a way not already captured by recoverability theory.

### Relation to Entanglement Wedge Reconstruction

Entanglement wedge reconstruction is relevant as a near or same-family framework because it uses quantum error correction and recovery maps to reconstruct bulk information from boundary subregions. Petz-map and universal-recovery-channel work make this overlap explicit.

This does not directly equal Frontera C-Mayor, but it shows that recoverability boundaries tied to subregion access already exist in advanced quantum-information and quantum-gravity contexts.

### Collapse Risk

```yaml
collapse_risk: VERY_HIGH
collapses_into:
  - Petz_recovery
  - quantum_error_correction
  - reconstruction_maps
  - entanglement_wedge_reconstruction
  - statistical_inference
```

### Possible Operational Residue

The possible residue is:

```txt
R could require that recoverability be evaluated only after causal support, local observability, information transfer, and coherence access are fixed.
```

This is a useful ordering constraint, not a currently novel recoverability concept.

Decision:

```txt
R_SURVIVES_AS_BRIDGE_GATE_ONLY
```

## 6. Joint-Layer Test

The combined layer:

```txt
I_c(O <- e) > 0
K(O,e) >= theta_K
R(O,e) >= theta_R
```

could create a useful composite boundary only if the conjunction does something no single known framework already does.

### What the Joint Layer Adds

It forces a disciplined sequence:

```txt
causal support
-> local observability / measurement availability
-> information transfer
-> coherence access
-> recoverability
```

This sequence is useful for claim control.

### What It Does Not Yet Add

It does not yet provide:

- a new capacity measure,
- a new coherence measure,
- a new recovery map,
- a new theorem,
- a new physical boundary,
- a falsifiable core prediction.

### Composite Boundary Assessment

The composite boundary may not be present as a named single object in one framework, but it is currently a conjunction of known conditions:

```txt
AQFT/local observables + quantum channels + decoherence/coherence theory + QEC/recoverability
```

That is bridge synthesis.

Decision:

```txt
JOINT_LAYER_USEFUL_AS_BRIDGE_ONLY
```

## 7. Collapse Table

| Object | Closest known framework | Covered? | Possible residue | Decision |
|---|---|---|---|---|
| `I_c(O <- e)` | Quantum channel capacity, coherent information, mutual information, causal communication | Mostly covered | Observer/target-specific information gate after causal support | BRIDGE_GATE_ONLY |
| `K(O,e)` | Decoherence, einselection, resource theory of coherence, open quantum systems | Mostly covered | Explicit observer-accessible coherence threshold | BRIDGE_GATE_ONLY |
| `R(O,e)` | Petz recovery, quantum error correction, reconstruction maps, entanglement wedge reconstruction | Strongly covered | Ordered recoverability gate after causal/information/coherence checks | BRIDGE_GATE_ONLY |
| `I_c/K/R` conjunction | Composite of QI, decoherence, QEC, AQFT-local access | Not named as one object, but components covered | Bridge checklist / layered claim-control boundary | BRIDGE_LAYER_ONLY |

## 8. Decision

Allowed decisions:

```txt
IKR_COLLAPSES_TO_KNOWN_FRAMEWORKS
IKR_SURVIVES_AS_BRIDGE_LAYER_ONLY
IKR_SURVIVES_WITH_OPERATIONAL_RESIDUE
IKR_BLOCKED_PENDING_EXPERT_REVIEW
```

Decision:

```txt
IKR_SURVIVES_AS_BRIDGE_LAYER_ONLY
```

Secondary qualifier:

```txt
IKR_BLOCKED_PENDING_EXPERT_REVIEW
```

Reason:

```txt
Each individual relation strongly overlaps known frameworks. The conjunction is useful as an ordered bridge checklist, but no non-redundant operational object has been established. Any promotion requires expert review plus a theorem or worked model showing that the composite boundary is not merely the intersection of known constraints.
```

## 9. Consequence for Frontera C-Mayor

Allowed consequences:

```txt
DEMOTE_TO_INTERPRETIVE_FRAME_ONLY
KEEP_AS_BRIDGE_FORMAL_FRAMEWORK
RESTORE_AS_CORE_THEORY_CANDIDATE_PENDING_THEOREM
BLOCK_PENDING_EXTERNAL_REVIEW
```

Decision:

```txt
KEEP_AS_BRIDGE_FORMAL_FRAMEWORK
```

Secondary qualifier:

```txt
BLOCK_PENDING_EXTERNAL_REVIEW
```

Interpretation:

```txt
Frontera C-Mayor remains a useful bridge formal framework. It is not restored as a core theory candidate. It should be demoted only if external review says the composite I/K/R layer adds no useful ordering, taxonomy, or claim-control value.
```

## 10. Required Next Action

Required next action:

```txt
DEFINE_IKR_AGAINST_KNOWN_FRAMEWORKS_OR_REQUEST_EXPERT_REVIEW
```

Specific safe options:

1. Define `I_c` explicitly against quantum channel capacity and coherent information.
2. Define `K` explicitly against decoherence/einselection and resource-theory coherence measures.
3. Define `R` explicitly against Petz recovery, QEC, and reconstruction maps.
4. Ask an external quantum information / mathematical physics reviewer whether the ordered conjunction has any nontrivial formal role.

Forbidden next actions:

- benchmarks,
- auxiliary thermal/visibility/contrast work,
- applications,
- validation claims,
- partial-support claims,
- novelty claims.

## 11. Sources Used

Primary / technical sources consulted:

- Coherent information and quantum channel capacity: https://arxiv.org/abs/2107.00392
- Decoherence and einselection: https://arxiv.org/abs/quant-ph/0105127
- Quantifying coherence: https://arxiv.org/abs/1311.0275
- Petz recovery map overview: https://en.wikipedia.org/wiki/Petz_recovery_map
- Entanglement wedge reconstruction using Petz map: https://arxiv.org/abs/1902.02844
- Entanglement wedge reconstruction via universal recovery channels: https://arxiv.org/abs/1704.05839

## 12. Status Update

```yaml
ikr_operational_residue_status: IKR_SURVIVES_AS_BRIDGE_LAYER_ONLY
secondary_status: IKR_BLOCKED_PENDING_EXPERT_REVIEW
frontera_c_consequence: KEEP_AS_BRIDGE_FORMAL_FRAMEWORK
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
core_theory_candidate: false
bridge_framework: true
redundancy_risk: HIGH_FOR_IKR_COMPONENTS_MEDIUM_HIGH_FOR_COMPOSITE
next_action: DEFINE_IKR_AGAINST_KNOWN_FRAMEWORKS_OR_REQUEST_EXPERT_REVIEW
```

Final discipline:

```txt
The I/K/R layer is useful only as bridge ordering until a non-redundant theorem or expert-reviewed operational residue exists.
```
