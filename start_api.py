#!/usr/bin/env python3
"""
Script de inicio para la API de FINOVA
"""
import uvicorn
import os
from pathlib import Path

# Agregar el directorio raíz al path
import sys
sys.path.append(str(Path(__file__).parent))

if __name__ == "__main__":
    # Configuración del servidor
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    reload = os.getenv("RELOAD", "True").lower() == "true"
    
    print("🚀 Iniciando FINOVA API...")
    print(f"📍 Servidor: http://{host}:{port}")
    print(f"📚 Documentación: http://{host}:{port}/docs")
    print(f"🔄 Modo debug: {debug}")
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info" if not debug else "debug"
    )
