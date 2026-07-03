# AQFT / Haag-Kastler Comparison — Frontera C-Mayor

## FOCUS CHECK

- Current objective: compare Frontera C-Mayor against Haag-Kastler / AQFT.
- Classification: CORE / BRIDGE
- Current accepted status: BRIDGE_FORMAL_FRAMEWORK_CREATED
- Current validation status: NOT_VALIDATED
- Current novelty status: UNRESOLVED
- Current redundancy risk: MEDIUM_HIGH
- Drift risk: LOW
- Allowed action: redundancy comparison only.

## Source Boundary

The local AQFT reference supplied for review was checked:

```txt
C:\Users\usuario\Downloads\AlgebraicQuantumFieldTheory.pdf
```

Extracted identity:

```txt
Title: Algebraic Quantum Field Theory
Author: Hans Halvorson
Appendix: Michael Mueger
Date: February 14, 2006
Pages: 202
```

Relevant sections reviewed:

- Section 2, Structure of the Net of Observable Algebras.
- Section 2.1, Nets of algebras, basic properties.
- Section 2.3, Reeh-Schlieder Theorem.
- Section 2.5, Type of local algebras.
- Section 3, Nonlocality and Open Systems in AQFT.
- Section 3.2, Independence of local algebras.

The comparison below uses this local PDF plus existing Frontera C-Mayor documents and the currently referenced AQFT/Haag-Kastler literature found during the internet redundancy check.

Primary reference anchors:

- Local PDF: `C:\Users\usuario\Downloads\AlgebraicQuantumFieldTheory.pdf`
- Algebraic quantum field theory / Haag-Kastler axioms: https://en.wikipedia.org/wiki/Algebraic_quantum_field_theory
- Haag-Kastler causal-axiom diagnostic: https://arxiv.org/abs/2401.06504
- Causal posets and nets of local algebras: https://arxiv.org/abs/1109.4824
- Locality axiom and tensor products of C*-algebras: https://arxiv.org/abs/1206.5484

This is not validation and not a novelty claim.

## 1. What Haag-Kastler / AQFT Already Formalizes

Haag-Kastler / AQFT formalizes quantum field theory through nets of local algebras assigned to spacetime regions.

Core ideas:

```txt
spacetime region O -> local algebra A(O)
```

The framework already includes:

- local observables associated with spacetime regions,
- isotony: inclusion of spacetime regions implies inclusion of algebras,
- microcausality/locality: spacelike separated local algebras commute,
- Poincare covariance in standard Minkowski settings,
- spectrum condition tied to the forward light cone,
- quasilocal algebra built from the net of local algebras,
- causal structure embedded in algebraic relations.

The local Halvorson PDF states the basic formalism as a net of local observable algebras over spacetime, with double cones mapped to C*-algebras. It gives isotony as the condition that if one region is included in another, the algebra of the smaller region embeds in the algebra of the larger region. It then identifies microcausality as the main relativistic assumption: spacelike separated double cones have commuting algebras.

The same source also strengthens the redundancy pressure through:

- Reeh-Schlieder: under spectrum/additivity assumptions, the vacuum vector is cyclic for every local algebra and, with microcausality, separating.
- Type III local algebras: physically relevant local algebras tend toward hyperfinite type III structures rather than simple finite-dimensional measurement algebras.
- Independence analysis: spacelike separated local algebras are studied through Schlieder, W*-independence, C*-independence, and split-property conditions.

Immediate implication for Frontera C-Mayor:

```txt
AQFT already gives a mature formalism connecting causal spacetime regions and local observable algebras.
```

Therefore, any Frontera C-Mayor object that only maps regions to available observables is at high risk of collapsing into AQFT.

## 2. Mapping Between AQFT Concepts and Frontera C Objects

