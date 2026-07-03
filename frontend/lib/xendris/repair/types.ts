export type RepairResult = {
  repaired: boolean
  originalContent: string
  finalContent: string
  repairReason?: string
  repairStrategy?: string
}

export type XendrisRepairMetadata = {
  repaired: boolean
  repairReason?: string
  repairStrategy?: string
}
