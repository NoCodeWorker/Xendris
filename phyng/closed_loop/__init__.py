"""Closed-loop learning and meta-improvement engine.

DEPRECATED (REFACTOR_PLAN.md — Fase 4):
    phyng.closed_loop is a DELETE_CANDIDATE.
    Sandbox and old feedback loops are superseded by xendris/benchmarks/false_formality/.
    This module will be removed in a future cleanup pass.
"""
import warnings
warnings.warn(
    "phyng.closed_loop is deprecated and scheduled for removal. "
    "Use xendris.benchmarks for evaluation and runner suites.",
    DeprecationWarning,
    stacklevel=2,
)

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.guards import run_loop_guards
from phyng.closed_loop.meta_loop import classify_meta_change_risk, propose_meta_improvement
from phyng.closed_loop.shadow_mode import run_shadow_mode
from phyng.closed_loop.versioning import create_versioned_update_record

__all__ = [
    "run_candidate_learning_loop",
    "propose_meta_improvement",
    "classify_meta_change_risk",
    "run_shadow_mode",
    "run_loop_guards",
    "create_versioned_update_record",
]
