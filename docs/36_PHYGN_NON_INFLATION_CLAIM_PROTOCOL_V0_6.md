# Phygn v0.6 — Non-Inflation Claim Protocol

## 0. Propósito

Este protocolo impide que v0.6 convierta una comparación toy en una afirmación física fuerte.

## 1. Claim ladder

Los claims deben subir por escalera, no saltar.

```txt
LEVEL-0:
calculation exists.

LEVEL-1:
structural identity validated.

LEVEL-2:
negative bound produced.

LEVEL-3:
toy model delta produced.

LEVEL-4:
toy benchmark gain produced.

LEVEL-5:
source-backed physical model comparison.

LEVEL-6:
detectable candidate prediction.

LEVEL-7:
empirically actionable proposal.
```

## 2. Prohibited jumps

No saltar:

```txt
LEVEL-2 → LEVEL-6
LEVEL-3 → LEVEL-7
LEVEL-4 → proof of new physics
LEVEL-5 → experimental evidence
```

## 3. Mapping

### CAMPAIGN-001

```txt
LEVEL-2:
negative bound produced.
```

### CAMPAIGN-002 initial

```txt
LEVEL-3:
toy model delta produced.
```

Only with y_true or benchmark target:

```txt
LEVEL-4:
toy benchmark gain.
```

Only with sources/model:

```txt
LEVEL-5:
source-backed physical model comparison.
```

## 4. Required permissions

To say:

```txt
candidate produces toy delta
```

Need:

```txt
model_base
model_candidate
parameters
tests
report
```

To say:

```txt
candidate improves toy benchmark
```

Need:

```txt
y_true
error metric
Gain_C > 0
tests
report
```

To say:

```txt
candidate predicts physical decoherence
```

Need:

```txt
source-backed physical model
experimental observable
epsilon_exp
benchmark
Predictive Gain
RAG support
Gatekeeper approval
```

## 5. Gatekeeper actions

```txt
if claim level > evidence level:
    BLOCKED_OVERCLAIM
```

Example:

```txt
claim:
Phygn predicts gravitational decoherence.

evidence:
toy delta only.

decision:
BLOCKED_OVERCLAIM
```

Safe rewrite:

```txt
Phygn computes a toy candidate delta under explicit assumptions. No physical decoherence prediction is claimed.
```

## 6. Report requirement

Every report must include:

```txt
Evidence Level
Maximum Allowed Claim Level
Blocked Claim Examples
Safe Rewrite
```

## 7. UI requirement

Dashboard must display:

```txt
Evidence Level
Claim Level
Blocked Overclaims
```

## 8. Final principle

```txt
La lógica no se rompe por ambición.
La ambición se somete a la lógica.
```
