"""Candidate disposition rules after control failure."""

from __future__ import annotations

from phyng.frontera_c_disposition.schemas import CandidateDisposition, ControlFailureReview


REOPEN_CRITERIA = [
    "at least 2 independent sources",
    "at least 10 accepted y_true records",
    "out-of-sample or leave-one-source-out evaluation",
    "negative controls survive",
    "simple controls no longer explain gain",
]

PROHIBITED_ACTIONS = [
    "C-structure ablation for LOG_BOUNDARY",
    "Frontera C validation from LOG_BOUNDARY",
    "physical claim from v5.4 or v5.5",
    "new benchmark-only score inflation",
    "architecture-only continuation to rescue LOG_BOUNDARY",
]


def build_candidate_disposition(review: ControlFailureReview) -> CandidateDisposition:
    return CandidateDisposition(
        candidate_family=review.candidate_family,
        primary_disposition="ARCHIVE_AS_VALIDATION_CANDIDATE",
        secondary_roles=[
            "BENCHMARK_FIXTURE",
            "NEGATIVE_CONTROL_FIXTURE",
            "YTRUE_PIPELINE_REGRESSION_FIXTURE",
            "SOURCE_IDENTITY_REGRESSION_FIXTURE",
        ],
        archived_as_validation_candidate=True,
        retained_as_fixture=True,
        reason=review.failure_summary,
        required_to_reopen_as_candidate=REOPEN_CRITERIA,
        prohibited_actions=PROHIBITED_ACTIONS,
        notes=[
            "Archived means removed from active Frontera C validation candidacy.",
            "Fixture roles are methodological only.",
        ],
    )
