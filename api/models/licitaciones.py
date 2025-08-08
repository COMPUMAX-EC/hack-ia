from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DocumentUploadRequest(BaseModel):
    """Modelo para subida de documentos de licitación"""
    document_name: str = Field(..., description="Nombre del documento")
    document_type: str = Field(..., description="Tipo de documento (PDF, DOCX, etc.)")
    file_size: int = Field(..., description="Tamaño del archivo en bytes")

class LicitacionAnalysisResult(BaseModel):
    """Resultado del análisis de licitación"""
    score: float = Field(..., ge=0, le=100, description="Puntuación general (0-100)")
    risk_level: str = Field(..., description="Nivel de riesgo: bajo, medio, alto")
    recommendations: List[str] = Field(..., description="Lista de recomendaciones")
    document_type: str = Field(..., description="Tipo de documento identificado")
    legal_compliance: float = Field(..., ge=0, le=100, description="Cumplimiento legal (%)")
    technical_compliance: float = Field(..., ge=0, le=100, description="Cumplimiento técnico (%)")
    estimated_processing_time: str = Field(..., description="Tiempo estimado de procesamiento")
    traditional_time: str = Field(..., description="Tiempo tradicional de procesamiento")
    analysis_timestamp: datetime = Field(default_factory=datetime.now)

class LicitacionAnalysisRequest(BaseModel):
    """Request para análisis de licitación"""
    document_content: str = Field(..., description="Contenido del documento a analizar")
    document_type: Optional[str] = Field("unknown", description="Tipo de documento")
    priority: Optional[str] = Field("normal", description="Prioridad del análisis")

class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    error: str = Field(..., description="Tipo de error")
    message: str = Field(..., description="Mensaje de error")
    details: Optional[str] = Field(None, description="Detalles adicionales del error")
