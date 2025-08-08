#!/usr/bin/env python3
"""
Script de prueba para verificar la integración de LangChain
"""
import asyncio
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

from api.services.langchain_service import LangChainService

async def test_langchain_integration():
    """Probar la integración de LangChain"""
    print("🧪 Iniciando pruebas de LangChain...")
    
    # Crear instancia del servicio
    langchain_service = LangChainService()
    
    # Prueba 1: Análisis de licitación
    print("\n📄 Prueba 1: Análisis de Licitación")
    document_content = """
    PROPUESTA TÉCNICA PARA LICITACIÓN PÚBLICA N° 001-2025
    
    1. OBJETO DEL CONTRATO
    Suministro e instalación de sistema de gestión documental para entidad pública.
    
    2. ESPECIFICACIONES TÉCNICAS
    - Sistema web moderno con base de datos PostgreSQL
    - Interfaz responsive compatible con dispositivos móviles
    - Capacidad para 10,000 documentos simultáneos
    - Integración con sistemas existentes
    
    3. EXPERIENCIA DE LA EMPRESA
    Nuestra empresa tiene 8 años de experiencia en desarrollo de software para el sector público.
    Hemos implementado más de 50 proyectos similares con éxito.
    
    4. PROPUESTA ECONÓMICA
    Valor total del proyecto: $85,000 USD
    Tiempo de implementación: 6 meses
    Garantía: 2 años
    """
    
    try:
        result = await langchain_service.analyze_licitacion_document(
            document_content=document_content,
            document_type="Propuesta Técnica"
        )
        
        print(f"✅ Puntuación: {result.get('score', 'N/A')}")
        print(f"✅ Nivel de riesgo: {result.get('risk_level', 'N/A')}")
        print(f"✅ Tipo de documento: {result.get('document_type', 'N/A')}")
        print(f"✅ Recomendaciones: {len(result.get('recommendations', []))} encontradas")
        
    except Exception as e:
        print(f"❌ Error en análisis de licitación: {e}")
    
    # Prueba 2: Análisis crediticio
    print("\n💰 Prueba 2: Análisis Crediticio")
    company_data = {
        "company_name": "TechStart Solutions",
        "business_type": "Desarrollo de software y aplicaciones móviles",
        "years_in_business": "4 años",
        "monthly_revenue": "25000",
        "digital_presence": "Excelente presencia en redes sociales, sitio web profesional, testimonios positivos",
        "commercial_references": "5 referencias comerciales verificadas de clientes satisfechos"
    }
    
    try:
        result = await langchain_service.analyze_credit_risk(company_data)
        
        print(f"✅ Puntuación crediticia: {result.get('credit_score', 'N/A')}")
        print(f"✅ Nivel de riesgo: {result.get('risk_level', 'N/A')}")
        print(f"✅ Probabilidad de aprobación: {result.get('approval_probability', 'N/A')}%")
        print(f"✅ Presencia digital: {result.get('digital_presence_score', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error en análisis crediticio: {e}")
    
    # Información del sistema
    print("\n🔧 Información del Sistema")
    if langchain_service.llm:
        print("✅ LangChain configurado correctamente con OpenAI")
        print("✅ Modelo: GPT-3.5-turbo")
        print("✅ Temperatura: 0.3 (análisis preciso)")
    else:
        print("⚠️ Funcionando en modo simulación (sin OPENAI_API_KEY)")
        print("ℹ️ Para usar IA real, configura OPENAI_API_KEY en .env")
    
    print("\n🎉 Pruebas completadas!")

if __name__ == "__main__":
    asyncio.run(test_langchain_integration())
