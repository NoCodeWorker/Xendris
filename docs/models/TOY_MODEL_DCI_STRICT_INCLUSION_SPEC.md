# Toy Model Spec: D_CI Strict Inclusion

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Model type: non-empirical toy model.
- Purpose: formal usability only.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Benchmark status: not run.

## 1. Purpose

This toy model tests whether the formal grammar can represent an event that is causally accessible but not causally-informationally measurable, coherent, and recoverable.

It does not test nature.

## 2. Toy Universe

Let:

```txt
O = a single observer
E = {e0, e1, e2, e3}
```

Relations are Boolean predicates:

```txt
A_c(O,e): event is inside causal accessibility domain
I_c(O <- e): event can transmit usable information to O
M(O,e): a measurement relation is possible
K(O,e): coherence access is above threshold
R(O,e): recoverability is above threshold
```

## 3. Domain Definitions

```txt
D_LC(O) = { e | A_c(O,e) = true }

D_CI(O) = { e |
  A_c(O,e) = true
  and I_c(O <- e) = true
  and M(O,e) = true
  and K(O,e) = true
  and R(O,e) = true
}
```

## 4. Toy Relation Table

| Event | `A_c` | `I_c` | `M` | `K` | `R` | Domain Result |
|---|---|---|---|---|---|---|
| `e0` | true | true | true | true | true | in `D_LC`, in `D_CI` |
| `e1` | true | false | true | true | true | in `D_LC`, outside `D_CI` |
| `e2` | true | true | true | false | true | in `D_LC`, outside `D_CI` |
| `e3` | true | true | true | true | false | in `D_LC`, outside `D_CI` |

## 5. Strict Inclusion Demonstration

From the table:

```txt
D_LC(O) = {e0, e1, e2, e3}
D_CI(O) = {e0}
```

Therefore:

```txt
D_CI(O) proper subset D_LC(O)
```

## 6. Example Interpretations

### `e1`: Information Failure

`e1` is causally accessible, but usable information transfer fails.

Known-framework collapse risk:

```txt
quantum channel / communication theory
```

### `e2`: Coherence Failure

`e2` is causally accessible and measurable, but coherence access fails.

Known-framework collapse risk:

```txt
decoherence / coherence theory
```

### `e3`: Recoverability Failure

`e3` is causally accessible, measurable, and coherent enough for access, but the relevant state cannot be reconstructed or recovered under the chosen threshold.

Known-framework collapse risk:

```txt
Petz recovery / QEC / reconstruction theory
```

## 7. What This Toy Model Shows

It shows:

- the grammar can represent strict inclusion,
- `D_CI(O)` can be smaller than `D_LC(O)`,
- a causal domain can be filtered by information, measurement, coherence, and recoverability predicates.

## 8. What This Toy Model Does Not Show

It does not show:

- physical validation,
- novelty,
- empirical support,
- benchmark performance,
- that `B_c(O)` exists in nature,
- that Frontera C-Mayor is a core theory.

## 9. Acceptance Criteria for Formal Usability

The toy model is usable if:

1. all relation values are explicit,
2. the strict-inclusion witness is visible,
3. no physical claim is made,
4. known-framework collapse risks are documented,
5. the model can be translated into Lean or another proof assistant.

## 10. Spec Status

```yaml
toy_model_spec_status: CREATED
classification: CORE_BRIDGE
strict_inclusion_witness: true
event_inside_D_LC_outside_D_CI: e1_e2_e3
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
purpose: formal_usability_only
```

