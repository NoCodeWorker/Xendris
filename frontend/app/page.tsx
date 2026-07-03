import { ThemeToggle } from "src/components/theme-toggle"

export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-6 py-16 text-foreground">
      <div className="fixed right-6 top-6">
        <ThemeToggle />
      </div>
      <section className="w-full max-w-2xl">
        <p className="mb-4 text-sm font-medium uppercase tracking-[0.16em] text-muted-foreground">
          MVP frontend reset completed.
        </p>
        <h1 className="text-5xl font-semibold tracking-tight sm:text-6xl">Xendris AI</h1>
        <p className="mt-6 max-w-xl text-lg leading-8 text-muted-foreground">
          Foco, evidencia y siguiente acción segura para proyectos creados con IA.
        </p>
        <a
          href="/x"
          className="mt-8 inline-flex h-10 items-center justify-center rounded-lg bg-primary px-4 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/85"
        >
          Abrir interfaz experimental
        </a>
      </section>
    </main>
  )
}
