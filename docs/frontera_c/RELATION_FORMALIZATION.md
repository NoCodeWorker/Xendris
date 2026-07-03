# Relation Formalization — Frontera C-Mayor

## LOOP CYCLE 5 — FOCUS CHECK

- Current objective: formalize `A_c`, `I_c`, `M`, `K`, and `R` enough to judge whether `D_CI(O)` is a meaningful subdomain of `D_LC(O)`.
- Classification: CORE / BRIDGE
- Link to FRONTERA_C_MAYOR: tests the internal structure of `c` as causal-informational membrane.
- Current validation state: NOT_VALIDATED
- Main uncertainty: whether the strict subdomain is non-redundant or a structured restatement of known physics.
- Drift risk: LOW
- Allowed action: relation formalization only.

## GAP SELECTED

```yaml
gap: RELATION_FORMALIZATION_GAP
reason: Cycle 4 left the CIS Proposition blocked because `I_c`, `M`, `K`, `R`, and thresholds were not independently formalized.
```

## 1. Working Domain

Let:

```txt
O = observer or measurement system
e = event/domain element
E = event/domain set
c = invariant causal speed
```

Define the light-cone-accessible domain:

```txt
D_LC(O) = { e in E | A_c(O,e)=1 }
```

Define the candidate causal-informational domain:

```txt
D_CI(O) = { e in E |
  A_c(O,e)=1
  and I_c(O <- e)>0
  and M(O,e)=1
  and K(O,e)>=theta_K
  and R(O,e)>=theta_R
}
```

Candidate membrane:

```txt
B_c(O) = boundary(D_CI(O), E \ D_CI(O))
```

This remains a definition candidate, not validation.

## 2. `A_c(O,e)` — Causal Accessibility

### Plain-Language Meaning

`A_c(O,e)` states whether event `e` can causally affect observer `O` under the invariant speed limit `c`.

### Formal Candidate Definition

```txt
A_c(O,e)=1 iff e is in the causal past/accessibility domain of O
```

Equivalently:

```txt
A_c(O,e)=1 iff there exists a future-directed causal curve or allowed physical signal path from e to O.
```

### Known-Physics Origin

- Special relativity.
- General-relativistic causal structure.
- Light-cone membership.
- Timelike and lightlike causal order.

### Whether It Is Already Standard

Yes. This is known physics.

### Whether Frontera C-Mayor Adds Anything

Not by itself. Frontera C-Mayor only uses `A_c` as the necessary causal-accessibility base layer.

### Required Assumptions

- A spacetime or causal-order structure exists.
- `O` and `e` are localized enough for causal relation analysis.
- Superluminal signalling is excluded.
- The relevant causal domain is physically specified.

### Failure Modes

- Observer or event not well-defined.
- Global spacetime causal structure is ambiguous.
- Horizon or boundary conditions are underspecified.
- The formalism silently treats causal accessibility as measurement availability.

### Possible Measurable Proxy

- Light-cone membership.
- Causal curve existence.
- Signal arrival possibility.
- Horizon-accessibility classification.

### Observer-Relative?

Yes. The relation depends on observer location, worldline, and causal domain.

### Directly Depends on `c`?

Yes. `c` defines the causal speed boundary.

### Can Separate `D_CI(O)` From `D_LC(O)`?

No. `A_c` defines `D_LC(O)`. Separation requires at least one of `I_c`, `M`, `K`, or `R` to fail while `A_c=1`.

### Relation Classification

```txt
KNOWN_PHYSICS
```

## 3. `I_c(O <- e)` — Transmissible Information

### Plain-Language Meaning

`I_c(O <- e)` measures whether physically transmissible information from `e` can reach `O` through channels allowed by causal structure.

### Formal Candidate Definition

Let `X_e` be a variable or state associated with `e`, and `Y_O` be the record available to `O`.

```txt
I_c(O <- e) > 0 iff there exists a c-supported physical channel Ch_{e->O}
such that I(X_e; Y_O | Ch_{e->O}, A_c(O,e)=1) > 0.
```

A channel-capacity form is:

```txt
C_c(e->O) > 0
```

where `C_c` is channel capacity restricted to physically allowed causal support.

### Known-Physics Origin

- Shannon information theory.
- Quantum information theory.
- Relativistic no-signalling constraints.
- Physical channel models.

### Whether It Is Already Standard

Mostly standard information theory plus known causal constraints.

### Whether Frontera C-Mayor Adds Anything

It adds a synthesis requirement: information transfer must be explicitly conditioned on `c`-constrained causal accessibility. This is bridge structure, not yet new physics.

