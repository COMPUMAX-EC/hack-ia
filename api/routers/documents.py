from fastapi import APIRouter

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# Puedes agregar endpoints aquí en el futuro