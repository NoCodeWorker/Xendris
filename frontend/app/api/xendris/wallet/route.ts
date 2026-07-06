import { NextResponse } from "next/server"

const RUNTIME_API_URL = process.env.XENDRIS_RUNTIME_API_URL || "http://localhost:8001"

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const tenantId = searchParams.get("tenant_id")
  const limit = searchParams.get("limit")
  const path = searchParams.get("path") || "balance"

  if (!tenantId) {
    return NextResponse.json({ error: "tenant_id query parameter required" }, { status: 400 })
  }

  try {
    let url: string
    if (path === "history") {
      url = `${RUNTIME_API_URL}/v1/wallet/history?tenant_id=${encodeURIComponent(tenantId)}${limit ? `&limit=${limit}` : ""}`
    } else {
      url = `${RUNTIME_API_URL}/v1/wallet/balance?tenant_id=${encodeURIComponent(tenantId)}`
    }

    const res = await fetch(url)
    if (!res.ok) {
      return NextResponse.json({ error: "Wallet API error", status: res.status }, { status: res.status })
    }
    const data = await res.json()
    return NextResponse.json(data)
  } catch {
    return NextResponse.json(
      { error: `Cannot reach Xendris Runtime API at ${RUNTIME_API_URL}` },
      { status: 502 },
    )
  }
}