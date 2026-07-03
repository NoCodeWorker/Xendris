import pytest
from xendris.benchmarks.false_formality.core.types import ModelResponse
from xendris.benchmarks.false_formality.core.base_model_client import BaseModelClient
from xendris.benchmarks.false_formality.core.xendris_pipeline import XendrisPipelineClient

def test_base_model_client_contract():
    client = BaseModelClient(provider="mock")
    assert hasattr(client, "generate")
    resp = client.generate("test-id", "test-prompt")
    assert isinstance(resp, ModelResponse)
    assert resp.case_id == "test-id"
    assert resp.system == "base_model"
    assert isinstance(resp.response_text, str)

def test_xendris_pipeline_client_contract():
    client = XendrisPipelineClient(provider="mock")
    assert hasattr(client, "generate")
    resp = client.generate("test-id", "test-prompt")
    assert isinstance(resp, ModelResponse)
    assert resp.case_id == "test-id"
    assert resp.system == "xendris"
    assert isinstance(resp.response_text, str)
