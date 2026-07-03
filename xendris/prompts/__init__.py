"""
xendris.prompts — Isolated system-prompt strings.

Store all LLM system-prompt text here, decoupled from orchestration logic.
Each variable is a plain string; no imports from model providers.

Naming convention:
    PROMPT_<DOMAIN>_<ROLE>
    e.g. PROMPT_EPISTEMIC_REPAIR, PROMPT_FRONTERA_C_EVALUATOR
"""

# Placeholder — move hardcoded prompt strings here in subsequent iterations.
# Example:
#
#   PROMPT_EPISTEMIC_REPAIR = """
#   You are an epistemic repair engine. When a claim exceeds what the
#   premises allow, replace it with a corrected version that exactly
#   matches the evidence.
#   """