### Required Assumptions

- A source variable or state at `e` is defined.
- A record variable at `O` is defined.
- A physical channel family is specified.
- Noise, loss, erasure, and coupling are modeled.
- Mutual information or capacity is the correct proxy for the claim.

### Failure Modes

- `A_c=1` but there is no coupling channel.
- Channel capacity is zero.
- Records are completely erased.
- The chosen information variable is arbitrary.
- Mutual information is nonzero but operationally unusable.

### Possible Measurable Proxy

- Mutual information.
- Channel capacity.
- Distinguishability of received records.
- Posterior entropy reduction at `O`.

### Observer-Relative?

Yes. Available records and channel access depend on `O`.

### Directly Depends on `c`?

Indirectly and structurally. The information measure itself is not `c`, but the allowed channel support is constrained by `c`.

### Can Separate `D_CI(O)` From `D_LC(O)`?

Yes. An event may be causally accessible while transmitting no recoverable information to `O`.

### Relation Classification

```txt
STANDARD_INFORMATION_THEORY
NEW_SYNTHESIS
```

## 4. `M(O,e)` — Measurement Possibility

### Plain-Language Meaning

`M(O,e)` states whether `O` can physically form a measurement record about `e`.

### Formal Candidate Definition

```txt
M(O,e)=1 iff there exists a physically allowed measurement interaction,
instrument, or record map from e to an accessible record of O with nonzero
distinguishability for the target observable.
```

A quantum measurement candidate:

```txt
M(O,e)=1 iff there exists an admissible instrument {E_i} and record Y_O
such that outcome statistics depend nontrivially on the target state/event at e.
```

### Known-Physics Origin

- Standard measurement theory.
- Quantum measurement/instrument formalism.
- Operational observability.

### Whether It Is Already Standard

Yes. Measurement possibility is standard, though details depend on the theory and apparatus model.

### Whether Frontera C-Mayor Adds Anything

Only a bridge constraint: measurement possibility is nested inside causal accessibility and information transfer.

### Required Assumptions

- Target observable is specified.
- Interaction or coupling is physically possible.
- A record can be formed and accessed by `O`.
- Measurement back-action and record stability are allowed in the model.
- The measurement relation is not confused with mere causal reachability.

### Failure Modes

- No physical interaction couples `e` to `O`.
- The target observable is not operationally defined.
- A record forms but is not accessible to `O`.
- Apparatus assumptions are smuggled into the definition.
- Measurement availability collapses into ordinary instrument limitation.

### Possible Measurable Proxy

- Existence of a stable record.
- Nonzero likelihood separation between possible event states.
- Operational distinguishability.
- Reproducible measurement protocol.

### Observer-Relative?

Yes. Measurement possibility depends on the observer system, available interactions, and accessible records.

### Directly Depends on `c`?

Indirectly. `c` constrains possible interactions and information arrival; `M` itself is a measurement relation.

### Can Separate `D_CI(O)` From `D_LC(O)`?

Yes. `A_c=1` does not imply that a measurement relation exists.

### Relation Classification

```txt
STANDARD_MEASUREMENT_THEORY
NEW_SYNTHESIS
```

## 5. `K(O,e)` — Coherence Access

### Plain-Language Meaning

`K(O,e)` measures whether coherence-relevant information from `e` remains accessible to `O` above a specified threshold.

### Formal Candidate Definition

Let `rho_{O,e}` be the state or record available to `O` that is relevant to `e`.

```txt
K(O,e) = C(rho_{O,e})
```

where `C` is a declared coherence measure. Then:

```txt
K(O,e) >= theta_K
```

means coherence access is above the accepted threshold.

### Known-Physics Origin

- Quantum coherence theory.
- Decoherence.
- Open quantum systems.
- Resource-theoretic coherence measures.

### Whether It Is Already Standard

The components are standard. The exact `K(O,e)` relation is a project-specific synthesis unless a standard coherence measure and subsystem are declared.

### Whether Frontera C-Mayor Adds Anything

It adds a layered role for coherence inside causal-informational measurability. This may be useful as bridge formalism, but it is not yet a new theorem.

### Required Assumptions

- The relevant quantum state or record is identified.
- A coherence basis or operational coherence measure is chosen.
- `theta_K` is justified rather than arbitrary.
- The observer-accessible subsystem is defined.
- Coherence access is distinguished from generic measurement success.

### Failure Modes

- Basis dependence is unresolved.
- `theta_K` is arbitrary.
- Decoherence alone explains the failure.
- Coherence measure is not operationally tied to `O`.
- The relation becomes a restatement of standard decoherence.

