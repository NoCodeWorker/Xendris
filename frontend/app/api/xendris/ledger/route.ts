import { NextResponse } from "next/server"

const RUNTIME_API_URL = process.env.XENDRIS_RUNTIME_API_URL || "http://localhost:8001"

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const runId = searchParams.get("run_id")

  if (!runId) {
    return NextResponse.json({ error: "run_id query parameter required" }, { status: 400 })
  }

  try {
    const res = await fetch(`${RUNTIME_API_URL}/v1/ledger/${runId}`)
    if (!res.ok) {
      return NextResponse.json({ error: "Ledger not found", run_id: runId }, { status: 404 })
    }
    const data = await res.json()
    return NextResponse.json(data)
  } catch {
    return NextResponse.json(
      { error: `Cannot reach Xendris Runtime API at ${RUNTIME_API_URL}`, run_id: runId },
      { status: 502 },
    )
  }
}