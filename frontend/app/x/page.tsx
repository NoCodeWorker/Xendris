import type { Metadata } from "next"
import { XendrisShell } from "src/components/xendris/xendris-shell"

export const metadata: Metadata = {
  title: "Xendris AI /x",
  description: "First experimental Xendris AI interface with local placeholder intent routing.",
}

export default function XendrisPage() {
  return <XendrisShell />
}