### Possible Measurable Proxy

- Coherence measure on the accessible state.
- Phase-information accessibility.
- Off-diagonal resource measure in a specified basis.
- Fidelity of coherent-state reconstruction.

### Observer-Relative?

Yes. Accessible subsystem and records depend on `O`.

### Directly Depends on `c`?

Indirectly. `c` constrains which coherent information can physically reach `O`; the coherence measure is not itself `c`.

### Can Separate `D_CI(O)` From `D_LC(O)`?

Yes. An event can be causally accessible and even measured while coherence access falls below threshold.

### Relation Classification

```txt
STANDARD_DECOHERENCE
NEW_SYNTHESIS
```

## 6. `R(O,e)` — Recoverability

### Plain-Language Meaning

`R(O,e)` measures whether `O` can reconstruct the relevant event information from available records.

### Formal Candidate Definition

Let `Y_O` be records available to `O`, and `X_e` be the target event variable.

```txt
R(O,e) >= theta_R iff there exists a reconstruction map g(Y_O)
such that expected reconstruction error L(g(Y_O), X_e) <= epsilon_R.
```

Equivalently, in uncertainty terms:

```txt
H(X_e | Y_O) <= h_R
```

or in fidelity terms:

```txt
F(g(Y_O), X_e) >= theta_R
```

depending on the domain.

### Known-Physics Origin

- Information theory.
- Statistical inference.
- Error correction and recovery maps.
- Quantum recoverability.

### Whether It Is Already Standard

The ingredients are standard. The project-specific relation is a bridge synthesis until the target variable, loss function, and threshold are fixed.

### Whether Frontera C-Mayor Adds Anything

It places recoverability as a required layer beyond causal accessibility, signal transfer, measurement relation, and coherence access.

### Required Assumptions

- The reconstruction target is defined.
- Available records are specified.
- A loss, entropy, or fidelity criterion is chosen.
- `theta_R` or equivalent error bound is justified.
- The reconstruction task is not model-dependent in a way that hides assumptions.

### Failure Modes

- Many-to-one channels make reconstruction underdetermined.
- Records are insufficient even if nonzero information exists.
- Recovery depends entirely on an arbitrary prior.
- Thresholds are arbitrary.
- The relation reduces to standard inference quality.

### Possible Measurable Proxy

- Reconstruction error.
- Posterior entropy.
- Recovery fidelity.
- Minimum description error for the target event variable.

### Observer-Relative?

Yes. Recoverability depends on the records and inference resources available to `O`.

### Directly Depends on `c`?

Indirectly. `c` constrains which records can physically be available; recoverability is an information/inference property.

### Can Separate `D_CI(O)` From `D_LC(O)`?

Yes. A causally accessible event can leave records that are too underdetermined to recover the target variable.

### Relation Classification

```txt
STANDARD_INFORMATION_THEORY
NEW_SYNTHESIS
```

## 7. Relation Classification Table

| Relation | Primary classification | Frontera C-Mayor addition | Can separate `D_CI(O)` from `D_LC(O)`? | Decision |
|---|---|---|---|---|
| `A_c(O,e)` | KNOWN_PHYSICS | Base causal layer only. | No; it defines `D_LC(O)`. | Keep as known-physics anchor. |
| `I_c(O <- e)` | STANDARD_INFORMATION_THEORY / NEW_SYNTHESIS | Requires information transfer to be explicitly conditioned on causal support. | Yes. | Keep as bridge relation. |
| `M(O,e)` | STANDARD_MEASUREMENT_THEORY / NEW_SYNTHESIS | Nests measurement inside causal and informational availability. | Yes. | Keep as bridge relation. |
| `K(O,e)` | STANDARD_DECOHERENCE / NEW_SYNTHESIS | Places coherence access inside the layered domain. | Yes. | Keep as bridge relation pending threshold review. |
| `R(O,e)` | STANDARD_INFORMATION_THEORY / NEW_SYNTHESIS | Makes recoverability a separate gate beyond raw information. | Yes. | Keep as bridge relation pending threshold review. |

## 8. Strict Inclusion Test

The strict inclusion:

```txt
D_CI(O) subset D_LC(O)
```

is true by construction because `A_c(O,e)=1` is required for membership in `D_CI(O)`.

The strict form:

```txt
D_CI(O) proper subset D_LC(O)
```

is meaningful if at least one event satisfies:

```txt
A_c(O,e)=1
```

while at least one of the following fails:

```txt
I_c(O <- e)>0
M(O,e)=1
K(O,e)>=theta_K
R(O,e)>=theta_R
```

Current decision:

