# Phygn v1.1 — Extracts & Support Tagging Protocol

## 0. Purpose

This document defines how local source extracts must be written and tagged so Phygn can audit support types.

Extracts are not for rhetoric.  
Extracts are for claim permission.

---

## 1. Extract folder

```txt
sources/baseline/extracts/
```

---

## 2. Extract file naming

Recommended:

```txt
{source_candidate_id}_extracts.md
```

Example:

```txt
SRC-BASE-DECOH-001_extracts.md
```

---

## 3. Extract file template

```md
# Extracts — SRC-BASE-DECOH-001

## Source Metadata

- Title:
- Authors:
- Year:
- Source file:
- URL:
- Trust level:

## Extract 1

Support type: FORMULA_SUPPORT  
Claim target: CLAIM-BASELINE-FORMULA-001  
Local reference: page/section/paragraph if known  
Text:

> short excerpt or careful paraphrase

Audit notes:

- Why this supports the claim:
- What this does not support:

## Extract 2

Support type: OBSERVABLE_SUPPORT  
Claim target: CLAIM-BASELINE-OBSERVABLE-001  
Local reference: page/section/paragraph if known  
Text:

> short excerpt or careful paraphrase

Audit notes:

- Why this supports the claim:
- What this does not support:
```

---

## 4. Support tag definitions

### FORMULA_SUPPORT

Use only when the source explicitly supports a formula or mathematical form relevant to:

```txt
visibility decay
coherence decay
exponential decay
decoherence rate
```

Do not use if the source merely mentions decoherence.

---

### OBSERVABLE_SUPPORT

Use when the source explicitly supports:

```txt
visibility
interference contrast
coherence as measured/readout quantity
loss of interference
```

---

### PARAMETER_SUPPORT

Use when the source supports:

```txt
Γ
decoherence rate
decay constant
timescale
visibility uncertainty
```

---

### CONTEXT_SUPPORT

Use when the source supports background only:

```txt
matter-wave context
historical context
general decoherence context
```

Cannot unlock baseline LIMITED alone.

---

### BENCHMARK_SUPPORT

Use when the source provides:

```txt
experimental data
table
curve
measurement
uncertainty
threshold
```

---

### CONTRADICTION

Use when the source contradicts the intended claim or warns that the intended simplification is invalid.

---

## 5. Claim targets

Recommended baseline claims:

```txt
CLAIM-BASELINE-FORMULA-001:
A visibility/coherence decay baseline can be represented phenomenologically by an exponential decay form under explicit assumptions.

CLAIM-BASELINE-OBSERVABLE-001:
Visibility/interference contrast is a valid observable in interferometric decoherence contexts.

CLAIM-BASELINE-PARAMETER-001:
Γ may represent an effective environmental decoherence or decay rate under explicit assumptions.

CLAIM-BASELINE-LIMITATION-001:
The exponential baseline is limited and not universal.
```

---

## 6. What every extract must include

```txt
support type
claim target
local reference
text or paraphrase
audit notes
limitations
```

---

## 7. Forbidden extract behavior

Do not:

```txt
paste long copyrighted chunks
invent quotation
assign FORMULA_SUPPORT to background statements
assign OBSERVABLE_SUPPORT to pure theory with no observable mention
omit limitations
turn source support into Frontera C support
```

---

## 8. Audit result mapping

```txt
FORMULA_SUPPORT + OBSERVABLE_SUPPORT + PASSED_LIMITED
→ possible BASELINE_SOURCE_BACKED_LIMITED

CONTEXT_SUPPORT only
→ no upgrade

PARAMETER_SUPPORT without formula/observable
→ no limited upgrade

CONTRADICTION
→ BASELINE_CONTRADICTED
```

---

## 9. Report

Generate:

```txt
reports/rag/extract_support_tags_v1_1.md
```

---

## 10. Final principle

```txt
A tagged extract is a legal argument.
A vague source is just noise.
```
