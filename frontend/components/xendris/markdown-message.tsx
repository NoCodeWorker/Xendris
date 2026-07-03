"use client"

import * as React from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

type MarkdownMessageProps = {
  content: string
}

function formatMathText(math: string): string {
  return math
    .replace(/\\mathbb\{E\}/g, "𝔼")
    .replace(/\\mathbb\{P\}/g, "ℙ")
    .replace(/\\mathbb\{R\}/g, "ℝ")
    .replace(/\\text\{fresh\}/g, "fresh")
    .replace(/\\text\{base\}/g, "base")
    .replace(/\\text\{cache\}/g, "cache")
    .replace(/\\ge(q)?/g, "≥")
    .replace(/\\le(q)?/g, "≤")
    .replace(/\\neq/g, "≠")
    .replace(/\\times/g, "×")
    .replace(/\\approx/g, "≈")
    .replace(/\\in/g, "∈")
    .replace(/\\notin/g, "∉")
    .replace(/\\infty/g, "∞")
    .replace(/\\pm/g, "±")
    .replace(/\\alpha/g, "α")
    .replace(/\\beta/g, "β")
    .replace(/\\gamma/g, "γ")
    .replace(/\\delta/g, "δ")
    .replace(/\\Delta/g, "Δ")
    .replace(/\\theta/g, "θ")
    .replace(/\\lambda/g, "λ")
    .replace(/\\mu/g, "μ")
    .replace(/\\pi/g, "π")
    .replace(/\\sigma/g, "σ")
    .replace(/\\phi/g, "φ")
    .replace(/\\omega/g, "ω")
}

function preprocessMath(text: string): string {
  let result = text

  // 1. Convert Display Math \[ ... \] to ```math-block ... ```
  result = result.replace(/\\\[([\s\S]*?)\\\]/g, (_, math) => {
    return `\n\`\`\`math-block\n${math.trim()}\n\`\`\`\n`
  })

  // 2. Convert Inline Math \( ... \) to `math-inline:...`
  result = result.replace(/\\\(([\s\S]*?)\\\)/g, (_, math) => {
    return `\`math-inline:${math.trim()}\``
  })

  return result
}

async function copyToClipboard(value: string) {
  if (!navigator.clipboard) return false

  try {
    await navigator.clipboard.writeText(value)
    return true
  } catch {
    return false
  }
}

function CopyableCodeBlock({ code }: { code: string }) {
  const [copyState, setCopyState] = React.useState<"idle" | "copied" | "failed">("idle")

  async function handleCopy() {
    const didCopy = await copyToClipboard(code)
    setCopyState(didCopy ? "copied" : "failed")
    window.setTimeout(() => setCopyState("idle"), 1400)
  }

  return (
    <div className="my-4 overflow-hidden rounded-2xl border border-current/15 bg-background/95 shadow-sm">
      <div className="flex items-center justify-between border-b border-border px-3 py-2">
        <span className="text-xs text-muted-foreground">code</span>
        <button
          type="button"
          aria-label="Copiar bloque de código"
          onClick={handleCopy}
          className="rounded-md px-2 py-1 text-xs text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-ring/30"
        >
          {copyState === "copied" ? "Copiado" : copyState === "failed" ? "No copiado" : "Copiar"}
        </button>
      </div>
      <pre className="overflow-x-auto scrollbar-thin">
        <code className="block whitespace-pre p-4 font-mono text-sm text-foreground">{code}</code>
      </pre>
    </div>
  )
}

export function MarkdownMessage({ content }: MarkdownMessageProps) {
  const processedContent = React.useMemo(() => preprocessMath(content), [content])

  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        h1: ({ children }) => (
          <h1 className="mb-4 mt-2 text-2xl font-semibold tracking-tight text-foreground">{children}</h1>
        ),
        h2: ({ children }) => (
          <h2 className="mb-4 mt-6 text-xl font-semibold tracking-tight text-foreground first:mt-1">
            {children}
          </h2>
        ),
        h3: ({ children }) => (
          <h3 className="mb-3 mt-5 text-base font-semibold tracking-tight text-foreground first:mt-1">
            {children}
          </h3>
        ),
        p: ({ children }) => (
          <p className="my-3.5 text-[15px] leading-8 text-foreground/90 font-sans tracking-wide">
            {children}
          </p>
        ),
        strong: ({ children }) => <strong className="font-semibold text-foreground">{children}</strong>,
        em: ({ children }) => <em className="italic">{children}</em>,
        ul: ({ children }) => (
          <ul className="my-4 list-disc pl-6 space-y-2 text-[15px] leading-8 text-foreground/90">
            {children}
          </ul>
        ),
        ol: ({ children }) => (
          <ol className="my-4 list-decimal pl-6 space-y-2 text-[15px] leading-8 text-foreground/90">
            {children}
          </ol>
        ),
        li: ({ children }) => <li className="pl-1">{children}</li>,
        code: ({ children, className }) => {
          const isBlock = Boolean(className)
          const code = String(children).replace(/\n$/, "")

          if (isBlock) {
            if (className === "language-math-block") {
              const formattedMath = formatMathText(code)
              return (
                <div className="my-5 overflow-x-auto rounded-2xl border border-current/15 bg-muted/30 px-6 py-5 text-center font-mono text-[1.05em] leading-relaxed shadow-sm text-foreground/90 whitespace-nowrap scrollbar-thin">
                  {formattedMath}
                </div>
              )
            }
            return <CopyableCodeBlock code={code} />
          }

          if (code.startsWith("math-inline:")) {
            const mathText = code.slice("math-inline:".length)
            const formattedMath = formatMathText(mathText)
            return (
              <code className="mx-0.5 inline-flex items-center rounded-md border border-current/15 bg-muted/45 px-1.5 py-0.5 font-mono text-[0.92em] text-foreground font-semibold shadow-sm">
                {formattedMath}
              </code>
            )
          }

          return (
            <code className="rounded-md bg-muted/45 px-1.5 py-0.5 font-mono text-[0.9em] text-foreground border border-current/10">
              {children}
            </code>
          )
        },
        pre: ({ children }) => <>{children}</>,
        table: ({ children }) => (
          <div className="my-5 overflow-x-auto rounded-xl border border-current/15 shadow-sm scrollbar-thin">
            <table className="w-full min-w-max border-collapse text-left text-sm">{children}</table>
          </div>
        ),
        thead: ({ children }) => <thead className="bg-muted/40 border-b border-current/15">{children}</thead>,
        th: ({ children }) => (
          <th className="px-4 py-3 font-semibold text-foreground">
            {children}
          </th>
        ),
        td: ({ children }) => (
          <td className="border-b border-current/10 px-4 py-3 align-top text-foreground/90">
            {children}
          </td>
        ),
        a: ({ children, href }) => (
          <a
            className="font-medium underline underline-offset-4 text-primary hover:text-primary/80 transition-colors"
            href={href}
            rel="noreferrer"
            target="_blank"
          >
            {children}
          </a>
        ),
      }}
    >
      {processedContent}
    </ReactMarkdown>
  )
}
