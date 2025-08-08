"""
SERVICIO GEMINI PARA ANÁLISIS DE LICITACIONES
Integración con Google Gemini API para análisis inteligente de documentos de compras públicas
"""

import google.generativeai as genai
import os
import json
import asyncio
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import time
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class GeminiLicitacionesService:
    """
    Servicio especializado en análisis de licitaciones usando Google Gemini
    """
    
    def __init__(self):
        # Configurar API Key
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.logger = logging.getLogger("GeminiLicitaciones")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.use_simulation = False
            self.logger.info("✅ Gemini API configurada correctamente")
        else:
            self.model = None
            self.use_simulation = True
            self.logger.warning("⚠️ GEMINI_API_KEY no encontrada - usando modo simulación")
    
    async def analizar_documento_licitacion(
        self, 
        document_content: str, 
        document_type: str = "Documento de Licitación"
    ) -> Dict[str, Any]:
        """
        Análisis completo de documento de licitación con Gemini
        """
        if self.use_simulation:
            return self._simulate_analysis(document_content, document_type)
        
        try:
            prompt = self._build_licitacion_prompt(document_content, document_type)
            
            # Generar respuesta con Gemini
            response = self.model.generate_content(prompt)
            
            # Procesar respuesta
            analysis_result = self._parse_gemini_response(response.text)
            
            # Enriquecer con metadata
            analysis_result.update({
                "model_used": "gemini-1.5-flash",
                "analysis_timestamp": datetime.now().isoformat(),
                "document_type": document_type,
                "content_length": len(document_content)
            })
            
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Error en análisis Gemini: {str(e)}")
            return self._simulate_analysis(document_content, document_type, error=str(e))
    
    async def evaluar_riesgo_contratista(
        self, 
        company_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluación de riesgo de contratista usando Gemini
        """
        if self.use_simulation:
            return self._simulate_risk_evaluation(company_data)
        
        try:
            prompt = self._build_risk_prompt(company_data)
            
            response = self.model.generate_content(prompt)
            risk_analysis = self._parse_risk_response(response.text)
            
            risk_analysis.update({
                "model_used": "gemini-1.5-flash",
                "evaluation_timestamp": datetime.now().isoformat(),
                "company_ruc": company_data.get("ruc", "N/A")
            })
            
            return risk_analysis
            
        except Exception as e:
            self.logger.error(f"Error en evaluación de riesgo: {str(e)}")
            return self._simulate_risk_evaluation(company_data, error=str(e))
    
    async def comparar_propuestas(
        self, 
        propuestas: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Comparación inteligente de múltiples propuestas
        """
        if self.use_simulation:
            return self._simulate_proposal_comparison(propuestas)
        
        try:
            prompt = self._build_comparison_prompt(propuestas)
            
            response = self.model.generate_content(prompt)
            comparison_result = self._parse_comparison_response(response.text)
            
            comparison_result.update({
                "model_used": "gemini-1.5-flash",
                "comparison_timestamp": datetime.now().isoformat(),
                "total_proposals": len(propuestas)
            })
            
            return comparison_result
            
        except Exception as e:
            self.logger.error(f"Error en comparación: {str(e)}")
            return self._simulate_proposal_comparison(propuestas, error=str(e))
    
    async def generar_recomendaciones_negocio(
        self, 
        licitacion_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generar recomendaciones estratégicas de negocio
        """
        if self.use_simulation:
            return self._simulate_business_recommendations(licitacion_data)
        
        try:
            prompt = self._build_business_prompt(licitacion_data)
            
            response = self.model.generate_content(prompt)
            recommendations = self._parse_business_response(response.text)
            
            recommendations.update({
                "model_used": "gemini-1.5-flash",
                "generation_timestamp": datetime.now().isoformat()
            })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generando recomendaciones: {str(e)}")
            return self._simulate_business_recommendations(licitacion_data, error=str(e))
    
    def _build_licitacion_prompt(self, content: str, doc_type: str) -> str:
        """Construir prompt especializado para análisis de licitaciones"""
        return f"""
Eres un experto analista de compras públicas ecuatorianas con 20+ años de experiencia.
Especialista en evaluación de licitaciones bajo normativa LOSNCP y reglamentos SERCOP.

CONTEXTO ESPECÍFICO ECUADOR:
- Ley Orgánica del Sistema Nacional de Contratación Pública (LOSNCP)
- Reglamento General de la LOSNCP
- Códigos CPC para clasificación
- Procedimientos: menor cuantía, cotización, licitación, contratación directa
- Causales de nulidad y vicios del consentimiento
- Portal de Compras Públicas y sistema OCDS

DOCUMENTO A ANALIZAR:
Tipo: {doc_type}
Contenido: {content[:3000]}...

ANÁLISIS REQUERIDO:
Evalúa el documento y proporciona un análisis estructurado en formato JSON con:

1. CUMPLIMIENTO_NORMATIVO (0-100):
   - Adherencia a LOSNCP
   - Completitud de requisitos
   - Coherencia con pliegos tipo

2. ANALISIS_TECNICO (0-100):
   - Especificaciones técnicas
   - Factibilidad del proyecto
   - Claridad de alcance

3. ANALISIS_ECONOMICO (0-100):
   - Presupuesto referencial
   - Desagregación de costos
   - Valor por dinero

4. RIESGOS_DETECTADOS:
   - Lista de riesgos específicos
   - Nivel de impacto (Alto/Medio/Bajo)
   - Probabilidad de ocurrencia

5. OPORTUNIDADES:
   - Ventajas competitivas identificadas
   - Nichos de especialización
   - Potencial de éxito

6. RECOMENDACIONES:
   - Acciones específicas a tomar
   - Estrategias de participación
   - Mitigación de riesgos

7. SCORE_GENERAL (0-100):
   - Evaluación integral
   - Viabilidad de participación

Responde ÚNICAMENTE en formato JSON válido sin explicaciones adicionales.
"""

    def _build_risk_prompt(self, company_data: Dict[str, Any]) -> str:
        """Construir prompt para evaluación de riesgo de contratista"""
        return f"""
Eres un especialista en evaluación de riesgo crediticio y capacidad operativa de empresas contratistas en Ecuador.

DATOS DE LA EMPRESA:
{json.dumps(company_data, indent=2, ensure_ascii=False)}

EVALUACIÓN REQUERIDA:
Analiza la empresa y proporciona evaluación de riesgo en formato JSON:

1. RIESGO_FINANCIERO (0-100):
   - Solvencia económica
   - Flujo de caja proyectado
   - Capacidad de financiamiento

2. RIESGO_OPERATIVO (0-100):
   - Experiencia en el sector
   - Capacidad técnica
   - Recursos humanos

3. RIESGO_LEGAL (0-100):
   - Cumplimiento tributario
   - Obligaciones laborales
   - Antecedentes contractuales

4. FACTORES_POSITIVOS:
   - Fortalezas identificadas
   - Ventajas competitivas

5. FACTORES_NEGATIVOS:
   - Debilidades detectadas
   - Riesgos específicos

6. RECOMENDACION:
   - "APROBAR", "APROBAR_CON_CONDICIONES", "RECHAZAR"

7. SCORE_RIESGO (0-100):
   - 0-30: Alto riesgo
   - 31-70: Riesgo medio
   - 71-100: Bajo riesgo

Responde ÚNICAMENTE en formato JSON válido.
"""

    def _build_comparison_prompt(self, propuestas: List[Dict[str, Any]]) -> str:
        """Construir prompt para comparación de propuestas"""
        propuestas_text = json.dumps(propuestas, indent=2, ensure_ascii=False)
        
        return f"""
Eres un evaluador experto en procesos de contratación pública ecuatoriana.

PROPUESTAS A COMPARAR:
{propuestas_text}

COMPARACIÓN REQUERIDA:
Analiza y compara las propuestas en formato JSON:

1. RANKING:
   - Ordenar propuestas por puntaje total
   - Incluir justificación del ranking

2. ANALISIS_COMPARATIVO:
   - Fortalezas de cada propuesta
   - Debilidades identificadas
   - Diferencias clave

3. CRITERIOS_EVALUACION:
   - Técnico (40%)
   - Económico (35%)
   - Legal (15%)
   - Experiencia (10%)

4. RECOMENDACION_ADJUDICACION:
   - Propuesta recomendada
   - Justificación técnica
   - Riesgos de la decisión

5. ALERTAS:
   - Inconsistencias detectadas
   - Posibles irregularidades
   - Recomendaciones especiales

Responde ÚNICAMENTE en formato JSON válido.
"""

    def _build_business_prompt(self, licitacion_data: Dict[str, Any]) -> str:
        """Construir prompt para recomendaciones de negocio"""
        return f"""
Eres un consultor estratégico especializado en oportunidades de negocio en contratación pública.

DATOS DE LA LICITACIÓN:
{json.dumps(licitacion_data, indent=2, ensure_ascii=False)}

RECOMENDACIONES ESTRATÉGICAS:
Genera recomendaciones de negocio en formato JSON:

1. VIABILIDAD_PARTICIPACION:
   - Probabilidad de éxito (0-100)
   - Justificación de la evaluación

2. ESTRATEGIA_PARTICIPACION:
   - Enfoque recomendado
   - Diferenciadores clave
   - Propuesta de valor

3. ALIANZAS_SUGERIDAS:
   - Tipo de socios necesarios
   - Capacidades complementarias

4. INVERSIONES_REQUERIDAS:
   - Capital necesario
   - Recursos técnicos
   - Personal especializado

5. RIESGOS_NEGOCIO:
   - Riesgos de mercado
   - Riesgos operativos
   - Mitigaciones sugeridas

6. OPORTUNIDADES_FUTURAS:
   - Contratos relacionados
   - Mercados expandibles
   - Crecimiento potencial

Responde ÚNICAMENTE en formato JSON válido.
"""

    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parsear respuesta de Gemini para análisis de licitación"""
        try:
            # Limpiar respuesta (remover markdown si existe)
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            result = json.loads(cleaned_response.strip())
            
            # Validar estructura mínima
            required_fields = ["CUMPLIMIENTO_NORMATIVO", "ANALISIS_TECNICO", "SCORE_GENERAL"]
            for field in required_fields:
                if field not in result:
                    result[field] = 75  # Valor por defecto
            
            return result
            
        except json.JSONDecodeError as e:
            self.logger.warning(f"Error parseando JSON de Gemini: {e}")
            return self._generate_fallback_analysis(response_text)
    
    def _parse_risk_response(self, response_text: str) -> Dict[str, Any]:
        """Parsear respuesta de evaluación de riesgo"""
        try:
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            return json.loads(cleaned_response.strip())
            
        except json.JSONDecodeError:
            return {
                "RIESGO_FINANCIERO": 70,
                "RIESGO_OPERATIVO": 65,
                "RIESGO_LEGAL": 80,
                "SCORE_RIESGO": 72,
                "RECOMENDACION": "APROBAR_CON_CONDICIONES",
                "FACTORES_POSITIVOS": ["Análisis automático con Gemini"],
                "FACTORES_NEGATIVOS": ["Requiere validación manual"]
            }
    
    def _parse_comparison_response(self, response_text: str) -> Dict[str, Any]:
        """Parsear respuesta de comparación de propuestas"""
        try:
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            return json.loads(cleaned_response.strip())
            
        except json.JSONDecodeError:
            return {
                "RANKING": [{"posicion": 1, "score": 85, "justificacion": "Análisis automático"}],
                "RECOMENDACION_ADJUDICACION": "Revisar manualmente",
                "ALERTAS": ["Validar análisis automático"]
            }
    
    def _parse_business_response(self, response_text: str) -> Dict[str, Any]:
        """Parsear respuesta de recomendaciones de negocio"""
        try:
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            return json.loads(cleaned_response.strip())
            
        except json.JSONDecodeError:
            return {
                "VIABILIDAD_PARTICIPACION": 75,
                "ESTRATEGIA_PARTICIPACION": "Análisis detallado requerido",
                "RIESGOS_NEGOCIO": ["Evaluar manualmente"],
                "OPORTUNIDADES_FUTURAS": ["Potencial identificado"]
            }
    
    def _generate_fallback_analysis(self, response_text: str) -> Dict[str, Any]:
        """Generar análisis de fallback cuando JSON falla"""
        return {
            "CUMPLIMIENTO_NORMATIVO": 75,
            "ANALISIS_TECNICO": 80,
            "ANALISIS_ECONOMICO": 70,
            "SCORE_GENERAL": 75,
            "RIESGOS_DETECTADOS": ["Análisis requiere validación manual"],
            "RECOMENDACIONES": ["Revisar respuesta de IA", "Validar con experto"],
            "gemini_raw_response": response_text[:500],
            "analysis_method": "fallback_structured"
        }
    
    # MÉTODOS DE SIMULACIÓN
    def _simulate_analysis(self, content: str, doc_type: str, error: str = None) -> Dict[str, Any]:
        """Simulación de análisis de licitación"""
        # Análisis básico del contenido
        content_length = len(content)
        has_technical = any(word in content.lower() for word in ["técnico", "especificación", "norma"])
        has_economic = any(word in content.lower() for word in ["presupuesto", "costo", "precio", "valor"])
        has_legal = any(word in content.lower() for word in ["legal", "contrato", "cláusula", "condición"])
        
        # Scores basados en contenido
        cumplimiento = 85 if has_legal else 70
        tecnico = 90 if has_technical else 75
        economico = 85 if has_economic else 70
        score_general = (cumplimiento + tecnico + economico) / 3
        
        # Riesgos simulados inteligentes
        riesgos = []
        if content_length < 500:
            riesgos.append("Documento muy breve - Puede faltar información")
        if not has_technical:
            riesgos.append("Especificaciones técnicas limitadas")
        if not has_economic:
            riesgos.append("Información económica insuficiente")
        
        # Recomendaciones simuladas
        recomendaciones = [
            "Validar cumplimiento con normativa LOSNCP",
            "Revisar capacidad técnica del oferente",
            "Confirmar disponibilidad presupuestaria"
        ]
        
        if score_general > 80:
            recomendaciones.append("Oportunidad viable - Recomendar participación")
        
        return {
            "CUMPLIMIENTO_NORMATIVO": round(cumplimiento, 1),
            "ANALISIS_TECNICO": round(tecnico, 1),
            "ANALISIS_ECONOMICO": round(economico, 1),
            "SCORE_GENERAL": round(score_general, 1),
            "RIESGOS_DETECTADOS": riesgos if riesgos else ["Riesgos estándar identificados"],
            "OPORTUNIDADES": [
                "Mercado de contratación pública activo",
                "Especialización en sector identificado",
                "Potencial de contratos futuros"
            ],
            "RECOMENDACIONES": recomendaciones,
            "model_used": "gemini-simulation",
            "analysis_timestamp": datetime.now().isoformat(),
            "simulation_reason": error if error else "GEMINI_API_KEY no configurada",
            "content_stats": {
                "length": content_length,
                "has_technical": has_technical,
                "has_economic": has_economic,
                "has_legal": has_legal
            }
        }
    
    def _simulate_risk_evaluation(self, company_data: Dict[str, Any], error: str = None) -> Dict[str, Any]:
        """Simulación de evaluación de riesgo"""
        ruc = company_data.get("ruc", "")
        company_name = company_data.get("company_name", "")
        years_in_business = company_data.get("years_in_business", 0)
        
        # Scoring simulado basado en datos
        financial_risk = 70 if years_in_business > 5 else 60
        operational_risk = 75 if len(company_name) > 10 else 65
        legal_risk = 80 if len(ruc) == 13 else 70
        
        overall_score = (financial_risk + operational_risk + legal_risk) / 3
        
        recommendation = "APROBAR" if overall_score > 75 else "APROBAR_CON_CONDICIONES" if overall_score > 60 else "REVISAR"
        
        return {
            "RIESGO_FINANCIERO": round(financial_risk, 1),
            "RIESGO_OPERATIVO": round(operational_risk, 1),
            "RIESGO_LEGAL": round(legal_risk, 1),
            "SCORE_RIESGO": round(overall_score, 1),
            "RECOMENDACION": recommendation,
            "FACTORES_POSITIVOS": [
                "RUC válido identificado" if len(ruc) == 13 else "Empresa registrada",
                "Experiencia en sector" if years_in_business > 3 else "Empresa constituida"
            ],
            "FACTORES_NEGATIVOS": [
                "Requiere validación de estados financieros",
                "Verificar historial crediticio"
            ],
            "model_used": "gemini-simulation",
            "evaluation_timestamp": datetime.now().isoformat(),
            "simulation_reason": error if error else "GEMINI_API_KEY no configurada"
        }
    
    def _simulate_proposal_comparison(self, propuestas: List[Dict[str, Any]], error: str = None) -> Dict[str, Any]:
        """Simulación de comparación de propuestas"""
        if not propuestas:
            return {"error": "No hay propuestas para comparar"}
        
        # Generar ranking simulado
        ranking = []
        for i, propuesta in enumerate(propuestas):
            score = 85 - (i * 5)  # Decrecer score por posición
            ranking.append({
                "posicion": i + 1,
                "propuesta_id": propuesta.get("id", f"PROP_{i+1}"),
                "score": score,
                "justificacion": f"Propuesta {i+1} - Análisis automático"
            })
        
        return {
            "RANKING": ranking,
            "TOTAL_PROPUESTAS": len(propuestas),
            "RECOMENDACION_ADJUDICACION": ranking[0]["propuesta_id"] if ranking else "N/A",
            "CRITERIOS_EVALUACION": {
                "tecnico": 40,
                "economico": 35,
                "legal": 15,
                "experiencia": 10
            },
            "ALERTAS": [
                "Validar análisis con evaluación manual",
                "Verificar cumplimiento de requisitos mínimos"
            ],
            "model_used": "gemini-simulation",
            "comparison_timestamp": datetime.now().isoformat(),
            "simulation_reason": error if error else "GEMINI_API_KEY no configurada"
        }
    
    def _simulate_business_recommendations(self, licitacion_data: Dict[str, Any], error: str = None) -> Dict[str, Any]:
        """Simulación de recomendaciones de negocio"""
        valor_estimado = licitacion_data.get("valor_estimado", 0)
        categoria = licitacion_data.get("categoria", "")
        
        viabilidad = 80 if valor_estimado > 500000 else 70
        
        return {
            "VIABILIDAD_PARTICIPACION": viabilidad,
            "ESTRATEGIA_PARTICIPACION": f"Enfoque especializado en {categoria}" if categoria else "Análisis de mercado requerido",
            "ALIANZAS_SUGERIDAS": [
                "Socios técnicos especializados",
                "Proveedores locales confiables"
            ],
            "INVERSIONES_REQUERIDAS": {
                "capital": f"${valor_estimado * 0.1:,.0f}" if valor_estimado else "Por determinar",
                "recursos_tecnicos": "Equipo especializado",
                "personal": "Profesionales certificados"
            },
            "RIESGOS_NEGOCIO": [
                "Competencia en sector",
                "Variabilidad de demanda pública",
                "Cambios regulatorios"
            ],
            "OPORTUNIDADES_FUTURAS": [
                "Contratos similares en pipeline",
                "Expansión a otros sectores",
                "Establecimiento de capacidades"
            ],
            "model_used": "gemini-simulation",
            "generation_timestamp": datetime.now().isoformat(),
            "simulation_reason": error if error else "GEMINI_API_KEY no configurada"
        }


# FUNCIÓN DE TESTING
async def test_gemini_service():
    """Test del servicio Gemini"""
    print("🤖 TESTING SERVICIO GEMINI")
    print("=" * 50)
    
    service = GeminiLicitacionesService()
    
    # Test 1: Análisis de documento
    print("\n📄 Test 1: Análisis de documento")
    doc_content = """
    PLIEGO DE CONDICIONES
    Construcción de puente vehicular sobre río Guayas
    Presupuesto referencial: $2,500,000
    Plazo de ejecución: 18 meses
    Requisitos técnicos: Cumplimiento norma AASHTO
    Garantía de cumplimiento: 10% del valor del contrato
    """
    
    resultado = await service.analizar_documento_licitacion(doc_content, "Pliego de Condiciones")
    print(f"✅ Score general: {resultado.get('SCORE_GENERAL', 'N/A')}")
    print(f"📊 Cumplimiento normativo: {resultado.get('CUMPLIMIENTO_NORMATIVO', 'N/A')}")
    print(f"🛠️ Análisis técnico: {resultado.get('ANALISIS_TECNICO', 'N/A')}")
    
    # Test 2: Evaluación de riesgo
    print("\n🏢 Test 2: Evaluación de riesgo de contratista")
    company_data = {
        "ruc": "1791234567001",
        "company_name": "Constructora Ecuatoriana S.A.",
        "years_in_business": 8,
        "sector": "construccion"
    }
    
    riesgo = await service.evaluar_riesgo_contratista(company_data)
    print(f"✅ Score de riesgo: {riesgo.get('SCORE_RIESGO', 'N/A')}")
    print(f"💼 Recomendación: {riesgo.get('RECOMENDACION', 'N/A')}")
    
    print(f"\n🎉 Testing completado - Gemini {'funcionando' if not service.use_simulation else 'en modo simulación'}")

if __name__ == "__main__":
    asyncio.run(test_gemini_service())
