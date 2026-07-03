export function detectLanguage(text: string): "es" | "en" {
  const textLower = text.toLowerCase()

  const spanishMarkers = [
    "¿",
    "¡",
    "qué",
    "cómo",
    "cuál",
    "responde",
    "explica",
    "demuestra",
    "caché",
    "siempre",
    "calidad",
    "por qué",
    "es cierto",
    "matemático",
    "explicación",
    "seguridad",
    "inmune",
    "protección",
    "ataques",
  ]

  const englishMarkers = [
    "what",
    "how",
    "why",
    "explain",
    "prove",
    "always",
    "quality",
    "is it true",
    "mathematical",
    "explanation",
    "security",
    "immune",
    "protection",
    "attacks",
    "architecture",
    "validation",
    "limiting",
    "complete",
  ]

  let spanishScore = 0
  let englishScore = 0

  for (const marker of spanishMarkers) {
    if (textLower.includes(marker)) {
      spanishScore++
    }
  }

  for (const marker of englishMarkers) {
    if (textLower.includes(marker)) {
      englishScore++
    }
  }

  return englishScore > spanishScore ? "en" : "es"
}
