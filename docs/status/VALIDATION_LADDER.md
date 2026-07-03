# Validation Ladder

## FOCUS CHECK

- Current objective: define the allowed validation sequence for Frontera C-Mayor.
- Classification: CORE
- Link to Frontera C-Mayor: prevents auxiliary progress from being counted as validation.
- Drift risk: low.
- Allowed action: validation governance only.

## 1. Current Status

```yaml
frontera_c_mayor:
  validation_status: NOT_VALIDATED
  mathematical_form_status: SKETCH
  novelty_status: UNRESOLVED
  accepted_status: BRIDGE_FORMAL_FRAMEWORK_CREATED
  falsifiability_status: PARTIAL
```

## 2. Validation Principle

No result validates Frontera C-Mayor unless it directly pressures the claim:

```txt
c as causal-informational membrane
```

Auxiliary progress remains separate.

## 3. Ladder Levels

### Level 0 — Governance Installed

Focus contract exists and drift is controlled.

Status:

```txt
ACHIEVED
```

### Level 1 — Stable Definition

The project has a strict definition, non-definition, and boundary against auxiliary substitution.

Current status:

```txt
PARTIAL
```

### Level 2 — Known Physics Alignment

The project states what relativity, horizon physics, measurement theory, information theory, and decoherence already say.

Current status:

```txt
PARTIAL
```

### Level 3 — Novelty Separation

The project identifies at least one claim not reducible to known physics.

Current status:

```txt
UNRESOLVED
```

### Level 4 — Formal Candidate

The project defines mathematical or operational objects for causal accessibility, information transfer, observer relation, coherence, and recoverability.

Current status:

```txt
BRIDGE_FORMAL_FRAMEWORK_CREATED
```

### Level 5 — Falsifiable Core Claim

The project states what would support and what would falsify the membrane model.

Current status:

```txt
NOT_ACHIEVED
```

### Level 6 — Bridge Formalization

Bridge topics such as information theory, coherence, decoherence, horizons, or recoverability are connected explicitly to `c`.

Current status:

```txt
NOT_ACHIEVED
```

### Level 7 — Evidence or Theorem Pressure

A theorem, derivation, or empirical result creates pressure on the core claim rather than on an auxiliary analogy.

Current status:

```txt
NOT_ACHIEVED
```

### Level 8 — Validation Decision

Only after prior levels can the project decide between:

- `NOT_VALIDATED`
- `PARTIAL_SUPPORT`
- `VALIDATED`
- `FALSIFIED`

Current status:

```txt
NOT_VALIDATED
```

## 4. Explicit Non-Validation Paths

The following do not advance the validation ladder by themselves:

- heating-power axis expansion,
- visibility or contrast benchmarks,
- camera/sensor/LiDAR studies,
- thermal-optical studies,
- auxiliary PredictiveGain,
- y_true extraction for auxiliary observables,
- application generation.

They may be archived as auxiliary or promoted to bridge only after an explicit bridge document.

## 5. Root v0.3 Ladder Disposition

| Artifact | Ladder Role | Preserve / Appendix / Rewrite |
|---|---|---|
| `docs/frontera_c/00_frontera_c_v0_3_manifesto_operacional.md` | Level 0/1 governance and operational framing | Preserve as CORE. |
| `docs/frontera_c/01_principio_seleccion_escala_operacional_L.md` | Potential Level 4 scale discipline | Appendix until tied to membrane formalism. |
| `docs/frontera_c/02_caso_estudio_1_canal_cuantico_huella_epistemologica.md` | Method pattern for trace/failure | Appendix as BRIDGE. |
| `docs/frontera_c/03_caso_estudio_2_interferometro_mesoscopico_negative_bound.md` | Negative-bound example | Appendix as BRIDGE. |
| `docs/frontera_c/04_claim_gatekeeper_v0_3.md` | Level 0/5 claim discipline | Preserve as CORE. |
| `docs/frontera_c/05_prompt_codex_frontera_c_v0_3_lab.md` | Historical implementation plan | Rewrite before reuse. |

## 6. Promotion Rules

### CORE to Validation

A CORE artifact can affect validation only if it contains:

- precise claim,
- known-physics baseline,
- formal distinction,
- failure condition,
- reproducible reasoning.

### BRIDGE to CORE

A BRIDGE artifact may become core-relevant only if it explicitly maps to:

- `c`,
- causal structure,
- information transfer,
- observability,
- coherence,
- recoverability.

### AUXILIARY to BRIDGE

An AUXILIARY artifact may become BRIDGE only after a bridge document states what it models and what it does not prove.

## 7. Current Gate

