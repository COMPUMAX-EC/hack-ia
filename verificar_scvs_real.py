"""
SCRIPT DE VERIFICACIÓN DE DATOS REALES SCVS
Este script te permite verificar empresas reales en el portal de SCVS
"""

import requests
from bs4 import BeautifulSoup
import time

def verificar_empresa_real(ruc: str):
    """
    Verificar una empresa real en el portal de SCVS
    """
    print(f"\n🔍 VERIFICANDO EMPRESA REAL: {ruc}")
    print("=" * 50)
    
    try:
        # URL del portal público de SCVS
        url = "https://appscvs.supercias.gob.ec/consultaCompanias/consultaCompanias.jsf"
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Parámetros de búsqueda
        params = {
            'ruc': ruc,
            'denominacion': '',
            'tipo': 'TODAS'
        }
        
        print("📡 Conectando al portal SCVS...")
        response = session.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            print("✅ Conexión exitosa al portal SCVS")
            print(f"📄 Respuesta recibida: {len(response.text)} caracteres")
            
            # Buscar información en la respuesta
            if ruc in response.text:
                print(f"✅ RUC {ruc} encontrado en los registros")
                
                # Buscar indicadores de estado
                if "ACTIVA" in response.text.upper():
                    print("🟢 Estado: EMPRESA ACTIVA")
                elif "INACTIVA" in response.text.upper():
                    print("🔴 Estado: EMPRESA INACTIVA")
                else:
                    print("⚪ Estado: No determinado")
                
                # Buscar nombre de empresa
                soup = BeautifulSoup(response.text, 'html.parser')
                # Aquí buscarías el nombre en las tablas de resultados
                
                return True
            else:
                print(f"❌ RUC {ruc} NO encontrado en los registros")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando: {str(e)}")
        return False

def empresas_ejemplo_verificacion():
    """
    Verificar algunas empresas reales conocidas
    """
    print("🏢 VERIFICACIÓN DE EMPRESAS REALES ECUATORIANAS")
    print("=" * 60)
    
    # Empresas grandes conocidas en Ecuador (RUCs reales)
    empresas_test = [
        "1790016919001",  # Banco Pichincha
        "1790011674001",  # Corporación Favorita
        "1791731885001",  # Diners Club del Ecuador
        "1792146739001",  # CNT EP
        "1792150417001",  # CELEC EP
    ]
    
    resultados = {}
    
    for ruc in empresas_test:
        resultado = verificar_empresa_real(ruc)
        resultados[ruc] = resultado
        time.sleep(2)  # Respetar el servidor
    
    print("\n📊 RESUMEN DE VERIFICACIONES:")
    print("-" * 40)
    for ruc, encontrada in resultados.items():
        status = "✅ ENCONTRADA" if encontrada else "❌ NO ENCONTRADA"
        print(f"{ruc}: {status}")

if __name__ == "__main__":
    # Ejecutar verificación
    empresas_ejemplo_verificacion()
    
    # Verificar empresa específica
    print("\n" + "="*60)
    ruc_test = input("Ingresa un RUC para verificar (o Enter para salir): ")
    if ruc_test.strip():
        verificar_empresa_real(ruc_test.strip())
