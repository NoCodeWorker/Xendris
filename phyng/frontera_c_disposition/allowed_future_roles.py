"""Allowed future roles for a failed candidate."""

from __future__ import annotations

from phyng.frontera_c_disposition.schemas import AllowedFutureRoles, CandidateDisposition


def build_allowed_future_roles(disposition: CandidateDisposition) -> AllowedFutureRoles:
    return AllowedFutureRoles(
        candidate_family=disposition.candidate_family,
        allowed_roles=[
            "benchmark fixture",
            "negative-control fixture",
            "pipeline regression test",
            "single-source y_true smoke-test example",
            "control-failure teaching case",
        ],
        blocked_roles=[
            "active Frontera C validation candidate",
            "physical mechanism",
            "PredictiveGain evidence",
            "invariant confirmation",
            "generalized decoherence model",
        ],
        notes=["Allowed roles do not create evidence support or validation."],
    )
