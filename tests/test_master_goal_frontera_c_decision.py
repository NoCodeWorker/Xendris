import json
from pathlib import Path

from phyng.master_goal.campaign import run_master_goal_campaign


def test_master_goal_reaches_dataset_threshold_but_not_validation():
    result = run_master_goal_campaign(".")

    assert result["total_accepted_ytrue_count"] >= 10
    assert result["independent_source_count"] >= 2
    assert result["terminal_status"] == "NO_CANDIDATE_WITH_REALITY_CONTACT"
    assert result["candidate_family_selected"] is None


def test_master_goal_does_not_compute_predictive_gain_or_claim_validation():
    run_master_goal_campaign(".")
    benchmark = json.loads(Path("data/frontera_c/master_goal/benchmark_readiness_v5_7_4_master.json").read_text(encoding="utf-8"))
    dataset = json.loads(Path("data/frontera_c/master_goal/dataset_v5_7_4_master.json").read_text(encoding="utf-8"))

    assert benchmark["predictive_gain_computed"] is False
    assert dataset["frontera_c_validated"] is False
    assert dataset["physical_claim_created"] is False


def test_master_decision_report_generated():
    run_master_goal_campaign(".")
    report = Path("docs/PHYGN_MASTER_FRONTERA_C_VALIDATION_DECISION_REPORT.md")

    assert report.exists()
    text = report.read_text(encoding="utf-8")
    assert "Final terminal status: `NO_CANDIDATE_WITH_REALITY_CONTACT`" in text
    assert "PredictiveGain: `NOT_COMPUTED`" in text
