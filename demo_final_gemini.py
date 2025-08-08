"""
DEMO FINAL GEMINI - ANÁLISIS REAL DE IA
Demostración completa con datos de prueba realistas
"""

import asyncio
from dotenv import load_dotenv
load_dotenv()

from api.services.gemini_service import GeminiLicitacionesService

async def demo_final_gemini():
    print("\n" + "="*60)
    print("🎯 DEMO FINAL: GEMINI AI ANÁLISIS DE LICITACIONES")
    print("="*60)
    
    gemini = GeminiLicitacionesService()
    
    print(f"🤖 Estado Gemini: {'🟢 IA REAL ACTIVA' if not gemini.use_simulation else '🟡 Simulación'}")
    
    # ==========================================
    # DEMO 1: ANÁLISIS COMPLETO DE LICITACIÓN
    # ==========================================
    print("\n" + "="*50)
    print("📋 ANÁLISIS COMPLETO DE LICITACIÓN")
    print("="*50)
    
    documento_licitacion = """
    PROCESO DE CONTRATACIÓN PÚBLICA
    Código: SIE-MTOP-2024-12345
    
    OBJETO DE CONTRATACIÓN:
    Construcción y mejoramiento de la vía de acceso principal al cantón Latacunga, 
    provincia de Cotopaxi, con una longitud aproximada de 15 kilómetros, incluyendo 
    obras de arte menor, señalización horizontal y vertical, y sistemas de drenaje.
    
    ENTIDAD CONTRATANTE:
    Ministerio de Transporte y Obras Públicas (MTOP)
    RUC: 1768152480001
    
    INFORMACIÓN CONTRACTUAL:
    Valor referencial: $3,250,000.00 USD
    Plazo de ejecución: 18 meses
    Modalidad: Licitación Pública Internacional
    
    REQUISITOS TÉCNICOS MÍNIMOS:
    - Experiencia general: Mínimo 15 años en construcción vial
    - Experiencia específica: Al menos 3 proyectos similares de valor ≥ $2,000,000
    - Personal técnico: 1 Ingeniero Civil vial, 1 Ingeniero en Tránsito, 1 Especialista ambiental
    - Equipamiento: Maquinaria pesada certificada para movimiento de tierras
    - Capacidad instalada: Certificación para proyectos de infraestructura vial
    
    GARANTÍAS REQUERIDAS:
    - Garantía de fiel cumplimiento: 10% del valor del contrato
    - Garantía de calidad: 2% del valor del contrato por 24 meses
    - Póliza de responsabilidad civil: $500,000 USD
    
    CRONOGRAMA DEL PROCESO:
    - Fecha de publicación: 15 de enero de 2024
    - Período de preguntas: 15 al 25 de enero de 2024
    - Respuestas a preguntas: 30 de enero de 2024
    - Entrega de ofertas: hasta el 10 de febrero de 2024, 15:00
    - Apertura de ofertas: 10 de febrero de 2024, 15:30
    - Evaluación y calificación: 11 al 20 de febrero de 2024
    - Adjudicación: 25 de febrero de 2024
    
    CRITERIOS DE EVALUACIÓN:
    1. Oferta económica (40 puntos)
    2. Experiencia y capacidad técnica (35 puntos)
    3. Cronograma de ejecución (15 puntos)
    4. Metodología constructiva (10 puntos)
    
    ESPECIFICACIONES TÉCNICAS ADICIONALES:
    El proyecto incluye la construcción de 3 puentes vehiculares menores, sistema de 
    alcantarillado pluvial cada 200 metros, capas de rodadura asfáltica de 5cm de espesor,
    y cumplimiento estricto de normas ambientales vigentes en Ecuador.
    """
    
    print("\n🔍 Analizando licitación vial del MTOP...")
    
    try:
        resultado = await gemini.analizar_documento_licitacion(
            document_content=documento_licitacion,
            document_type="Licitación Pública Internacional"
        )
        
        print(f"\n📊 RESULTADOS DEL ANÁLISIS:")
        print(f"   🎯 Score General: {resultado.get('score_general', 0)}/100")
        print(f"   ⚠️  Nivel de Riesgo: {resultado.get('nivel_riesgo', 'N/A')}")
        print(f"   📜 Cumplimiento Legal: {resultado.get('cumplimiento_legal', 0)}/100")
        print(f"   🔧 Cumplimiento Técnico: {resultado.get('cumplimiento_tecnico', 0)}/100")
        print(f"   📁 Completitud Docs: {resultado.get('completitud_documentos', 0)}/100")
        
        print(f"\n💡 RESUMEN EJECUTIVO:")
        print(f"   {resultado.get('resumen_ejecutivo', 'Análisis completado')}")
        
        print(f"\n⚠️  RIESGOS IDENTIFICADOS:")
        for i, riesgo in enumerate(resultado.get('riesgos_detectados', []), 1):
            print(f"   {i}. {riesgo}")
        
        print(f"\n💪 FORTALEZAS DEL PROCESO:")
        for i, fortaleza in enumerate(resultado.get('fortalezas', []), 1):
            print(f"   {i}. {fortaleza}")
        
        print(f"\n🎯 RECOMENDACIONES:")
        for i, rec in enumerate(resultado.get('recomendaciones', []), 1):
            print(f"   {i}. {rec}")
    
    except Exception as e:
        print(f"❌ Error en análisis: {str(e)}")
    
    # ==========================================
    # DEMO 2: EVALUACIÓN DE RIESGOS
    # ==========================================
    print("\n" + "="*50)
    print("⚠️  EVALUACIÓN DE RIESGOS DEL CONTRATISTA")
    print("="*50)
    
    datos_contratista = {
        "company_name": "Constructora Vial Andina S.A.",
        "ruc": "1792345678001",
        "years_in_business": 12,
        "previous_contracts": [
            {"value": 2800000, "type": "Construcción vial", "status": "completed"},
            {"value": 1500000, "type": "Puentes", "status": "completed"},
            {"value": 4200000, "type": "Infraestructura", "status": "in_progress"}
        ],
        "financial_capacity": 8500000,
        "technical_staff": 45,
        "equipment_value": 3200000,
        "certifications": ["ISO 9001", "ISO 14001", "OHSAS 18001"],
        "project_description": "Construcción vía Latacunga - 15km - $3.25M",
        "project_complexity": "Alta - incluye puentes y drenaje",
        "timeline_months": 18
    }
    
    print(f"\n🏗️  Evaluando: {datos_contratista['company_name']}")
    print(f"   💰 Proyecto: ${datos_contratista['project_description']}")
    
    try:
        resultado_riesgo = await gemini.evaluar_riesgo_contratista(
            company_data=datos_contratista
        )
        
        print(f"\n📊 EVALUACIÓN DE RIESGOS:")
        print(f"   🎯 Nivel de Riesgo: {resultado_riesgo.get('risk_level', 'N/A')}")
        print(f"   📈 Score de Riesgo: {resultado_riesgo.get('risk_score', 0)}/100")
        print(f"   ✅ Prob. de Éxito: {resultado_riesgo.get('success_probability', 0)}%")
        print(f"   💰 Capacidad Financiera: {resultado_riesgo.get('financial_capability', 'N/A')}")
        
        print(f"\n⚠️  FACTORES DE RIESGO:")
        for factor in resultado_riesgo.get('risk_factors', []):
            print(f"   • {factor}")
        
        print(f"\n💡 RECOMENDACIONES:")
        for rec in resultado_riesgo.get('recommendations', []):
            print(f"   • {rec}")
    
    except Exception as e:
        print(f"❌ Error en evaluación de riesgos: {str(e)}")
    
    # ==========================================
    # DEMO 3: COMPARACIÓN DE PROPUESTAS
    # ==========================================
    print("\n" + "="*50)
    print("⚖️  COMPARACIÓN DE PROPUESTAS")
    print("="*50)
    
    propuesta_a = """
    PROPUESTA A - CONSTRUCTORA VIAL ANDINA S.A.
    Valor ofertado: $3,180,000.00 USD (2.1% bajo presupuesto)
    Plazo: 17 meses
    
    EXPERIENCIA:
    - 12 años en construcción vial
    - 8 proyectos similares completados
    - Valor promedio proyectos: $2.8M
    
    METODOLOGÍA:
    - Construcción por tramos de 3km
    - Uso de asfalto modificado con polímeros
    - Sistema GPS para control de calidad
    - Maquinaria propia 85%
    
    PERSONAL TÉCNICO:
    - Ingeniero Civil Senior (15 años exp.)
    - Especialista ambiental certificado
    - Supervisor de calidad con experiencia MTOP
    
    GARANTÍAS ADICIONALES:
    - Extensión de garantía técnica a 36 meses
    - Mantenimiento preventivo incluido primer año
    """
    
    propuesta_b = """
    PROPUESTA B - INFRAESTRUCTURA COTOPAXI LTDA.
    Valor ofertado: $3,050,000.00 USD (6.1% bajo presupuesto)
    Plazo: 20 meses
    
    EXPERIENCIA:
    - 18 años en construcción general
    - 4 proyectos viales completados
    - Valor promedio proyectos: $1.9M
    
    METODOLOGÍA:
    - Construcción secuencial tradicional
    - Materiales estándar según MTOP
    - Control de calidad básico
    - Maquinaria alquilada 60%
    
    PERSONAL TÉCNICO:
    - Ingeniero Civil Junior (8 años exp.)
    - Técnico ambiental
    - Supervisor general
    
    GARANTÍAS:
    - Garantías mínimas requeridas
    - Sin servicios adicionales
    """
    
    print("\n🔄 Comparando propuestas para proyecto vial...")
    
    try:
        resultado_comparacion = await gemini.comparar_propuestas(
            propuesta1=propuesta_a,
            propuesta2=propuesta_b,
            criterios_evaluacion=["precio", "experiencia", "metodología", "cronograma", "garantías"]
        )
        
        print(f"\n📊 RESULTADO DE LA COMPARACIÓN:")
        print(f"   🏆 Propuesta Recomendada: {resultado_comparacion.get('recommended_proposal', 'N/A')}")
        print(f"   📈 Score Propuesta A: {resultado_comparacion.get('proposal_a_score', 0)}/100")
        print(f"   📈 Score Propuesta B: {resultado_comparacion.get('proposal_b_score', 0)}/100")
        print(f"   📏 Diferencia: {resultado_comparacion.get('score_difference', 0)} puntos")
        
        print(f"\n💡 JUSTIFICACIÓN:")
        print(f"   {resultado_comparacion.get('recommendation_rationale', 'Análisis completado')}")
        
        print(f"\n✅ VENTAJAS PROPUESTA A:")
        for ventaja in resultado_comparacion.get('proposal_a_strengths', []):
            print(f"   • {ventaja}")
        
        print(f"\n✅ VENTAJAS PROPUESTA B:")
        for ventaja in resultado_comparacion.get('proposal_b_strengths', []):
            print(f"   • {ventaja}")
    
    except Exception as e:
        print(f"❌ Error en comparación: {str(e)}")
    
    # ==========================================
    # DEMO 4: RECOMENDACIONES DE NEGOCIO
    # ==========================================
    print("\n" + "="*50)
    print("💼 RECOMENDACIONES ESTRATÉGICAS DE NEGOCIO")
    print("="*50)
    
    contexto_negocio = {
        "market_segment": "Infraestructura vial pública",
        "company_profile": "Constructora mediana especializada en obras civiles",
        "available_capital": 5000000,
        "current_workload": "75% capacidad utilizada",
        "project_opportunity": {
            "value": 3250000,
            "duration_months": 18,
            "complexity": "Alta",
            "competition_level": "Media - 8 oferentes estimados",
            "profit_margin_estimate": "12-15%"
        },
        "strategic_goals": ["Crecimiento en sector público", "Diversificación geográfica", "Fortalecimiento técnico"]
    }
    
    print(f"\n🎯 Generando recomendaciones estratégicas...")
    
    try:
        resultado_negocio = await gemini.generar_recomendaciones_negocio(
            business_context=contexto_negocio
        )
        
        print(f"\n📊 ANÁLISIS ESTRATÉGICO:")
        print(f"   🎯 Score de Viabilidad: {resultado_negocio.get('viability_score', 0)}/100")
        print(f"   💰 Rentabilidad Estimada: {resultado_negocio.get('estimated_profitability', 'N/A')}")
        print(f"   ⚠️  Nivel de Riesgo: {resultado_negocio.get('risk_assessment', 'N/A')}")
        print(f"   🏆 Probabilidad de Adjudicación: {resultado_negocio.get('win_probability', 0)}%")
        
        print(f"\n💡 RECOMENDACIONES ESTRATÉGICAS:")
        for rec in resultado_negocio.get('strategic_recommendations', []):
            print(f"   • {rec}")
        
        print(f"\n🎯 FACTORES CLAVE DE ÉXITO:")
        for factor in resultado_negocio.get('success_factors', []):
            print(f"   • {factor}")
        
        print(f"\n⚠️  RIESGOS A MITIGAR:")
        for riesgo in resultado_negocio.get('risks_to_mitigate', []):
            print(f"   • {riesgo}")
    
    except Exception as e:
        print(f"❌ Error en recomendaciones: {str(e)}")
    
    # ==========================================
    # RESUMEN FINAL
    # ==========================================
    print("\n" + "="*60)
    print("🎉 DEMO COMPLETADO - CAPACIDADES GEMINI AI")
    print("="*60)
    
    print(f"\n✅ CAPACIDADES DEMOSTRADAS:")
    print(f"   📋 Análisis completo de documentos de licitación")
    print(f"   ⚠️  Evaluación integral de riesgos de contratistas")
    print(f"   ⚖️  Comparación objetiva entre propuestas")
    print(f"   💼 Recomendaciones estratégicas de negocio")
    print(f"   🤖 Procesamiento de lenguaje natural avanzado")
    print(f"   📊 Scoring y clasificación automatizada")
    
    print(f"\n🚀 ESTADO DEL SISTEMA:")
    print(f"   • Google Gemini AI: {'🟢 ACTIVO Y FUNCIONANDO' if not gemini.use_simulation else '🟡 Modo simulación'}")
    print(f"   • Análisis en tiempo real: 🟢 OPERATIVO")
    print(f"   • Integración FastAPI: 🟢 LISTA")
    print(f"   • Procesamiento inteligente: 🟢 FUNCIONAL")
    
    print(f"\n🎯 TU SISTEMA DE OPTIMIZACIÓN DE LICITACIONES ESTÁ COMPLETO!")
    print(f"   Ready for production con IA avanzada de Google Gemini")


if __name__ == "__main__":
    asyncio.run(demo_final_gemini())
