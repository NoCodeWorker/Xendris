# PATCH para Codex — usar preset shadcn correcto

En el desarrollo del dashboard fullstack de Phygn, corrige la inicialización de shadcn/ui.

## Comando obligatorio

Dentro de la carpeta `frontend/`, ejecutar:

```bash
npx shadcn@latest init --preset b4gMUX5Dk --template next
```

## No usar

No uses inicialización genérica:

```bash
npx shadcn@latest init
```

El preset elegido por el usuario es:

```txt
b4gMUX5Dk
```

## Flujo correcto

Desde:

```txt
d:\BIOCULTOR\PHYNG\
```

ejecuta:

```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir false
cd frontend
npx shadcn@latest init --preset b4gMUX5Dk --template next
npx shadcn@latest add button card badge input label select textarea tabs separator sheet dialog tooltip table scroll-area sonner alert form switch
npm install @tanstack/react-query recharts lucide-react katex react-katex zod react-hook-form @hookform/resolvers next-themes
```

## Prioridad

1. Mantén backend y tests existentes.
2. Inicializa frontend con preset `b4gMUX5Dk`.
3. Añade componentes shadcn.
4. Implementa dashboard Phygn.
5. Añade utilidades CSS Phygn solo si no rompen el preset.

## Validación

Al terminar:

```bash
cd frontend
npm run dev
```

Debe cargar:

```txt
Dashboard
Signature
Scale
Trace
Gain
Claims
Case Studies
Physicists
Docs
```
