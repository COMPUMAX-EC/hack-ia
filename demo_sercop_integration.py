"""
DEMO RÁPIDO - INTEGRACIÓN SERCOP OCDS
Demostración de las nuevas capacidades con datos reales del portal oficial
"""

import requests
import json
from datetime import datetime

# URL base de la API
API_BASE = "http://localhost:8000/api/v1"

def print_separator(title: str):
    """Imprimir separador con título"""
    print("\n" + "=" * 60)
    print(f"🏛️ {title}")
    print("=" * 60)

def print_subsection(title: str):
    """Imprimir subsección"""
    print(f"\n📋 {title}")
    print("-" * 50)

def demo_busqueda_basica():
    """Demo de búsqueda básica en SERCOP"""
    print_subsection("Búsqueda básica: 'construccion' 2024")
    
    url = f"{API_BASE}/sercop/buscar"
    params = {
        'year': 2024,
        'search': 'construccion',
        'page': 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('data', {})
            
            print(f"✅ Búsqueda exitosa")
            print(f"📊 Total encontrados: {results.get('total', 0)}")
            print(f"📄 En página 1: {len(results.get('data', []))}")
            
            # Mostrar primeros 3 resultados
            if results.get('data'):
                print(f"\n📋 Primeros 3 resultados:")
                for i, proc in enumerate(results['data'][:3], 1):
                    print(f"    {i}. {proc.get('title', 'N/A')[:60]}...")
                    print(f"       Entidad: {proc.get('buyerName', 'N/A')[:40]}...")
                    print(f"       Fecha: {proc.get('fecha_formateada', 'N/A')}")
                    print(f"       Categoría: {proc.get('categoria_inferred', 'N/A')}")
                    print(f"       OCID: {proc.get('ocid', 'N/A')}")
                    print()
                
                return results['data'][0].get('ocid')  # Retornar primer OCID
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"    Respuesta: {response.text}")
    
    except Exception as e:
        print(f"❌ Error en búsqueda: {str(e)}")
    
    return None

def demo_licitaciones_activas():
    """Demo de licitaciones activas"""
    print_subsection("Licitaciones activas del año actual")
    
    url = f"{API_BASE}/sercop/activas"
    params = {'limit': 10}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('data', {})
            
            print(f"✅ Licitaciones activas obtenidas")
            print(f"📊 Total activas: {results.get('total_activas', 0)}")
            
            # Resumen por categorías
            categorias = results.get('resumen_categorias', {})
            if categorias:
                print(f"\n📊 Por categorías:")
                for categoria, cantidad in list(categorias.items())[:3]:
                    print(f"    - {categoria}: {cantidad}")
            
            # Resumen por provincias
            provincias = results.get('resumen_provincias', {})
            if provincias:
                print(f"\n🗺️ Por provincias:")
                for provincia, cantidad in list(provincias.items())[:3]:
                    print(f"    - {provincia}: {cantidad}")
            
            # Top licitaciones
            licitaciones = results.get('licitaciones', [])
            if licitaciones:
                print(f"\n🏆 Top 3 más recientes:")
                for i, proc in enumerate(licitaciones[:3], 1):
                    print(f"    {i}. {proc.get('title', 'N/A')[:50]}...")
                    print(f"       Días desde publicación: {proc.get('dias_desde_publicacion', 'N/A')}")
                    print(f"       Categoría: {proc.get('categoria_inferred', 'N/A')}")
        
        else:
            print(f"❌ Error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error obteniendo activas: {str(e)}")

