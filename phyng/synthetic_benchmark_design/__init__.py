"""Synthetic benchmark design tools for heuristic candidates.

DEPRECATED (REFACTOR_PLAN.md — Fase 4):
    phyng.synthetic_benchmark_design is a DELETE_CANDIDATE.
    Redundant simulated sweeps are replaced by false_formality/cases.json.
    This module will be removed in a future cleanup pass.
"""
import warnings
warnings.warn(
    "phyng.synthetic_benchmark_design is deprecated and scheduled for removal. "
    "Use xendris.benchmarks.false_formality for test cases.",
    DeprecationWarning,
    stacklevel=2,
)

from phyng.synthetic_benchmark_design.admissibility import check_log_boundary_admissibility
from phyng.synthetic_benchmark_design.detectability_protocol import build_detectability_protocol
from phyng.synthetic_benchmark_design.log_boundary import (
    create_log_boundary_candidate_spec,
    design_synthetic_benchmark,
)
from phyng.synthetic_benchmark_design.execution import execute_log_boundary_synthetic_benchmark
from phyng.synthetic_benchmark_design.sweep import run_log_boundary_sweep
from phyng.synthetic_benchmark_design.sensitivity import run_log_boundary_sensitivity_ablation
from phyng.synthetic_benchmark_design.phi_search import run_phi_candidate_search

__all__ = [
    "create_log_boundary_candidate_spec",
    "check_log_boundary_admissibility",
    "design_synthetic_benchmark",
    "build_detectability_protocol",
    "execute_log_boundary_synthetic_benchmark",
    "run_log_boundary_sweep",
    "run_log_boundary_sensitivity_ablation",
    "run_phi_candidate_search",
]
