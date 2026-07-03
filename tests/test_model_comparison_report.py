from phyng.model_comparison import (
    ModelComparisonSpec,
    generate_model_comparison_report,
    run_model_comparison,
)


def test_report_generated(tmp_path):
    spec = ModelComparisonSpec(
        comparison_id="TEST-REPORT",
        campaign_id="CAMPAIGN-002",
        system_id="SYS-TEST",
        observable="visibility_loss",
        t=[0.0, 1.0],
        parameters={"gamma_base": 0.05, "alpha": 1.0, "B": 1e-6, "QB": 1e-12},
        model_base_name="TOY_BASE",
        model_candidate_name="TOY_CANDIDATE",
        model_base_description="Toy base.",
        model_candidate_description="Toy candidate.",
        epsilon_exp=1e-6,
        error_metric="MAE",
        status="ACTIVE",
    )
    result = run_model_comparison(spec)

    path = generate_model_comparison_report(spec, result, tmp_path)

    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "TEST-REPORT" in text
    assert "No physical decoherence prediction is claimed" in text