| AQFT / Haag-Kastler concept | Frontera C object | Mapping strength | Redundancy risk |
|---|---|---:|---|
| Causal spacetime region | `D_LC(O)` | High | `D_LC(O)` is likely background known physics, not a Frontera-specific object. |
| Net of local algebras `A(O)` | Measurement-access structure around `M(O,e)` | High | Local observables already encode what can be represented as observables in a region. |
| Microcausality / locality | `A_c(O,e)` | High | Spacelike-separated commutativity and causal ordering cover the causal-access layer. |
| Nontrivial local observables | `I_c(O <- e)` | Medium/High | If information availability means nontrivial observable dependence, AQFT may absorb much of it. |
| State restriction to local algebra | Observer-accessible record domain | Medium | AQFT can represent local state/observable access, but may not itself define the project’s recovery thresholds. |
| Split property / independence of spacelike systems | Information separation and locality constraints | Medium | Strong overlap with independence/locality, but not identical to `R(O,e)`. |
| Missing explicit layer | `K(O,e)`, `R(O,e)` | Medium | Coherence and recoverability may survive as bridge additions only if independently defined. |

### Causal Region ↔ `D_LC(O)`

AQFT already uses spacetime regions as the domains to which local algebras are assigned. In standard settings, causal structure and light-cone constraints are already part of the background.

Decision:

```txt
D_LC(O) is covered by AQFT-compatible known physics.
```

### Local Algebra / Observables ↔ `M(O,e)`

`M(O,e)` asks whether a measurement relation can form an accessible record. AQFT assigns local observable algebras to spacetime regions, making this the strongest redundancy pressure point.

The Halvorson PDF is especially strong here: the isotony motivation is exactly that an observable measurable in a smaller region is measurable in any containing region. This directly overlaps the measurement-availability part of `M(O,e)`.

Decision:

```txt
M(O,e) is at high risk of collapsing into local observable algebra / admissible local measurement structure.
```

### Microcausality ↔ `A_c(O,e)`

Microcausality states that observables localized in spacelike separated regions commute. This is not identical to `A_c(O,e)`, but it formalizes the causal-separation discipline that `A_c` depends on.

The local PDF explicitly frames microcausality as reflecting constraints imposed by relativity. This means Frontera C-Mayor cannot treat causal separation or no-superluminal-influence structure as a novel component.

Decision:

```txt
A_c(O,e) is background known physics under AQFT/locality.
```

### Non-Trivial Observables ↔ `I_c(O <- e)`

If `I_c(O <- e)>0` merely means that some observable in a causally accessible local algebra depends nontrivially on event data, then `I_c` is likely redundant with AQFT plus standard state/observable dependence.

If `I_c` is instead defined as channel capacity, mutual information, or operational information recoverable by a specific observer, then it may survive as a bridge layer beyond the raw local algebra assignment.

Decision:

```txt
I_c(O <- e) is not currently independent enough to be core theory; it may survive as bridge information layer.
```

The Halvorson PDF also defines a non-triviality condition for nets where each local algebra differs from the scalar identity algebra. That condition is not equivalent to project-specific information transfer, but it increases the risk that a weak `I_c` definition collapses into existence of nontrivial local observables.

### Possible Missing Layer ↔ `K(O,e)`, `R(O,e)`

AQFT is not primarily a recovery-threshold framework. It provides local algebras and states, but does not by itself impose Frontera C-Mayor’s `theta_K` coherence-access or `theta_R` recoverability thresholds.

However, coherence and recoverability already exist in quantum information and decoherence theory. Thus they do not become novel merely by being added to AQFT.

Decision:

```txt
K(O,e) and R(O,e) are the only plausible bridge residue, but remain standard unless tied to a nontrivial theorem.
```

The Reeh-Schlieder and type III discussions in the local PDF make this residue more delicate. AQFT local algebras already have highly nonclassical state/observable structure. Therefore `K` and `R` cannot be informal add-ons; they must be operationally defined against this AQFT background.

## 3. Redundancy Risk

Current risk:

```yaml
redundancy_risk: HIGH_AGAINST_AQFT_FOR_A_c_D_LC_M
overall_redundancy_risk: MEDIUM_HIGH
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
```

High-collapse components:

- `D_LC(O)` as causal-access domain,
- `A_c(O,e)` as causal accessibility,
- `M(O,e)` as local observable / measurement availability.

Medium-collapse components:

