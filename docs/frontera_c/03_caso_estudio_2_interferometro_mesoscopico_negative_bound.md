# Caso de estudio 2 — Interferómetro mesoscópico y cota negativa Q,B

## Objetivo

Usar la firma mínima:

\[
Q=\frac{\lambda_C}{L},\quad B=\frac{r_g}{L}
\]

para generar una cota negativa: determinar cuándo una frontera gravitacional directa es despreciable para un sistema mesoscópico.

## Sistema candidato

\[
m = 10^{-17}\,kg
\]

\[
L = 10^{-7}\,m
\]

Tipo de escala:

```txt
L_INT — separación interferométrica
```

## Constantes

\[
\hbar=1.054571817\times10^{-34}\,J\,s
\]

\[
G=6.67430\times10^{-11}\,m^3kg^{-1}s^{-2}
\]

\[
c=299792458\,m/s
\]

## Cálculos

\[
\lambda_C=\frac{\hbar}{mc}
\]

\[
r_g=\frac{Gm}{c^2}
\]

\[
Q=\frac{\lambda_C}{L}
\]

\[
B=\frac{r_g}{L}
\]

\[
QB=\left(\frac{\ell_P}{L}\right)^2
\]

## Resultado esperado aproximado

```txt
Q ≈ 3.5e-19
B ≈ 7.4e-38
QB ≈ 2.6e-56
```

## Interpretación

Resultado:

```txt
TRACE_TYPE: NEGATIVE_BOUND_TRACE
```

Claim permitido:

> Para este régimen de masa y escala, una frontera gravitacional directa basada en r_g/L es despreciable.

Claim prohibido:

```txt
Frontera C predice nueva decoherencia gravitacional mensurable.
```
