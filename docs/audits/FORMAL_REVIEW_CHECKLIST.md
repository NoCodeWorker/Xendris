# Formal Review Checklist — Frontera C-Mayor

## FOCUS CHECK

- Current objective: prepare a strict external scientific review checklist for Frontera C-Mayor as `BRIDGE_FORMAL_FRAMEWORK_CREATED`.
- Classification: CORE / BRIDGE
- Link to Frontera C-Mayor: tests whether `c` as causal-informational membrane can move beyond bridge synthesis.
- Current accepted status: BRIDGE_FORMAL_FRAMEWORK_CREATED
- Current validation status: NOT_VALIDATED
- Current novelty status: UNRESOLVED
- Current redundancy risk: MEDIUM_HIGH
- Drift risk: LOW
- Allowed action: external-review preparation only.

## 1. Current Status to Be Reviewed

```yaml
project: Frontera C-Mayor
accepted_status: BRIDGE_FORMAL_FRAMEWORK_CREATED
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
redundancy_risk: MEDIUM_HIGH
core_theory_candidate: false
bridge_framework: true
partial_support: false
```

The object under review is the accepted bridge framework:

```txt
D_CI(O) subset D_LC(O)
```

with the interpretation:

```txt
Causal accessibility is necessary but not sufficient for causal-informational measurability.
```

## 2. What Is Not Being Claimed

The review must not assume that the project claims:

- Frontera C-Mayor is validated.
- Frontera C-Mayor has partial support.
- Frontera C-Mayor is established new physics.
- `B_c(O)` is a proven physical boundary.
- `D_CI(O)` is already a theorem.
- Auxiliary studies validate the framework.
- Benchmarks or applications are part of the current core claim.

The current question is formal and conceptual, not empirical validation.

## 3. Core Formal Objects

### `D_LC(O)`

```txt
D_LC(O) = { e in E | A_c(O,e)=1 }
```

Review role:

```txt
Known causal-accessibility domain under c-constrained causal structure.
```

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

Review role:

```txt
Candidate causal-informational measurability domain.
```

### `B_c(O)`

```txt
B_c(O) = boundary(D_CI(O), E \ D_CI(O))
```

Review role:

```txt
Candidate boundary of causal-informational measurability.
```

### `A_c(O,e)`

```txt
A_c(O,e)=1 iff e is causally accessible to O under c-constrained causal structure.
```

Review classification:

```txt
KNOWN_PHYSICS
```

### `I_c(O <- e)`

```txt
I_c(O <- e)>0 iff a c-supported physical channel carries nonzero information from e to records available to O.
```

Review classification:

```txt
STANDARD_INFORMATION_THEORY / NEW_SYNTHESIS
```

### `M(O,e)`

```txt
M(O,e)=1 iff a physically allowed measurement relation can form an accessible record at O for the target event variable.
```

Review classification:

```txt
STANDARD_MEASUREMENT_THEORY / NEW_SYNTHESIS
```

### `K(O,e)`

```txt
K(O,e)>=theta_K iff coherence-relevant information remains accessible above a declared threshold.
```

Review classification:

```txt
STANDARD_DECOHERENCE / NEW_SYNTHESIS
```

### `R(O,e)`

```txt
R(O,e)>=theta_R iff the relevant event information is recoverable from records available to O above a declared threshold.
```

Review classification:

```txt
STANDARD_INFORMATION_THEORY / NEW_SYNTHESIS
```

## 4. Main Review Question

Primary question:

```txt
Is D_CI(O) subset D_LC(O) a useful non-redundant formal distinction, or only a synthesis of known physics?
```

Subquestions:

1. Does the framework add anything beyond standard causal accessibility plus ordinary measurement/information limitations?
2. Does `B_c(O)` identify a boundary not already captured by light cones, horizons, channel capacity, decoherence, or measurement access?
3. Are `K` and `R` independently necessary, or do they collapse into existing information/measurement criteria?
4. Can the framework produce a theorem, classification result, or failure condition?

## 5. Redundancy Checks

For each item, reviewers should answer:

```txt
already covered / partially covered / not covered / unclear
```

| Known concept | Redundancy check |
|---|---|
| Light-cone causality | Does `D_CI(O)` merely restate causal accessibility plus extra wording? |
| Timelike/lightlike/spacelike separation | Does the framework add any distinction beyond causal order? |
| Event horizons | Is `B_c(O)` just a horizon boundary in other language? |
| Cosmological horizons | Does observer-relative access add anything beyond standard horizon observability? |
| Causal diamonds | Is `D_CI(O)` reducible to a causal diamond plus measurement constraints? |
| Standard observability | Is the framework only standard observability with renamed layers? |
| Measurement theory | Does `M(O,e)` carry all the nontrivial content? |
| Information theory | Does `I_c` or `R` reduce the framework to channel/reconstruction theory? |
| Decoherence | Does `K` reduce the framework to ordinary decoherence? |
| Black-hole information problem | Does the framework add any formal tool or only analogy? |
| Holographic principle | Is there a distinct formal relation, or only thematic overlap? |

