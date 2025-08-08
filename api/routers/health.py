from fastapi import APIRouter, HTTPException, status
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "FINOVA API",
        "version": "1.0.0"
    }

@router.get("/ping")
async def ping():
    """Endpoint simple de ping"""
    return {"message": "pong"}
