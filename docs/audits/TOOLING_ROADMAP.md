# Core/Bridge Tooling Roadmap

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Primary focus: `c` as causal-informational membrane.
- Current accepted status: `BRIDGE_FORMAL_FRAMEWORK_CREATED`.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Partial support: false.
- Forbidden scope: auxiliary thermal, visibility, contrast, camera, sensor, LiDAR, PredictiveGain, benchmark, and application work.

## 1. Purpose

This roadmap defines internal tools that can improve the formal clarity of Frontera C-Mayor without claiming validation, novelty, or empirical support.

The roadmap is allowed to organize:

- redundancy review,
- formal definitions,
- source-backed comparison,
- bridge-layer documentation,
- theorem-preparation work,
- non-empirical toy models.

It is not allowed to produce:

- physical validation,
- PredictiveGain,
- benchmark conclusions,
- empirical confirmation,
- product or application deliverables.

## 2. Phase Overview

| Phase | Tooling Track | Expected Output | Allowed Claim | Forbidden Claim |
|---|---|---|---|---|
| Phase 1 | Collapse matrix | Structured comparison against known frameworks | A redundancy map exists | Frontera C-Mayor is novel |
| Phase 2 | RAG corpus | Curated review corpus and claim index | Literature review is organized | Literature review validates the theory |
| Phase 3 | Lean formalization plan | Minimal formal object plan | Definitions can be mechanically checked | Lean proves physical truth |
| Phase 4 | Toy strict-inclusion model | Non-empirical model of `D_CI(O) subset D_LC(O)` | Formal usability can be tested | Toy model validates nature |
| Phase 5 | External review preparation | Expert-facing materials | Expert review can be requested | Expert review has already accepted novelty |

## 3. Tools

### Redundancy Matrix

Tool:

```txt
docs/audits/IKR_COLLAPSE_MATRIX.md
```

Expected output:

- object-by-framework coverage table,
- collapse categories,
- possible residue classification,
- expert review needs.

Can prove:

- whether the project has documented overlap risk.

Cannot prove:

- that a non-redundant theorem exists,
- that Frontera C-Mayor is new physics,
- that the bridge layer is physically real.

### RAG Corpus

Tool:

```txt
docs/rag/RAG_CORPUS_PLAN.md
```

Expected output:

- folder structure,
- metadata schema,
- ingestion workflow,
- claim extraction schema,
- redundancy questions.

Can prove:

- that future literature review is auditable and source-linked.

Cannot prove:

- source support,
- novelty,
- validation.

### Lean Formalization

Tool:

```txt
docs/lean/FORMAL_LEAN_PLAN.md
```

Expected output:

- minimal formal universe,
- provisional relation types,
- subset proof target,
- strict-inclusion condition,
- limits of formalization.

Can prove:

- internal consistency of selected definitions,
- trivial subset relations if definitions imply them.

Cannot prove:

- empirical truth,
- physical interpretation,
- novelty relative to physics,
- correct threshold choices.

### Toy Model

Tool:

```txt
docs/models/TOY_MODEL_DCI_STRICT_INCLUSION_SPEC.md
```

Expected output:

- non-empirical example where an event lies in `D_LC(O)` but not in `D_CI(O)`,
- relation values,
- failure mode classification.

Can prove:

- that the formal distinction is syntactically usable.

Cannot prove:

- physical validation,
- benchmark value,
- observational support.

## 4. Governance Constraints

All tooling must preserve:

```yaml
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
core_theory_candidate: false
bridge_framework: true
```

Any tool output that attempts to promote Frontera C-Mayor to validation, support, or novelty must be rejected until:

1. a non-redundant theorem is externally reviewed, or
2. a falsifiable operational criterion is accepted, or
3. a known-physics collapse review explicitly fails to absorb the object.

## 5. What Tools Can and Cannot Prove

| Tool | Can Prove | Cannot Prove |
|---|---|---|
| Collapse matrix | documented redundancy risk | novelty |
| RAG corpus | source organization | source support |
| Lean plan | definitional consistency targets | physical truth |
| Toy model | formal usability | empirical validity |
| External review package | review readiness | reviewer endorsement |

## 6. Allowed Next Steps

1. Build a source-indexed RAG corpus from known physics and redundancy references.
2. Translate `D_LC`, `D_CI`, `A_c`, `I_c`, `M`, `K`, and `R` into minimal formal definitions.
3. Create non-empirical toy examples to test whether the formal grammar is usable.
4. Ask external reviewers whether the composite layer is useful or redundant.

## 7. Blocked Next Steps

- Benchmark continuation.
- PredictiveGain computation.
- Auxiliary visibility or contrast expansion.
- Thermal-optical axis development.
- Application generation.
- Validation language.
- Novelty language.

## 8. Roadmap Decision

```yaml
tooling_roadmap_status: CREATED
classification: CORE_BRIDGE
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
allowed_next_action: build_collapse_matrix_rag_corpus_lean_plan_or_toy_formal_model
blocked_next_action: benchmark_or_validation_claim
```

