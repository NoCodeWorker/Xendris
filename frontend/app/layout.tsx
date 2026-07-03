import type { Metadata } from "next"
import "./globals.css"
import { Inter } from "next/font/google";
import { ThemeProvider } from "src/components/theme-provider";
import { cn } from "src/lib/utils";

const inter = Inter({subsets:['latin'],variable:'--font-sans'});

export const metadata: Metadata = {
  title: "Xendris AI",
  description: "Foco, evidencia y siguiente acción segura para proyectos creados con IA.",
  openGraph: {
    title: "Xendris AI",
    description: "Foco, evidencia y siguiente acción segura para proyectos creados con IA.",
    type: "website",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html
      lang="es"
      className={cn("antialiased", "font-sans", inter.variable)}
      suppressHydrationWarning
    >
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  )
}
