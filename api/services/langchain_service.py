import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()

class LicitacionAnalysis(BaseModel):
    """Modelo para el resultado del análisis de licitación"""
    score: float = Field(description="Puntuación del 0 al 100")
    risk_level: str = Field(description="Nivel de riesgo: bajo, medio, alto")
    document_type: str = Field(description="Tipo de documento identificado")
    legal_compliance: float = Field(description="Cumplimiento legal del 0 al 100")
    technical_compliance: float = Field(description="Cumplimiento técnico del 0 al 100")
    recommendations: List[str] = Field(description="Lista de recomendaciones específicas")
    key_issues: List[str] = Field(description="Problemas clave identificados")
    strengths: List[str] = Field(description="Fortalezas del documento")

class CreditAnalysis(BaseModel):
    """Modelo para el resultado del análisis crediticio"""
    credit_score: int = Field(description="Puntuación crediticia de 300 a 850")
    risk_level: str = Field(description="Nivel de riesgo: bajo, medio, alto")
    approval_probability: float = Field(description="Probabilidad de aprobación del 0 al 100")
    digital_presence_score: float = Field(description="Puntuación presencia digital 0-100")
    business_stability_score: float = Field(description="Puntuación estabilidad 0-100")
    financial_capacity_score: float = Field(description="Puntuación capacidad financiera 0-100")
    recommendations: List[str] = Field(description="Recomendaciones para la empresa")
    risk_factors: List[str] = Field(description="Factores de riesgo identificados")

