from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import licitaciones, credito, health

# Crear la instancia de FastAPI
app = FastAPI(
    title="FINOVA API",
    description="API para análisis de licitaciones y evaluación crediticia con IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir requests desde el frontend Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://hack-ia.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(licitaciones.router, prefix="/api/v1", tags=["Licitaciones"])
app.include_router(credito.router, prefix="/api/v1", tags=["Crédito"])

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a FINOVA API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
