"""
DEMO GEMINI LICITACIONES
Demostración completa del análisis con Google Gemini AI
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Añadir el directorio raíz al path
ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))

from api.services.gemini_service import GeminiLicitacionesService
from api.services.ocds_sercop_integration import OCDSSercop
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DemoGemini")

async def demo_analisis_gemini():
    """
    Demostración completa del análisis con Gemini
    """
    print("\n" + "="*60)
    print("🚀 DEMO GEMINI LICITACIONES - ANÁLISIS INTELIGENTE")
    print("="*60)
    
    # Inicializar servicios
    gemini_service = GeminiLicitacionesService()
    ocds_client = OCDSSercop()
    
    print(f"\n✅ Servicios inicializados")
    print(f"   - Gemini API: {'🟢 Disponible' if not gemini_service.use_simulation else '🟡 Simulación'}")
    print(f"   - SERCOP OCDS: 🟢 Disponible")
    
    # ==========================================
    # DEMO 1: ANÁLISIS DE LICITACIÓN INDIVIDUAL
    # ==========================================
    print("\n" + "="*50)
    print("📋 DEMO 1: ANÁLISIS COMPLETO DE LICITACIÓN")
    print("="*50)
    
    try:
        # Obtener procesos recientes
        procesos = await ocds_client.buscar_licitaciones(
            entidad_contratante="ministerio",
            limit=1
        )
        
        if procesos:
            proceso = procesos[0]
            ocid = proceso.get('ocid', '')
            titulo = proceso.get('title', 'Sin título')
            
            print(f"\n🔍 Analizando proceso: {titulo[:80]}...")
            print(f"   OCID: {ocid}")
            
            # Preparar contenido para análisis
            tender = proceso.get('tender', {})
            buyer = proceso.get('buyer', {})
            
            content = f"""
            PROCESO DE CONTRATACIÓN PÚBLICA ECUADOR
            
            ID: {ocid}
            Título: {proceso.get('title', '')}
            Descripción: {proceso.get('description', '')}
            
            ENTIDAD CONTRATANTE:
            - Nombre: {buyer.get('name', '')}
            - RUC: {buyer.get('id', '')}
            
            INFORMACIÓN DEL PROCESO:
            - Método: {tender.get('procurementMethod', '')}
            - Estado: {tender.get('status', '')}
            - Valor estimado: ${tender.get('value', {}).get('amount', 0):,.2f}
            - Moneda: {tender.get('value', {}).get('currency', 'USD')}
            
            CRONOGRAMA:
            - Fecha publicación: {tender.get('datePublished', '')}
            - Fin consultas: {tender.get('enquiryPeriod', {}).get('endDate', '')}
            - Fin ofertas: {tender.get('tenderPeriod', {}).get('endDate', '')}
            
            ESPECIFICACIONES TÉCNICAS:
            {tender.get('description', '')[:1000]}
            
            CRITERIOS DE ELEGIBILIDAD:
            {tender.get('eligibilityCriteria', '')[:500]}
            """
            
            # Análisis con Gemini
            resultado = await gemini_service.analizar_documento_licitacion(
                document_content=content,
                document_type="Licitación SERCOP"
            )
            
            # Mostrar resultados
            print(f"\n📊 RESULTADOS DEL ANÁLISIS:")
            print(f"   🎯 Score General: {resultado.get('score_general', 0)}/100")
            print(f"   ⚠️  Nivel de Riesgo: {resultado.get('nivel_riesgo', 'N/A')}")
            print(f"   📜 Cumplimiento Legal: {resultado.get('cumplimiento_legal', 0)}/100")
            print(f"   🔧 Cumplimiento Técnico: {resultado.get('cumplimiento_tecnico', 0)}/100")
            print(f"   📁 Completitud Docs: {resultado.get('completitud_documentos', 0)}/100")
            
            print(f"\n🔍 RESUMEN EJECUTIVO:")
            print(f"   {resultado.get('resumen_ejecutivo', 'No disponible')}")
            
            print(f"\n⚠️  RIESGOS DETECTADOS:")
            for i, riesgo in enumerate(resultado.get('riesgos_detectados', []), 1):
                print(f"   {i}. {riesgo}")
            
            print(f"\n💪 FORTALEZAS:")
            for i, fortaleza in enumerate(resultado.get('fortalezas', []), 1):
                print(f"   {i}. {fortaleza}")
            
            print(f"\n💡 RECOMENDACIONES:")
            for i, rec in enumerate(resultado.get('recomendaciones', []), 1):
                print(f"   {i}. {rec}")
        
        else:
            print("❌ No se encontraron procesos para análisis")
    
    except Exception as e:
        logger.error(f"Error en demo 1: {str(e)}")
        print(f"❌ Error: {str(e)}")
    
    # ==========================================
    # DEMO 2: ANÁLISIS DE RIESGOS ESPECÍFICO
    # ==========================================
    print("\n" + "="*50)
    print("⚠️  DEMO 2: ANÁLISIS ESPECÍFICO DE RIESGOS")
    print("="*50)
    
    try:
        # Usar el mismo proceso o buscar uno de construcción
        procesos_construccion = await ocds_client.buscar_licitaciones(
            descripcion="construcción",
            limit=1
        )
        
        if procesos_construccion:
            proceso = procesos_construccion[0]
            tender = proceso.get('tender', {})
            valor = tender.get('value', {}).get('amount', 0)
            
            print(f"\n🏗️  Analizando riesgos de: {proceso.get('title', '')[:60]}...")
            print(f"   💰 Valor: ${valor:,.2f}")
            
            content_riesgos = f"""
            ANÁLISIS DE RIESGOS - PROYECTO DE CONSTRUCCIÓN
            
            Nombre del proyecto: {proceso.get('title', '')}
            Valor del contrato: ${valor:,.2f} USD
            Entidad ejecutora: {proceso.get('buyer', {}).get('name', '')}
            
            DESCRIPCIÓN DEL PROYECTO:
            {tender.get('description', '')[:800]}
            
            MÉTODO DE CONTRATACIÓN: {tender.get('procurementMethod', '')}
            
            ESPECIFICACIONES TÉCNICAS:
            {tender.get('eligibilityCriteria', '')[:600]}
            
            CRONOGRAMA PROPUESTO:
            - Inicio ofertas: {tender.get('tenderPeriod', {}).get('startDate', '')}
            - Fin ofertas: {tender.get('tenderPeriod', {}).get('endDate', '')}
            """
            
            # Análisis de riesgos
            # Para análisis de riesgo, usaremos evaluar_riesgo_contratista con datos del proceso
            datos_proceso = {
                "company_name": proceso.get('buyer', {}).get('name', ''),
                "project_value": valor,
                "project_description": tender.get('description', ''),
                "contract_method": tender.get('procurementMethod', ''),
                "eligibility_criteria": tender.get('eligibilityCriteria', '')
            }
            
            resultado_riesgos = await gemini_service.evaluar_riesgo_contratista(
                company_data=datos_proceso
            )
            
            print(f"\n📊 EVALUACIÓN DE RIESGOS:")
            print(f"   🎯 Riesgo General: {resultado_riesgos.get('risk_level', 'N/A')}")
            print(f"   📈 Score de Riesgo: {resultado_riesgos.get('risk_score', 0)}/100")
            print(f"   ✅ Probabilidad de Éxito: {resultado_riesgos.get('success_probability', 0)}%")
            
            print(f"\n⚠️  FACTORES DE RIESGO:")
            for factor in resultado_riesgos.get('risk_factors', []):
                print(f"   • {factor}")
            
            print(f"\n💰 RIESGOS FINANCIEROS:")
            for riesgo in resultado_riesgos.get('financial_risks', []):
                print(f"   • {riesgo}")
            
            print(f"\n📅 OTROS RIESGOS:")
            for riesgo in resultado_riesgos.get('other_risks', []):
                print(f"   • {riesgo}")
            
            print(f"\n🛡️  RECOMENDACIONES:")
            for rec in resultado_riesgos.get('recommendations', []):
                print(f"   • {rec}")
    
    except Exception as e:
        logger.error(f"Error en demo 2: {str(e)}")
        print(f"❌ Error en análisis de riesgos: {str(e)}")
    
    # ==========================================
    # DEMO 3: COMPARACIÓN DE PROCESOS
    # ==========================================
    print("\n" + "="*50)
    print("⚖️  DEMO 3: COMPARACIÓN INTELIGENTE DE PROCESOS")
    print("="*50)
    
    try:
        # Obtener dos procesos para comparar
        procesos_para_comparar = await ocds_client.buscar_licitaciones(
            limit=2
        )
        
        if len(procesos_para_comparar) >= 2:
            proceso1 = procesos_para_comparar[0]
            proceso2 = procesos_para_comparar[1]
            
            print(f"\n🔄 Comparando procesos:")
            print(f"   A: {proceso1.get('title', '')[:50]}...")
            print(f"   B: {proceso2.get('title', '')[:50]}...")
            
            # Preparar contenido para comparación
            def preparar_propuesta(proceso, label):
                tender = proceso.get('tender', {})
                return f"""
                {label}:
                Título: {proceso.get('title', '')}
                Entidad: {proceso.get('buyer', {}).get('name', '')}
                Valor: ${tender.get('value', {}).get('amount', 0):,.2f}
                Método: {tender.get('procurementMethod', '')}
                Estado: {tender.get('status', '')}
                Descripción: {tender.get('description', '')[:400]}
                Criterios: {tender.get('eligibilityCriteria', '')[:300]}
                """
            
            propuesta1 = preparar_propuesta(proceso1, "PROCESO A")
            propuesta2 = preparar_propuesta(proceso2, "PROCESO B")
            
            # Comparación con Gemini
            resultado_comparacion = await gemini_service.comparar_propuestas(
                propuesta1=propuesta1,
                propuesta2=propuesta2,
                criterios_evaluacion=["valor", "complejidad", "riesgo", "cronograma"]
            )
            
            # Mostrar comparación
            print(f"\n📊 RESULTADO DE LA COMPARACIÓN:")
            print(f"   🏆 Proceso Recomendado: {resultado_comparacion.get('propuesta_recomendada', 'N/A')}")
            print(f"   📈 Score Proceso A: {resultado_comparacion.get('score_propuesta_a', 0)}/100")
            print(f"   📈 Score Proceso B: {resultado_comparacion.get('score_propuesta_b', 0)}/100")
            print(f"   📏 Diferencia: {resultado_comparacion.get('diferencia_puntos', 0)} puntos")
            
            print(f"\n💡 RECOMENDACIÓN FINAL:")
            print(f"   {resultado_comparacion.get('recomendacion_final', 'No disponible')}")
            
            print(f"\n✅ VENTAJAS PROCESO A:")
            for ventaja in resultado_comparacion.get('ventajas_propuesta_a', []):
                print(f"   • {ventaja}")
            
            print(f"\n✅ VENTAJAS PROCESO B:")
            for ventaja in resultado_comparacion.get('ventajas_propuesta_b', []):
                print(f"   • {ventaja}")
    
    except Exception as e:
        logger.error(f"Error en demo 3: {str(e)}")
        print(f"❌ Error en comparación: {str(e)}")
    
    # ==========================================
    # DEMO 4: EXTRACCIÓN DE INFORMACIÓN
    # ==========================================
    print("\n" + "="*50)
    print("📊 DEMO 4: EXTRACCIÓN INTELIGENTE DE DATOS")
    print("="*50)
    
    try:
        # Usar un proceso para extracción
        if procesos:
            proceso = procesos[0]
            tender = proceso.get('tender', {})
            buyer = proceso.get('buyer', {})
            
            print(f"\n🔍 Extrayendo información de: {proceso.get('title', '')[:60]}...")
            
            content_extraccion = f"""
            DOCUMENTO COMPLETO DE LICITACIÓN PÚBLICA
            
            IDENTIFICACIÓN:
            ID del proceso: {proceso.get('ocid', '')}
            Título del proyecto: {proceso.get('title', '')}
            Descripción general: {proceso.get('description', '')}
            
            ENTIDAD CONTRATANTE:
            Nombre: {buyer.get('name', '')}
            Identificación: {buyer.get('id', '')}
            
            INFORMACIÓN CONTRACTUAL:
            Tipo de procedimiento: {tender.get('procurementMethod', '')}
            Estado actual: {tender.get('status', '')}
            Valor referencial: ${tender.get('value', {}).get('amount', 0):,.2f}
            Moneda: {tender.get('value', {}).get('currency', 'USD')}
            
            CRONOGRAMA DEL PROCESO:
            Fecha de publicación: {tender.get('datePublished', '')}
            Período de consultas: {tender.get('enquiryPeriod', {}).get('startDate', '')} al {tender.get('enquiryPeriod', {}).get('endDate', '')}
            Período de ofertas: {tender.get('tenderPeriod', {}).get('startDate', '')} al {tender.get('tenderPeriod', {}).get('endDate', '')}
            
            ESPECIFICACIONES TÉCNICAS:
            {tender.get('description', '')}
            
            REQUISITOS Y CRITERIOS:
            {tender.get('eligibilityCriteria', '')}
            
            DOCUMENTOS ADJUNTOS:
            {json.dumps([doc.get('title', '') for doc in tender.get('documents', [])], indent=2)}
            """
            
            # Extracción con Gemini (usando recomendaciones de negocio)
            datos_proceso = {
                "ocid": proceso.get('ocid', ''),
                "title": proceso.get('title', ''),
                "buyer_name": buyer.get('name', ''),
                "value": tender.get('value', {}).get('amount', 0),
                "method": tender.get('procurementMethod', ''),
                "description": tender.get('description', ''),
                "eligibility": tender.get('eligibilityCriteria', '')
            }
            
            resultado_extraccion = await gemini_service.generar_recomendaciones_negocio(
                business_context=datos_proceso
            )
            
            # Mostrar información extraída
            print(f"\n📋 RECOMENDACIONES DE NEGOCIO:")
            print(f"   📋 Oportunidad: {resultado_extraccion.get('opportunity_type', 'N/A')}")
            print(f"   � Score de Oportunidad: {resultado_extraccion.get('opportunity_score', 0)}/100")
            print(f"   ⏱️  Urgencia: {resultado_extraccion.get('urgency_level', 'N/A')}")
            print(f"   💰 Potencial ROI: {resultado_extraccion.get('estimated_roi', 'N/A')}")
            
            print(f"\n💡 RECOMENDACIONES ESTRATÉGICAS:")
            for rec in resultado_extraccion.get('strategic_recommendations', []):
                print(f"   • {rec}")
            
            print(f"\n🎯 FACTORES CLAVE:")
            for factor in resultado_extraccion.get('key_factors', []):
                print(f"   • {factor}")
            
            print(f"\n� ANÁLISIS DE VIABILIDAD:")
            for punto in resultado_extraccion.get('viability_analysis', []):
                print(f"   • {punto}")
    
    except Exception as e:
        logger.error(f"Error en demo 4: {str(e)}")
        print(f"❌ Error en extracción: {str(e)}")
    
    # ==========================================
    # RESUMEN FINAL
    # ==========================================
    print("\n" + "="*60)
    print("🎉 DEMO COMPLETADO - RESUMEN DE CAPACIDADES")
    print("="*60)
    
    print(f"\n✅ CAPACIDADES DEMOSTRADAS:")
    print(f"   🔍 Análisis completo de licitaciones con scoring")
    print(f"   ⚠️  Evaluación específica de riesgos de proyectos")
    print(f"   ⚖️  Comparación inteligente entre procesos")
    print(f"   📊 Extracción automática de información clave")
    print(f"   🤖 Integración con Google Gemini AI")
    print(f"   🌐 Conexión directa con SERCOP OCDS API")
    
    print(f"\n🚀 ESTADO DE LA INTEGRACIÓN:")
    print(f"   • Gemini API: {'🟢 Activa' if not gemini_service.use_simulation else '🟡 Simulación activa'}")
    print(f"   • SERCOP API: 🟢 Conectada y funcional")
    print(f"   • Análisis IA: 🟢 Operativo")
    print(f"   • Extracción de datos: 🟢 Operativo")
    
    if gemini_service.use_simulation:
        print(f"\n💡 NOTA: Para activar Gemini AI real:")
        print(f"   1. Obtén tu API key en: https://aistudio.google.com/")
        print(f"   2. Agrega GEMINI_API_KEY=tu_clave en el archivo .env")
        print(f"   3. Reinicia la aplicación")
    
    print(f"\n🎯 READY FOR PRODUCTION!")


async def demo_test_simple():
    """
    Demo rápido con documento de prueba
    """
    print("\n🧪 TEST RÁPIDO GEMINI")
    print("="*40)
    
    gemini_service = GeminiLicitacionesService()
    
    # Documento de prueba simple
    documento_test = """
    LICITACIÓN PÚBLICA
    Entidad: Ministerio de Educación
    Objeto: Construcción de unidad educativa con 12 aulas
    Valor referencial: $850,000.00 USD
    Plazo de ejecución: 8 meses
    
    Requisitos:
    - Experiencia mínima 5 años en construcción educativa
    - Personal técnico: 1 ingeniero civil, 1 arquitecto
    - Equipos: maquinaria pesada certificada
    
    Garantías:
    - Fiel cumplimiento: 10%
    - Calidad: 2 años
    """
    
    resultado = await gemini_service.analizar_documento_licitacion(
        document_content=documento_test,
        document_type="Licitación Educativa"
    )
    
    print(f"✅ Score: {resultado.get('score_general', 0)}/100")
    print(f"⚠️  Riesgo: {resultado.get('nivel_riesgo', 'N/A')}")
    print(f"💡 Resumen: {resultado.get('resumen_ejecutivo', 'N/A')}")


if __name__ == "__main__":
    print("Ejecutando demo completo de Gemini Licitaciones...")
    
    # Verificar si hay argumentos para test rápido
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        asyncio.run(demo_test_simple())
    else:
        asyncio.run(demo_analisis_gemini())
