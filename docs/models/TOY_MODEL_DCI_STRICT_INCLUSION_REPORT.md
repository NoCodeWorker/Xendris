# Toy Model D_CI Strict Inclusion Report

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Scope: abstract Lean toy witness.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Partial support: false.
- Benchmarks run: none.
- Auxiliary thermal/visibility/contrast work touched: no.
- Applications generated: no.

## 1. What Toy Model Was Added

Created:

```txt
formal/FrC/ToyModel.lean
```

Updated:

```txt
formal/FrC.lean
```

The toy module defines:

```lean
constant O0 : Observer
constant e0 : Event
```

and assumes:

```lean
axiom toy_A_c_O0_e0 : A_c O0 e0
axiom toy_not_I_c_O0_e0 : Not (I_c O0 e0)
```

This means the event is causally accessible for the toy observer, while the information-transfer predicate fails.

## 2. What Was Proven

The Lean module proves:

```lean
toy_e0_in_D_LC : D_LC O0 e0
```

and:

```lean
toy_e0_notin_D_CI : Not (D_CI O0 e0)
```

It also proves:

```lean
toy_exists_LC_not_CI_for_O0 : exists_LC_not_CI_for O0
toy_proper_subdomain_for_O0 : ProperSubdomainFor O0
toy_exists_LC_not_CI_global : exists_LC_not_CI
toy_strict_inclusion_possible : ProperSubdomainExists
```

## 3. Why This Is Still Abstract

The toy model uses abstract constants and axioms only.

It does not define:

- a real observer,
- a real event,
- a real channel,
- a real measurement,
- a real coherence threshold,
- a real recovery threshold.

The witness is formal:

```txt
A_c O0 e0 is assumed.
I_c O0 e0 is assumed false.
```

## 4. Why This Is Not Physical Validation

The proof does not show that any physical event exists with these properties.

It shows only that the formal system can represent the pattern:

```txt
inside D_LC(O) but outside D_CI(O)
```

under explicit assumptions.

This does not validate Frontera C-Mayor, does not establish novelty, and does not create partial support.

## 5. What This Adds Compared To The Previous Lean Build

The previous Lean build proved:

```txt
D_CI(O,e) -> D_LC(O,e)
```

by definition.

This toy model adds an explicit abstract witness pattern:

```txt
D_LC(O0,e0)
not D_CI(O0,e0)
```

and connects it to the existing proper-subdomain scaffold.

## 6. Compile Result

```yaml
toy_model_status: ABSTRACT_STRICT_INCLUSION_WITNESS_COMPILED
compile_result: COMPILED
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
partial_support: false
physical_claims_created: false
```

## 7. Next Safe Action

Allowed next action:

```txt
Request formal-methods review of whether the witness scaffold should remain axiom-based or be converted into a parameterized theorem over failure predicates.
```

Blocked next actions:

- validation claim,
- novelty claim,
- partial-support claim,
- benchmark continuation,
- PredictiveGain,
- auxiliary thermal/visibility/contrast expansion,
- application generation.

