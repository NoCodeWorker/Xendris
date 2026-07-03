# Minimal Theorem Attempt — Frontera C-Mayor

## LOOP CYCLE 4 — FOCUS CHECK

- Current objective: attempt a minimal non-redundant theorem/proposition for `B_c(O)`.
- Classification: CORE / BRIDGE
- Link to FRONTERA_C_MAYOR: tests whether `c` as causal-informational membrane can be stricter than light-cone membership and broader than ordinary measurement availability.
- Current validation state: NOT_VALIDATED
- Main uncertainty: whether the proposed theorem produces a distinction beyond known physics.
- Drift risk: LOW
- Allowed action: theorem attempt only.

## GAP SELECTED

```yaml
gap: FORMAL_THEOREM_GAP
reason: Cycle 3 left `B_c(O)` blocked pending a theorem or classification. This cycle attempts that theorem without claiming validation.
```

## 1. Proposed Theorem Name

```txt
Causal-Informational Subboundary Proposition
```

Short name:

```txt
CIS Proposition
```

## 2. Plain-Language Statement

Light-cone accessibility is a necessary condition for an observer to receive physical information from an event, but it is not sufficient for causal-informational measurability. A stricter boundary can be defined by requiring causal accessibility, transmissible information, physical measurement possibility, coherence access, and recoverability to hold jointly.

This boundary is not the light cone itself. It is a candidate subboundary inside, or constrained by, the light-cone-accessible domain.

## 3. Formal Statement

Let:

```txt
O = observer or measurement system
E = event/domain set
A_c(O,e) in {0,1} = c-constrained causal accessibility
I_c(O <- e) >= 0 = information transmissible from e to O through c-constrained physical channels
M(O,e) in {0,1} = physical measurement relation
K(O,e) >= 0 = coherent information access
R(O,e) >= 0 = recoverability from available records
theta_K = coherence threshold
theta_R = recoverability threshold
```

Define:

```txt
D_LC(O) = { e in E | A_c(O,e)=1 }
```

and:

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

Proposition:

```txt
If there exists e in E such that A_c(O,e)=1 but at least one of I_c(O<-e)>0, M(O,e)=1, K(O,e)>=theta_K, or R(O,e)>=theta_R fails, then D_CI(O) is a strict subset of D_LC(O). In that case B_c(O) is stricter than the light-cone accessibility boundary.
```

## 4. Required Variables

| Variable | Meaning | Status |
|---|---|---|
| `c` | invariant causal speed | KNOWN_PHYSICS |
| `O` | observer/measurement system | NEEDS_FORMALIZATION |
| `E` | event/domain set | NEEDS_FORMALIZATION |
| `A_c(O,e)` | causal accessibility under `c` | KNOWN_PHYSICS baseline |
| `I_c(O <- e)` | transmissible information through allowed physical channels | NEEDS_FORMALIZATION |
| `M(O,e)` | measurement possibility | NEEDS_FORMALIZATION |
| `K(O,e)` | coherence access | NEEDS_FORMALIZATION |
| `R(O,e)` | recoverability | NEEDS_FORMALIZATION |
| `theta_K` | coherence threshold | NEEDS_JUSTIFICATION |
| `theta_R` | recoverability threshold | NEEDS_JUSTIFICATION |
| `D_LC(O)` | light-cone accessible domain | KNOWN_PHYSICS |
| `D_CI(O)` | causal-informationally measurable domain | THEOREM_CANDIDATE |
| `B_c(O)` | boundary of `D_CI(O)` | THEOREM_CANDIDATE |

## 5. Necessary Conditions

For an event/domain element `e` to be in `D_CI(O)`, all of these are necessary:

1. `A_c(O,e)=1`
2. `I_c(O <- e)>0`
3. `M(O,e)=1`
4. `K(O,e)>=theta_K`
5. `R(O,e)>=theta_R`

Therefore:

```txt
D_CI(O) subset D_LC(O)
```

This subset relation is formally clear but not yet physically novel.

## 6. Sufficient Conditions

The conjunction is sufficient by definition:

```txt
A_c(O,e)=1
and I_c(O <- e)>0
and M(O,e)=1
and K(O,e)>=theta_K
and R(O,e)>=theta_R
=> e in D_CI(O)
```

This is currently definitional, not a derived theorem.

## 7. Difference From Light-Cone Causality

Light-cone causality says whether causal influence is possible under `c`.

The proposed `D_CI(O)` adds:

- channel information transfer,
- measurement possibility,
- coherence access,
- recoverability.

Potential distinction:

```txt
There can be events inside the light cone that are not in D_CI(O).
```

Redundancy risk:

```txt
Known physics already accepts that being inside the light cone does not guarantee measurement.
```

Decision:

```txt
DIFFERENCE_EXISTS_AS_CLASSIFICATION, NOT YET AS NEW PHYSICS
```

## 8. Difference From Horizons

Horizons define causal accessibility boundaries in specific spacetime settings.

