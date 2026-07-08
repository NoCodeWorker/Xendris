# Finitexo Methodology Deviation Note — Runtime vs Wrapper Classification

## Summary

v0.7.0 and v0.8.1 are valid real-provider diagnostic runs, but they measured a **prompt-wrapper approximation** of Xendris, not the foundational Xendris runtime. This note documents the deviation, reclassifies those runs, and defines the corrective path.

## Foundational Methodology

Xendris is defined as a **runtime trust architecture** comprising:

- runtime trust architecture
- deterministic gates
- claim evaluation
- admissibility checks
- audit decision
- repair/degradation/blocking loop
- final controlled response

The architecture does not rely on instruction-level prompting alone. It enforces post-generation controls that inspect, evaluate, and conditionally repair or block model output before it is accepted as a final response.

## What v0.7.0 and v0.8.1 Measured

- base provider response
- provider response with Xendris **wrapper instructions** prepended to the prompt
- documented scorer applied directly to the provider output
- **no full runtime loop**
- **no independent repair pass**
- **no post-generation gate** controlling final admissibility
- **no final runtime audit decision** selecting, repairing, degrading, blocking, or replacing the output

## Reclassification

### v0.7.0

- **classification:** `WRAPPER_DIAGNOSTIC_ONLY`
- **not admissible as** `XENDRIS_RUNTIME_EVALUATION`

### v0.8.1

- **classification:** `HARD_WRAPPER_DIAGNOSTIC_ONLY`
- **not admissible as** `XENDRIS_RUNTIME_EVALUATION`

## Preserved Claims

- providers were real where artifacts say `provider_mode=real`
- attempts completed as recorded
- costs were tracked
- scores/lifts are valid for **wrapper diagnostics**
- v0.8.1 completed 120/120 attempts with 0 errors
- v0.8.1 DeepSeek wrapper lift was negative
- v0.8.1 OpenAI wrapper lift was slightly positive

## Blocked Claims

The following claims are explicitly **not authorized** by v0.7.0 or v0.8.1:

- v0.7.0 proves Xendris runtime improvement
- v0.8.1 refutes Xendris runtime
- Xendris runtime has been evaluated on hard programming n=30
- Xendris is only a prompt wrapper
- wrapper results generalize to runtime results
- universal superiority
- statistical superiority
- production readiness

## Root Cause

The deviation came from simplifying the experiment to reduce cost, complexity and implementation time, but this reduced fidelity to the foundational architecture. The wrapper approach was chosen as a faster path to measurement, but it bypassed the runtime audit, repair, and control loop that defines Xendris.

## Corrective Action

The next valid methodological step is **v0.9.0 Runtime Paired Lift n=30**, which implements the full runtime audit and repair loop for all runtime variants.

## Final Decision

`METHODOLOGY_DEVIATION_RECORDED_RUNTIME_REQUIRED`
