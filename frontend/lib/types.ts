export type Role = 'farmer' | 'expert' | 'official'
export type Language = 'en' | 'hi' | 'mr'
export type ThreatKind = 'disease' | 'pest'
export type RiskLevel = 'low' | 'moderate' | 'high'
export type ConfidenceLevel = 'high' | 'medium' | 'low'

export interface User {
  id: string
  name: string
  email: string
  phone?: string | null
  role: Role
  language: Language
  district?: string | null
  created_at?: string
}

export interface Crop {
  id: string
  user_id: string
  crop: string
  variety?: string | null
  growth_stage: string
  district: string
  location?: string | null
  current_risk?: { score: number; level: RiskLevel }
  created_at?: string
}

export interface MetaCrops {
  crops: string[]
  growth_stages: Record<string, string[]>
  districts: string[]
  crop_capability?: Record<string, CropCapability>
  model_crops?: string[]
}

export interface ImageQuality {
  acceptable: boolean
  score: number
  message?: string | null
}

export interface Explanation {
  available: boolean
  heatmap_url?: string | null
  message?: string | null
}

export interface RiskFactor {
  name: string
  level: string
  weight: number
  explanation: string
}

export interface RiskResult {
  score: number
  level: RiskLevel
  factors: RiskFactor[]
  explanation: string
}

export interface Recommendation {
  title: string
  immediate_actions: string[]
  monitoring: string[]
  preventive_measures: string[]
  escalation_required: boolean
  escalation_message?: string | null
}

export interface VerificationInfo {
  recommended: boolean
  status: string
}

export type CropCapability = 'ai_disease' | 'advisory_pest'

export interface ForecastDriver {
  name: string
  level: string
  weight: number
}

export interface Forecast {
  probability: number
  level: RiskLevel
  drivers: ForecastDriver[]
  explanation: string
}

export interface Prediction {
  id: string
  user_id: string
  crop_id: string
  image_url?: string | null
  crop: string
  disease: string
  confidence: number
  confidence_level: ConfidenceLevel
  district: string
  growth_stage: string
  symptoms?: string
  image_quality: ImageQuality
  explanation: Explanation
  risk: RiskResult
  recommendation: Recommendation
  verification: VerificationInfo
  forecast?: Forecast | null
  capability?: CropCapability | null
  kind?: string
  verification_status: string
  timestamp: string
  final_diagnosis?: string
}

export interface Alert {
  id: string
  user_id?: string
  district: string
  disease: string
  severity: RiskLevel
  message: string
  created_at: string
  read_status: boolean
}

export interface Hotspot {
  district: string
  disease: string
  kind?: ThreatKind
  crops?: string[]
  risk_level: RiskLevel
  risk_score: number
  report_count: number
  confirmed_count: number
  trend: string
  region?: string
  lat?: number
  lng?: number
  demo?: boolean
}

export interface DistrictThreat {
  name: string
  kind: ThreatKind
  risk_score: number
  risk_level: RiskLevel
  report_count: number
  trend: string
}

export interface DistrictRisk {
  district: string
  region: string
  lat?: number
  lng?: number
  risk_score: number
  risk_level: RiskLevel
  dominant_threat?: string
  dominant_kind?: ThreatKind
  threats: DistrictThreat[]
  crops_affected: string[]
  total_reports: number
  recommended_action: string
  outbreak_forecast?: number
  forecast_level?: RiskLevel
  demo?: boolean
}

export interface Pest {
  key: string
  pest: string
  disease: string
  crops: string[]
  checklist: string[]
  symptoms: string
}

export interface PestReportResult {
  report_id: string
  pest: string
  crop: string
  district: string
  confidence: number
  risk: RiskResult
  recommendation: Recommendation
}

export interface OfficialSummary {
  total_scans: number
  disease_scans: number
  pest_reports: number
  confirmed_cases: number
  registered_farmers: number
  active_districts: number
  high_risk_zones: number
  window_days: number
}

export interface OfficialThreat {
  name: string
  kind: ThreatKind
  districts: number
  reports: number
  max_risk: number
}

export interface OfficialRegion {
  region: string
  districts: number
  high: number
  reports: number
}

export interface OfficialDashboardData {
  summary: OfficialSummary
  districts: DistrictRisk[]
  top_threats: OfficialThreat[]
  regions: OfficialRegion[]
  note: string
}

export interface ExpertReview {
  id: string
  prediction_id: string
  expert_id: string
  expert_name: string
  original_prediction: string
  decision: 'confirm' | 'correct' | 'uncertain'
  final_diagnosis: string
  remarks?: string
  reviewed_at: string
}

export interface PendingReviewItem extends Prediction {
  field_observation?: { symptoms?: string; crop_stage?: string; location?: string } | null
  farmer?: { id: string; name: string; email: string } | null
}

export interface ExpertDashboardData {
  pending_verifications: number
  confirmed_cases: number
  hotspots: Hotspot[]
  recent_reviews: ExpertReview[]
  note: string
}
