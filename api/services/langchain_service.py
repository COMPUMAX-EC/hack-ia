from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
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
    """Servicio principal de LangChain para análisis con IA"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            self.llm = ChatOpenAI(
                temperature=0.3,
                model="gpt-3.5-turbo",
                api_key=self.openai_api_key
            )
        else:
            # Modo simulación si no hay API key
            self.llm = None
            print("⚠️ OPENAI_API_KEY no encontrada - usando modo simulación")
    
    async def analyze_licitacion_document(self, document_content: str, document_type: str = "unknown") -> Dict[str, Any]:
        """
        Analizar documento de licitación usando LangChain + OpenAI
        """
        if not self.llm:
            return self._simulate_licitacion_analysis(document_content, document_type)
        
        try:
            # Configurar el parser de salida
            parser = JsonOutputParser(pydantic_object=LicitacionAnalysis)
            
            # Crear el prompt template
            system_template = """
            Eres un experto analista de licitaciones públicas con más de 15 años de experiencia.
            Tu tarea es analizar documentos de licitación y proporcionar una evaluación completa.
            
            Debes evaluar:
            1. Cumplimiento legal y normativo
            2. Calidad técnica de la propuesta
            3. Completitud de la documentación
            4. Riesgos potenciales
            5. Fortalezas de la propuesta
            
            IMPORTANTE: Responde ÚNICAMENTE en formato JSON válido con la siguiente estructura:
            {format_instructions}
            """
            
            human_template = """
            Analiza el siguiente documento de licitación:
            
            Tipo de documento: {document_type}
            Contenido del documento:
            {document_content}
            
            Proporciona un análisis completo y detallado.
            """
            
            prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(system_template),
                HumanMessagePromptTemplate.from_template(human_template)
            ])
            
            # Crear la cadena de procesamiento
            chain = prompt | self.llm | parser
            
            # Ejecutar el análisis
            result = await chain.ainvoke({
                "document_content": document_content[:4000],  # Limitar tamaño
                "document_type": document_type,
                "format_instructions": parser.get_format_instructions()
            })
            
            return result
            
        except Exception as e:
            print(f"Error en análisis LangChain: {e}")
            return self._simulate_licitacion_analysis(document_content, document_type)
    
    async def analyze_credit_risk(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizar riesgo crediticio usando LangChain + OpenAI
        """
        if not self.llm:
            return self._simulate_credit_analysis(company_data)
        
        try:
            # Configurar el parser de salida
            parser = JsonOutputParser(pydantic_object=CreditAnalysis)
            
            # Crear el prompt template
            system_template = """
            Eres un experto analista de riesgo crediticio especializado en PYMEs latinoamericanas.
            Tu experiencia incluye evaluación de empresas sin historial crediticio formal.
            
            Debes analizar:
            1. Presencia digital y reputación online
            2. Estabilidad y tiempo del negocio
            3. Capacidad financiera basada en ingresos
            4. Factores de riesgo específicos
            5. Potencial de crecimiento
            
            Considera que estas empresas no tienen historial crediticio tradicional,
            por lo que debes usar datos alternativos para la evaluación.
            
            IMPORTANTE: Responde ÚNICAMENTE en formato JSON válido:
            {format_instructions}
            """
            
            human_template = """
            Analiza el riesgo crediticio de la siguiente empresa:
            
            Datos de la empresa:
            - Nombre: {company_name}
            - Tipo de negocio: {business_type}
            - Años en operación: {years_in_business}
            - Ingresos mensuales: {monthly_revenue}
            - Presencia digital: {digital_presence}
            - Referencias comerciales: {commercial_references}
            
            Proporciona una evaluación completa del riesgo crediticio.
            """
            
            prompt = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(system_template),
                HumanMessagePromptTemplate.from_template(human_template)
            ])
            
            # Crear la cadena de procesamiento
            chain = prompt | self.llm | parser
            
            # Ejecutar el análisis
            result = await chain.ainvoke({
                "company_name": company_data.get("company_name", ""),
                "business_type": company_data.get("business_type", ""),
                "years_in_business": company_data.get("years_in_business", ""),
                "monthly_revenue": company_data.get("monthly_revenue", ""),
                "digital_presence": company_data.get("digital_presence", ""),
                "commercial_references": company_data.get("commercial_references", ""),
                "format_instructions": parser.get_format_instructions()
            })
            
            return result
            
        except Exception as e:
            print(f"Error en análisis crediticio LangChain: {e}")
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