- `I_c(O <- e)` if treated as nontrivial local observable dependence,
- `B_c(O)` if treated as boundary of local observable access.

Potential bridge-only components:

- `K(O,e)` as coherence-access layer,
- `R(O,e)` as recoverability layer,
- the full conjunction defining `D_CI(O)`.

Critical risk:

```txt
If D_CI(O) is just the region whose local algebra contains observables relevant to O, then it collapses into AQFT/local measurement structure.
```

Additional local-PDF risk:

```txt
If D_CI(O) only rephrases AQFT's net of local observable algebras, isotony, microcausality, nontriviality, Reeh-Schlieder consequences, or independence properties of local algebras, it collapses into AQFT.
```

## 4. Possible Non-Redundant Residue

The possible residue is not the causal region and not the existence of local observables.

The only surviving candidate is:

```txt
A bridge layer that takes AQFT/local-algebra causal accessibility as input, then adds operational information transfer, coherence access, and recoverability gates for an observer-relative target variable.
```

In symbols:

```txt
AQFT gives: region O -> A(O)
Frontera C-Mayor may add: A(O) + target variable + channel/record relation + K threshold + R threshold
```

This is useful only if:

1. `I_c`, `K`, and `R` are not reducible to ordinary local observable existence.
2. `theta_K` and `theta_R` are non-arbitrary.
3. `B_c(O)` differs from standard local algebra, causal completion, or measurement-access boundaries.
4. The framework produces a theorem, negative theorem, or classification result.

Current residue classification:

```yaml
candidate_non_redundant_residue: bridge_information_coherence_recoverability_layer
strength: weak_to_moderate
core_theory_candidate: false
bridge_framework: true
```

## 5. Decision

Allowed decisions:

```txt
COLLAPSES_TO_AQFT
SURVIVES_AS_BRIDGE_LAYER
BLOCKED_PENDING_EXPERT_REVIEW
```

Decision:

```txt
SURVIVES_AS_BRIDGE_LAYER
```

Secondary qualifier:

```txt
BLOCKED_PENDING_EXPERT_REVIEW
```

Reason:

```txt
AQFT/Haag-Kastler appears to absorb the causal-region, local-observable, and microcausality components of Frontera C-Mayor. D_LC(O), A_c(O,e), and much of M(O,e) are not non-redundant against AQFT. The framework survives only as a bridge layer if I_c, K, and R are operationally defined beyond local observable existence and if their conjunction yields a nontrivial classification.
```

Local PDF adjustment:

```txt
After reviewing Halvorson's Algebraic Quantum Field Theory PDF, the same decision is strengthened. AQFT already formalizes nets of local observable algebras, isotony, microcausality, Reeh-Schlieder consequences, type-III local algebra structure, and independence properties of local algebras. This does not eliminate every possible Frontera C-Mayor bridge role, but it makes any core-theory promotion harder.
```

## 6. Status Update

```yaml
aqft_comparison_status: SURVIVES_AS_BRIDGE_LAYER
secondary_status: BLOCKED_PENDING_EXPERT_REVIEW
local_pdf_reviewed: true
local_pdf: AlgebraicQuantumFieldTheory.pdf
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
redundancy_risk: MEDIUM_HIGH
core_theory_candidate: false
bridge_framework: true
partial_support: false
next_action: compare_against_relativistic_measurement_theory_or_define_I_K_R_against_AQFT
```

## 7. Claims Allowed

Allowed:

- Frontera C-Mayor has been compared against AQFT/Haag-Kastler at a first-pass conceptual level.
- AQFT creates serious redundancy pressure on `D_LC(O)`, `A_c(O,e)`, and `M(O,e)`.
- Frontera C-Mayor currently survives only as a possible bridge layer involving information transfer, coherence access, and recoverability.

## 8. Claims Forbidden

Forbidden:

- Frontera C-Mayor is validated.
- Frontera C-Mayor is novel against AQFT.
- `B_c(O)` is a new physical boundary.
- `D_CI(O)` is a theorem.
- AQFT review proves Frontera C-Mayor.

Final discipline:

```txt
AQFT absorbs much of the causal-observable structure.
Only the bridge layer remains live.
```