`B_c(O)` is not a horizon unless `D_CI(O)` reduces to a horizon-bounded domain.

Potential distinction:

```txt
B_c(O)` could exist inside a horizon-accessible region when information, measurement, coherence, or recoverability constraints fail.
```

Redundancy risk:

```txt
If applied to black holes or cosmology without additional formal content, this becomes ordinary horizon/information language.
```

Decision:

```txt
DISTINCT_FROM_HORIZONS_ONLY_IF_D_CI_SUBBOUNDARY_IS FORMALIZED
```

## 9. Difference From Decoherence Alone

Decoherence concerns loss of coherent phase access through entanglement with uncontrolled degrees of freedom.

`B_c(O)` includes coherence but is not only coherence:

```txt
K(O,e) is one condition among A_c, I_c, M, K, R.
```

Potential distinction:

```txt
An event can fail D_CI because of information transfer, measurement, or recoverability even if decoherence is not the limiting factor.
```

Redundancy risk:

```txt
If K is the only nontrivial condition, the proposition collapses to decoherence/measurement theory.
```

Decision:

```txt
NOT_DECOHERENCE_ALONE, BUT STILL DEPENDENT ON STANDARD CONCEPTS
```

## 10. Difference From Standard Measurement Theory

Standard measurement theory already says physical records require interactions, observables, apparatus, coupling, and noise constraints.

`B_c(O)` tries to force measurement theory to be explicitly conditioned on relativistic causal accessibility:

```txt
M_c(O,e) = M(O,e) constrained by A_c(O,e)
```

Potential distinction:

```txt
It provides a layered classification: causal access first, then information/measurement/coherence/recoverability.
```

Redundancy risk:

```txt
This may be ordinary operational measurement theory plus relativistic causality, not a new theorem.
```

Decision:

```txt
BRIDGE_SYNTHESIS_UNTIL_NONTRIVIAL_RESULT_EXISTS
```

## 11. Possible Non-Redundant Residue

The possible residue is a classification theorem:

```txt
There are at least two boundary layers:
1. LC boundary: causal accessibility under c.
2. CI boundary: causal-informational measurability under A_c, I_c, M, K, R.
```

This is non-redundant only if `CI boundary` is not merely:

- an instrument limit,
- a noise threshold,
- generic decoherence,
- channel capacity failure,
- ordinary horizon access,
- a vocabulary bundle.

Current residue:

```yaml
non_redundant_residue_found: weak
residue_type: layered_classification
not_yet_theorem: true
```

## 12. Failure Modes

The theorem attempt fails if:

1. `D_CI(O)` is only a definition with no theorem.
2. `I_c`, `M`, `K`, or `R` are not independently definable.
3. Thresholds `theta_K` and `theta_R` are arbitrary.
4. Every example of `D_LC \ D_CI` is just ordinary detector failure.
5. The boundary cannot be distinguished from standard observability.
6. The boundary cannot produce a falsifiable classification.
7. The model implies superluminal signalling or violates Lorentz invariance.

## 13. Falsifiability Route

A falsifiable route would require:

```yaml
candidate_domain:
  event_class:
  observer_model:
  known_light_cone_status: A_c=1
  information_channel_definition:
  measurement_relation_definition:
  coherence_access_definition:
  recoverability_definition:
  predicted_boundary: B_c(O)
  failure_condition:
    - D_CI equals D_LC
    - D_CI boundary equals ordinary measurement/noise boundary
    - thresholds are arbitrary
    - no nontrivial classification results
```

This route is not yet instantiated.

## 14. Decision

Allowed decision:

```txt
THEOREM_BLOCKED_PENDING_FORMAL_REVIEW
```

Secondary classification:

```txt
THEOREM_IS_ONLY_BRIDGE_SYNTHESIS in current form
```

Reason:

The candidate creates a useful layered classification, but the subset result is definitional. It does not yet produce a non-redundant theorem beyond known physics. It should not be treated as CORE_THEORY until `I_c`, `M`, `K`, `R`, and thresholds are independently specified and a nontrivial classification follows.

## 15. Status After Cycle 4

```yaml
theorem_candidate: CIS Proposition
theorem_decision: THEOREM_BLOCKED_PENDING_FORMAL_REVIEW
secondary_decision: THEOREM_IS_ONLY_BRIDGE_SYNTHESIS
non_redundant_residue_found: weak_layered_classification_only
redundancy_risk_before: HIGH
redundancy_risk_after: MEDIUM_HIGH
validation_status: NOT_VALIDATED
mathematical_form_status: SKETCH
novelty_status: UNRESOLVED_THEOREM_BLOCKED
human_review_required: true
```

## 16. Human Review Question

Should the project:

1. attempt to formalize `I_c`, `M`, `K`, and `R` into a real theorem, or
2. demote Frontera C-Mayor to a BRIDGE_FRAMEWORK that organizes known causal, measurement, and information concepts without claiming new theory?
