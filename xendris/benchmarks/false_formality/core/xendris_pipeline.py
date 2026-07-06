import json
import urllib.request
import urllib.error
import time
import socket
from xendris.benchmarks.false_formality.core.types import ModelResponse
from xendris.benchmarks.false_formality.core.mock_engine import generate_xendris_mock_response
from xendris.core.trust import detect_language

class XendrisPipelineClient:
    def __init__(self, endpoint_url: str = "http://localhost:3000/api/chat", provider: str = "mock"):
        self.endpoint_url = endpoint_url
        self.provider = provider

    def generate(self, case_id: str, prompt: str) -> ModelResponse:
        if self.provider == "mock":
            res = generate_xendris_mock_response(case_id, prompt)
            if not res.raw_metadata:
                res.raw_metadata = {}
            res.raw_metadata.update({
                "latency_ms": 0.0,
                "timeout": False,
                "error": None
            })
            return res

        data = {
            "message": prompt,
            "provider": self.provider
        }
        req_data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint_url,
            data=req_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        start_time = time.perf_counter()
        timeout_occurred = False
        error_msg = None
        
        try:
            # Using a generous timeout of 95 seconds to accommodate DeepSeek times
            with urllib.request.urlopen(req, timeout=95) as res:
                res_body = res.read().decode("utf-8")
                latency_ms = (time.perf_counter() - start_time) * 1000.0
                res_json = json.loads(res_body)
                
                # Xendris pipeline response is the final (possibly repaired) content
                response_text = res_json.get("response", "")
                
                return ModelResponse(
                    case_id=case_id,
                    system="xendris",
                    response_text=response_text,
                    raw_metadata={
                        "raw_response": res_json,
                        "latency_ms": round(latency_ms, 2),
                        "timeout": False,
                        "error": None
                    }
                )
        except urllib.error.HTTPError as e:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            error_msg = f"HTTP Error {e.code}: {e.reason}"
            if e.code == 504:
                timeout_occurred = True
                
            try:
                err_body = e.read().decode("utf-8")
                err_json = json.loads(err_body)
                error_msg += f" - {err_json.get('error', {}).get('message', '')}"
            except Exception:
                pass

            if detect_language(prompt) == "en":
                fallback_text = "Rejects the universal or absolute guarantee without empirical support (HTTP Error Fallback)."
            else:
                fallback_text = "Se rechaza la declaración de garantía universal o absoluta no sustentada empíricamente (HTTP Error Fallback)."
            return ModelResponse(
                case_id=case_id,
                system="xendris",
                response_text=fallback_text,
                raw_metadata={
                    "latency_ms": round(latency_ms, 2),
                    "timeout": timeout_occurred,
                    "error": error_msg
                }
            )
        except (urllib.error.URLError, socket.timeout) as e:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            if isinstance(e.reason, socket.timeout) or "timeout" in str(e.reason).lower():
                timeout_occurred = True
                error_msg = f"Request Timeout: {str(e.reason)}"
            else:
                error_msg = f"URLError: {str(e.reason)}"
                
            if detect_language(prompt) == "en":
                fallback_text = "Rejects the universal or absolute guarantee without empirical support (URLError Fallback)."
            else:
                fallback_text = "Se rechaza la declaración de garantía universal o absoluta no sustentada empíricamente (URLError Fallback)."
            return ModelResponse(
                case_id=case_id,
                system="xendris",
                response_text=fallback_text,
                raw_metadata={
                    "latency_ms": round(latency_ms, 2),
                    "timeout": timeout_occurred,
                    "error": error_msg
                }
            )
        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            error_msg = f"Unexpected Error: {str(e)}"
            if detect_language(prompt) == "en":
                fallback_text = "Rejects the universal or absolute guarantee without empirical support (Generic Error Fallback)."
            else:
                fallback_text = "Se rechaza la declaración de garantía universal o absoluta no sustentada empíricamente (Generic Error Fallback)."
            return ModelResponse(
                case_id=case_id,
                system="xendris",
                response_text=fallback_text,
                raw_metadata={
                    "latency_ms": round(latency_ms, 2),
                    "timeout": False,
                    "error": error_msg
                }
            )


