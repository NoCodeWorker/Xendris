# Xendris Product Roadmap 2026

**Date:** 2026-07-06  
**Based on:** Product Goal document (Xendris Membrana de Certeza Cognitiva para IA)  
**Project state:** v0.2.0 (xendris), v0.3.0 (phyng), frontend reset clean

---

## Resumen de hitos

```
Hito A — v0.2.x Clean Public Framework Release    [P0 — NEXT]
Hito B — API Boundary Audit                       [P1 — after A]
Hito C — Real Provider Evidence Import             [P1 — after A]
Hito D — Runtime API MVP                           [P1 — after B]
Hito E — Wallet & Usage Core                       [P1 — after D]
Hito F — Adaptive Council & Sycophancy Layer       [P1 — after D]
Hito G — Epistemic Frame Layer                     [P1 — after B]
Hito H — Xendris Agent UI                          [P1 — after D+E+F+G]
Hito I — Trust Dashboard                           [P1 — after D+E+F]
```

## Documentos de roadmap

| Documento | Contenido |
|-----------|-----------|
| `backlog/XENDRIS_ROADMAP_2026.md` | Roadmap completo con dependencias, exit criteria, tests |
| `backlog/XENDRIS_TASKS.md` | Desglose detallado de cada tarea con acceptance criteria |
| `backlog/phygn_core_backlog.json` | Backlog ejecutable (schema BacklogTask) con 70+ tareas |
| `docs/status/XENDRIS_PRODUCT_ROADMAP_2026.md` | Este documento — resumen ejecutivo |
| `docs/roadmap/` | Roadmaps anteriores (v0.3 a v1.3, preservados) |

## Principios rectores

1. **No overclaiming** — cada hito validado con tests antes de declararse completo
2. **Evidencia primero** — ningún claim de rendimiento sin artefacto admitido en evidence registry
3. **Compatibilidad** — capas experimentales no rompen API pública estable
4. **Coste consciente** — cada decisión considera `cost_per_admissible_answer`
5. **Default minimal** — local CPU first, cheap models when sufficient, frontier only when justified

## Métrica central

```
cost_per_admissible_answer = total_ai_cost / admitted_or_limited_answers
```

## Tags objetivo

```
v0.2.2 — Hito A (clean public release)
v0.3.0 — Hito B (API audit)
v0.4.0 — Hito C + G (provider evidence + epistemic frames)
v0.5.0 — Hito D (runtime API)
v0.6.0 — Hito E (wallet)
v0.7.0 — Hito F (council + sycophancy)
v0.8.0 — Hito H (agent UI)
v0.9.0 — Hito I (dashboard)
v1.0.0 — Hito H + I (producto completo)
```

## Backend vs Frontend mapping

```txt
Python (xendris/ + phyng/)
  Hito A: release gates, quarantine policy
  Hito B: API audit, classification
  Hito C: real provider benchmarks
  Hito D: FastAPI runtime service
  Hito E: wallet & billing models
  Hito F: sycophancy guard, council policy
  Hito G: epistemic frame layer

Frontend (Next.js + shadcn/ui)
  Hito H: Xendris Agent UI (chat, trust/cost panels, modes)
  Hito I: Trust Dashboard (metrics, charts, ledger, wallet)
```