```yaml
current_gate: FORMAL_THEOREM_REVIEW_REQUIRED
allowed_next_action: decide_whether_to_attempt_core_theorem_or_keep_bridge_framework
blocked_next_actions:
  - benchmark_continuation
  - PredictiveGain
  - thermal_optical_expansion
  - application_generation
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
accepted_status: BRIDGE_FORMAL_FRAMEWORK_CREATED
redundancy_risk: MEDIUM_HIGH
```

## 8. Cycle 5 Relation Formalization Result

```yaml
source: docs/frontera_c/RELATION_FORMALIZATION.md
relations_formalized:
  - A_c(O,e)
  - I_c(O <- e)
  - M(O,e)
  - K(O,e)
  - R(O,e)
strict_inclusion_meaningful: true
D_CI_decision: BRIDGE_FORMAL_FRAMEWORK
validation_status: NOT_VALIDATED
human_decision: ACCEPTED_AS_BRIDGE_FORMAL_FRAMEWORK
next_gate: CORE_THEOREM_OR_INTERPRETIVE_FRAME_DECISION
```

## 9. Human Bridge Framework Decision

```yaml
source: docs/audits/BRIDGE_FRAMEWORK_DECISION.md
accepted_status: BRIDGE_FORMAL_FRAMEWORK_CREATED
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
redundancy_risk: MEDIUM_HIGH
core_theory_candidate: false
bridge_framework: true
partial_support: false
```

## 10. I/K/R Operational Residue Review

```yaml
source: docs/audits/IKR_OPERATIONAL_RESIDUE_REVIEW.md
ikr_operational_residue_status: IKR_SURVIVES_AS_BRIDGE_LAYER_ONLY
frontera_c_consequence: KEEP_AS_BRIDGE_FORMAL_FRAMEWORK
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
current_gate: DEFINE_IKR_AGAINST_KNOWN_FRAMEWORKS_OR_REQUEST_EXPERT_REVIEW
blocked_next_actions:
  - benchmark_continuation
  - PredictiveGain
  - thermal_optical_expansion
  - application_generation
```

## 11. Core/Bridge Tooling Roadmap

```yaml
source:
  - docs/audits/TOOLING_ROADMAP.md
  - docs/audits/IKR_COLLAPSE_MATRIX.md
  - docs/rag/RAG_CORPUS_PLAN.md
  - docs/lean/FORMAL_LEAN_PLAN.md
  - docs/models/TOY_MODEL_DCI_STRICT_INCLUSION_SPEC.md
tooling_status: CORE_BRIDGE_TOOLING_ROADMAP_CREATED
allowed_use:
  - redundancy_mapping
  - source_indexed_review
  - minimal_formal_consistency_check
  - non_empirical_toy_model_usability_check
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
blocked_next_actions:
  - benchmark_continuation
  - PredictiveGain
  - auxiliary_visibility_contrast_expansion
  - thermal_optical_axis_development
  - application_generation
current_gate: SOURCE_INDEXED_RAG_OR_MINIMAL_LEAN_FORMALIZATION
```

## 12. Minimal Lean Formalization

```yaml
source:
  - formal/FrC/Basic.lean
  - formal/FrC/Subdomain.lean
  - formal/FrC/StrictInclusion.lean
  - docs/lean/LEAN_FORMALIZATION_REPORT.md
lean_formalization_status: MINIMAL_ABSTRACT_FORMALIZATION_COMPILED
formalized:
  - Observer
  - Event
  - A_c
  - I_c
  - M
  - K
  - R
  - D_LC
  - D_CI
proven:
  - D_CI_subset_D_LC
  - witness_for_observer_implies_proper_subdomain
  - exists_LC_not_CI_implies_proper_subdomain_exists
compile_checked: true
compile_result: COMPILED
latest_build_check: COMPILED
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
current_gate: FORMAL_METHODS_REVIEW_OR_KEEP_MINIMAL
blocked_next_actions:
  - validation_claim
  - novelty_claim
  - partial_support_claim
  - benchmark_continuation
  - PredictiveGain
  - auxiliary_visibility_contrast_expansion
  - application_generation
```

## 13. Lean Compile Wrapper

```yaml
source:
  - lakefile.lean
  - lean-toolchain
  - formal/FrC.lean
  - docs/lean/LEAN_COMPILE_STATUS.md
lean_compile_wrapper_status: CREATED
compile_result: COMPILED
lean_available: true
lake_available: true
compile_command_attempted: true
latest_build_check: COMPILED
intended_compile_command: lake build
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
current_gate: FORMAL_METHODS_REVIEW_OR_KEEP_MINIMAL
blocked_next_actions:
  - validation_claim
  - novelty_claim
  - partial_support_claim
  - benchmark_continuation
  - PredictiveGain
  - auxiliary_visibility_contrast_expansion
  - application_generation
```

