# Caso de estudio 1 — Canal cuántico y huella epistemológica

## Objetivo

Implementar el primer caso operativo del Principio de Huella Epistemológica:

\[
\tau_O(H)=D[P(Y_O|H),P(Y_O|\neg H)]
\]

En este caso, H no será una hipótesis de física fundamental, sino una hipótesis operacional sobre un canal cuántico.

## Sistema

Un qubit inicial:

\[
\rho_0 = |0\rangle\langle 0|
\]

Canal bajo hipótesis H:

\[
\mathcal{E}_p(\rho)=(1-p)\rho+p\frac{I}{2}
\]

Hipótesis nula:

\[
\neg H: p=0
\]

Hipótesis alternativa:

\[
H: p>0
\]

## Observador

El observador mide en la base computacional:

\[
Y_O\in\{0,1\}
\]

## Distribuciones predictivas

Bajo \(\neg H\):

\[
P(Y=0|\neg H)=1,\quad P(Y=1|\neg H)=0
\]

Bajo H:

\[
P(Y=0|H)=1-\frac{p}{2},\quad P(Y=1|H)=\frac{p}{2}
\]

## Huella

Usar Jensen-Shannon divergence para evitar singularidades:

\[
\tau_O(H)=JS(P_H,P_{\neg H})
\]

Si:

\[
p=0\Rightarrow \tau_O(H)=0
\]

Si:

\[
p>0\Rightarrow \tau_O(H)>0
\]

## Resultado esperado

```txt
TRACE_TYPE: DETECTABLE_TRACE si p > 0 y tau > epsilon_exp
TRACE_TYPE: NULL_TRACE si p = 0 o tau <= epsilon_exp
```

## Valor para Frontera C

Este caso no valida el núcleo gravitacional. Valida el motor operacional:

```txt
hipótesis → distribución predictiva → divergencia → huella → benchmark
```
