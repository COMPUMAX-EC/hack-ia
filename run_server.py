"""
Servidor de desarrollo para el sistema de licitaciones
"""

import os
import sys
from pathlib import Path

# Añadir el directorio raíz al path para imports
ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Importar FastAPI y crear app básica
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FINOVA API - Sistema de Optimización de Licitaciones",
    description="API completa para análisis inteligente de licitaciones con IA",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🚀 FINOVA API - Sistema de Licitaciones",
        "status": "✅ OPERATIVO",
        "version": "1.0.0",
        "features": [
            "🤖 Google Gemini AI",
            "🌐 SERCOP OCDS Integration",
            "📊 Análisis en tiempo real",
            "⚖️ Comparación de propuestas"
        ],
        "endpoints": {
            "docs": "/docs",
            "sercop": "/sercop/*",
            "gemini": "/sercop/analisis-gemini/*"
        }
    }

@app.get("/health")
async def health_check():
    """Health check para monitoring"""
    return {
        "status": "healthy",
        "gemini_ai": "🟢 configured" if os.getenv("GEMINI_API_KEY") else "🟡 not configured",
        "timestamp": "2025-08-08T17:00:00Z"
    }

# Intentar importar routers
try:
    from api.routers.sercop_ocds import router as sercop_router
    app.include_router(sercop_router)
    print("✅ SERCOP router cargado")
except Exception as e:
    print(f"⚠️ Error cargando SERCOP router: {e}")

try:
    from api.routers.documents import router as docs_router
    app.include_router(docs_router)
    print("✅ Documents router cargado")
except Exception as e:
    print(f"⚠️ Error cargando Documents router: {e}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor FINOVA API...")
    print("📍 URL: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Desactivar reload para evitar problemas
        log_level="info"
    )
