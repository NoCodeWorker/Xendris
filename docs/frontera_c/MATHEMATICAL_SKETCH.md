# Mathematical Sketch — Frontera C-Mayor

## LOOP CYCLE 2 — FOCUS CHECK

- Current objective: create a minimal formal sketch for Frontera C-Mayor.
- Classification: CORE
- Link to FRONTERA_C_MAYOR: formalizes `c` as causal-informational membrane without claiming validation.
- Current validation state: NOT_VALIDATED
- Main uncertainty: whether the formalism adds anything beyond known causal structure.
- Drift risk: LOW
- Allowed action: define variables, relations, claim discipline, and failure modes.

## GAP SELECTED

```yaml
gap: MATHEMATICAL_FORM_GAP
reason: The project has definition, alignment, novelty guardrails, and falsifiability routes, but no minimal formal object. Without a formal sketch, novelty and falsifiability cannot be judged.
```

## 1. Claim Discipline

| Claim | Classification | Status |
|---|---|---|
| `c` defines relativistic causal structure. | KNOWN_PHYSICS | Accepted baseline. |
| Light cones bound direct causal signalling. | KNOWN_PHYSICS | Accepted baseline. |
| Horizons bound observer access in known settings. | KNOWN_PHYSICS | Accepted baseline. |
| Frontera C-Mayor may organize causal, informational, coherent, and measurable access under one membrane formalism. | NEW_HYPOTHESIS | Needs formalization and falsification. |
| The membrane formalism validates new physics. | UNSUPPORTED | Blocked. |
| Auxiliary signal-degradation work validates Frontera C-Mayor. | CONTRADICTED_BY_GOVERNANCE | Blocked. |

## 2. Primitive Objects

Let:

```txt
O = observer or measurement system
E = set of physical events
D = physical domain, subset of E or state/event structure
c = invariant causal speed
J^-(O) = causal past of O
J^+(O) = causal future of O
LC(O) = light-cone structure relative to O
H = horizon or causal boundary, when present
```

These objects are standard or compatible with standard relativity. They do not by themselves create a new theory.

## 3. Candidate Relations

### 3.1 Causal Accessibility

```txt
A_c(O, e) = 1 if event e can be causally connected to O under c-constrained propagation
A_c(O, e) = 0 otherwise
```

Known-physics baseline:

```txt
A_c(O, e) is determined by light-cone membership in ordinary relativistic settings.
```

Novelty risk:

```txt
If A_c is all the model contains, Frontera C-Mayor is only a rename of light-cone causality.
```

### 3.2 Information Transfer

```txt
I_c(O <- e) = physically transmissible information from e to O through c-constrained channels
```

This is not yet a final information measure. It is a placeholder for a future definition using classical, quantum, or operational information.

Known-physics baseline:

```txt
No information can be transferred through a channel that violates relativistic causal constraints.
```

### 3.3 Measurement Relation

```txt
M(O, e) = 1 if O can obtain a measurable record of e
M(O, e) = 0 otherwise
```

Important distinction:

```txt
A_c(O, e) = 1 does not guarantee M(O, e) = 1.
```

An event can be causally accessible in principle but not measured in practice because of coupling, noise, decoherence, detector limits, or missing channel.

### 3.4 Coherence Relation

```txt
K(O, e) = degree to which phase/coherence-relevant information from e remains accessible to O
```

Status:

```txt
NEEDS_FORMALIZATION
```

This relation must not be confused with generic visibility or contrast. It concerns recoverable coherent physical information.

### 3.5 Recoverability

```txt
R(O, e) = degree to which information about e can be reconstructed by O from allowed records
```

Known-physics baseline:

```txt
Recoverability depends on causal access, channel capacity, noise, measurement interaction, and available records.
```

## 4. Candidate Membrane Boundary

Define a provisional membrane boundary:

```txt
B_c(O) = boundary between events/domains for which causal-informational exchange with O is possible and those for which it is not.
```

Minimal set expression:

```txt
D_accessible(O) = { e in E | A_c(O,e)=1 and I_c(O<-e)>0 and M(O,e) is physically possible }
D_inaccessible(O) = E \ D_accessible(O)
B_c(O) = boundary(D_accessible(O), D_inaccessible(O))
```

This is a sketch, not a final equation.

## 5. What This Adds Beyond Light-Cones, If Anything

Potential addition:

```txt
Light-cone membership is necessary but not sufficient for causal-informational measurability.
```

The membrane model attempts to distinguish:

- causal reachability,
- transmissible information,
- measurable record formation,
- coherence preservation,
- recoverability.

This may be useful if it produces a theorem or classification not reducible to light-cone membership alone.

## 6. Redundancy Risk

The sketch becomes non-novel if:

```txt
B_c(O) = boundary(J^-(O)) only
```

or if all added relations reduce to standard measurement limits without any new organizing theorem, classification, or falsifiable claim.

Current risk:

```yaml
REDUNDANCY_RISK: HIGH
```

## 7. Falsifiability Conditions

The sketch fails as a new framework if:

1. `B_c(O)` cannot be distinguished from ordinary light-cone or horizon boundaries.
2. `I_c`, `M`, `K`, and `R` cannot be defined without circularity.
3. The formalism cannot generate a theorem, classification, or prediction that can be wrong.
4. Any proposed consequence is already fully covered by standard relativity, quantum theory, or information theory.
5. The model requires superluminal signalling or contradicts Lorentz invariance.

## 8. Minimal Candidate Claim

```yaml
claim_id: FC-MAYOR-MIN-001
claim_text: Light-cone causal accessibility is necessary but not sufficient for causal-informational measurability; a Frontera C membrane can be modeled as the boundary of events/domains satisfying causal access, nonzero transmissible information, physically possible measurement, and recoverability constraints.
known_physics_baseline: Relativity supplies light-cone causal accessibility; measurement theory and information theory supply channel and record constraints.
membrane_specific_addition: A unified boundary object B_c(O) combining causal access, information transfer, measurement possibility, coherence, and recoverability.
possible_formal_variable: B_c(O)
possible_falsifier: B_c(O) reduces entirely to standard light-cone/horizon membership or ordinary measurement theory with no additional classification or theorem.
possible_observable_or_inferential_consequence: A classification of domains that are causally accessible but not causal-informationally measurable under explicit channel/recoverability constraints.
current_status: NEEDS_FORMALIZATION
validation_scope: NONE
```

## 9. Mathematical Form Status

```yaml
mathematical_form_status: SKETCH
not_final_equation: true
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
falsifiability_status: PARTIAL
human_review_required: true
```

## 10. Next Review Question

The next CORE question is:

```txt
Is FC-MAYOR-MIN-001 merely a restatement of known causal structure plus measurement theory, or does B_c(O) support a distinct theorem/classification?
```
