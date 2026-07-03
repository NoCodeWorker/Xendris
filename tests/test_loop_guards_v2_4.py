from phyng.closed_loop.guards import run_loop_guards


def test_guard_blocks_permission_elevation_from_heuristic_only():
    results = run_loop_guards(source_status="HEURISTIC_ONLY", target_permission="CLAIM_LIMITED_ALLOWED")
    guard = next(result for result in results if result.guard_name == "NO_PERMISSION_ELEVATION_FROM_HEURISTIC_ONLY")

    assert guard.passed is False
    assert guard.severity == "CRITICAL"


def test_guard_blocks_synthetic_to_physical_promotion():
    results = run_loop_guards(synthetic_to_physical=True)
    guard = next(result for result in results if result.guard_name == "NO_SYNTHETIC_TO_PHYSICAL_PROMOTION")

    assert guard.passed is False
    assert guard.severity == "CRITICAL"
