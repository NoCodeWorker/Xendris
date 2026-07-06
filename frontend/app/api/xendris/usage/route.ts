import { NextResponse } from "next/server"

const RUNTIME_API_URL = process.env.XENDRIS_RUNTIME_API_URL || "http://localhost:8001"

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const tenantId = searchParams.get("tenant_id")
  const startDate = searchParams.get("start_date")
  const endDate = searchParams.get("end_date")

  if (!tenantId) {
    return NextResponse.json({ error: "tenant_id query parameter required" }, { status: 400 })
  }

  try {
    let url = `${RUNTIME_API_URL}/v1/usage?tenant_id=${encodeURIComponent(tenantId)}`
    if (startDate) url += `&start_date=${encodeURIComponent(startDate)}`
    if (endDate) url += `&end_date=${encodeURIComponent(endDate)}`

    const res = await fetch(url)
    if (!res.ok) {
      return NextResponse.json({ error: "Usage API error", status: res.status }, { status: res.status })
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