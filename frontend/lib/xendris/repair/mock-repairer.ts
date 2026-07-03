import type { AnswerControllerDecision } from "src/lib/xendris/controller/types"
import type { RepairResult } from "src/lib/xendris/repair/types"

function normalizeContent(content: string) {
  return content.trimEnd()
}

export function repairWithMockRules(
  content: string,
  controllerDecision: AnswerControllerDecision
): RepairResult {
  const originalContent = content
  const normalizedContent = normalizeContent(content)

  if (controllerDecision.action === "needs_improvement") {
    const suggestedNextStep =
      controllerDecision.suggestedNextStep ?? "Pide una versión más concreta o añade el contexto que falta."

    return {
      repaired: true,
      originalContent,
      finalContent: `${normalizedContent}\n\n### Clarificación\n\n- Esta respuesta fue marcada para mejora por el controlador interno.\n- Motivo: ${controllerDecision.reason}\n- Siguiente paso sugerido: ${suggestedNextStep}`,
      repairReason: controllerDecision.reason,
      repairStrategy: "append_structured_clarification",
    }
  }

  if (controllerDecision.action === "needs_review") {
    return {
      repaired: true,
      originalContent,
      finalContent: `${normalizedContent}\n\n> Nota de cautela: esta respuesta requiere revisión antes de usarse. Motivo: ${controllerDecision.reason}`,
      repairReason: controllerDecision.reason,
      repairStrategy: "append_caution_note",
    }
  }

  return {
    repaired: false,
    originalContent,
    finalContent: content,
  }
}
