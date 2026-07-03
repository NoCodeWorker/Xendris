from phyng.real_source_acquisition.campaign_gate import run_phi_gradient_real_source_acquisition
from phyng.real_source_acquisition.candidate_manifest import (
    ManifestOnlySourceAcquisitionBackend,
    NoopSourceAcquisitionBackend,
    build_candidate_manifest,
    manifest_only_candidate_fixture,
)
from phyng.real_source_acquisition.query_plan import build_phi_gradient_real_source_query_plan


def test_noop_backend_does_not_create_real_sources():
    plan = build_phi_gradient_real_source_query_plan()
    manifest = build_candidate_manifest(plan, NoopSourceAcquisitionBackend())

    assert manifest.backend_status == "NOOP_SOURCE_ACQUISITION_BACKEND"
    assert manifest.candidates == []
    assert manifest.actual_real_sources_acquired is False


def test_manifest_only_backend_marks_sources_as_candidates_not_support():
    plan = build_phi_gradient_real_source_query_plan()
    candidate = manifest_only_candidate_fixture()
    manifest = build_candidate_manifest(plan, ManifestOnlySourceAcquisitionBackend([candidate]))

    assert manifest.candidates[0].source_id == candidate.source_id
    assert manifest.actual_real_sources_acquired is False
    assert manifest.candidates[0].is_support is False


def test_no_backend_keeps_source_pressure_inconclusive():
    result = run_phi_gradient_real_source_acquisition()

    assert result.status == "PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING"
    assert result.actual_real_sources_acquired is False
    assert "A query plan is evidence." in result.blocked_claims
