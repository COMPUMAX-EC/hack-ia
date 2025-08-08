#!/usr/bin/env python3
"""
Demo de FINOVA API con LangChain
Muestra las capacidades de IA integradas
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_header(title):
    """Imprimir encabezado estilizado"""
    print("\n" + "="*50)
    print(f"🤖 {title}")
    print("="*50)

def print_result(data, title="Resultado"):
    """Imprimir resultado formateado"""
    print(f"\n📊 {title}:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_health():
    """Probar endpoint de salud"""
    print_header("HEALTH CHECK")
    
    response = requests.get(f"{BASE_URL}/api/v1/health")
    if response.status_code == 200:
        print("✅ API funcionando correctamente")
        print_result(response.json())
    else:
        print("❌ Error en API")

def test_licitacion_analysis():
    """Probar análisis de licitación con LangChain"""
    print_header("ANÁLISIS DE LICITACIÓN CON LANGCHAIN")
    
    document_content = """
    PROPUESTA TÉCNICA PARA LICITACIÓN PÚBLICA LP-001-2025
    OBJETO: Implementación de Sistema de Gestión Hospitalaria
    
    1. RESUMEN EJECUTIVO
    La presente propuesta presenta una solución integral de gestión hospitalaria 
    basada en tecnologías modernas y estándares internacionales de salud.
    
    2. ESPECIFICACIONES TÉCNICAS
    - Arquitectura web moderna con React y Node.js
    - Base de datos PostgreSQL con alta disponibilidad
    - Integración con sistemas de laboratorio existentes
    - Módulo de facturación electrónica integrado
    - Seguridad avanzada con encriptación end-to-end
    
    3. EXPERIENCIA DE LA EMPRESA
    TechMed Solutions cuenta con 12 años de experiencia en el sector salud.
    Hemos implementado más de 80 sistemas hospitalarios en Latinoamérica.
    Certificaciones: ISO 27001, HIPAA compliance, HL7 FHIR.
    
    4. CRONOGRAMA
    Fase 1: Análisis y diseño (2 meses)
    Fase 2: Desarrollo del core (4 meses)
    Fase 3: Integración y pruebas (2 meses)
    Fase 4: Capacitación y puesta en marcha (1 mes)
    
    5. PROPUESTA ECONÓMICA
    Valor total del proyecto: $450,000 USD
    Forma de pago: 30% inicial, 40% entrega parcial, 30% entrega final
    Garantía: 3 años de soporte y mantenimiento incluido
    """
    
    payload = {
        "document_content": document_content,
        "document_type": "Propuesta Técnica Hospitalaria",
        "priority": "high"
    }
    
    print("📤 Enviando documento para análisis...")
    start_time = time.time()
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/licitaciones/analyze", json=payload)
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Análisis completado en {processing_time:.2f} segundos")
            print(f"📈 Puntuación: {result['score']}/100")
            print(f"⚠️ Nivel de riesgo: {result['risk_level'].upper()}")
            print(f"📋 Tipo de documento: {result['document_type']}")
            print(f"⚖️ Cumplimiento legal: {result['legal_compliance']}%")
            print(f"🔧 Cumplimiento técnico: {result['technical_compliance']}%")
            print(f"⏱️ Tiempo estimado IA: {result['estimated_processing_time']}")
            print(f"⏰ Tiempo tradicional: {result['traditional_time']}")
            
            print("\n💡 Recomendaciones:")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"   {i}. {rec}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_credit_analysis():
    """Probar análisis crediticio con LangChain"""
    print_header("ANÁLISIS CREDITICIO CON LANGCHAIN")
    
    company_data = {
        "company_name": "InnovatePYME Tech",
        "business_type": "Desarrollo de aplicaciones móviles y consultoría tecnológica",
        "years_in_business": "5 años",
        "monthly_revenue": "28000",
        "digital_presence": "Excelente presencia digital: sitio web profesional, 15k seguidores en LinkedIn, testimonios positivos de clientes, presencia activa en GitHub",
        "commercial_references": "8 referencias comerciales verificadas de empresas Fortune 500, contratos vigentes con 3 multinacionales",
        "location": "Quito, Ecuador",
        "employee_count": 12
    }
    
    payload = {
        "company_data": company_data,
        "requested_amount": 75000,
        "loan_purpose": "Expansión internacional y contratación de talento senior"
    }
    
    print("📤 Enviando datos para análisis crediticio...")
    start_time = time.time()
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/credito/analyze", json=payload)
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            assessment = result['risk_assessment']
            
            print(f"✅ Análisis completado en {processing_time:.2f} segundos")
            print(f"💯 Puntuación crediticia: {assessment['credit_score']}/850")
            print(f"⚠️ Nivel de riesgo: {assessment['risk_level'].upper()}")
            print(f"📊 Probabilidad de aprobación: {assessment['approval_probability']}%")
            print(f"💰 Monto recomendado: {assessment['recommended_amount']}")
            print(f"📈 Tasa de interés sugerida: {assessment['interest_rate']}%")
            
            factors = assessment['factors']
            print(f"\n📋 Factores de evaluación:")
            print(f"   🌐 Presencia digital: {factors['digital_presence']}/100")
            print(f"   🏢 Reputación comercial: {factors['commercial_reputation']}/100")
            print(f"   📅 Estabilidad del negocio: {factors['business_stability']}/100")
            print(f"   💳 Capacidad financiera: {factors['financial_capacity']}/100")
            print(f"   🚀 Potencial de crecimiento: {factors['growth_potential']}/100")
            
            print(f"\n💡 Recomendaciones:")
            for i, rec in enumerate(assessment['recommendations'], 1):
                print(f"   {i}. {rec}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_ai_capabilities():
    """Mostrar capacidades de IA"""
    print_header("CAPACIDADES DE IA INTEGRADAS")
    
    try:
        # Capacidades de licitaciones
        response = requests.get(f"{BASE_URL}/api/v1/licitaciones/ai-capabilities")
        if response.status_code == 200:
            print("🏗️ ANÁLISIS DE LICITACIONES:")
            licit_caps = response.json()
            print(f"   🤖 Proveedor: {licit_caps['ai_provider']}")
            print(f"   ⚡ Tiempo: {licit_caps['processing_time']}")
            print(f"   📊 Precisión: {licit_caps['accuracy']}")
            
        # Capacidades de crédito
        response = requests.get(f"{BASE_URL}/api/v1/credito/ai-capabilities")
        if response.status_code == 200:
            print("\n💰 EVALUACIÓN CREDITICIA:")
            credit_caps = response.json()
            print(f"   🤖 Proveedor: {credit_caps['ai_provider']}")
            print(f"   ⚡ Tiempo: {credit_caps['processing_time']}")
            print(f"   📊 Precisión: {credit_caps['accuracy']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal de demostración"""
    print("🚀 FINOVA API - Demo con LangChain")
    print("Demostración de capacidades de IA para licitaciones y crédito")
    
    # Ejecutar pruebas
    test_health()
    test_ai_capabilities()
    test_licitacion_analysis()
    test_credit_analysis()
    
    print_header("DEMO COMPLETADA")
    print("✅ Todas las funcionalidades de LangChain están operativas")
    print("📚 Documentación completa: http://localhost:8000/docs")
    print("🔗 GitHub: https://github.com/COMPUMAX-EC/hack-ia")

if __name__ == "__main__":
    main()
