# Frontera C-Mayor Lessons Learned

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE governance only.
- Purpose: document lessons learned after demotion to `BRIDGE_ONLY_FRAMEWORK`.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Partial support: false.
- Core theory candidate: false.
- Bridge framework: true.
- Auxiliary branches touched: no.
- Benchmarks run: none.

## 1. Original Hypothesis

The original Frontera C-Mayor hypothesis investigated whether `c` could be treated as more than a speed limit:

```txt
c as causal-informational membrane
```

The candidate framing asked whether `c` separates domains not only by causal accessibility, but by possible information transfer, measurement relation, coherence access, and recoverability for an observer.

The working formal structure became:

```txt
D_LC(O) = causal-accessible domain for observer O
D_CI(O) = causal-informationally measurable domain for observer O
B_c(O) = candidate boundary of D_CI(O)
```

The minimal bridge claim was:

```txt
Causal accessibility may be necessary but not sufficient for causal-informational measurability.
```

## 2. Main Drift Detected and Corrected

The main drift was the promotion of auxiliary thermal, visibility, contrast, and PredictiveGain work into a primary validation path.

The corrected classification is:

```yaml
thermal_optical_visibility_path: AUXILIARY_ONLY
heating_power_W_axis: AUXILIARY_ONLY
contrast_visibility_benchmarks: AUXILIARY_ONLY
PredictiveGain: FROZEN_FOR_CORE_VALIDATION
```

The correction restored the main focus:

```txt
Frontera C-Mayor must be judged against causal structure, information transfer, measurement theory, coherence, and recoverability, not against auxiliary optical or thermal benchmarks.
```

## 3. What AQFT Absorbed

The AQFT / Haag-Kastler comparison showed strong redundancy pressure on the causal and observable-access layers.

AQFT already formalizes:

- spacetime regions mapped to local observable algebras,
- local observables associated with regions,
- isotony,
- microcausality,
- causal separation discipline,
- local algebra independence and nonclassical local structure.

Mapping result:

| Frontera C object | AQFT pressure | Lesson |
|---|---|---|
| `D_LC(O)` | Strongly absorbed | Causal domain structure is not novel. |
| `A_c(O,e)` | Strongly absorbed | Causal accessibility is known physics. |
| `M(O,e)` | Largely absorbed | Local observables and measurement access are already formalized. |
| `B_c(O)` | High risk | Cannot be treated as a new physical boundary without extra structure. |

AQFT did not leave enough room to claim a core theory from causal-region or local-observable structure alone.

## 4. What I/K/R Redundancy Review Found

The remaining possible residue after AQFT was the `I/K/R` layer:

```txt
I_c(O <- e): transmissible information
K(O,e): coherence access
R(O,e): recoverability
```

The redundancy review found:

| Layer | Finding | Risk |
|---|---|---|
| `I_c(O <- e)` | Partially collapses into quantum channel capacity, coherent information, mutual information, information causality, and causal communication. | HIGH |
| `K(O,e)` | Collapses strongly into decoherence, einselection, open quantum systems, and resource theory of coherence unless independently operationalized. | HIGH |
| `R(O,e)` | Collapses strongly into Petz recovery, quantum error correction, reconstruction maps, and entanglement wedge reconstruction. | VERY_HIGH |
| Joint `I/K/R` | Survives as bridge ordering only. | MEDIUM_HIGH |

The lesson is conservative:

```txt
The individual I/K/R components are not currently non-redundant. Their conjunction is useful as a checklist and ordering scaffold, not as a validated or novel physical object.
```

## 5. What Lean Formalization Proved

The Lean formalization proved abstract definitional consistency.

It defined:

```lean
Observer
Event
A_c : Observer -> Event -> Prop
I_c : Observer -> Event -> Prop
M   : Observer -> Event -> Prop
K   : Observer -> Event -> Prop
R   : Observer -> Event -> Prop
```

It defined:

```lean
D_LC O e := A_c O e

D_CI O e :=
  A_c O e /\ I_c O e /\ M O e /\ K O e /\ R O e
```

It proved:

```txt
D_CI(O,e) implies D_LC(O,e)
```

It also proved conditional strict-inclusion consequences:

```txt
If there exists an event inside D_LC(O) but outside D_CI(O),
then D_CI(O) is a proper subdomain for that observer.
```

The toy witness showed that strict inclusion is logically possible under explicit abstract assumptions such as:

```txt
A_c(O0,e0)
not I_c(O0,e0)
```

## 6. What Lean Formalization Did Not Prove

