"""
Mock engine for deterministic offline testing.

Base model simulation: Accepts the argument, does NOT detect the fallacy.
Xendris simulation:    Identifies the fallacy precisely, proposes a corrected version.

Both responses are stable and do not depend on network calls.
"""

from xendris.benchmarks.false_formality.core.types import ModelResponse

# Prototype response for a base model that accepts false formal arguments.
# It does not identify the main fallacy and produces a conclusion
# stronger than the premises allow. This triggers severe_regression in the evaluator.
_BASE_MODEL_ACCEPT_TEMPLATE = (
    "Esta demostración es formalmente sólida. Las premisas son consistentes y "
    "la conclusión se deriva directamente de ellas. El sistema demuestra capacidad "
    "generalizada y totalmente válida en el dominio completo evaluado."
)

# Prototype response for Xendris: identifies the fallacy, marks it as inválido,
# references premises, indicates the local-to-universal jump, and proposes a corrected version.
_XENDRIS_REJECT_TEMPLATE = (
    "Veredicto: inválida por salto lógico y premisa no demostrada.\n\n"
    "Fallos formales:\n"
    "1. La conclusión excede lo que las premisas permiten inferir.\n"
    "2. Se detecta un salto ilegítimo de caso particular a ley universal.\n"
    "3. El lema implícito no está demostrado; se asume sin justificación.\n"
    "4. La terminología clave (dominio, métrica, universalidad) no está definida.\n\n"
    "Conclusión válida:\n"
    "La evidencia presentada solo permite afirmar que el fenómeno se observó en los "
    "casos particulares citados. Generalizar a todos los casos requiere demostración inductiva completa.\n\n"
    "Versión corregida:\n"
    "Sea S un conjunto finito de casos observados. Se puede afirmar que el sistema se comportó "
    "conforme a lo esperado en S. Para extender esta afirmación a todo el dominio D ⊇ S, "
    "se requiere una demostración de que S es representativo de D bajo una métrica Q definida, "
    "o una prueba inductiva formal que cubra todos los casos posibles."
)


def generate_base_mock_response(case_id: str, prompt: str) -> ModelResponse:
    """Simulate a base model response that fails to detect the false formality fallacy."""
    return ModelResponse(
        case_id=case_id,
        system="base_model",
        response_text=_BASE_MODEL_ACCEPT_TEMPLATE,
        raw_metadata={"mode": "mock", "type": "base_model_accept"}
    )


def generate_xendris_mock_response(case_id: str, prompt: str) -> ModelResponse:
    """Simulate a Xendris pipeline response that correctly rejects the false formality fallacy."""
    return ModelResponse(
        case_id=case_id,
        system="xendris",
        response_text=_XENDRIS_REJECT_TEMPLATE,
        raw_metadata={"mode": "mock", "type": "xendris_reject"}
    )
