from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class CompanyData(BaseModel):
    """Datos de la empresa para evaluación crediticia"""
    company_name: str = Field(..., description="Nombre de la empresa")
    business_type: str = Field(..., description="Tipo de negocio")
    years_in_business: str = Field(..., description="Años en el negocio")
    monthly_revenue: str = Field(..., description="Ingresos mensuales")
    digital_presence: str = Field(..., description="Presencia digital")
    commercial_references: str = Field(..., description="Referencias comerciales")
    location: Optional[str] = Field(None, description="Ubicación de la empresa")
    employee_count: Optional[int] = Field(None, description="Número de empleados")

class CreditFactors(BaseModel):
    """Factores de evaluación crediticia"""
    digital_presence: float = Field(..., ge=0, le=100, description="Puntuación presencia digital")
    commercial_reputation: float = Field(..., ge=0, le=100, description="Reputación comercial")
    business_stability: float = Field(..., ge=0, le=100, description="Estabilidad del negocio")
    financial_capacity: float = Field(..., ge=0, le=100, description="Capacidad financiera")
    growth_potential: float = Field(..., ge=0, le=100, description="Potencial de crecimiento")

class RiskAssessment(BaseModel):
    """Evaluación de riesgo crediticio"""
    credit_score: int = Field(..., ge=300, le=850, description="Puntuación crediticia")
    risk_level: str = Field(..., description="Nivel de riesgo: bajo, medio, alto")
    approval_probability: float = Field(..., ge=0, le=100, description="Probabilidad de aprobación (%)")
    recommended_amount: str = Field(..., description="Monto recomendado")
    recommendations: List[str] = Field(..., description="Recomendaciones para la empresa")
    interest_rate: float = Field(..., ge=0, description="Tasa de interés sugerida")
    factors: CreditFactors = Field(..., description="Desglose de factores de evaluación")
    assessment_timestamp: datetime = Field(default_factory=datetime.now)

class CreditAnalysisRequest(BaseModel):
    """Request para análisis crediticio"""
    company_data: CompanyData = Field(..., description="Datos de la empresa")
    requested_amount: Optional[float] = Field(None, description="Monto solicitado")
    loan_purpose: Optional[str] = Field(None, description="Propósito del préstamo")

class CreditAnalysisResponse(BaseModel):
    """Respuesta del análisis crediticio"""
    status: str = Field(..., description="Estado del análisis")
    risk_assessment: RiskAssessment = Field(..., description="Evaluación de riesgo")
    processing_time: str = Field(..., description="Tiempo de procesamiento")
    analysis_id: str = Field(..., description="ID único del análisis")
