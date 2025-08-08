"""
TEST GEMINI API - Verificación directa
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

print("🔍 VERIFICANDO CONFIGURACIÓN GEMINI")
print("=" * 50)

# Verificar API key
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key encontrada: {'✅ SÍ' if api_key else '❌ NO'}")

if api_key:
    print(f"API Key (primeros 10 chars): {api_key[:10]}...")
    print(f"API Key (longitud): {len(api_key)} caracteres")
    
    try:
        # Configurar Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("\n🤖 PROBANDO GEMINI AI...")
        
        # Test simple
        prompt = """
        Analiza esta licitación y dame un score del 1 al 100:
        
        LICITACIÓN: Construcción de escuela
        Valor: $500,000 USD
        Plazo: 6 meses
        Entidad: Ministerio de Educación
        
        Responde solo con un número del 1 al 100.
        """
        
        response = model.generate_content(prompt)
        print(f"✅ Respuesta de Gemini: {response.text}")
        print("\n🎉 ¡GEMINI API FUNCIONANDO CORRECTAMENTE!")
        
    except Exception as e:
        print(f"❌ Error al conectar con Gemini: {str(e)}")
        
else:
    print("\n❌ No se encontró GEMINI_API_KEY")
    print("📝 Verifica el archivo .env")

print("\n📂 Archivos .env en el directorio:")
import glob
env_files = glob.glob(".env*")
for file in env_files:
    print(f"   - {file}")

print(f"\n📍 Directorio actual: {os.getcwd()}")
