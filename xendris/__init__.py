"""
Xendris — AI control layer over a base model (Frontera C framework).

Public namespace structure:
    xendris.frontera_c   — Physical rules & epistemic validation (re-exports phyng core)
    xendris.core         — Orchestration engines (RAG, campaigns, loops)
    xendris.models       — Typed data contracts shared across modules
    xendris.benchmarks   — Evaluation suites by failure family
    xendris.prompts      — Isolated system-prompt strings
    xendris.outputs      — Generated report artifacts (not importable logic)
    xendris.scripts      — One-off runners and utilities

See GOAL.md for the stable project definition.
"""

__version__ = "0.3.0"
__all__ = ["frontera_c", "core", "models", "benchmarks", "prompts"]