Decision criterion:

```txt
If every layer is fully absorbed by known concepts, Frontera C-Mayor should remain bridge or be demoted to interpretive frame.
```

## 6. Formal Theorem Requirements

To promote the framework toward `CORE_THEORY_CANDIDATE`, reviewers should require:

1. Definitions of `O`, `E`, event variables, record variables, and admissible channels.
2. A non-arbitrary definition of `theta_K` and `theta_R`.
3. A theorem or proposition not true by definition alone.
4. A proof that `D_CI(O)` has a nontrivial structure not reducible to `D_LC(O)` plus standard limitations.
5. A worked model where the distinction changes classification in a way not already captured by known physics.
6. A clear collapse condition if the formal distinction fails.

Minimum theorem candidate:

```txt
There exists a physically meaningful class of events for which D_CI(O) is a strict, nontrivially structured subdomain of D_LC(O), and the structure cannot be reduced to ordinary measurement, channel, coherence, or recoverability limits.
```

## 7. Falsifiability Requirements

The framework becomes scientifically reviewable only if it can fail.

Required failure routes:

1. Redundancy failure:

```txt
Every proposed result reduces to light cones, horizons, measurement, information, decoherence, or recoverability.
```

2. Formal incoherence:

```txt
Definitions are circular, inconsistent, or unable to distinguish causal access, information access, measurement access, coherence, and recoverability.
```

3. Physical conflict:

```txt
The framework implies superluminal signalling, Lorentz violation without evidence, unsupported horizon modification, or unsupported measurement-rule modification.
```

4. Infalsifiability:

```txt
Every possible result can be reinterpreted as compatible.
```

5. Auxiliary substitution:

```txt
An auxiliary benchmark or application result is treated as core validation.
```

## 8. Questions for Relativity / Causal-Structure Reviewer

1. Is `A_c(O,e)` correctly grounded in causal structure?
2. Does `D_LC(O)` add anything beyond standard light-cone accessibility?
3. Does `D_CI(O)` create a meaningful subdomain inside the causal domain, or is it merely causal accessibility plus measurement limitations?
4. Is `B_c(O)` distinguishable from light cones, horizons, causal diamonds, or observer horizons?
5. Does the framework preserve Lorentz invariance and standard causal ordering?
6. Are there spacetime settings where `D_CI(O)` could be nontrivially structured without contradicting known relativity?
7. Does the use of `c` as membrane language clarify or obscure standard causal structure?

## 9. Questions for Quantum Information / Decoherence Reviewer

1. Is `I_c(O <- e)` a useful formal object or just channel mutual information with causal support?
2. Is `K(O,e)` independently meaningful, or does it collapse into standard coherence/decoherence measures?
3. Is `R(O,e)` independently meaningful, or does it collapse into standard recovery/inference theory?
4. Are `theta_K` and `theta_R` defensible without arbitrary tuning?
5. Can coherence access and recoverability be separated operationally?
6. Does the framework identify a useful boundary between causal reachability and coherent recoverability?
7. Is there any quantum-information theorem that could support or reject this layered structure?

## 10. Questions for Mathematical Physics Reviewer

1. Are `D_LC(O)`, `D_CI(O)`, and `B_c(O)` well-defined sets or domains?
2. Is the subset relation nontrivial or merely definitional?
3. Can the boundary `B_c(O)` be made mathematically precise?
4. Are the relations `A_c`, `I_c`, `M`, `K`, and `R` compatible in one formal setting?
5. Can thresholds `theta_K` and `theta_R` be defined invariantly or operationally?
6. Does the framework admit theorem statements with proofs?
7. What minimal counterexample would collapse the framework into known physics?

## 11. Possible Reviewer Decisions

Allowed reviewer decisions:

```txt
PROMOTE_TO_CORE_THEORY_CANDIDATE
KEEP_AS_BRIDGE_FORMAL_FRAMEWORK
DEMOTE_TO_INTERPRETIVE_FRAME_ONLY
REJECT_AS_REDUNDANT_WITH_KNOWN_PHYSICS
REWRITE_REQUIRED
BLOCKED_PENDING_FORMAL_DEFINITIONS
BLOCKED_PENDING_EXTERNAL_EXAMPLES
```

Decision meanings:

| Decision | Meaning |
|---|---|
| `PROMOTE_TO_CORE_THEORY_CANDIDATE` | Reviewer finds a plausible non-redundant theorem path. |
| `KEEP_AS_BRIDGE_FORMAL_FRAMEWORK` | Framework is useful but not novel or validated. |
| `DEMOTE_TO_INTERPRETIVE_FRAME_ONLY` | Framework is explanatory language only. |
| `REJECT_AS_REDUNDANT_WITH_KNOWN_PHYSICS` | Framework adds no formal or conceptual value beyond known physics. |
| `REWRITE_REQUIRED` | Core definitions are unclear or mis-specified. |
| `BLOCKED_PENDING_FORMAL_DEFINITIONS` | Review cannot proceed until variables/thresholds are formalized. |
| `BLOCKED_PENDING_EXTERNAL_EXAMPLES` | Review requires nontrivial worked examples. |

