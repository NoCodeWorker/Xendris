# I/K/R Review Query Set

Date: 2026-07-02

## FOCUS CHECK

- Mode: CORE/BRIDGE only.
- Purpose: source-review questions for I/K/R redundancy.
- Validation status: `NOT_VALIDATED`.
- Novelty status: `UNRESOLVED`.
- Partial support: false.

## 1. Primary Review Questions

1. Does this source already define observer-relative information transfer?
2. Does this source already define accessible coherence?
3. Does this source already define recoverability or reconstruction?
4. Does this source combine information, coherence, and recoverability under causal constraints?
5. Does this source imply `D_CI`-like subdomains?
6. Does this source make `B_c(O)` redundant?

## 2. `I_c(O <- e)` Queries

- Does the source define information transfer through a channel from event/domain to observer?
- Does it define quantum channel capacity, coherent information, or mutual information in a way that covers `I_c`?
- Does it explicitly condition information transfer on causal support or no-signalling?
- Does it make observer-relative information availability reducible to local observables?
- Does it require a target variable or record available to an observer?

## 3. `K(O,e)` Queries

- Does the source define coherence as an operational resource?
- Does it define observer-accessible coherence rather than global coherence?
- Does it discuss decoherence/einselection as loss of accessible phase information?
- Does it define coherence under subsystem, algebra, or state restriction?
- Does it imply that `K` is redundant with standard decoherence or resource-theory coherence?

## 4. `R(O,e)` Queries

- Does the source define recoverability from channel outputs or records?
- Does it define a reconstruction map equivalent to `R`?
- Does Petz recovery or approximate recovery already cover the intended use?
- Does QEC already define the relevant threshold for recoverability?
- Does entanglement wedge reconstruction provide a same-family boundary of reconstructability?

## 5. `D_CI(O)` Queries

- Does the source define a domain stricter than causal accessibility?
- Does the stricter domain require information transfer?
- Does it require measurement/local observability?
- Does it require coherence access?
- Does it require recoverability?
- Does it define a boundary equivalent to `B_c(O)`?

## 6. Redundancy Decision Prompts

For each source:

```txt
If I_c is fully covered, mark relation_to_I_c = DIRECT.
If K is fully covered, mark relation_to_K = DIRECT.
If R is fully covered, mark relation_to_R = DIRECT.
If the source covers only one layer, mark D_CI relation as PARTIAL or BACKGROUND.
If the source combines all layers under causal constraints, mark redundancy_threat = DIRECT_REDUNDANCY_THREAT.
If the source requires domain expert interpretation, mark review_status = NEEDS_EXPERT_REVIEW.
```

## 7. Expert Review Questions

### Quantum Information Reviewer

- Is `I_c` anything more than channel capacity/coherent information conditioned on causal support?
- Is `R` anything more than recoverability/reconstruction under known maps?

### Decoherence Reviewer

- Is `K` anything more than standard decoherence/coherence access under a chosen measure?
- Can observer-accessible coherence be formalized without inventing a redundant object?

### AQFT / Relativistic Measurement Reviewer

- Does AQFT/local measurement theory already absorb `D_CI` as local observable availability plus state restriction?
- Is the I/K/R layer meaningful after AQFT absorption of `D_LC`, `A_c`, and most of `M`?

## 8. Allowed Outcomes

```txt
DIRECT_REDUNDANCY_THREAT
PARTIAL_REDUNDANCY_THREAT
BACKGROUND
POSSIBLE_BRIDGE
LOW_RELEVANCE
NEEDS_DEEP_REVIEW
```

No outcome validates Frontera C-Mayor.

