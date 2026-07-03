import type { AnswerControllerDecision } from "src/lib/xendris/controller/types"
import type { RepairResult } from "src/lib/xendris/repair/types"
import type { EpistemicEvaluation } from "src/lib/xendris/epistemic/types"
import { detectLanguage } from "src/lib/xendris/language/detect-language"

function normalizeContent(content: string) {
  return content.trimEnd()
}

function getEpistemicTopic(
  userMessage: string,
  content: string
): "xendris_vs_deepseek" | "cache_quality" | "security_absolute_guarantee" | "generic" {
  const msgLower = userMessage.toLowerCase()
  const contentLower = content.toLowerCase()
  const combined = `${msgLower} ${contentLower}`

  // Topic A: Xendris and DeepSeek comparison
  const mentionsXendris = msgLower.includes("xendris")
  const mentionsDeepseek = msgLower.includes("deepseek")
  const mentionsUniversal = ["siempre", "mejor", "supera", "superioridad", "always", "better", "superior"].some((term) =>
    msgLower.includes(term)
  )
  if (mentionsXendris && mentionsDeepseek && mentionsUniversal) {
    return "xendris_vs_deepseek"
  }

  // Topic B: Cache Quality improvement
  const mentionsCache = msgLower.includes("cache") || msgLower.includes("caché")
  const mentionsQuality = msgLower.includes("calidad") || msgLower.includes("quality")
  const mentionsAlways = ["siempre", "always", "domina", "dominates", "estrictamente", "strictly", "mejorar", "improve"].some((term) =>
    msgLower.includes(term)
  )
  if (mentionsCache && mentionsQuality && mentionsAlways) {
    return "cache_quality"
  }

  // Topic C: Security Absolute Guarantee
  const hasSecurityContext = [
    "cybersecurity",
    "security",
    "web app",
    "next.js",
    "jwt",
    "rate limiting",
    "input validation",
    "ciberseguridad",
    "seguridad",
    "validación de entrada",
    "limitación de tasa",
  ].some((term) => combined.includes(term))

  const hasSecurityAbsolutist = [
    "inmune",
    "impenetrable",
    "seguro contra cualquier ataque",
    "cualquier ataque web moderno",
    "todo el espectro",
    "cobertura completa",
    "barrera completa",
    "anula cualquier vector",
    "no existe ataque",
    "garantiza confidencialidad",
    "garantiza integridad",
    "garantiza disponibilidad",
    "owasp top 10 completely covered",
    "immune",
    "secure against any attack",
    "all modern web attacks",
    "complete protection",
    "no attack can compromise",
  ].some((term) => combined.includes(term))

  if (hasSecurityContext && hasSecurityAbsolutist) {
    return "security_absolute_guarantee"
  }

  return "generic"
}