## 12. How Each Decision Updates `docs/status/PROJECT_STATUS.md`

### `PROMOTE_TO_CORE_THEORY_CANDIDATE`

```yaml
frontera_c_mayor:
  accepted_status: CORE_THEORY_CANDIDATE
  novelty_status: POTENTIALLY_DIFFERENTIATED
  validation_status: NOT_VALIDATED
  core_theory_candidate: true
  bridge_framework: true
  partial_support: false
  redundancy_risk: MEDIUM
next_action:
  priority: formal_theorem_or_falsifiable_core_claim
  classification: CORE
```

Promotion does not validate the project.

### `KEEP_AS_BRIDGE_FORMAL_FRAMEWORK`

```yaml
frontera_c_mayor:
  accepted_status: BRIDGE_FORMAL_FRAMEWORK_CREATED
  novelty_status: UNRESOLVED
  validation_status: NOT_VALIDATED
  core_theory_candidate: false
  bridge_framework: true
  partial_support: false
  redundancy_risk: MEDIUM_HIGH
next_action:
  priority: formal_toy_model_or_threshold_discipline
  classification: CORE_BRIDGE
```

This preserves the current state.

### `DEMOTE_TO_INTERPRETIVE_FRAME_ONLY`

```yaml
frontera_c_mayor:
  accepted_status: INTERPRETIVE_FRAME_ONLY
  novelty_status: NOT_DIFFERENTIATED
  validation_status: NOT_VALIDATED
  core_theory_candidate: false
  bridge_framework: false
  partial_support: false
  redundancy_risk: HIGH
next_action:
  priority: archive_as_interpretive_framework_or_rewrite_from_known_physics
  classification: CORE_GOVERNANCE
```

### `REJECT_AS_REDUNDANT_WITH_KNOWN_PHYSICS`

```yaml
frontera_c_mayor:
  accepted_status: REDUNDANT_WITH_KNOWN_PHYSICS
  novelty_status: REJECTED_AS_NON_NOVEL
  validation_status: NOT_VALIDATED
  core_theory_candidate: false
  bridge_framework: false
  partial_support: false
  redundancy_risk: MAXIMAL
next_action:
  priority: close_or_rewrite_core_hypothesis
  classification: CORE_GOVERNANCE
```

### `REWRITE_REQUIRED`

```yaml
frontera_c_mayor:
  accepted_status: REWRITE_REQUIRED
  novelty_status: UNRESOLVED
  validation_status: NOT_VALIDATED
  core_theory_candidate: false
  bridge_framework: provisional
  partial_support: false
  redundancy_risk: HIGH
next_action:
  priority: rewrite_definitions_before_any_theorem_or_benchmark
  classification: CORE
```

### `BLOCKED_PENDING_FORMAL_DEFINITIONS`

```yaml
frontera_c_mayor:
  accepted_status: BLOCKED_PENDING_FORMAL_DEFINITIONS
  novelty_status: UNRESOLVED
  validation_status: NOT_VALIDATED
  core_theory_candidate: false
  bridge_framework: provisional
  partial_support: false
  redundancy_risk: HIGH
next_action:
  priority: define_variables_thresholds_and_boundary_conditions
  classification: CORE_BRIDGE
```

### `BLOCKED_PENDING_EXTERNAL_EXAMPLES`

```yaml
frontera_c_mayor:
  accepted_status: BLOCKED_PENDING_EXTERNAL_EXAMPLES
  novelty_status: UNRESOLVED
  validation_status: NOT_VALIDATED
  core_theory_candidate: false
  bridge_framework: true
  partial_support: false
  redundancy_risk: MEDIUM_HIGH
next_action:
  priority: develop_non_empirical_worked_examples_or_request_review_examples
  classification: CORE_BRIDGE
```

## 13. Reviewer Response Template

```yaml
reviewer_name_or_role:
review_domain:
decision:
main_reason:
redundancy_assessment:
formal_definition_gaps:
theorem_path_exists:
falsifiability_path_exists:
required_revisions:
status_update_recommendation:
claims_that_remain_forbidden:
```

## 14. Final Review Boundary

This checklist supports external review only.

It does not:

- validate Frontera C-Mayor,
- create partial support,
- establish novelty,
- authorize benchmarks,
- authorize auxiliary expansion,
- authorize applications.

Final discipline:

```txt
External review can change classification.
It cannot create validation without a theorem, falsifiable core pressure, or accepted non-redundant result.
```