Lean did not prove any physical claim.

It did not prove:

- that `A_c` correctly models relativistic causal accessibility,
- that `I_c` is a new information-transfer relation,
- that `K` is a new coherence-access relation,
- that `R` is a new recoverability relation,
- that `D_CI(O)` exists as a physical domain,
- that `B_c(O)` is a real physical boundary,
- that Frontera C-Mayor is novel,
- that Frontera C-Mayor is validated,
- that the framework has partial support.

The lesson:

```txt
Formal consistency is not physical validation.
```

## 7. Why the Project Was Demoted From Core Theory Candidate

Frontera C-Mayor was demoted because the current structure has not produced a non-redundant theorem, operational distinction, or empirical target that survives known-physics comparison.

The demotion follows from three results:

1. AQFT absorbed the causal/local-observable layer.
2. Quantum information, decoherence, and recoverability frameworks strongly absorbed the I/K/R layer.
3. Lean proved only definitional and conditional structure, not physical content.

Current decision:

```yaml
core_theory_candidate: false
bridge_framework: true
joint_ikr_layer_status: SURVIVES_AS_BRIDGE_ONLY
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
redundancy_risk:
  individual_I_K_R_components: HIGH_TO_VERY_HIGH
```

## 8. What Remains Useful

Frontera C-Mayor remains useful as:

- a bridge formal framework,
- a source-indexed literature review scaffold,
- a conceptual ordering tool,
- a claim-control framework,
- a way to prevent confusing causal accessibility with measurability,
- a way to separate information transfer, coherence access, and recoverability checks,
- a minimal Lean formalization example for abstract domain inclusion.

Allowed use:

```yaml
allowed_use:
  - bridge_formal_framework
  - literature_review_scaffold
  - conceptual_ordering_tool
```

## 9. Claims Permanently Forbidden

Unless a future gate explicitly changes the status, the following claims are forbidden:

- Frontera C-Mayor is validated.
- Frontera C-Mayor is new physics.
- Frontera C-Mayor has partial support.
- `B_c(O)` is a proven physical boundary.
- `D_CI(O)` is a non-redundant physical domain.
- The I/K/R layer is a proven operational residue.
- Lean compilation validates the theory.
- Auxiliary thermal, visibility, contrast, camera, sensor, LiDAR, or PredictiveGain work validates Frontera C-Mayor.

## 10. Future Reopen Conditions

Reopening `CORE_THEORY_CANDIDATE` requires at least one strict condition:

1. A theorem showing that `D_CI(O)` has nontrivial consequences not reducible to AQFT, causal structure, measurement theory, quantum information, decoherence, or recoverability.
2. A primary-source deep review showing that the joint causal-information-coherence-recoverability boundary is not already defined in another framework.
3. An expert reviewer classifying the framework as a formal theorem candidate rather than a bridge synthesis.
4. A worked model where `B_c(O)` classifies cases not already handled by known frameworks.
5. A non-arbitrary operational definition of `I_c`, `K`, and `R` with falsifiable consequences.

Without one of these, the framework remains bridge-only.

## 11. Methodological Lessons for Future Speculative Physics Projects

1. Start with known-physics absorption tests before building benchmarks.
2. Separate conceptual synthesis from novelty.
3. Treat formalization as clarity, not validation.
4. Require source-indexed redundancy review before naming a new object.
5. Do not let auxiliary datasets become primary validation routes.
6. Maintain explicit allowed and forbidden claims.
7. Use Lean or similar tools to reduce ambiguity only after the physical meaning is disciplined.
8. Ask what existing theories already absorb before asking what the new framework adds.
9. Prefer honest demotion over inflated progress.
10. Preserve bridge value even when core-theory novelty fails.

## 12. Final Conservative Status

```yaml
final_conservative_status: BRIDGE_ONLY_FRAMEWORK
core_theory_candidate: false
bridge_framework: true
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
joint_ikr_layer_status: SURVIVES_AS_BRIDGE_ONLY
redundancy_risk:
  individual_I_K_R_components: HIGH_TO_VERY_HIGH
allowed_use:
  - bridge_formal_framework
  - literature_review_scaffold
  - conceptual_ordering_tool
forbidden_use:
  - new_physics_claim
  - validation_claim
  - partial_support_claim
  - proven_physical_boundary_claim
next_safe_action: expert_review_or_primary_source_deep_review
```

Final discipline:

```txt
Bridge usefulness is not validation.
Formal clarity is not novelty.
Auxiliary evidence is not core support.
```
