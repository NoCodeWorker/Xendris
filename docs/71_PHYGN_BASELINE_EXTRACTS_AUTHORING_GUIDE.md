# Phygn v1.2 — Baseline Extracts Authoring Guide

## 0. Purpose

This document defines extract templates for each canonical source slot.

Extract files should live in:

```txt
sources/baseline/extracts/
```

---

## 1. Extract file list

Recommended files:

```txt
SRC-BASE-DECOH-001_extracts.md
SRC-BASE-VIS-001_extracts.md
SRC-BASE-MWI-001_extracts.md
SRC-BASE-THRESH-001_extracts.md
SRC-BASE-PARAM-001_extracts.md
```

---

## 2. Universal extract template

```md
# Extracts — SRC-ID

## Source Metadata

- Title:
- Authors:
- Year:
- Source file:
- URL:
- Trust level:

## Extract 1

Support type: SUPPORT_TYPE  
Claim target: CLAIM-ID  
Local reference: page/section/paragraph if known  
Text:

> short excerpt or careful paraphrase

Audit notes:

- Why this supports the claim:
- What this does not support:
- Limitations:
```

---

## 3. Decoherence extract target

File:

```txt
SRC-BASE-DECOH-001_extracts.md
```

Primary claim target:

```txt
CLAIM-BASELINE-FORMULA-001
```

Possible support tags:

```txt
FORMULA_SUPPORT
CONTEXT_SUPPORT
PARAMETER_SUPPORT
ASSUMPTION_SUPPORT
```

Required limitation:

```txt
This does not validate Frontera C or the boundary-aware candidate.
```

---

## 4. Visibility extract target

File:

```txt
SRC-BASE-VIS-001_extracts.md
```

Primary claim target:

```txt
CLAIM-BASELINE-OBSERVABLE-001
```

Possible support tags:

```txt
OBSERVABLE_SUPPORT
FORMULA_SUPPORT
EXPERIMENTAL_CONTEXT
```

Required limitation:

```txt
This supports visibility/contrast as an observable only.
```

---

## 5. Matter-wave extract target

File:

```txt
SRC-BASE-MWI-001_extracts.md
```

Primary claim target:

```txt
CLAIM-BASELINE-CONTEXT-001
```

Possible support tags:

```txt
CONTEXT_SUPPORT
OBSERVABLE_SUPPORT
EXPERIMENTAL_CONTEXT
```

Required limitation:

```txt
This supports experimental context, not the boundary-aware candidate.
```

---

## 6. Threshold extract target

File:

```txt
SRC-BASE-THRESH-001_extracts.md
```

Primary claim target:

```txt
CLAIM-BASELINE-THRESHOLD-001
```

Possible support tags:

```txt
BENCHMARK_SUPPORT
PARAMETER_SUPPORT
OBSERVABLE_SUPPORT
```

Required limitation:

```txt
Do not infer epsilon_exp unless the source gives or constrains it.
```

---

## 7. Parameter extract target

File:

```txt
SRC-BASE-PARAM-001_extracts.md
```

Primary claim target:

```txt
CLAIM-BASELINE-PARAMETER-001
```

Possible support tags:

```txt
PARAMETER_SUPPORT
ASSUMPTION_SUPPORT
FORMULA_SUPPORT
```

Required limitation:

```txt
This does not make arbitrary Gamma values physical.
```

---

## 8. Forbidden phrases inside extracts

Extract files must not include as conclusions:

```txt
Frontera C is validated
Phygn predicts decoherence
candidate is validated
baseline proves the theory
SyntheticGain is PredictiveGain
```

They may include these only inside explicit blocked-claim sections if the validator allows it.

---

## 9. Minimum valid extract

A minimum extract must include:

```txt
Support type:
Claim target:
Local reference:
Text:
Audit notes:
Limitations:
```

---

## 10. Final principle

```txt
The extract is where source text becomes claim discipline.
```
