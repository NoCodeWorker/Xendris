import { cn } from "src/lib/utils"
import type { XendrisMode } from "src/lib/xendris/types"

type ModeSelectorProps = {
  selected: XendrisMode
  onChange: (mode: XendrisMode) => void
}

const MODES: { value: XendrisMode; label: string; description: string }[] = [
  {
    value: "eco",
    label: "Eco",
    description: "Cheap model + local guards",
  },
  {
    value: "normal",
    label: "Normal",
    description: "Medium model + gates",
  },
  {
    value: "precision",
    label: "Precision",
    description: "Full gates + council",
  },
  {
    value: "custom",
    label: "Custom",
    description: "User-configured profile",
  },
]

export function ModeSelector({ selected, onChange }: ModeSelectorProps) {
  return (
    <div className="rounded-xl border bg-card p-3 shadow-xs">
      <p className="mb-2.5 text-xs font-semibold text-foreground">Modo cognitivo</p>
      <div className="flex flex-wrap gap-1.5">
        {MODES.map((mode) => (
          <button
            key={mode.value}
            type="button"
            onClick={() => onChange(mode.value)}
            className={cn(
              "group relative flex-1 min-w-[80px] rounded-xl border px-3 py-2 text-left transition-all",
              selected === mode.value
                ? "border-primary/30 bg-primary/5 shadow-xs"
                : "border-transparent bg-muted/30 hover:bg-muted/50 hover:border-border",
            )}
          >
            <p
              className={cn(
                "text-xs font-semibold",
                selected === mode.value ? "text-foreground" : "text-muted-foreground",
              )}
            >
              {mode.label}
            </p>
            <p className="mt-0.5 text-[10px] leading-snug text-muted-foreground/70">
              {mode.description}
            </p>
          </button>
        ))}
      </div>
    </div>
  )
}