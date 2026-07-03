# Redundancy Risk Review — Frontera C-Mayor

## LOOP CYCLE 3 — FOCUS CHECK

- Current objective: determine whether `B_c(O)` is non-redundant or merely a restatement of known physics.
- Classification: CORE / BRIDGE
- Link to FRONTERA_C_MAYOR: tests the distinctness of `c` as causal-informational membrane.
- Current validation state: NOT_VALIDATED
- Main uncertainty: whether `B_c(O)` adds a theorem, classification, or falsifiable distinction beyond light cones, horizons, measurement theory, decoherence, and information theory.
- Drift risk: LOW
- Allowed action: redundancy review only.

## GAP SELECTED

```yaml
gap: REDUNDANCY_RISK
reason: docs/frontera_c/MATHEMATICAL_SKETCH.md created `B_c(O)` but explicitly marked REDUNDANCY_RISK: HIGH. The next priority is to decide whether the minimal membrane claim survives as a core candidate or must be demoted/reworked.
```

## 1. Object Under Review

From `docs/frontera_c/MATHEMATICAL_SKETCH.md`:

```txt
B_c(O) = boundary between events/domains for which causal-informational exchange with O is possible and those for which it is not.
```

Minimal candidate claim:

```txt
FC-MAYOR-MIN-001:
Light-cone causal accessibility is necessary but not sufficient for causal-informational measurability; a Frontera C membrane can be modeled as the boundary of events/domains satisfying causal access, nonzero transmissible information, physically possible measurement, and recoverability constraints.
```

## 2. Known Physics Comparison

| Known concept | What it already explains | Does `B_c(O)` merely rename it? | Does `B_c(O)` only combine concepts without predictive power? | Remaining non-redundant role | Requirement to become non-redundant |
|---|---|---|---|---|---|
| Light-cone causal accessibility | Defines which events can causally influence an observer under relativistic propagation. | Partly yes if `B_c(O)` only tracks `J^-(O)` or light-cone membership. | Yes in current sketch if no additional theorem is supplied. | Could classify causally accessible but non-measurable domains. | Define a formal class where `A_c=1` but causal-informational measurability fails for nontrivial reasons. |
| Timelike/lightlike/spacelike separation | Classifies intervals by possible causal relation. | Yes if `B_c(O)` only rephrases interval classification. | Yes in current sketch. | Could add post-causal-access distinctions among timelike/lightlike accessible events. | Show measurable/recoverable information boundary not captured by interval type. |
| Event horizons | Bound causal communication from regions such as black-hole interiors to external observers. | Yes if `B_c(O)` is just horizon boundary. | Yes unless recoverability/information accounting adds a distinct formal result. | Could compare causal horizon with information-recoverability horizon. | State a theorem or model distinguishing causal horizon from recoverability boundary. |
| Cosmological horizons | Bound observable regions in expanding spacetime. | Yes if `B_c(O)` is just cosmological causal access. | Yes currently. | Could classify indirect/inferential access versus direct causal access. | Formalize indirect inference and show a boundary different from ordinary particle/event horizon. |
| Causal diamonds | Bound events that can both influence and be influenced within an observer interval. | Mostly yes if `B_c(O)` maps to causal diamond boundary. | Yes currently. | Could add measurement-channel and recoverability constraints inside the diamond. | Define channel constraints inside a causal diamond and prove they generate a distinct sub-boundary. |
| Standard observability | Covers what can be observed given instruments, signals, noise, and physical access. | Partly yes. | Yes if `B_c(O)` means ordinary observability. | Could unify observability with relativistic causal structure. | Demonstrate that the unified boundary yields a nontrivial classification unavailable from observability alone. |
| Standard measurement theory | Describes interaction, records, POVMs/observables, noise, and measurement limits. | Partly yes through `M(O,e)`. | Yes if measurement relation is imported without new structure. | Could require measurement theory to respect explicit causal-access constraints. | Define a causal-constrained measurement relation and show a result not implicit in standard formulations. |
| Decoherence | Explains loss of accessible phase coherence through environmental entanglement and effective classicality. | Partly yes through `K(O,e)`. | Yes if `K` only means ordinary decoherence. | Could link coherence recoverability to causal accessibility. | Prove or model a causal boundary for coherence recoverability distinct from generic decoherence. |
| Information theory | Quantifies information, channel capacity, entropy, mutual information, and recoverability. | Partly yes through `I_c` and `R`. | Yes if no `c`-specific constraint beyond causal signalling is added. | Could define relativistically constrained information recoverability. | Produce a precise information measure conditioned on causal structure and show nontrivial behavior. |
| Black-hole information problem | Concerns unitarity, horizon information, Hawking radiation, and information recoverability. | No direct rename, but `B_c(O)` risks being a loose metaphor. | Yes unless it states a concrete relation to horizon information. | Could serve as a bridge classification for causal versus recoverable information. | Define whether `B_c(O)` predicts, clarifies, or only labels black-hole information boundaries. |
| Holographic principle | Relates bulk information to boundary encoding in gravitational systems. | No direct rename. | Current sketch only gestures toward boundary/information language. | Could be a bridge if membrane boundary maps to encoding/recoverability boundaries. | State a precise relation or explicitly mark as unrelated. |

