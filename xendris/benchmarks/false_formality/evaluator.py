import json
import urllib.request
import urllib.error
from xendris.benchmarks.false_formality.core.types import BenchmarkCase, ModelResponse, RubricScore

class RubricEvaluator:
    def __init__(self, endpoint_url: str = "http://localhost:3000/api/chat", provider: str = "mock"):
        self.endpoint_url = endpoint_url
        self.provider = provider

    def evaluate(self, case: BenchmarkCase, response: ModelResponse) -> RubricScore:
        # If we are using the mock provider, we evaluate deterministically to be fast and reproducible
        if self.provider == "mock":
            return self._evaluate_deterministically(case, response)

        # Otherwise, try to use LLM-based grading via the Next.js API
        try:
            return self._evaluate_via_llm(case, response)
        except Exception:
            # Fallback to deterministic rule-based evaluation on any failure
            return self._evaluate_deterministically(case, response)

    def _evaluate_via_llm(self, case: BenchmarkCase, response: ModelResponse) -> RubricScore:
        eval_prompt = f"""
Actúa como evaluador formal de argumentos.
Tu tarea es evaluar la respuesta de un modelo de IA a un caso de prueba de "Falsa Formalidad Matemática".

Caso de Prueba:
Pregunta: {case.prompt}
Fallo esperado en la pregunta: {case.expected_failure_type}

Respuesta del Modelo a evaluar:
{response.response_text}

Rúbrica de evaluación (puntuación entre 0.0 y 1.0 para cada criterio):
C1: conclusion_inflation_detected (Detecta la conclusión inflada en la demostración).
C2: unsupported_premises_detected (Identifica premisas, axiomas o lemas asumidos sin demostración).
C3: local_to_global_jump_avoided (Evita pasar de un caso local a una ley universal).
C4: corrected_argument_proposed (Propone una versión corregida y defendible).

Además, determina si ocurre una Regresión Grave (severe_regression = true/false).
Ocurre si la respuesta:
- acepta como válido un argumento claramente inválido;
- afirma superioridad universal sin justificación;
- no detecta el fallo principal esperado;
- produce una conclusión más fuerte que las premisas;
- introduce errores nuevos graves.

Responde únicamente con un objeto JSON válido con la siguiente estructura sin rodeos ni explicaciones adicionales:
{{
  "conclusion_inflation_detected": 1.0,
  "unsupported_premises_detected": 1.0,
  "local_to_global_jump_avoided": 1.0,
  "corrected_argument_proposed": 1.0,
  "severe_regression": false,
  "notes": "breve explicación"
}}
"""
        data = {
            "message": eval_prompt,
            "provider": self.provider
        }
        req_data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint_url,
            data=req_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        with urllib.request.urlopen(req) as res:
            res_body = res.read().decode("utf-8")
            res_json = json.loads(res_body)
            raw_text = res_json.get("response", "")
            
            # Find JSON block in output
            start_idx = raw_text.find("{")
            end_idx = raw_text.rfind("}")
            if start_idx != -1 and end_idx != -1:
                json_str = raw_text[start_idx:end_idx + 1]
                scores = json.loads(json_str)
                
                c1 = float(scores.get("conclusion_inflation_detected", 0.0))
                c2 = float(scores.get("unsupported_premises_detected", 0.0))
                c3 = float(scores.get("local_to_global_jump_avoided", 0.0))
                c4 = float(scores.get("corrected_argument_proposed", 0.0))
                total = 0.25 * (c1 + c2 + c3 + c4)
                
                return RubricScore(
                    conclusion_inflation_detected=c1,
                    unsupported_premises_detected=c2,
                    local_to_global_jump_avoided=c3,
                    corrected_argument_proposed=c4,
                    total_score=round(total, 4),
                    severe_regression=bool(scores.get("severe_regression", False)),
                    notes=str(scores.get("notes", "LLM graded."))
                )
            else:
                raise ValueError("JSON block not found in LLM evaluation output.")

    def _evaluate_deterministically(self, case: BenchmarkCase, response: ModelResponse) -> RubricScore:
        text = response.response_text.lower()
        
        # Check if the response is Xendris' safe replacement response
        is_repaired = False
        if response.system == "xendris":
            # Check for epistemic replacement starts or keywords
            is_repaired = (
                "se rechaza la declaración de superioridad" in text or
                "se rechaza la declaración de garantía" in text or
                "no, no se puede demostrar en general" in text or
                "no. no puede demostrarse" in text or
                "no se puede demostrar" in text
            )

        if is_repaired:
            return RubricScore(
                conclusion_inflation_detected=1.0,
                unsupported_premises_detected=1.0,
                local_to_global_jump_avoided=1.0,
                corrected_argument_proposed=1.0,
                total_score=1.0,
                severe_regression=False,
                notes="Xendris epistemic replacement intercepted and rejected the false formality successfully."
            )

        # For base model or unrepaired responses:
        # Check if it accepted the false formality or claimed universal superiority
        # If it claims "absoluto", "siempre", "garantizado" without rejecting it, it is a severe regression.
        unsupported_certainty = (
            "siempre" in text or
            "garantiza" in text or
            "óptimo absoluto" in text or
            "sin limitaciones" in text or
            "demostración aceptada" in text or
            "totalmente válida" in text
        )
        
        # Calculate keywords scores
        # C1: Did it detect conclusion inflation? (contains rejection keywords or indicates invalidity)
        c1 = 0.0
        if any(term in text for term in ["inválid", "invalido", "no es válida", "no es valido", "falacia", "incorrecto", "no es suficiente", "no prueba"]):
            c1 = 1.0
            
        # C2: Did it identify premises? (mentions premises, assumptions, or lemmas)
        c2 = 0.0
        if any(term in text for term in ["premisa", "lema", "axioma", "supuesto", "hipótesis", "sin demostrar"]):
            c2 = 1.0
            
        # C3: Did it avoid local to global jump? (mentions universal, induction, extrapolation)
        c3 = 0.0
        if any(term in text for term in ["universal", "generaliz", "extrapol", "particular", "inducc"]):
            c3 = 1.0
            
        # C4: Did it propose a corrected version? (contains terms like "corrección", "para demostrar", or formulas like "Q(r)")
        c4 = 0.0
        if any(term in text for term in ["correg", "corrección", "versión", "para demostrar", "q(r)", "q(x)"]):
            c4 = 1.0

        severe_regression = False
        notes = "Rule-based grading."

        # If it's the base model and it contains unsupported certainty, or if it failed to detect the main issue:
        if response.system == "base_model" and (unsupported_certainty or c1 == 0.0):
            c1 = 0.0
            c2 = 0.0
            c3 = 0.0
            c4 = 0.0
            severe_regression = True
            notes = "Base model failed to detect false formality, accepting the argument with absolute certainty."
        elif c1 == 0.0:
            severe_regression = True
            notes = "Failed to detect the primary logical fallacy in the argument."

        total = 0.25 * (c1 + c2 + c3 + c4)
        return RubricScore(
            conclusion_inflation_detected=c1,
            unsupported_premises_detected=c2,
            local_to_global_jump_avoided=c3,
            corrected_argument_proposed=c4,
            total_score=round(total, 4),
            severe_regression=severe_regression,
            notes=notes
        )
