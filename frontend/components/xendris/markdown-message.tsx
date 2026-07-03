"use client"

import * as React from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

type MarkdownMessageProps = {
  content: string
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
    <div className="my-4 overflow-hidden rounded-xl bg-zinc-950 shadow-sm">
      <div className="flex items-center justify-between border-b border-white/10 px-3 py-2">
        <span className="text-xs text-zinc-400">code</span>
        <button
          type="button"
          onClick={handleCopy}
          className="rounded-md px-2 py-1 text-xs text-zinc-300 transition-colors hover:bg-white/10 hover:text-white"
        >
          {copyState === "copied" ? "Copiado" : copyState === "failed" ? "No copiado" : "Copiar"}
        </button>
      </div>
      <pre className="overflow-x-auto">
        <code className="block whitespace-pre p-4 font-mono text-sm text-zinc-100">{code}</code>
      </pre>
    </div>
  )
}

export function MarkdownMessage({ content }: MarkdownMessageProps) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        h1: ({ children }) => (
          <h1 className="mb-3 mt-1 text-2xl font-semibold tracking-tight">{children}</h1>
        ),
        h2: ({ children }) => (
          <h2 className="mb-3 mt-5 text-xl font-semibold tracking-tight first:mt-1">
            {children}
          </h2>
        ),
        h3: ({ children }) => (
          <h3 className="mb-2 mt-4 text-base font-semibold tracking-tight first:mt-1">
            {children}
          </h3>
        ),
        p: ({ children }) => <p className="my-3 first:mt-0 last:mb-0">{children}</p>,
        strong: ({ children }) => <strong className="font-semibold text-foreground">{children}</strong>,
        em: ({ children }) => <em className="italic">{children}</em>,
        ul: ({ children }) => <ul className="my-3 list-disc space-y-1 pl-5">{children}</ul>,
        ol: ({ children }) => <ol className="my-3 list-decimal space-y-1 pl-5">{children}</ol>,
        li: ({ children }) => <li className="pl-1">{children}</li>,
        code: ({ children, className }) => {
          const isBlock = Boolean(className)
          const code = String(children).replace(/\n$/, "")

          if (isBlock) {
            return <CopyableCodeBlock code={code} />
          }

          return (
            <code className="rounded-md bg-muted px-1.5 py-0.5 font-mono text-[0.9em] text-foreground">
              {children}
            </code>
          )
        },
        pre: ({ children }) => <>{children}</>,
        table: ({ children }) => (
          <div className="my-4 overflow-x-auto rounded-xl border">
            <table className="w-full min-w-max border-collapse text-left text-sm">{children}</table>
          </div>
        ),
        thead: ({ children }) => <thead className="bg-muted/70">{children}</thead>,
        th: ({ children }) => (
          <th className="border-b px-3 py-2 font-semibold text-foreground">{children}</th>
        ),
        td: ({ children }) => <td className="border-b px-3 py-2 align-top">{children}</td>,
        a: ({ children, href }) => (
          <a
            className="font-medium underline underline-offset-4"
            href={href}
            rel="noreferrer"
            target="_blank"
          >
            {children}
          </a>
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  )
}