## 3. Test of FC-MAYOR-MIN-001

### 3.1 Already Known Physics?

The first clause is mostly known:

```txt
Light-cone causal accessibility is necessary but not sufficient for actual measurement.
```

Known physics already recognizes that causal access does not guarantee detection, channel capacity, coupling, signal-to-noise, decoherence control, or record formation.

Decision:

```txt
ALREADY_COVERED_IN_BROAD_FORM
```

### 3.2 Useful Synthesis?

Yes. `FC-MAYOR-MIN-001` usefully gathers causal access, information transfer, measurement, coherence, and recoverability under one vocabulary.

Decision:

```txt
USEFUL_SYNTHESIS
```

But useful synthesis is not validation and not yet novelty.

### 3.3 New Formal Distinction?

Not yet. The distinction is plausible but not formal enough.

Missing:

- exact definition of `I_c`,
- exact definition of `K`,
- exact definition of `R`,
- non-circular relation between `M` and information transfer,
- theorem showing `B_c(O)` differs from known boundaries.

Decision:

```txt
NEW_FORMAL_DISTINCTION_NOT_ESTABLISHED
```

### 3.4 Too Vague?

Yes in current form. `B_c(O)` is a useful label but not yet a precise mathematical object.

Decision:

```txt
TOO_VAGUE_FOR_VALIDATION
```

### 3.5 Redundant?

Partly. The claim is redundant wherever it only says:

- causal influence is light-cone constrained,
- actual measurement needs a physical channel,
- coherence/recoverability can fail.

Decision:

```txt
PARTIALLY_REDUNDANT
```

### 3.6 Potentially Falsifiable?

Potentially, but only after a formal theorem or classification is stated.

A falsifiable version would need to predict that a class of events/domains is:

```txt
causally accessible but not causal-informationally measurable
```

for reasons captured by `B_c(O)` and not already captured by standard measurement theory.

Decision:

```txt
FALSIFIABILITY_REQUIRED
```

## 4. Decision Table

| Candidate claim | Already covered by known physics? | Non-redundant residue | Falsifiability potential | Decision |
|---|---|---|---|---|
| `c` defines causal accessibility. | Yes. | None. | Already tested/established as standard relativity. | REDUNDANT_WITH_KNOWN_PHYSICS |
| Light-cone access is necessary but not sufficient for actual measurement. | Broadly yes. | Useful synthesis of causal and measurement limits. | Low until formalized. | DEMOTE_TO_BRIDGE |
| `B_c(O)` unifies causal access, information transfer, measurement, coherence, and recoverability. | Partly. | Possible organizing object. | Medium only if theorem/classification is written. | BLOCKED_PENDING_FORMAL_THEOREM |
| There exists a domain with `A_c=1` but `I_c/M/K/R` fail under explicit constraints. | Not fully specified. | Potentially non-redundant if constraints are precise. | Medium/high after formal model. | FALSIFIABILITY_REQUIRED |
| Frontera C-Mayor is validated by this sketch. | No support. | None. | None. | REDUNDANT_OR_UNSUPPORTED_CLAIM_BLOCKED |

## 5. Cycle 3 Decision

```yaml
FC-MAYOR-MIN-001:
  decision: BLOCKED_PENDING_FORMAL_THEOREM
  secondary_decision: DEMOTE_TO_BRIDGE_UNTIL_THEOREM_EXISTS
  redundancy_risk_after: HIGH
  surviving_core_claims: []
  bridge_claims:
    - Light-cone causal accessibility is necessary but not sufficient for causal-informational measurability.
  blocked_claims:
    - B_c(O) is a validated new physical boundary.
    - B_c(O) is non-redundant without theorem/classification.
    - Frontera C-Mayor has partial support from the sketch alone.
```

## 6. Required Theorem Shape

To return from BRIDGE to CORE candidate, the next version must produce something like:

```yaml
theorem_candidate:
  name: causal_informational_subboundary
  statement: For an observer O and event/domain class D, there exists a nonempty subset S where A_c(O,e)=1 but causal-informational measurability fails under specified I_c, M, K, or R constraints.
  baseline: standard light-cone access permits causal contact.
  non_redundant_addition: a stricter boundary than light-cone access, not reducible to ordinary instrument failure.
  failure_condition: S is empty, circularly defined, or fully reducible to standard measurement theory.
```

This is not yet proven.

## 7. Status After Review

```yaml
validation_status: NOT_VALIDATED
mathematical_form_status: SKETCH
novelty_status: UNRESOLVED
redundancy_risk: HIGH
falsifiability_status: PARTIAL
human_review_required: true
```

## 8. Stop Condition

Stop after Cycle 3.

Reason:

```txt
The central claim is not rejected, but it is not yet non-redundant. Human review is required to decide whether to attempt a formal theorem or demote the membrane language to a bridge synthesis.
```
