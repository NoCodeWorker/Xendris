"""Frame-specific evidence requirements for Xendris Epistemic Frame Layer.

Each EpistemicFrame defines what evidence is required for claims made within
that frame. This module enforces those requirements.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .epistemic_frame import EpistemicFrame, EvidenceRequirements


class EvidenceRequirementVerdict(Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"


@dataclass(frozen=True)
class RequirementCheck:
    requirement: str
    verdict: EvidenceRequirementVerdict
    message: str


@dataclass(frozen=True)
class EvidenceRequirementsResult:
    passed: bool
    checks: tuple[RequirementCheck, ...]
    summary: str


def _check_requirement(
    condition: bool,
    requirement_name: str,
    pass_msg: str,
    fail_msg: str,
) -> RequirementCheck:
    if condition:
        return RequirementCheck(
            requirement=requirement_name,
            verdict=EvidenceRequirementVerdict.PASS,
            message=pass_msg,
        )
    return RequirementCheck(
        requirement=requirement_name,
        verdict=EvidenceRequirementVerdict.FAIL,
        message=fail_msg,
    )


def check_evidence_requirements(
    frame: EpistemicFrame,
    has_deployment_evidence: bool = False,
    has_dataset_scope: bool = False,
    has_provider_disclosure: bool = False,
    has_cost_disclosure: bool = False,
    has_latency_disclosure: bool = False,
    has_universal_language: bool = False,
    has_absolute_guarantees: bool = False,
    has_external_citation: bool = False,
    has_limitation_statement: bool = False,
    is_hypothesis: bool = False,
) -> EvidenceRequirementsResult:
    """Check whether a model output meets the evidence requirements for its frame."""
    reqs: EvidenceRequirements = frame.evidence_requirements
    checks: list[RequirementCheck] = []

    checks.append(_check_requirement(
        not reqs.requires_deployment_evidence or has_deployment_evidence,
        "deployment_evidence",
        "Deployment evidence present.",
        "Frame requires deployment evidence but none provided.",
    ))

    checks.append(_check_requirement(
        not reqs.requires_dataset_scope or has_dataset_scope,
        "dataset_scope",
        "Dataset scope disclosed.",
        "Frame requires dataset scope disclosure.",
    ))

    checks.append(_check_requirement(
        not reqs.requires_provider_disclosure or has_provider_disclosure,
        "provider_disclosure",
        "Provider disclosed.",
        "Frame requires provider disclosure.",
    ))

    checks.append(_check_requirement(
        not reqs.requires_cost_disclosure or has_cost_disclosure,
        "cost_disclosure",
        "Costs disclosed.",
        "Frame requires cost disclosure.",
    ))

    checks.append(_check_requirement(
        not reqs.requires_latency_disclosure or has_latency_disclosure,
        "latency_disclosure",
        "Latency disclosed.",
        "Frame requires latency disclosure.",
    ))

    checks.append(_check_requirement(
        not reqs.bans_universal_language or not has_universal_language,
        "universal_language_ban",
        "No universal language detected.",
        "Frame bans universal language (e.g., 'always', 'never', 'superior in every way').",
    ))

    checks.append(_check_requirement(
        not reqs.bans_absolute_guarantees or not has_absolute_guarantees,
        "absolute_guarantees_ban",
        "No absolute guarantees detected.",
        "Frame bans absolute guarantees (e.g., 'guarantees correctness').",
    ))

    checks.append(_check_requirement(
        not reqs.requires_external_citation or has_external_citation,
        "external_citation",
        "External citations provided.",
        "Frame requires external citations.",
    ))

    checks.append(_check_requirement(
        not reqs.requires_limitation_statement or has_limitation_statement,
        "limitation_statement",
        "Limitations stated.",
        "Frame requires a limitation statement.",
    ))

    checks.append(_check_requirement(
        not reqs.requires_human_review_for_critical or True,
        "human_review_for_critical",
        "Human review available for critical outputs.",
        "Frame requires human review for critical outputs.",
    ))

    checks.append(_check_requirement(
        not reqs.allows_hypothesis_without_proof or is_hypothesis,
        "hypothesis_allowed",
        "Hypothesis without proof allowed in this frame.",
        "Frame allows exploratory claims without full proof.",
    ))

    failures = [c for c in checks if c.verdict == EvidenceRequirementVerdict.FAIL]
    passed = len(failures) == 0

    if passed:
        summary = f"All evidence requirements met for frame {frame.profile.name}."
    else:
        failed_names = [c.requirement for c in failures]
        summary = f"Evidence requirements not met for frame {frame.profile.name}: {', '.join(failed_names)}."

    return EvidenceRequirementsResult(
        passed=passed,
        checks=tuple(checks),
        summary=summary,
    )
