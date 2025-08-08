from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import licitaciones, credito, health, construction_tender, sercop_ocds

# Crear la instancia de FastAPI
app = FastAPI(
    title="VIAMATICA - Sistema de Optimización de Licitaciones con IA + SERCOP OCDS",
    description="Sistema inteligente para automatizar el análisis de documentos de licitación en construcción + Integración oficial API OCDS SERCOP Ecuador - Reto 1 Hack IA Ecuador 2024",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir requests desde el frontend Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "https://hack-ia.vercel.app",
        "https://datosabiertos.compraspublicas.gob.ec",  # SERCOP oficial
        "https://www.compraspublicas.gob.ec"  # Portal SERCOP
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(licitaciones.router, prefix="/api/v1", tags=["Licitaciones Básicas"])
app.include_router(construction_tender.router, prefix="/api/v1/licitaciones", tags=["Licitaciones Construcción - VIAMATICA"])
app.include_router(credito.router, prefix="/api/v1", tags=["Crédito"])
app.include_router(sercop_ocds.router, prefix="/api/v1", tags=["🏛️ SERCOP OCDS OFICIAL"])

@app.get("/")
async def root():
    return {
        "message": "Sistema de Optimización de Licitaciones con IA - VIAMATICA",
        "reto": "Reto 1 - Optimización Inteligente de Procesos de Licitación en Construcción", 
        "version": "2.0.0",
        "funcionalidades": [
            "Análisis automático de pliegos de condiciones",
            "Procesamiento de propuestas técnicas y económicas", 
            "Validación de RUC y razón social",
            "Detección de riesgos legales y técnicos",
            "Comparación objetiva entre oferentes",
            "Dashboard comparativo interactivo"
        ],
        "docs": "/docs",
        "status": "online",
        "demo_endpoints": {
            "upload_document": "/api/v1/licitaciones/upload",
            "compare_proposals": "/api/v1/licitaciones/compare",
            "validate_contractor": "/api/v1/licitaciones/validate-ruc",
            "dashboard": "/api/v1/licitaciones/dashboard"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