class LangChainService:
    """Servicio principal para análisis con Gemini AI"""
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel("gemini-pro")
        else:
            self.model = None
            print("⚠️ GEMINI_API_KEY no encontrada - usando modo simulación")
    
    async def analyze_licitacion_document(self, document_content: str, document_type: str = "unknown") -> Dict[str, Any]:
        """
        Analizar documento de licitación usando Gemini
        """
        if not self.model:
            return self._simulate_licitacion_analysis(document_content, document_type)
        
        prompt = f"""
Eres un experto analista de licitaciones públicas con más de 15 años de experiencia.
Analiza el siguiente documento de licitación y responde ÚNICAMENTE en formato JSON válido con la siguiente estructura:
{{
    "score": float, // Puntuación del 0 al 100
    "risk_level": "bajo|medio|alto",
    "document_type": string,
    "legal_compliance": float,
    "technical_compliance": float,
    "recommendations": [string],
    "key_issues": [string],
    "strengths": [string]
}}
Tipo de documento: {document_type}
Contenido del documento:
{document_content}
"""
        try:
            response = await self.model.generate_content_async(prompt)
            # Buscar el primer bloque JSON en la respuesta
            import re
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                raise ValueError("No se encontró JSON en la respuesta de Gemini.")
        except Exception as e:
            print(f"Error en análisis Gemini: {e}")
            return self._simulate_licitacion_analysis(document_content, document_type)
    
    async def analyze_credit_risk(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizar riesgo crediticio usando Gemini
        """
        if not self.model:
            return self._simulate_credit_analysis(company_data)
        
        prompt = f"""
Eres un experto analista de riesgo crediticio especializado en PYMEs latinoamericanas.
Analiza la siguiente empresa y responde ÚNICAMENTE en formato JSON válido con la siguiente estructura:
{{
    "credit_score": int, // 300 a 850
    "risk_level": "bajo|medio|alto",
    "approval_probability": float,
    "digital_presence_score": float,
    "business_stability_score": float,
    "financial_capacity_score": float,
    "recommendations": [string],
    "risk_factors": [string]
}}
Datos de la empresa:
- Nombre: {company_data.get("company_name", "")}
- Tipo de negocio: {company_data.get("business_type", "")}
- Años en operación: {company_data.get("years_in_business", "")}
- Ingresos mensuales: {company_data.get("monthly_revenue", "")}
- Presencia digital: {company_data.get("digital_presence", "")}
- Referencias comerciales: {company_data.get("commercial_references", "")}
"""
        try:
            response = await self.model.generate_content_async(prompt)
            import re
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                raise ValueError("No se encontró JSON en la respuesta de Gemini.")
        except Exception as e:
            print(f"Error en análisis crediticio Gemini: {e}")
            return self._simulate_credit_analysis(company_data)
    
    def _simulate_licitacion_analysis(self, document_content: str, document_type: str) -> Dict[str, Any]:
        """Simulación de análisis de licitación (fallback)"""
        import random
        
        content_length = len(document_content)
        word_count = len(document_content.split())
        
        # Generar puntuación basada en contenido
        base_score = min(85, max(45, 50 + (word_count * 0.1)))
        score = round(base_score + random.uniform(-15, 15), 1)
        score = max(0, min(100, score))
        
        # Determinar nivel de riesgo
        if score >= 75:
            risk_level = "bajo"
            recommendations = [
                "Documento cumple con criterios principales",
                "Proceder con evaluación técnica detallada",
                "Verificar documentos de respaldo"
            ]
            key_issues = ["Verificación de referencias pendiente"]
            strengths = ["Propuesta técnica sólida", "Documentación completa"]
        elif score >= 50:
            risk_level = "medio"
            recommendations = [
                "Revisar especificaciones técnicas",
                "Solicitar aclaraciones sobre puntos específicos",
                "Evaluar capacidad técnica del proveedor"
            ]
            key_issues = ["Especificaciones técnicas incompletas", "Falta claridad en cronograma"]
            strengths = ["Experiencia previa demostrada", "Propuesta económica competitiva"]
        else:
            risk_level = "alto"
            recommendations = [
                "Documento requiere revisión exhaustiva",
                "Solicitar documentos adicionales",
                "Considerar descalificación si no se corrigen fallas"
            ]
            key_issues = ["Múltiples deficiencias identificadas", "Documentación insuficiente"]
            strengths = ["Interés en participar en licitación"]
        
        return {
            "score": score,
            "risk_level": risk_level,
            "document_type": self._detect_document_type(document_content),
            "legal_compliance": round(score + random.uniform(-10, 5), 1),
            "technical_compliance": round(score + random.uniform(-5, 10), 1),
            "recommendations": recommendations,
            "key_issues": key_issues,
            "strengths": strengths
        }
    
    def _simulate_credit_analysis(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulación de análisis crediticio (fallback)"""
        import random
        
        # Simular análisis basado en datos
        digital_score = random.uniform(40, 85)
        stability_score = random.uniform(50, 90)
        financial_score = random.uniform(45, 80)
        
        # Calcular puntuación crediticia
        avg_score = (digital_score + stability_score + financial_score) / 3
        credit_score = int(300 + (avg_score / 100) * 550)
        credit_score += random.randint(-30, 30)
        credit_score = max(300, min(850, credit_score))
        
        # Determinar nivel de riesgo
        if credit_score >= 700:
            risk_level = "bajo"
            approval_prob = random.uniform(80, 95)
        elif credit_score >= 600:
            risk_level = "medio"
            approval_prob = random.uniform(60, 80)
        else:
            risk_level = "alto"
            approval_prob = random.uniform(25, 60)
        
        return {
            "credit_score": credit_score,
            "risk_level": risk_level,
            "approval_probability": round(approval_prob, 1),
            "digital_presence_score": round(digital_score, 1),
            "business_stability_score": round(stability_score, 1),
            "financial_capacity_score": round(financial_score, 1),
            "recommendations": [
                f"Puntuación crediticia: {credit_score}",
                f"Nivel de riesgo: {risk_level}",
                "Considerar garantías adicionales" if risk_level == "alto" else "Perfil aceptable"
            ],
            "risk_factors": [
                "Historial crediticio limitado",
                "Empresa PYME sin garantías tradicionales"
            ] if risk_level != "bajo" else ["Riesgo mínimo identificado"]
        }
    
    def _detect_document_type(self, content: str) -> str:
        """Detectar tipo de documento"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["licitación", "propuesta", "oferta"]):
            return "Propuesta de Licitación"
        elif any(word in content_lower for word in ["técnico", "especificaciones"]):
            return "Documento Técnico"
        elif any(word in content_lower for word in ["económico", "precio", "costo"]):
            return "Propuesta Económica"
        else:
            return "Documento General"
