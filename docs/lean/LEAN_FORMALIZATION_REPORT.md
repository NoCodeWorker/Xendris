# Lean Formalization Report

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Scope: minimal abstract formalization.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Partial support: false.
- Benchmarks run: none.
- Auxiliary thermal/visibility/contrast work touched: no.
- Applications generated: no.

## 1. What Was Formalized

Created:

```txt
formal/FrC/Basic.lean
formal/FrC/Subdomain.lean
formal/FrC/StrictInclusion.lean
```

The formalization defines abstract types:

```lean
Observer
Event
```

It defines abstract predicates:

```lean
A_c : Observer -> Event -> Prop
I_c : Observer -> Event -> Prop
M   : Observer -> Event -> Prop
K   : Observer -> Event -> Prop
R   : Observer -> Event -> Prop
```

It defines domains:

```lean
D_LC O e := A_c O e

D_CI O e :=
  A_c O e /\ I_c O e /\ M O e /\ K O e /\ R O e
```

It also defines strict-inclusion witness predicates:

```lean
exists_LC_not_CI_for O :=
  Exists fun e => D_LC O e /\ Not (D_CI O e)

exists_LC_not_CI :=
  Exists fun O => Exists fun e => D_LC O e /\ Not (D_CI O e)
```

## 2. What Was Proven

The formalization proves:

```lean
D_CI_subset_D_LC :
  forall O e, D_CI O e -> D_LC O e
```

This follows directly from the definition of `D_CI`.

It also proves:

```lean
witness_for_observer_implies_proper_subdomain :
  exists_LC_not_CI_for O -> ProperSubdomainFor O
```

and:

```lean
exists_LC_not_CI_implies_proper_subdomain_exists :
  exists_LC_not_CI -> ProperSubdomainExists
```

These results mean: if an event is abstractly assumed to be inside `D_LC` but outside `D_CI`, then `D_CI` is a proper subdomain for that observer, or for some observer in the global version.

The toy witness module additionally proves:

```lean
toy_e0_in_D_LC : D_LC O0 e0
toy_e0_notin_D_CI : Not (D_CI O0 e0)
toy_strict_inclusion_possible : ProperSubdomainExists
```

These are conditional on explicit toy axioms:

```lean
A_c O0 e0
Not (I_c O0 e0)
```

## 3. What Remains Purely Definitional

The subset theorem is definitional:

```txt
D_CI(O,e) contains A_c(O,e), so D_CI(O,e) implies D_LC(O,e).
```

The strict-inclusion result is conditional:

```txt
Lean does not create the witness.
Lean only proves what follows if the witness is assumed.
```

The predicates remain placeholders. No physical meaning is built into Lean.

## 4. What Lean Cannot Prove Physically

Lean cannot prove:

- that `A_c` correctly models relativistic causal accessibility,
- that `I_c` correctly models information transfer,
- that `M` correctly models measurement possibility,
- that `K` correctly models coherence access,
- that `R` correctly models recoverability,
- that `D_CI` corresponds to a physical domain in nature,
- that `B_c(O)` is a real causal-informational membrane,
- that Frontera C-Mayor is novel,
- that Frontera C-Mayor is validated,
- that the framework has empirical support.

## 5. Whether the Formalization Reduces Ambiguity

It reduces one ambiguity:

```txt
D_CI(O) subset D_LC(O)
```

is now represented as a precise definitional theorem rather than prose.

It also separates:

- subset by construction,
- strict inclusion by witness,
- physical interpretation outside Lean.

It does not reduce ambiguity around the physical meanings of `I_c`, `K`, or `R`.

## 6. Whether This Changes Validation Status

No.

```yaml
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
core_theory_candidate: false
bridge_framework: true
```

The formalization is internal consistency scaffolding only.

## 7. Verification Status

No Lean toolchain or Lake project was detected in the repository before creation of these files.

A minimal compile wrapper has now been created:

```txt
lakefile.lean
lean-toolchain
formal/FrC.lean
docs/lean/LEAN_COMPILE_STATUS.md
```

Current compile status:

```yaml
lean_toolchain_detected: true
lake_detected: true
lake_wrapper_created: true
lean_compile_checked: true
compile_result: COMPILED
lean_version: 4.12.0
lake_version: 5.0.0-dc25334
note: current shell did not refresh PATH, so explicit ~/.elan/bin paths were used
```

The files were written to a conventional module layout:

```txt
formal/FrC/
```

Compile command used:

```txt
C:\Users\usuario\.elan\bin\lake.exe build
```

Result:

```txt
Build completed successfully.
```

Latest build check:

```yaml
date: 2026-07-02
command_requested: lake build
command_executed: C:\Users\usuario\.elan\bin\lake.exe build
compile_result: COMPILED
output: Build completed successfully.
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
```

## 8. Next Safe Step

Allowed next step:

```txt
Create a minimal Lean/Lake project wrapper or request external formal-method review of the abstract encoding.
```

Blocked next steps:

- validation claim,
- novelty claim,
- partial-support claim,
- benchmark continuation,
- PredictiveGain,
- auxiliary thermal/visibility/contrast expansion,
- application generation.

## 9. Status

```yaml
lean_formalization_status: MINIMAL_ABSTRACT_FORMALIZATION_COMPILED
lean_compile_wrapper_status: CREATED
lean_compile_result: COMPILED
latest_build_check: COMPILED
toy_model_status: ABSTRACT_STRICT_INCLUSION_WITNESS_COMPILED
classification: CORE_BRIDGE
formal_scope:
  - abstract_types
  - abstract_predicates
  - D_LC_definition
  - D_CI_definition
  - subset_theorem
  - strict_inclusion_witness_condition
  - abstract_toy_witness
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
physical_claims_created: false
compile_checked: true
```
