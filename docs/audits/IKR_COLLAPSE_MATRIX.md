# I/K/R Collapse Matrix

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Object under review: `D_LC`, `A_c`, `M`, `I_c`, `K`, `R`, `B_c`, `D_CI`.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Purpose: redundancy control, not validation.

## 1. Classification Legend

| Classification | Meaning |
|---|---|
| `COVERED` | The known framework appears to already contain the core object or function. |
| `PARTIALLY_COVERED` | The known framework covers part of the role but not the full composite use. |
| `UNCLEAR` | The relation needs deeper review. |
| `POSSIBLE_RESIDUE` | A bridge-level role may remain, but it is not yet a theorem or validation. |
| `NOT_COVERED` | No clear overlap has been identified. |
| `REQUIRES_EXPERT_REVIEW` | A domain expert must decide the redundancy boundary. |

## 2. Collapse Matrix

| Object | AQFT / Haag-Kastler | Relativistic measurement theory | Quantum channels | Decoherence | Petz recovery | Quantum error correction | Entanglement wedge reconstruction | Information causality |
|---|---|---|---|---|---|---|---|---|
| `D_LC(O)` | `COVERED` | `COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `NOT_COVERED` | `NOT_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` |
| `A_c(O,e)` | `COVERED` | `COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `NOT_COVERED` | `NOT_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` |
| `M(O,e)` | `PARTIALLY_COVERED` | `COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `NOT_COVERED` | `NOT_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` |
| `I_c(O <- e)` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `COVERED` |
| `K(O,e)` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` |
| `R(O,e)` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `COVERED` | `COVERED` | `COVERED` | `PARTIALLY_COVERED` |
| `B_c(O)` | `REQUIRES_EXPERT_REVIEW` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` | `PARTIALLY_COVERED` |
| `D_CI(O)` | `POSSIBLE_RESIDUE` | `POSSIBLE_RESIDUE` | `POSSIBLE_RESIDUE` | `POSSIBLE_RESIDUE` | `POSSIBLE_RESIDUE` | `POSSIBLE_RESIDUE` | `POSSIBLE_RESIDUE` | `POSSIBLE_RESIDUE` |

## 3. Object Notes

### `D_LC(O)`

`D_LC(O)` is strongly absorbed by relativistic causal structure and AQFT region assignment.

Decision:

```txt
COVERED
```

### `A_c(O,e)`

`A_c(O,e)` is strongly absorbed by causal accessibility, microcausality, and light-cone structure.

Decision:

```txt
COVERED
```

### `M(O,e)`

`M(O,e)` overlaps local observability and relativistic measurement theory. It may survive only as a bridge predicate that organizes whether the observer has an operational measurement relation.

Decision:

```txt
PARTIALLY_COVERED
```

### `I_c(O <- e)`

`I_c` is mostly absorbed by quantum channels, capacity, coherent information, and communication constraints. The project adds only ordering inside a composite gate.

Decision:

```txt
PARTIALLY_COVERED_WITH_HIGH_COLLAPSE_RISK
```

### `K(O,e)`

`K` is mostly absorbed by decoherence theory, coherence resource theory, and state degradation.

Decision:

```txt
PARTIALLY_COVERED_WITH_HIGH_COLLAPSE_RISK
```

### `R(O,e)`

`R` is mostly absorbed by Petz recovery, quantum error correction, and reconstruction maps.

Decision:

```txt
COVERED_OR_PARTIALLY_COVERED_WITH_VERY_HIGH_COLLAPSE_RISK
```

### `B_c(O)`

`B_c(O)` does not currently survive as a new physical boundary. It survives only as the boundary of a bridge-defined domain if `D_CI(O)` remains useful.

Decision:

```txt
REQUIRES_EXPERT_REVIEW
```

### `D_CI(O)`

`D_CI(O)` remains useful as an ordered bridge framework:

```txt
causal access + measurement relation + information transfer + coherence access + recoverability
```

This is not yet a core theorem.

Decision:

```txt
POSSIBLE_RESIDUE_AS_BRIDGE_LAYER_ONLY
```

## 4. Composite Conclusion

The individual objects are mostly covered by known frameworks. The remaining residue is not a new physics claim. It is an ordered bridge grammar for avoiding the invalid inference:

```txt
inside light cone -> measurable, coherent, recoverable information
```

## 5. Matrix Status

```yaml
collapse_matrix_status: CREATED
classification: CORE_BRIDGE
overall_decision: D_CI_SURVIVES_AS_BRIDGE_LAYER_ONLY
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
expert_review_required: true
```

