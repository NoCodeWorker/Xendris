# Phygn v2.5 — LOG_BOUNDARY Synthetic Benchmark Execution Goal

## 0. Context

The latest confirmed document is:

```txt
147_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_RESULTS.md
```

Therefore, v2.5 starts at:

```txt
148
```

v2.3 produced an explicit synthetic benchmark design for:

```txt
HEUR-PHY-003 / LOG_BOUNDARY
```

v2.4 introduced the closed-loop learning and meta-improvement engine, including:

```txt
Candidate Learning Loop
Meta-Improvement Loop
Shadow Mode
Self-Confirmation Guards
Versioned Update Records
```

v2.5 now executes the LOG_BOUNDARY synthetic benchmark under the declared parameter sweep.

---

## 1. Core thesis

```txt
A designed benchmark earns no status until it is executed.
```

The goal of v2.5 is to compute:

```txt
V_base(t)
V_log(t)
delta(t)
max_abs_delta
detectability status
failure conditions
parameter sensitivity
loop feedback
```

under declared toy parameters.

---

## 2. Hard rule

```txt
Synthetic signal may update search priority.
It may not authorize physical truth.
```

Even if LOG_BOUNDARY produces a detectable synthetic delta, physical claims remain blocked until source support, benchmark data or experimental evidence exists.

---

## 3. Candidate under test

```txt
candidate_id: HEUR-PHY-003
candidate_family: LOG_BOUNDARY
previous_status: SYNTHETIC_BENCHMARK_DESIGNED
```

Core model:

```txt
V_base(t)=exp(-Gamma_env*t)
V_log(t)=exp(-(Gamma_env + DeltaGamma_log)*t)
DeltaGamma_log = alpha * Gamma_env * phi_log(q,b,u,w)
phi_log = sigmoid(k * (u - u0)) * tanh(k2 * (w - w0))^2
```

---

## 4. Required execution outputs

v2.5 must produce:

```txt
numerical sweep result
max_abs_delta
detectability classification
best parameter record
parameter reasonableness classification
failure conditions
canonical status
closed-loop feedback proposal
reports
tests
```

---

## 5. Required statuses

Possible domain statuses:

```txt
LOG_BOUNDARY_SYNTHETIC_EXECUTED
LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA
LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_POST_HOC_TUNING
LOG_BOUNDARY_EXECUTION_BLOCKED
```

Canonical mapping must preserve:

```txt
synthetic evidence is not physical evidence
detectability is not validation
source/data requirements remain blocked
```

---

## 6. Acceptance criteria

v2.5 is complete when:

```txt
synthetic benchmark execution works
sweep computes max_abs_delta
detectability classification works
parameter reasonableness classification works
failure conditions are recorded
reports include canonical status
loop feedback is generated
all physical claims remain blocked
tests pass
previous behavior remains unchanged
```

---

## 7. Final principle

```txt
Let LOG_BOUNDARY bleed numbers before it earns attention.
```
