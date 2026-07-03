from phyng.targeted_ytrue.candidate_builder import build_candidates
from phyng.targeted_ytrue.loader import load_inputs


def test_observed_measurement_candidate_is_not_automatically_ytrue():
    candidates, rejected, _audit = build_candidates(load_inputs("."))

    assert len(candidates) == 10
    assert rejected
    assert any(candidate.qc_status != "PASS_WITH_LIMITATIONS" for candidate in candidates)


def test_unverified_missing_sources_do_not_enter_ytrue():
    candidates, _rejected, _audit = build_candidates(load_inputs("."))

    assert all(candidate.source_id not in {"VD-SRC-v5_7_1-002-GERLICH-2011-LARGE-ORGANIC", "VD-SRC-v5_7_1-006-ARNDT-1999-C60"} for candidate in candidates)
