# Frontera C-Mayor External Review Brief

## Purpose

This brief requests a technical sanity check of Frontera C-Mayor in its current accepted status:

```yaml
accepted_status: BRIDGE_FORMAL_FRAMEWORK_CREATED
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
redundancy_risk: MEDIUM_HIGH
core_theory_candidate: false
bridge_framework: true
partial_support: false
```

No validation, partial support, or new-physics claim is being made. The review target is narrower: determine whether the formal distinction introduced below is useful and potentially non-redundant, or whether it is only a synthesis of known physics.

## 1. Short Summary

Frontera C-Mayor asks whether `c` can be used not only as the invariant maximum propagation speed in relativistic physics, but also as the organizing boundary for a causal-informational classification of observer-relative accessibility.

The current bridge framework distinguishes:

```txt
causal accessibility
```

from:

```txt
causal-informational measurability, coherence access, and recoverability.
```

The accepted formal relation is:

```txt
D_CI(O) subset D_LC(O)
```

where `D_LC(O)` is the light-cone/causal-accessibility domain of observer `O`, and `D_CI(O)` is a stricter candidate domain requiring information transfer, measurement possibility, coherence access, and recoverability.

The main review question is:

```txt
Is D_CI(O) subset D_LC(O) a useful non-redundant formal distinction, or only a synthesis of known physics?
```

## 2. What Is Not Claimed

The current project does not claim:

- Frontera C-Mayor is validated.
- Frontera C-Mayor has partial support.
- Frontera C-Mayor is established new physics.
- `B_c(O)` is a proven physical boundary.
- `D_CI(O)` is already a theorem.
- Auxiliary studies validate the framework.
- Benchmarks or applications are relevant to the current review.

The project is explicitly asking whether the bridge formalism is worth developing or should be demoted.

## 3. Formal Objects

Let:

```txt
O = observer or measurement system
e = event or domain element
E = event/domain set
c = invariant causal speed
```

### `D_LC(O)`

```txt
D_LC(O) = { e in E | A_c(O,e)=1 }
```

This is the domain of events causally accessible to `O` under `c`-constrained causal structure.

### `D_CI(O)`

```txt
D_CI(O) = { e in E |
  A_c(O,e)=1
  and I_c(O <- e)>0
  and M(O,e)=1
  and K(O,e)>=theta_K
  and R(O,e)>=theta_R
}
```

This is the candidate causal-informational measurability domain.

### `B_c(O)`

```txt
B_c(O) = boundary(D_CI(O), E \ D_CI(O))
```

This is the candidate boundary between causal-informational measurability and failure of at least one required layer.

It is not currently claimed as a proven physical boundary.

## 4. Relation Definitions

### `A_c(O,e)` — Causal Accessibility

```txt
A_c(O,e)=1 iff e is causally accessible to O under c-constrained causal structure.
```

Classification:

```txt
KNOWN_PHYSICS
```

### `I_c(O <- e)` — Transmissible Information

```txt
I_c(O <- e)>0 iff a c-supported physical channel carries nonzero information from e to records available to O.
```

Classification:

```txt
STANDARD_INFORMATION_THEORY / NEW_SYNTHESIS
```

### `M(O,e)` — Measurement Possibility

```txt
M(O,e)=1 iff a physically allowed measurement relation can form an accessible record at O for the target event variable.
```

Classification:

```txt
STANDARD_MEASUREMENT_THEORY / NEW_SYNTHESIS
```

### `K(O,e)` — Coherence Access

```txt
K(O,e)>=theta_K iff coherence-relevant information remains accessible above a declared threshold.
```

Classification:

```txt
STANDARD_DECOHERENCE / NEW_SYNTHESIS
```

### `R(O,e)` — Recoverability

```txt
R(O,e)>=theta_R iff the relevant event information is recoverable from records available to O above a declared threshold.
```

Classification:

```txt
STANDARD_INFORMATION_THEORY / NEW_SYNTHESIS
```

## 5. Meaning of `D_CI(O) subset D_LC(O)`

The subset relation is accepted as meaningful in a conservative sense:

```txt
Any event in D_CI(O) must be causally accessible to O.
```

The strict distinction is:

```txt
An event can be causally accessible while still failing information transfer, measurement possibility, coherence access, or recoverability.
```

This is not automatically novel. Known physics already recognizes that causal accessibility does not guarantee measurement or recoverability. The review question is whether the formal packaging of those layers around `c` creates any non-redundant formal value.

## 6. Redundancy Risk

Current redundancy risk:

```txt
MEDIUM_HIGH
```

The framework may collapse into known physics if:

- `D_CI(O)` is only light-cone accessibility plus ordinary measurement constraints,
- `I_c` is only standard channel information,
- `K` is only ordinary decoherence,
- `R` is only standard reconstruction/inference,
- `B_c(O)` cannot be distinguished from existing observability, horizon, or channel-capacity boundaries.

## 7. Rejection Criteria

A reviewer should reject or demote the framework if any of the following hold:

1. `D_CI(O)` is purely definitional and creates no theorem path.
2. `B_c(O)` is indistinguishable from known light-cone, horizon, measurement, channel, decoherence, or recoverability boundaries.
3. `theta_K` and `theta_R` cannot be defined non-arbitrarily.
4. The framework creates no falsifiable failure condition.
5. The formalism obscures rather than clarifies standard causal structure.
6. All examples are already fully explained by known physics with no remaining formal value.

## 8. Survival Criteria

The framework survives as useful bridge formalism if:

1. It clearly prevents the mistaken inference that causal accessibility implies measurability.
2. It provides a disciplined layered checklist for causal access, information transfer, measurement, coherence, and recoverability.
3. It can be formalized without contradicting relativity or quantum theory.
4. It creates a clear path to either a theorem candidate or principled demotion.

The framework could be promoted toward `CORE_THEORY_CANDIDATE` only if:

1. a nontrivial theorem path exists,
2. the theorem is not true by definition alone,
3. the result is not reducible to known physics,
4. falsification or collapse conditions are explicit.

## 9. Requested Reviewer Output

Please classify the framework as one of:

```txt
REDUNDANT_WITH_KNOWN_PHYSICS
USEFUL_BRIDGE_FRAMEWORK
FORMAL_THEOREM_CANDIDATE
NEEDS_MAJOR_REWRITE
CONCEPTUAL_ERROR
REVIEWER_REQUESTS_CLARIFICATION
```

Useful comments would identify:

- which relation is redundant or unclear,
- whether `D_CI(O)` is mathematically meaningful,
- whether `B_c(O)` can be made precise,
- whether thresholds can be non-arbitrary,
- whether a theorem or falsifiability path exists.

## 10. Current Working Decision

Until external review says otherwise:

```yaml
accepted_status: BRIDGE_FORMAL_FRAMEWORK_CREATED
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
redundancy_risk: MEDIUM_HIGH
```

Final boundary:

```txt
External review may change classification.
It does not itself validate Frontera C-Mayor.
```
