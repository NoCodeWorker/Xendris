export type EpistemicRiskLevel = "low" | "medium" | "high";

export type EpistemicEvaluation = {
  riskLevel: EpistemicRiskLevel;
  overconfidenceScore: number;
  unsupportedCertainty: boolean;
  falsePremiseRisk: boolean;
  absolutistLanguage: string[];
  missingLimitations: boolean;
  recommendedCorrection: string;
};
