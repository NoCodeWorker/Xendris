# Phygn v1.0 — Baseline Source Pack Ingestion Goal

## 0. Propósito

Phygn v0.9 construyó la tubería formal para aceptar o rechazar fuentes:

```txt
SourceCandidate
SourceRecordV09
CitationAuditResult
ClaimSourceLinkV09
BaselineSourcePack
BaselineUpgradeAttemptResult
```

y demostró el comportamiento correcto en ausencia de fuentes:

```txt
Pack Status = EMPTY
Baseline Ingestion Result = BASELINE_REQUIRES_SOURCE
Upgrade Success = False
Max Allowed Claim Level = 3
```

v1.0 tiene una misión concreta:

```txt
preparar y ejecutar la primera ingesta real de fuentes locales para intentar subir el baseline de CAMPAIGN-002.
```

El objetivo realista es:

```txt
BASELINE_REQUIRES_SOURCE
→ BASELINE_SOURCE_BACKED_LIMITED
```

No:

```txt
Frontera C validated
Phygn predicts decoherence
Candidate model validated
PredictiveGain achieved
```

---

## 1. Estado heredado

De v0.5:

```txt
CAMPAIGN-001:
NEGATIVE_GRAVITY_BOUND
B = 7.43e-38
decoherence overclaim blocked
```

De v0.6:

```txt
CAMPAIGN-002:
MODEL_DELTA_ONLY
Gain_C undefined without y_true
```

De v0.7:

```txt
Benchmark provenance exists
SyntheticGain only
SyntheticGain is not PredictiveGain
```

De v0.8:

```txt
baseline subsystem exists
baseline_after = BASELINE_REQUIRES_SOURCE
candidate prediction blocked
```

De v0.9:

```txt
real source ingestion pipeline exists
citation audit exists
baseline upgrade attempt exists
empty source pack fails honestly
188 tests passed
```

---

## 2. Goal v1.0

Implementar una campaña:

```txt
BASELINE-SRC-PACK-001
```

que:

```txt
1. busque fuentes locales en sources/baseline/;
2. registre SourceCandidates;
3. audite metadata;
4. audite contenido local;
5. cree SourceRecords si procede;
6. cree ClaimSourceLinks solo si el soporte es explícito;
7. evalúe FORMULA_SUPPORT y OBSERVABLE_SUPPORT;
8. intente subir el baseline;
9. genere reports;
10. mantenga candidato y Frontera C bloqueados.
```

---

## 3. Pregunta científica

```txt
¿Podemos respaldar el baseline fenomenológico V_base(t)=exp(-Γt) con fuentes reales suficientes para usarlo como adversario físico limitado en CAMPAIGN-002?
```

---

## 4. Criterio de éxito mínimo

v1.0 puede terminar en dos estados válidos.

### Éxito por bloqueo honesto

```txt
sources present but insufficient
→ baseline remains BASELINE_REQUIRES_SOURCE or BASELINE_REQUIRES_DIRECT_SUPPORT
→ reports explain why
→ tests pass
```

### Éxito por upgrade limitado

```txt
audited sources provide FORMULA_SUPPORT and OBSERVABLE_SUPPORT
→ baseline_after = BASELINE_SOURCE_BACKED_LIMITED
→ candidate remains blocked
→ no physical prediction
→ tests pass
```

Ambos son científicamente válidos.

---

## 5. Qué puede desbloquear v1.0

Solo esto:

```txt
CAMPAIGN-002 has a source-backed limited baseline.
The baseline is admissible as a limited physical reference.
The candidate remains hypothetical.
Physical prediction remains blocked.
```

---

## 6. Qué debe seguir bloqueado

```txt
Phygn predicts gravitational decoherence.
Boundary C causes decoherence.
The source-backed baseline validates the candidate.
Frontera C is proven.
SyntheticGain is physical PredictiveGain.
```

---

## 7. Claim level esperado

Si el baseline sube a LIMITED:

```txt
max_claim_level may rise for the baseline only.
candidate max claim level remains constrained.
physical prediction remains blocked.
```

---

## 8. Input esperado

Archivos locales:

```txt
sources/baseline/*.pdf
sources/baseline/*.md
sources/baseline/*.txt
sources/baseline/*.html
sources/baseline/source_manifest.json
```

Si no existen:

```txt
create source preparation tasks
do not upgrade baseline
```

---

## 9. Reportes esperados

```txt
reports/rag/baseline_source_pack_v1_0.md
reports/rag/source_candidate_audit_v1_0.md
reports/rag/citation_audit_v1_0.md
reports/rag/baseline_support_matrix_v1_0.md
reports/campaigns/BASELINE-SRC-PACK-001_ingestion_result.md
reports/campaigns/CAMPAIGN-002_baseline_upgrade_attempt_v1_0.md
```

---

## 10. Frase guía

```txt
La puerta ya existe.
Ahora hay que traer pruebas reales.
```

---

## 11. Principio final

```txt
Si una fuente entra, debe poder limitar.
Si no puede limitar, no puede desbloquear.
```
