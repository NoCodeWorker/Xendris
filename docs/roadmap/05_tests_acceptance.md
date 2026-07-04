# 05 — Tests y criterios de aceptación

## Principio

Cada nueva regla debe tener test determinista.

Nada debe depender de llamadas a proveedores, prompts frágiles o interpretaciones subjetivas.

## Tests obligatorios v0.4

### 1. Benchmark no implica superioridad universal

```text
test_benchmark_claim_cannot_become_universal_claim
```

Entrada:

```text
source_context = BENCHMARK
source_claim = “Xendris scored 0.985 on Trust Traps v0.1”
target_claim = “Xendris is universally superior”
```

Resultado esperado:

```text
BLOCK
reason = forbidden transition BENCHMARK -> UNIVERSAL_SUPERIORITY
```

### 2. Latencia dry-run no implica latencia de producción

```text
test_dry_run_latency_cannot_become_production_latency
```

Resultado esperado:

```text
BLOCK
reason = missing real latency measurement
```

### 3. Claim del usuario no se vuelve factual sin evidencia

```text
test_user_provided_claim_cannot_become_factual_without_evidence
```

Resultado esperado:

```text
BLOCK or HUMAN_REVIEW
```

### 4. Claim de código no se vuelve producción sin pruebas

```text
test_code_state_claim_cannot_become_production_ready_without_verification
```

Resultado esperado:

```text
BLOCK
```

### 5. Puente válido permite promoción limitada

```text
test_valid_evidence_bridge_allows_limited_promotion
```

Entrada:

```text
source_context = BENCHMARK
target_context = DOCUMENTATION
evidence_bridge = BENCHMARK_ARTIFACT
```

Resultado esperado:

```text
ALLOW_WITH_LIMITATIONS
```

### 6. Error runtime se excluye del scoring

```text
test_runtime_error_excluded_from_scoring_with_trace
```

Resultado esperado:

```text
ALLOW_WITH_LIMITATIONS or BLOCK_SCORING
```

### 7. Normal control no debe sobrebloquearse

```text
test_normal_control_claim_passes_without_overblocking
```

Resultado esperado:

```text
ALLOW
```

## Anti-Overblocking and Usefulness Preservation Tests

Para asegurar que Xendris maximiza la admisibilidad segura y evita el sobrebloqueo destructivo, se especifican las siguientes pruebas obligatorias:

1. `test_normal_control_claim_passes_without_overblocking`:
   * Verifica que las respuestas de control que no contienen trampas epistémicas fluyan limpiamente con decisión `ALLOW`.
2. `test_low_risk_unsupported_claim_is_downgraded_not_blocked`:
   * Prueba que un claim de bajo riesgo no soportado se degrade/acote de forma segura en lugar de retornar `BLOCK` ciego.
3. `test_exploratory_claim_allowed_as_hypothesis`:
   * Valida que las aserciones puramente especulativas ("We could explore...") se admitan bajo la categoría `ALLOW_AS_HYPOTHESIS`.
4. `test_creative_non_factual_output_passes_without_gate_interference`:
   * Comprueba que los outputs creativos, brainstorming o pitches no factuales fluyan sin obstrucciones.
5. `test_overbroad_claim_is_scoped_before_blocking_when_safe`:
   * Demuestra que claims sobremedidos se reescriben/acotan a su contexto local en lugar de descartarse.
6. `test_high_risk_unsupported_claim_requires_human_review_or_block`:
   * Confirma que claims factuales de alto riesgo sin evidencia puente válida resulten obligatoriamente en `BLOCK` o `HUMAN_REVIEW`.
7. `test_usefulness_preservation_does_not_override_forbidden_transition`:
   * Garantiza que la búsqueda de preservación de utilidad no anule las prohibiciones rígidas de la compuerta.
8. `test_usefulness_preservation_does_not_promote_user_claim_without_evidence`:
   * Asegura que claims declarados por el usuario no se promuevan a factuales verificados a menos que exista un puente real.
9. `test_usefulness_preservation_does_not_convert_benchmark_win_to_universal_superiority`:
   * Impide la generalización de victoria en benchmarks a claims de calidad universal.
10. `test_usefulness_preservation_does_not_convert_dry_run_latency_to_production_latency`:
    * Protege la integridad del runtime bloqueando la asunción de latencia local simulada como medición real de producción.
11. `test_allow_with_limitations_contains_explicit_scope`:
    * Verifica que la decisión `ALLOW_WITH_LIMITATIONS` incluya una anotación legible de límites en los metadatos.
12. `test_allow_as_hypothesis_contains_non_factual_marker`:
    * Asegura que claims hipotéticos queden marcados con etiquetas de especulación no factuales.

## Métricas mínimas

Cada ejecución del runtime o suite de benchmark de Xendris debe computar e informar las siguientes métricas epistémicas:

* **`normal_control_pass_rate`**: Proporción de claims normales (de control) admitidos con éxito (`ALLOW`) sobre el total de claims de control evaluados.
* **`false_positive_block_rate`**: Proporción de claims de bajo riesgo o creativos válidos que fueron bloqueados por error.
* **`overblocking_rate`**: Tasa general de outputs válidos e inocuos rechazados innecesariamente.
* **`useful_answer_preservation_rate`**: Proporción de respuestas con claims sobremedidos que fueron exitosamente acotadas/degradadas en lugar de bloqueadas.
* **`human_review_overuse_rate`**: Tasa de derivación a auditoría humana sobre el total de decisiones.
* **`downgrade_success_rate`**: Porcentaje de aserciones corregidas/mitigadas hacia estados seguros admisibles.
* **`unsafe_transition_block_rate`**: Proporción de transiciones prohibidas que fueron bloqueadas con total éxito (debe ser del 100%).
* **`limitation_clarity_rate`**: Porcentaje de claims limitados que disponen de una justificación/acotación explícita.

### Expectativas Mínimas para v0.4
* `normal_control_pass_rate`: Debe ser elevado (mínimo **98%**).
* `overblocking_rate`: Debe medirse y registrarse sistemáticamente en cada corrida (no asumirse).
* `unsafe_transition_block_rate`: Debe ser del **100.0%** (rigor estricto para transiciones prohibidas).
* `useful_answer_preservation_rate`: Debe medirse de forma independiente respecto a la tasa de aprobación simple (`ALLOW` general).


## Criterios de documentación

Cada release debe incluir:

```text
docs/status/XENDRIS_ALGEBRAIC_TRUST_V0_4.md
```

Debe contener:

- propósito;
- alcance;
- inspiración AQFT sin claim de validación física;
- lista de módulos creados;
- tests ejecutados;
- resultados reales;
- limitaciones;
- próximos pasos.

## Criterio de bloqueo de release

Bloquear release si:

- hay tests fallidos;
- la documentación afirma conteos de tests no observados;
- aparece claim de superioridad universal;
- se confunde latencia dry-run con latencia real;
- se afirma producción sin trazas;
- se presenta AQFT como prueba física de Xendris.