export function repairWithMockRules(
  userMessage: string,
  content: string,
  controllerDecision: AnswerControllerDecision,
  epistemicEvaluation?: EpistemicEvaluation
): RepairResult {
  const originalContent = content
  const normalizedContent = normalizeContent(content)

  if (epistemicEvaluation?.riskLevel === "high") {
    const topic = getEpistemicTopic(userMessage, content)
    const lang = detectLanguage(userMessage)

    if (topic === "xendris_vs_deepseek") {
      const replacementTextEs = `Se rechaza la declaración de superioridad universal o absoluta sobre Xendris frente a DeepSeek directo.

La superioridad de Xendris no es universal y debe validarse empíricamente en cada escenario. Aunque el sistema añade capas de análisis (evaluación, reparación y caché de respuestas), solo puede mejorar los resultados de DeepSeek directo en condiciones específicas donde las reglas deterministas identifiquen y corrijan anomalías.

Modos de fallo potenciales del pipeline de Xendris:
1. Clasificación de intenciones incorrecta: El enrutador puede clasificar de forma errónea una petición, aplicando directrices inadecuadas.
2. Evaluador débil: El evaluador determinista de calidad podría no detectar respuestas deficientes o imprecisas.
3. Reparación innecesaria: El bucle de reparación podría reescribir una respuesta correcta de forma no deseada, introduciendo errores o reduciendo claridad.
4. Caché desactualizada: La caché de memoria podría devolver información obsoleta.
5. Prompt del sistema deficiente: El prompt del sistema configurado podría no ser el óptimo para tareas muy específicas.
6. Latencia añadida: El paso extra de evaluación y reparación incrementa el tiempo total de respuesta.`;

      const replacementTextEn = `The statement of universal or absolute superiority of Xendris over direct DeepSeek is rejected.

The superiority of Xendris is not universal and must be empirically validated in each scenario. Although the system adds analysis layers (evaluation, repair, and response cache), it can only improve direct DeepSeek results under specific conditions where deterministic rules identify and correct anomalies.

Potential failure modes of the Xendris pipeline:
1. Incorrect intent classification: The router may misclassify a request, applying inappropriate guidelines.
2. Weak evaluator: The deterministic quality evaluator might fail to detect poor or imprecise responses.
3. Unnecessary repair: The repair loop could overwrite a correct response in an undesired way, introducing errors or reducing clarity.
4. Stale cache: The memory cache could return obsolete information.
5. Ineffective system prompt: The configured system prompt may not be optimal for highly specific tasks.
6. Added latency: The extra step of evaluation and repair increases the total response time.`;

      return {
        repaired: true,
        originalContent,
        finalContent: lang === "es" ? replacementTextEs : replacementTextEn,
        repairReason: lang === "es"
          ? "Se detectó certeza no sustentada o aserción absoluta sobre la superioridad de Xendris vs DeepSeek."
          : "Unsupported certainty or absolute assertion about Xendris vs DeepSeek superiority detected.",
        repairStrategy: "epistemic_replacement_xendris_comparison",
      }
    }

    if (topic === "cache_quality") {
      const replacementTextEs = `No, no se puede demostrar en general que añadir una caché a una IA siempre aumente la calidad media de sus respuestas.

A nivel de análisis formal:
- Sea Q(r) una función de calidad que evalúa una respuesta r.
- Para demostrar la dominancia matemática de la caché frente a la generación directa, sería necesario garantizar que Q(r_cache(x)) >= Q(r_base(x)) para toda consulta x, con una mejora estricta en un subconjunto de medida positiva.

Esta condición de dominancia no se cumple en general debido a múltiples factores:
1. Respuestas obsoletas (stale cache): Los datos cacheados pueden perder vigencia ante cambios en el entorno de la consulta.
2. Desajustes en la recuperación semántica (retrieval mismatch): Un sistema de recuperación semántica puede asociar una consulta nueva con una entrada cacheada similar pero conceptualmente no equivalente, devolviendo una respuesta errónea.
3. Respuestas de base potencialmente mejores (fresh generation): Una consulta fresca puede beneficiarse de una mejor generación directa o de datos actualizados en tiempo real.
4. Dependencia del contexto temporal: La función Q puede variar según las condiciones externas del momento de la consulta.
5. Amplificación de errores previos: La caché puede fijar y repetir de forma persistente respuestas incorrectas generadas anteriormente.

Aunque la caché optimiza la latencia, el costo operativo y la consistencia de las respuestas, la mejora de la calidad media solo ocurre bajo condiciones controladas (evaluación rigurosa de entradas cacheadas, políticas estrictas de expiración y distribución adecuada de consultas).`;

      const replacementTextEn = `No, it cannot be proven in general that adding a cache to an AI always increases the average quality of its responses.

At a formal analysis level:
- Let Q(r) be a quality function evaluating a response r.
- To prove mathematical dominance of the cache over direct generation, it would be necessary to guarantee that Q(r_cache(x)) >= Q(r_base(x)) for all queries x, with a strict improvement on a positive-measure subset.

This dominance condition is not guaranteed in general due to multiple factors:
1. Obsolete responses (stale cache): Cached data may lose validity due to changes in the environment of the query.
2. Semantic retrieval mismatch (retrieval mismatch): A semantic retrieval system may associate a new query with a similar but conceptually non-equivalent cached entry, returning an incorrect response.
3. Potentially better base responses (fresh generation): A fresh query can benefit from better direct generation or real-time updated data.
4. Time/context dependency: The function Q may vary according to the external conditions at the time of the query.
5. Amplification of previous errors: The cache may persistently store and repeat previously generated incorrect responses.

Although the cache optimizes latency, operational cost, and response consistency, average quality improvement only occurs under controlled conditions (rigorous evaluation of cached entries, strict expiration policies, and suitable query distribution).`;

      return {
        repaired: true,
        originalContent,
        finalContent: lang === "es" ? replacementTextEs : replacementTextEn,
        repairReason: lang === "es"
          ? "Se detectó aserción absoluta sobre el impacto de la caché en la calidad media de respuestas."
          : "Absolute assertion about cache impact on response quality detected.",
        repairStrategy: "epistemic_replacement_cache_quality",
      }
    }

    if (topic === "security_absolute_guarantee") {
      const replacementTextEs = `Se rechaza la declaración de garantía absoluta de seguridad, inmunidad o protección completa.

Aunque la validación de entradas, la limitación de tasa y el uso de JWT reducen significativamente la superficie de exposición y el riesgo de explotación, ningún sistema de software es completamente invulnerable ni está exento de fallos de seguridad.

Riesgos residuales a considerar:
1. Scripting entre sitios (XSS): A través de un renderizado inseguro de datos en el cliente o vulnerabilidades en dependencias externas.
2. Falsificación de peticiones en sitios cruzados (CSRF): Si la configuración de tokens o cookies (como atributos SameSite/Secure) es incorrecta.
3. Falsificación de peticiones del lado del servidor (SSRF): En endpoints del servidor que procesan URLs de forma no controlada.
4. Fallos de autorización a nivel de objeto o función (IDOR/BOLA): Errores en la lógica de control de acceso que permiten consultar recursos ajenos.
5. Exposición de secretos: Claves de API, certificados o variables de entorno expuestos accidentalmente en repositorios o logs.
6. Políticas de CORS inseguras: Configuraciones permisivas que habilitan accesos no autorizados desde orígenes externos maliciosos.
7. Vulnerabilidades en dependencias y cadena de suministro: Librerías obsoletas o comprometidas en el árbol de dependencias.
8. Errores en middleware: Flujos de control que omiten verificaciones críticas bajo ciertas rutas o condiciones.
9. Fallas en la lógica de negocio: Escenarios donde un atacante puede alterar flujos legítimos del sistema sin violar restricciones técnicas explícitas.
10. Problemas en la carga de archivos: Carga de archivos ejecutables o manipulación de rutas si se permiten subidas al servidor.
11. Almacenamiento, rotación o validación débil de JWT: Uso de claves de firma débiles, falta de validación de campos/atributos críticos en el payload o exposición del token en el cliente.

Controles adicionales recomendados:
- Verificación exhaustiva de autorización en cada recurso.
- Implementación de cabeceras de seguridad y Política de Seguridad de Contenido (CSP) estricta.
- Estrategias de mitigación contra CSRF (como cookies SameSite estrictas o tokens de sincronización).
- Escaneo continuo de dependencias y análisis de seguridad estático/dinámico (SAST/DAST).
- Registro (logging) robusto y monitoreo activo de anomalías.
- Pruebas de penetración periódicas.
- Uso de gestores de secretos dedicados.
- Configuración segura del entorno de despliegue.`;

      const replacementTextEn = `The statement of an absolute guarantee of security, immunity, or complete protection is rejected.

Although input validation, rate limiting, and the use of JWTs significantly reduce the exposure surface and the risk of exploitation, no software system is completely invulnerable or free from security flaws.

Residual risks to consider:
1. Cross-Site Scripting (XSS): Through insecure data rendering on the client or vulnerabilities in third-party dependencies.
2. Cross-Site Request Forgery (CSRF): If token or cookie configurations (such as SameSite/Secure attributes) are incorrect.
3. Server-Side Request Forgery (SSRF): In server-side endpoints that process input URLs without verification.
4. Broken Object/Function Level Authorization (IDOR/BOLA): Access control logic errors that allow querying other users' resources.
5. Secrets exposure: API keys, certificates, or environment variables accidentally exposed in repositories or logs.
6. Insecure CORS policies: Permissive configurations that enable unauthorized access from malicious external origins.
7. Dependency and supply chain vulnerabilities: Outdated or compromised libraries in the dependency tree.
8. Middleware errors: Control flows that bypass critical verification checks under certain routes or conditions.
9. Business logic flaws: Scenarios where an attacker can alter legitimate system flows without violating explicit technical constraints.
10. File upload issues: Upload of executable files or path manipulation if file uploads are permitted.
11. Weak JWT storage, rotation, or attribute validation: Use of weak signing keys, lack of critical payload validation, or token exposure on the client.

Recommended additional controls:
- Thorough authorization checks for every resource.
- Implementation of security headers and a strict Content Security Policy (CSP).
- CSRF mitigation strategies (such as strict SameSite cookies or anti-CSRF tokens).
- Continuous dependency scanning and static/dynamic security analysis (SAST/DAST).
- Robust logging and active anomaly monitoring.
- Periodic penetration testing.
- Use of dedicated secrets managers.
- Secure deployment environment configuration.`;

      return {
        repaired: true,
        originalContent,
        finalContent: lang === "es" ? replacementTextEs : replacementTextEn,
        repairReason: lang === "es"
          ? "Se detectó aserción absoluta sobre la seguridad o protección del sistema."
          : "Absolute assertion about system security or protection detected.",
        repairStrategy: "epistemic_replacement_security",
      }
    }

    // Generic fallback
    const replacementTextEs = `Se rechaza la declaración de garantía universal o absoluta no sustentada empíricamente.

Toda aserción de superioridad o desempeño garantizado sin excepciones requiere de una validación empírica en el escenario particular bajo estudio o de premisas adicionales extremadamente fuertes.

Para formalizar y sostener este tipo de declaraciones absolutas, sería necesario cumplir con las siguientes suposiciones:
1. Uniformidad total del dominio: Que el rendimiento de la alternativa propuesta supere de forma no decreciente a la base en todo punto de evaluación.
2. Invariabilidad temporal: Que las condiciones de evaluación permanezcan estacionarias en el tiempo.
3. Determinismo absoluto: Ausencia de aleatoriedad o derivas en la distribución de las consultas.

Sin cumplir estas hipótesis, la validez debe determinarse mediante pruebas experimentales exhaustivas y no puede deducirse en términos universales abstractos.`;

    const replacementTextEn = `The statement of an unsupported universal or absolute guarantee is rejected.

Any assertion of superiority or guaranteed performance without exceptions requires empirical validation in the specific scenario under study or extremely strong additional assumptions.

To formalize and support such absolute statements, it would be necessary to meet the following assumptions:
1. Full domain uniformity: That the performance of the proposed alternative non-decreasably exceeds the base at every evaluation point.
2. Time invariance: That the evaluation conditions remain stationary over time.
3. Absolute determinism: Absence of randomness or drift in the distribution of queries.

Without meeting these hypotheses, validity must be determined through exhaustive experimental testing and cannot be deduced in universal abstract terms.`;

    return {
      repaired: true,
      originalContent,
      finalContent: lang === "es" ? replacementTextEs : replacementTextEn,
      repairReason: lang === "es"
        ? "Se detectó certeza no sustentada o aserción universal absoluta."
        : "Unsupported certainty or universal absolute assertion detected.",
      repairStrategy: "epistemic_replacement_generic",
    }
  }

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