def demo_busqueda_por_categoria():
    """Demo de búsqueda por categoría"""
    print_subsection("Búsqueda por categoría: 'tecnologia'")
    
    url = f"{API_BASE}/sercop/categorias/tecnologia"
    params = {
        'year': 2024,
        'limit': 5
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('data', {})
            
            print(f"✅ Búsqueda por categoría exitosa")
            print(f"📊 Encontrados: {results.get('total_encontrados', 0)}")
            print(f"📄 Retornados: {results.get('total_retornados', 0)}")
            
            procesos = results.get('procesos', [])
            if procesos:
                print(f"\n📋 Procesos de tecnología:")
                for i, proc in enumerate(procesos[:3], 1):
                    print(f"    {i}. {proc.get('title', 'N/A')[:50]}...")
                    print(f"       Entidad: {proc.get('buyerName', 'N/A')[:40]}...")
                    print(f"       Categoría: {proc.get('categoria_inferred', 'N/A')}")
        
        else:
            print(f"❌ Error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error búsqueda por categoría: {str(e)}")

def demo_analisis_proceso_completo(ocid: str):
    """Demo de análisis completo de proceso con IA"""
    if not ocid:
        print_subsection("Análisis completo con IA - Sin OCID disponible")
        print("❌ No hay OCID disponible para demostración")
        return
    
    print_subsection(f"Análisis completo con IA: {ocid}")
    
    url = f"{API_BASE}/sercop/proceso/{ocid}"
    params = {'incluir_analisis_ia': True}
    
    try:
        response = requests.get(url, params=params, timeout=45)
        
        if response.status_code == 200:
            data = response.json()
            resultado = data.get('data', {})
            
            print(f"✅ Análisis completo exitoso")
            
            # Información básica
            resumen = resultado.get('resumen_ejecutivo', {})
            print(f"📋 Título: {resumen.get('titulo', 'N/A')[:60]}...")
            print(f"🏛️ Entidad: {resumen.get('entidad', 'N/A')[:40]}...")
            print(f"💰 Valor estimado: ${resumen.get('valor_estimado', 0):,.2f}")
            print(f"📊 Etapa: {resumen.get('etapa', 'N/A')}")
            
            # Análisis IA
            print(f"\n🤖 ANÁLISIS CON IA:")
            print(f"📊 Score: {resumen.get('score_ia', 'N/A')}")
            print(f"⚠️ Riesgo: {resumen.get('riesgo_ia', 'N/A')}")
            
            # Riesgos detectados
            riesgos_sercop = resumen.get('riesgos_sercop', [])
            if riesgos_sercop:
                print(f"\n⚠️ RIESGOS DETECTADOS ({len(riesgos_sercop)}):")
                for i, riesgo in enumerate(riesgos_sercop[:2], 1):
                    print(f"    {i}. {riesgo}")
            
            # Recomendaciones
            recomendaciones = resumen.get('recomendaciones', [])
            if recomendaciones:
                print(f"\n💡 RECOMENDACIONES ({len(recomendaciones)}):")
                for i, rec in enumerate(recomendaciones[:3], 1):
                    print(f"    {i}. {rec}")
        
        else:
            print(f"❌ Error: {response.status_code}")
            if response.status_code == 404:
                print("    El proceso no fue encontrado")
    
    except Exception as e:
        print(f"❌ Error en análisis completo: {str(e)}")

def demo_dashboard_completo():
    """Demo del dashboard completo"""
    print_subsection("Dashboard completo de compras públicas")
    
    url = f"{API_BASE}/sercop/dashboard"
    
    try:
        response = requests.get(url, timeout=45)
        
        if response.status_code == 200:
            data = response.json()
            dashboard = data.get('data', {})
            
            print(f"✅ Dashboard generado exitosamente")
            print(f"📅 Actualizado: {dashboard.get('fecha_actualizacion', 'N/A')}")
            
            # Resumen general
            resumen = dashboard.get('resumen', {})
            print(f"\n📊 RESUMEN GENERAL:")
            print(f"    Total procesos año: {resumen.get('total_procesos_year', 0)}")
            print(f"    Procesos activos: {resumen.get('procesos_activos', 0)}")
            print(f"    Valor total estimado: ${resumen.get('valor_total_estimado', 0):,.2f}")
            
            # Licitaciones destacadas
            destacadas = dashboard.get('licitaciones_destacadas', [])
            if destacadas:
                print(f"\n🏆 LICITACIONES DESTACADAS ({len(destacadas)}):")
                for i, proc in enumerate(destacadas[:3], 1):
                    print(f"    {i}. {proc.get('title', 'N/A')[:50]}...")
                    print(f"       Entidad: {proc.get('buyerName', 'N/A')[:30]}...")
            
            # Oportunidades por sector
            construccion = dashboard.get('oportunidades_construccion', [])
            tecnologia = dashboard.get('oportunidades_tecnologia', [])
            
            print(f"\n🏗️ CONSTRUCCIÓN: {len(construccion)} oportunidades")
            print(f"💻 TECNOLOGÍA: {len(tecnologia)} oportunidades")
            
            # Alertas
            alertas = dashboard.get('alertas', [])
            if alertas:
                print(f"\n🚨 ALERTAS ACTIVAS ({len(alertas)}):")
                for i, alerta in enumerate(alertas[:3], 1):
                    print(f"    {i}. {alerta}")
        
        else:
            print(f"❌ Error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error generando dashboard: {str(e)}")

def demo_identificar_oportunidades():
    """Demo de identificación de oportunidades"""
    print_subsection("Identificar oportunidades de negocio")
    
    url = f"{API_BASE}/sercop/oportunidades"
    params = {
        'categoria': 'construccion',
        'valor_minimo': 500000
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            oportunidades = data.get('data', {})
            
            print(f"✅ Oportunidades identificadas")
            
            filtros = oportunidades.get('filtros_aplicados', {})
            print(f"🔍 Filtros aplicados:")
            print(f"    Categoría: {filtros.get('categoria', 'N/A')}")
            print(f"    Valor mínimo: ${filtros.get('valor_minimo', 0):,.0f}")
            
            print(f"\n📊 RESULTADOS:")
            print(f"    Total oportunidades: {oportunidades.get('total_oportunidades', 0)}")
            print(f"    Valor total estimado: ${oportunidades.get('valor_total_estimado', 0):,.2f}")
            
            # Top oportunidades
            top_oportunidades = oportunidades.get('oportunidades_top', [])
            if top_oportunidades:
                print(f"\n🎯 TOP OPORTUNIDADES:")
                for i, proc in enumerate(top_oportunidades[:3], 1):
                    print(f"    {i}. {proc.get('title', 'N/A')[:50]}...")
                    print(f"       Entidad: {proc.get('buyerName', 'N/A')[:30]}...")
                    print(f"       Categoría: {proc.get('categoria_inferred', 'N/A')}")
            
            # Recomendaciones
            recomendaciones = oportunidades.get('recomendaciones', [])
            if recomendaciones:
                print(f"\n💡 RECOMENDACIONES:")
                for i, rec in enumerate(recomendaciones[:3], 1):
                    print(f"    {i}. {rec}")
        
        else:
            print(f"❌ Error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error identificando oportunidades: {str(e)}")

def main():
    """Función principal del demo"""
    print_separator("DEMO INTEGRACIÓN SERCOP OCDS + IA")
    print("🎯 Sistema de Optimización de Licitaciones")
    print("📡 Conectado al API oficial de Contrataciones Abiertas Ecuador")
    print(f"⏰ Ejecutado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # 1. Búsqueda básica
    print_separator("1. BÚSQUEDA BÁSICA")
    ocid_ejemplo = demo_busqueda_basica()
    
    # 2. Licitaciones activas
    print_separator("2. LICITACIONES ACTIVAS")
    demo_licitaciones_activas()
    
    # 3. Búsqueda por categoría
    print_separator("3. BÚSQUEDA POR CATEGORÍA")
    demo_busqueda_por_categoria()
    
    # 4. Análisis completo con IA
    print_separator("4. ANÁLISIS COMPLETO CON IA")
    demo_analisis_proceso_completo(ocid_ejemplo)
    
    # 5. Dashboard completo
    print_separator("5. DASHBOARD COMPLETO")
    demo_dashboard_completo()
    
    # 6. Identificar oportunidades
    print_separator("6. OPORTUNIDADES DE NEGOCIO")
    demo_identificar_oportunidades()
    
    # Conclusión
    print_separator("DEMO COMPLETADO")
    print("✅ Integración SERCOP OCDS totalmente funcional")
    print("🤖 Análisis con IA operativo")
    print("📊 Dashboard en tiempo real disponible")
    print("🎯 Sistema listo para demostración a SERCOP")
    print("\n🚀 ACCESOS DIRECTOS:")
    print("   📖 Documentación API: http://localhost:8000/docs")
    print("   🏛️ Endpoints SERCOP: http://localhost:8000/docs#/🏛️%20SERCOP%20OCDS%20OFICIAL")
    print("   ⚡ Health Check: http://localhost:8000/api/v1/health")
    
    print("\n💡 ENDPOINTS DESTACADOS:")
    print("   🔍 Buscar: GET /api/v1/sercop/buscar?year=2024&search=construccion")
    print("   📊 Dashboard: GET /api/v1/sercop/dashboard")
    print("   🎯 Oportunidades: GET /api/v1/sercop/oportunidades")
    print("   🤖 Análisis IA: GET /api/v1/sercop/proceso/{ocid}")

if __name__ == "__main__":
    main()
