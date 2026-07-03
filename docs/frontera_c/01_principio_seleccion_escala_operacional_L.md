# Principio de Selección de Escala Operacional L

## Problema

La firma mínima de Frontera C usa:

\[
Q=\frac{\lambda_C}{L}
\]

\[
B=\frac{r_g}{L}
\]

pero L no puede elegirse libremente sin justificar. Si L es arbitraria, Q y B se convierten en coordenadas ad hoc.

## Principio P-L

> La escala operacional L debe corresponder a una escala físicamente justificada del sistema, del canal, del aparato de medición o de la resolución observacional. No puede elegirse para maximizar artificialmente la relevancia de una frontera.

## Tipos permitidos de L

```txt
L_SYS       Tamaño físico característico del sistema.
L_DET       Resolución espacial efectiva del detector.
L_INT       Separación interferométrica o distancia entre ramas.
L_COH       Longitud de coherencia del sistema.
L_WAVELENGTH Longitud de onda relevante del probe/aparato/canal.
L_CURV      Escala de curvatura gravitacional.
L_HORIZON   Escala causal u horizonte físico.
L_BOX       Tamaño de confinamiento o caja.
L_CHANNEL   Escala espacial efectiva del canal de información.
```

## Metadatos obligatorios

Toda elección de L debe registrar:

```json
{
  "L_value_m": 0.0,
  "L_type": "L_INT",
  "physical_role": "interferometer arm separation",
  "observer_channel": "position measurement",
  "justification": "direct experimental control parameter",
  "allowed_range_m": [0.0, 0.0],
  "claim_dependency": "Q/B frontier signature",
  "arbitrariness_risk": "LOW|MEDIUM|HIGH",
  "review_status": "ACCEPTED|REQUIRES_JUSTIFICATION|REJECTED"
}
```

## Regla de bloqueo

Si L no tiene justificación física:

```txt
B(L) = BLOCKED_AS_AD_HOC_SCALE
```

## Selección múltiple

Un mismo sistema puede admitir varias escalas L, pero deben tratarse como firmas distintas:

\[
\mathcal{B}_C(S;L_1)\neq \mathcal{B}_C(S;L_2)
\]

No hay una única firma absoluta del sistema. Hay una firma relativa al canal operacional.
