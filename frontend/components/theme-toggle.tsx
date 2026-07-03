"use client"

import * as React from "react"
import { MoonIcon, SunIcon } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "src/components/ui/button"
import { cn } from "src/lib/utils"

export function ThemeToggle({ className }: { className?: string }) {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = React.useState(false)

  React.useEffect(() => {
    setMounted(true)
  }, [])

  const activeTheme = mounted ? theme : "light"

  return (
    <div
      className={cn(
        "inline-flex items-center gap-1 rounded-xl border bg-background p-1 shadow-sm",
        className
      )}
      aria-label="Selector de tema"
    >
      <Button
        type="button"
        variant={activeTheme === "light" ? "secondary" : "ghost"}
        size="sm"
        onClick={() => setTheme("light")}
        aria-pressed={activeTheme === "light"}
      >
        <SunIcon data-icon="inline-start" />
        Claro
      </Button>
      <Button
        type="button"
        variant={activeTheme === "dark" ? "secondary" : "ghost"}
        size="sm"
        onClick={() => setTheme("dark")}
        aria-pressed={activeTheme === "dark"}
      >
        <MoonIcon data-icon="inline-start" />
        Oscuro
      </Button>
    </div>
  )
}
