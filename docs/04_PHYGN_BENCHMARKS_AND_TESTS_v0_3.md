# Phygn v0.3 — Benchmarks and Tests

## Objetivo

Phygn debe ser testeable.  
Si no pasa tests, no hay teoría: hay literatura.

## Tests actuales esperados

```txt
test_frontier_lengths.py       11 tests
test_operational_scale.py       8 tests
test_signature.py               5 tests
test_epistemic_trace.py         8 tests
test_predictive_gain.py         6 tests
test_claim_gatekeeper.py       10 tests
test_case_quantum_channel.py    7 tests
test_case_mesoscopic.py         8 tests
```

Total aproximado:

```txt
63 tests
```

## Benchmarks mínimos

### BENCH-001 — Compton-gravity invariant

Debe verificar:

\[
\lambda_C r_g = \ell_P^2
\]

para varias masas positivas.

Estado esperado:

```txt
STRUCTURAL_TRACE
```

### BENCH-002 — QB constraint

Debe verificar:

\[
QB=\left(\frac{\ell_P}{L}\right)^2
\]

para varias masas y escalas justificadas.

Estado esperado:

```txt
STRUCTURAL_TRACE
```

### BENCH-003 — L ad hoc blocking

Si \(L\) no tiene justificación:

```txt
BLOCKED_AS_AD_HOC_SCALE
```

### BENCH-004 — Depolarizing tau zero

Si \(p=0\):

\[
\tau=0
\]

Estado:

```txt
NULL_TRACE
```

### BENCH-005 — Depolarizing tau positive

Si \(p>0\):

\[
\tau>0
\]

Estado:

```txt
DETECTABLE_TRACE
```

si supera \(\epsilon_{exp}\).

### BENCH-006 — Mesoscopic negative bound

Para:

```txt
m = 1e-17 kg
L = 1e-7 m
```

Debe producir:

```txt
NEGATIVE_BOUND_TRACE
```

y bloquear cualquier claim de decoherencia gravitacional nueva si no hay modelo adicional.

### BENCH-007 — Claim blocking

Debe bloquear:

```txt
El invariante demuestra nueva física.
Minkowski demuestra Frontera C completa.
La conciencia valida Frontera C.
La cancelación de masa prueba una nueva ley.
```

### BENCH-008 — Structural lemma allowed limited

Debe permitir:

```txt
El invariante es un lema estructural de consistencia.
```

con:

```txt
ALLOWED_LIMITED
```

## Comando

```bash
pytest -v
```

## Criterio de calidad

No basta con pasar tests felices.  
Debe haber tests de fallo:

```txt
masa negativa
probabilidad fuera de rango
distribución inválida
L sin justificación
claim contaminado
hipótesis sin traza
```

## Regla

Todo bug conceptual encontrado debe convertirse en test.
