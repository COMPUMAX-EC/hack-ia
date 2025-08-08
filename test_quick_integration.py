"""
TEST RÁPIDO SERCOP + GEMINI
"""

import asyncio
import json
from dotenv import load_dotenv
load_dotenv()

from api.services.gemini_service import GeminiLicitacionesService
from api.services.ocds_sercop_integration import OCDSSercop

async def test_quick():
    print("🚀 TEST RÁPIDO SERCOP + GEMINI")
    print("=" * 40)
    
    # Servicios
    gemini = GeminiLicitacionesService()
    ocds = OCDSSercop()
    
    print(f"✅ Gemini: {'🟢 Real' if not gemini.use_simulation else '🟡 Simulación'}")
    
    # Test SERCOP
    try:
        print("\n🔍 Buscando licitaciones activas...")
        licitaciones = await ocds.obtener_licitaciones_activas(limit=1)
        
        print("\n🔍 Buscando licitaciones activas...")
        licitaciones = await ocds.obtener_licitaciones_activas(limit=1)
        
        print(f"📊 Tipo de respuesta: {type(licitaciones)}")
        
        if licitaciones and len(licitaciones) > 0:
            proceso = licitaciones[0]
            print(f"✅ Proceso encontrado: {proceso.get('title', 'Sin título')[:60]}...")
            
            # Test Gemini
            print("\n🤖 Analizando con Gemini...")
            
            content = f"""
            LICITACIÓN SERCOP
            Título: {proceso.get('title', '')}
            Descripción: {proceso.get('description', '')}
            Entidad: {proceso.get('buyer', {}).get('name', '')}
            Valor: {proceso.get('tender', {}).get('value', {}).get('amount', 0)}
            """
            
            resultado = await gemini.analizar_documento_licitacion(
                document_content=content,
                document_type="Licitación SERCOP"
            )
            
            print(f"✅ Análisis completado:")
            print(f"   📊 Score: {resultado.get('score_general', 0)}/100")
            print(f"   ⚠️  Riesgo: {resultado.get('nivel_riesgo', 'N/A')}")
            print(f"   📝 Resumen: {resultado.get('resumen_ejecutivo', 'N/A')[:100]}...")
            
        else:
            print("❌ No se encontraron licitaciones")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_quick())
