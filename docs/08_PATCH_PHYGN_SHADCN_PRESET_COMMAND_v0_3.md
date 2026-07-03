# PATCH — Phygn shadcn preset command

## Corrección obligatoria

El frontend de Phygn debe inicializar shadcn/ui usando exactamente este comando:

```bash
npx shadcn@latest init --preset b4gMUX5Dk --template next
```

No usar:

```bash
npx shadcn@latest init
```

salvo que el preset falle y el usuario autorice una alternativa.

## Motivo

El preset `b4gMUX5Dk` contiene la configuración visual base elegida para Phygn.  
Debe respetarse como fuente principal del sistema visual.

## Regla de prioridad

Prioridad de diseño:

```txt
1. Preset b4gMUX5Dk
2. Ajustes específicos Phygn en globals.css
3. Componentes shadcn instalados después
4. Custom components Phygn
```

## Inicialización correcta

Desde:

```txt
d:\BIOCULTOR\PHYNG\
```

crear frontend:

```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir false
cd frontend
npx shadcn@latest init --preset b4gMUX5Dk --template next
```

Después instalar componentes:

```bash
npx shadcn@latest add button card badge input label select textarea tabs separator sheet dialog tooltip table scroll-area sonner alert form switch
```

Instalar dependencias adicionales:

```bash
npm install @tanstack/react-query recharts lucide-react katex react-katex zod react-hook-form @hookform/resolvers next-themes
```

## Ajustes posteriores

Tras aplicar el preset, Codex debe revisar:

```txt
frontend/app/globals.css
frontend/components.json
frontend/tailwind.config.ts
```

y añadir solamente las utilidades específicas de Phygn que no entren en conflicto:

```css
.phygn-spectrum {
  background: linear-gradient(
    90deg,
    #ef4444,
    #f97316,
    #eab308,
    #22c55e,
    #06b6d4,
    #3b82f6,
    #7c3aed
  );
}

.phygn-spectrum-text {
  background: linear-gradient(
    90deg,
    #ef4444,
    #f97316,
    #eab308,
    #22c55e,
    #06b6d4,
    #3b82f6,
    #7c3aed
  );
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.phygn-muted-grid {
  background-image:
    linear-gradient(to right, hsl(var(--border) / 0.28) 1px, transparent 1px),
    linear-gradient(to bottom, hsl(var(--border) / 0.28) 1px, transparent 1px);
  background-size: 32px 32px;
}

.phygn-formula {
  font-family: var(--font-mono);
  letter-spacing: -0.03em;
}
```

## Regla visual

No sobrescribir el preset de forma agresiva.

El preset es la base.  
Phygn añade semántica científica encima:

```txt
physical signs
epistemic traces
boundary signatures
claim validation
```
