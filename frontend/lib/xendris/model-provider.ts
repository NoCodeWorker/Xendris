import { deepseekProvider } from "src/lib/xendris/providers/deepseek-provider"
import { mockProvider, mockStreamingProvider } from "src/lib/xendris/providers/mock-provider"
import {
  XendrisProviderError,
  type XendrisModelProvider,
  type XendrisProviderName,
  type XendrisStreamingModelProvider,
} from "src/lib/xendris/providers/types"

const DEFAULT_PROVIDER: XendrisProviderName = "mock"

export function selectModelProvider(providerName: string | null | undefined): XendrisModelProvider {
  const normalized = normalizeProviderName(providerName)

  switch (normalized) {
    case "mock":
      return mockProvider
    case "deepseek":
      return deepseekProvider
    default:
      return mockProvider
  }
}

export function selectStreamingModelProvider(
  providerName: string | null | undefined
): XendrisStreamingModelProvider {
  const normalized = normalizeProviderName(providerName)

  switch (normalized) {
    case "mock":
      return mockStreamingProvider
    case "deepseek":
      throw new XendrisProviderError(
        "DeepSeek streaming is not supported in this local build yet.",
        "deepseek",
        501
      )
    default:
      return mockStreamingProvider
  }
}

export function normalizeProviderName(providerName: string | null | undefined): XendrisProviderName {
  if (providerName === "deepseek") return "deepseek"
  if (providerName === "mock") return "mock"
  return DEFAULT_PROVIDER
}
