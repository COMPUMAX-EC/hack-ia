from api.models.licitaciones import LicitacionAnalysisResult
from api.services.langchain_service import LangChainService
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random
import re

class LicitacionesService:
    def __init__(self):
        self.analysis_history = []
        self.langchain_service = LangChainService()
    
    async def analyze_document(self, content: str, document_type: str = "unknown", priority: str = "normal") -> LicitacionAnalysisResult:
        """
        Analizar documento de licitación usando LangChain + IA
        """
        # Usar LangChain para análisis avanzado
        langchain_result = await self.langchain_service.analyze_licitacion_document(
            document_content=content,
            document_type=document_type
        )
        
        # Extraer resultados de LangChain
        score = langchain_result.get("score", 75.0)
        risk_level = langchain_result.get("risk_level", "medio")
        recommendations = langchain_result.get("recommendations", ["Análisis completado"])
        detected_type = langchain_result.get("document_type", "Documento General")
        legal_compliance = langchain_result.get("legal_compliance", score)
        technical_compliance = langchain_result.get("technical_compliance", score)
        
        # Calcular métricas adicionales
        word_count = len(content.split())
        estimated_time = self._calculate_processing_time(word_count, priority)
        traditional_time = "8-12 horas"
        
        result = LicitacionAnalysisResult(
            score=score,
            risk_level=risk_level,
            recommendations=recommendations,
            document_type=detected_type,
            legal_compliance=max(0, min(100, legal_compliance)),
            technical_compliance=max(0, min(100, technical_compliance)),
            estimated_processing_time=estimated_time,
            traditional_time=traditional_time,
            analysis_timestamp=datetime.now()
        )
        
        # Guardar en historial
        self.analysis_history.append({
            "id": len(self.analysis_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "risk_level": risk_level,
            "document_type": detected_type,
            "ai_powered": True  # Indicar que se usó IA
        })
        
        return result
    
    def _detect_document_type(self, content: str) -> str:
        """Detectar tipo de documento basado en contenido"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["licitación", "propuesta", "oferta"]):
            return "Propuesta de Licitación"
        elif any(word in content_lower for word in ["técnico", "especificaciones", "tecnología"]):
            return "Documento Técnico"
        elif any(word in content_lower for word in ["económico", "precio", "costo", "financiero"]):
            return "Propuesta Económica"
        elif any(word in content_lower for word in ["legal", "jurídico", "contrato"]):
            return "Documento Legal"
        else:
            return "Documento General"
    
    def _calculate_processing_time(self, word_count: int, priority: str) -> str:
        """Calcular tiempo estimado de procesamiento"""
        base_minutes = max(2, word_count // 100)
        
        if priority == "high":
            base_minutes = int(base_minutes * 0.7)
        elif priority == "low":
            base_minutes = int(base_minutes * 1.3)
        
        if base_minutes < 60:
            return f"{base_minutes} minutos"
        else:
            hours = base_minutes // 60
            minutes = base_minutes % 60
            return f"{hours}h {minutes}m"
    
    async def process_uploaded_file(self, filename: str, content: bytes, content_type: str) -> LicitacionAnalysisResult:
        """Procesar archivo subido"""
        # Simular extracción de texto del archivo
        if content_type == "application/pdf":
            extracted_text = f"Contenido extraído del PDF: {filename}. Documento de licitación con especificaciones técnicas detalladas."
        else:
            extracted_text = f"Contenido extraído del documento: {filename}. Propuesta económica y técnica para proceso licitatorio."
        
        # Agregar más contenido simulado para análisis más realista
        extracted_text += " El presente documento contiene la propuesta integral para el proyecto solicitado, incluyendo aspectos técnicos, económicos y de implementación. Se han considerado todos los requerimientos especificados en los términos de referencia."
        
        return await self.analyze_document(extracted_text, "uploaded_document")
    
    async def get_analysis_history(self) -> List[Dict[str, Any]]:
        """Obtener historial de análisis"""
        return self.analysis_history[-10:]  # Últimos 10 análisis
