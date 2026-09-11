from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    phone: Optional[str] = None
    role: Literal["farmer", "expert", "official"] = "farmer"
    language: Literal["en", "hi", "mr"] = "en"
    district: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


class CropCreate(BaseModel):
    crop: str
    variety: Optional[str] = None
    growth_stage: str
    district: str
    location: Optional[str] = None


class CropUpdate(BaseModel):
    crop: Optional[str] = None
    variety: Optional[str] = None
    growth_stage: Optional[str] = None
    district: Optional[str] = None
    location: Optional[str] = None


class ImageQuality(BaseModel):
    acceptable: bool
    score: float
    message: Optional[str] = None


class Explanation(BaseModel):
    available: bool
    heatmap_url: Optional[str] = None
    message: Optional[str] = None


class RiskFactor(BaseModel):
    name: str
    level: str
    weight: float
    explanation: str


class RiskResult(BaseModel):
    score: int
    level: Literal["low", "moderate", "high"]
    factors: List[RiskFactor]
    explanation: str


class Recommendation(BaseModel):
    title: str
    immediate_actions: List[str]
    monitoring: List[str]
    preventive_measures: List[str]
    escalation_required: bool
    escalation_message: Optional[str] = None


class VerificationInfo(BaseModel):
    recommended: bool
    status: str


class ForecastDriver(BaseModel):
    name: str
    level: str
    weight: float


class Forecast(BaseModel):
    probability: int
    level: Literal["low", "moderate", "high"]
    drivers: List[ForecastDriver]
    explanation: str


class PredictResponse(BaseModel):
    prediction_id: str
    crop: str
    disease: str
    confidence: float
    confidence_level: Literal["high", "medium", "low"]
    image_quality: ImageQuality
    explanation: Explanation
    risk: RiskResult
    recommendation: Recommendation
    verification: VerificationInfo
    forecast: Optional[Forecast] = None
    capability: Optional[str] = None
    image_url: Optional[str] = None
    district: Optional[str] = None
    timestamp: datetime


class VerifyRequest(BaseModel):
    prediction_id: str
    symptoms: Optional[str] = None


class ExpertReviewRequest(BaseModel):
    prediction_id: str
    decision: Literal["confirm", "correct", "uncertain"]
    final_diagnosis: Optional[str] = None
    remarks: Optional[str] = None


class AlertReadPatch(BaseModel):
    read: bool = True


class PestReportRequest(BaseModel):
    pest_key: str
    crop: str
    district: str
    observed_symptoms: List[str] = Field(default_factory=list)
    severity: Literal["low", "moderate", "high"] = "moderate"
    notes: Optional[str] = None
