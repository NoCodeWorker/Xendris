import os
import json
import pytest
from xendris.benchmarks.false_formality.runner import load_cases
from xendris.benchmarks.false_formality.core.types import BenchmarkCase

def test_load_cases_contract():
    cases_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "xendris", "benchmarks", "false_formality", "cases.json"
    )
    assert os.path.exists(cases_path)
    
    cases = load_cases(cases_path)
    assert isinstance(cases, list)
    assert len(cases) > 0
    for case in cases:
        assert isinstance(case, BenchmarkCase)
        assert case.id.startswith("FF-")
        assert case.prompt != ""
        assert case.expected_failure_type != ""
        assert case.expected_detection != ""
        assert case.category != ""

def test_rubric_file_contract():
    rubric_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "xendris", "benchmarks", "false_formality", "rubric.json"
    )
    assert os.path.exists(rubric_path)
    with open(rubric_path, "r", encoding="utf-8") as f:
        rubric = json.load(f)
    assert "criteria" in rubric
    assert "formula" in rubric
    assert "severe_regression_criteria" in rubric
