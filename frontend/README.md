# Xendris AI Frontend

This frontend has been reset to a neutral Next.js baseline for Xendris AI.

Current state:

```txt
frontend_status: CLEAN_RESET_COMPLETED
xendris_placeholder: PRESENT
xendris_experimental_route: /x
```

The first experimental `/x` interface contains local placeholder intent routing only.

Integrations, authentication, billing, Canvas, upload flows, dashboards, memory, databases, streaming, and business logic have not been implemented yet.

## Model Provider Configuration

Xendris uses a provider abstraction for model calls. The default provider is `mock`, so the app runs without external credentials.

```bash
XENDRIS_MODEL_PROVIDER=mock
```

Reserved provider values:

```bash
XENDRIS_MODEL_PROVIDER=mock
XENDRIS_MODEL_PROVIDER=deepseek
```

DeepSeek configuration:

```bash
DEEPSEEK_API_KEY=...
DEEPSEEK_MODEL=deepseek-v4-flash
```

Defaults:

```txt
XENDRIS_MODEL_PROVIDER defaults to mock.
DEEPSEEK_MODEL defaults to deepseek-v4-flash.
```

If `XENDRIS_MODEL_PROVIDER=deepseek` is set without `DEEPSEEK_API_KEY`, `/api/chat` returns a controlled JSON error instead of crashing the app.

The DeepSeek provider uses `fetch` against the OpenAI-compatible chat completions endpoint. No SDK dependency is installed.

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the placeholder.

Open [http://localhost:3000/x](http://localhost:3000/x) to test the first local Xendris intent-routing scaffold.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.
