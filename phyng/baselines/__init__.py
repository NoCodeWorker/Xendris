"""
Phygn v0.8 — Baselines package

DEPRECATED (REFACTOR_PLAN.md — Fase 4):
    phyng.baselines is a DELETE_CANDIDATE.
    Initial experiments superseded by xendris/benchmarks/false_formality/.
    Import from xendris.benchmarks instead. This module will be removed
    in a future cleanup pass.
"""
import warnings
warnings.warn(
    "phyng.baselines is deprecated and scheduled for removal. "
    "Use xendris.benchmarks for evaluation suites.",
    DeprecationWarning,
    stacklevel=2,
)

from phyng.baselines.schemas import (
    BaselineSourceRequirement,
    BaselineReadinessResult,
    BaselineSourceSupport,
    VisibilityDecayBaselineSpec,
    Campaign002BaselineUpgradeResult,
)
from phyng.baselines.visibility_decay import (
    build_visibility_decay_baseline,
    compute_visibility,
    compute_visibility_series,
    ensure_baseline_research_tasks,
)
from phyng.baselines.readiness import classify_baseline_readiness
from phyng.baselines.source_support import (
    build_baseline_source_requirements,
    build_source_support_matrix,
)
from phyng.baselines.report import (
    write_baseline_source_requirements,
    write_baseline_literature_ingestion,
    write_baseline_source_support_matrix,
    write_visibility_decay_readiness_report,
)
from phyng.baselines.source_pack import BaselineSourcePack, evaluate_source_pack
from phyng.baselines.upgrade_attempt import BaselineUpgradeAttemptResult, run_baseline_upgrade_attempt_v0_9
from phyng.baselines.limited_upgrade_execution import (
    BaselineUpgradeExecutionResult,
    run_limited_upgrade_execution,
)