```yaml
strict_inclusion_meaningful: true
strict_inclusion_novel: false
reason: known physics already allows causal accessibility without measurement, usable information, coherence access, or recoverability.
```

## 9. Example Cases

### Example 1 — Causal Access Without Physical Channel Coupling

```yaml
case_id: CI_CASE_001
description: An event lies inside the causal past of O, but no physical channel couples the relevant event variable to any record available to O.
A_c: 1
I_c: 0
M: 0
K: not_applicable_or_below_threshold
R: below_threshold
fails:
  - I_c(O <- e)>0
  - M(O,e)=1
classification: already_fully_explained_by_known_physics
bridge_value: useful_as_layered_diagnostic
candidate_non_redundant_frontera_c_structure: false
```

Interpretation:

```txt
This shows `D_CI(O)` can be smaller than `D_LC(O)`, but ordinary channel and measurement theory already explain the separation.
```

### Example 2 — Causal Access With Records But Non-Recoverable Target

```yaml
case_id: CI_CASE_002
description: A record reaches O, but the mapping from event states to records is many-to-one or too lossy to reconstruct the target variable.
A_c: 1
I_c: positive_but_insufficient
M: 1
K: unspecified
R: below_threshold
fails:
  - R(O,e)>=theta_R
classification: already_fully_explained_by_known_physics
bridge_value: useful_as_recoverability_gate
candidate_non_redundant_frontera_c_structure: false
```

Interpretation:

```txt
Recoverability is a valid layer, but current content is standard inference and information theory.
```

### Example 3 — Causal Access and Measurement With Coherence Loss

```yaml
case_id: CI_CASE_003
description: A measurement record exists, but coherence-relevant information is inaccessible below the required threshold.
A_c: 1
I_c: positive_for_some_records
M: 1
K: below_threshold
R: below_threshold_for_coherence_target
fails:
  - K(O,e)>=theta_K
  - R(O,e)>=theta_R
classification: already_fully_explained_by_known_physics
bridge_value: useful_as_coherence_access_gate
candidate_non_redundant_frontera_c_structure: false
```

Interpretation:

```txt
This supports `D_CI(O)` as a layered bridge object, but standard decoherence already explains the failure.
```

### Example 4 — Causal Access With Measurement Relation But Ambiguous Target Variable

```yaml
case_id: CI_CASE_004
description: O can measure something causally linked to e, but the target event variable is not specified well enough for information or recovery claims.
A_c: 1
I_c: undefined_or_target_dependent
M: 1_for_some_observable
K: undefined
R: undefined_or_below_threshold
fails:
  - I_c(O <- e)>0 as a target-specific claim
  - R(O,e)>=theta_R
classification: useful_as_bridge_synthesis
bridge_value: highlights_need_for_target_variable_definition
candidate_non_redundant_frontera_c_structure: false
```

Interpretation:

```txt
This is not new physics. It is a useful guardrail against treating generic measurement as causal-informational measurability.
```

## 10. Non-Redundancy Assessment

`D_CI(O)` is meaningful as a formal bridge object because it prevents this invalid inference:

```txt
A_c(O,e)=1 therefore e is measurable/recoverable by O.
```

However, that correction is already compatible with known physics.

Current non-redundant residue:

```yaml
residue: weak_layered_classification_only
non_redundant_theorem: false
bridge_framework_value: true
core_theory_value: not_established
```

## 11. Decision

Allowed decision:

```txt
BRIDGE_FORMAL_FRAMEWORK
```

Reason:

```txt
D_CI(O) is a meaningful strict subdomain candidate of D_LC(O), but the current separation is explained by standard causal structure, information theory, measurement theory, decoherence, and recoverability. The formalism is useful as a bridge framework and claim-control device, not yet as a CORE theorem.
```

## 12. Status After Cycle 5

```yaml
relations_formalized:
  - A_c(O,e)
  - I_c(O <- e)
  - M(O,e)
  - K(O,e)
  - R(O,e)
strict_inclusion_meaningful: true
strict_inclusion_novel: false
D_CI_decision: BRIDGE_FORMAL_FRAMEWORK
non_redundant_residue_found: weak_layered_classification_only
redundancy_risk_before: MEDIUM_HIGH
redundancy_risk_after: MEDIUM_HIGH
validation_status: NOT_VALIDATED
human_review_required: true
```

## 13. Human Review Question

Should Frontera C-Mayor continue by attempting an external-reviewable theorem for `D_CI(O)`, or should `D_CI(O)` be explicitly demoted to a bridge formal framework that organizes known causal, informational, measurement, coherence, and recoverability constraints?