## 14. Abstract Strict-Inclusion Toy Witness

```yaml
source:
  - formal/FrC/ToyModel.lean
  - formal/FrC.lean
  - docs/models/TOY_MODEL_DCI_STRICT_INCLUSION_REPORT.md
toy_model_status: ABSTRACT_STRICT_INCLUSION_WITNESS_COMPILED
assumptions:
  - A_c O0 e0
  - Not (I_c O0 e0)
proven:
  - toy_e0_in_D_LC
  - toy_e0_notin_D_CI
  - toy_exists_LC_not_CI_for_O0
  - toy_proper_subdomain_for_O0
  - toy_strict_inclusion_possible
compile_result: COMPILED
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
current_gate: FORMAL_METHODS_REVIEW_OF_AXIOM_BASED_TOY_WITNESS
blocked_next_actions:
  - validation_claim
  - novelty_claim
  - partial_support_claim
  - benchmark_continuation
  - PredictiveGain
  - auxiliary_visibility_contrast_expansion
  - application_generation
```

## 15. Source-Indexed I/K/R Redundancy Workflow

```yaml
source:
  - docs/rag/SOURCE_INDEXED_RAG_PLAN.md
  - docs/rag/PAPER_SOURCE_SCHEMA.md
  - docs/audits/IKR_REVIEW_QUERY_SET.md
  - docs/audits/IKR_REDUNDANCY_SOURCE_TABLE.md
source_indexed_rag_status: IKR_SOURCE_INDEXED_RAG_WORKFLOW_CREATED
purpose: source_indexed_redundancy_review
target_relations:
  - I_c
  - K
  - R
  - D_CI
initial_result: DIRECT_AND_PARTIAL_REDUNDANCY_THREATS_PRESENT
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
current_gate: POPULATE_SOURCE_METADATA_OR_REQUEST_IKR_EXPERT_REVIEW
blocked_next_actions:
  - validation_claim
  - novelty_claim
  - partial_support_claim
  - benchmark_continuation
  - PredictiveGain
  - auxiliary_visibility_contrast_expansion
  - application_generation
```

## 16. Populated I/K/R Source Metadata

```yaml
source:
  - docs/audits/IKR_SOURCE_METADATA_TABLE.md
  - docs/audits/IKR_CLAIM_EXTRACTION_TABLE.md
  - docs/audits/IKR_REDUNDANCY_FINDINGS.md
  - docs/audits/IKR_REDUNDANCY_SOURCE_TABLE.md
source_metadata_status: POPULATED_INITIAL_SOURCE_INDEX
ik_claim_extraction_status: CLAIMS_EXTRACTED_INITIAL
ik_r_collapse_risk: HIGH_TO_VERY_HIGH
joint_ikr_layer_status: SURVIVES_AS_BRIDGE_ONLY
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
current_gate: EXPERT_REVIEW_OR_PRIMARY_SOURCE_DEEP_REVIEW
blocked_next_actions:
  - validation_claim
  - novelty_claim
  - partial_support_claim
  - benchmark_continuation
  - PredictiveGain
  - auxiliary_visibility_contrast_expansion
  - application_generation
```

## 17. Human Bridge-Only Framework Decision

```yaml
source:
  - docs/audits/IKR_REDUNDANCY_FINDINGS.md
  - docs/audits/BRIDGE_ONLY_FRAMEWORK_DECISION.md
human_decision: DEMOTE_TO_BRIDGE_ONLY_FRAMEWORK
core_theory_candidate: false
bridge_framework: true
joint_ikr_layer_status: SURVIVES_AS_BRIDGE_ONLY
ik_r_collapse_risk: HIGH_TO_VERY_HIGH
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
current_gate: EXPERT_REVIEW_OR_PRIMARY_SOURCE_DEEP_REVIEW
allowed_use:
  - bridge_formal_framework
  - literature_review_scaffold
  - conceptual_ordering_tool
blocked_next_actions:
  - validation_claim
  - novelty_claim
  - partial_support_claim
  - benchmark_continuation
  - PredictiveGain
  - auxiliary_visibility_contrast_expansion
  - thermal_optical_axis_development
  - application_generation
```

This decision does not advance the validation ladder. It narrows the allowed path: Frontera C-Mayor may be used as a bridge framework only unless expert review or primary-source deep review reopens `CORE_THEORY_CANDIDATE`.
