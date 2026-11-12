"""Punto de entrada de la API (capa de negocio)."""
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db

app = FastAPI(
    title=settings.app_name,
    description="API REST para la trazabilidad y el control de inventario de activos TI de Instech.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
def raiz():
    return {"mensaje": "API de inventario Instech. Documentación en /docs"}


@app.get("/health", tags=["General"])
def health(db: Session = Depends(get_db)):
    """Verifica que la API esté arriba y que pueda hablar con PostgreSQL."""
    try:
        version = db.execute(text("SELECT version()")).scalar()
        db_estado = "conectada"
    except Exception as exc:  # noqa: BLE001
        version = str(exc.__class__.__name__)
        db_estado = "sin conexión"
    return {
        "api": "ok",
        "base_de_datos": db_estado,
        "postgres": version,
        "entorno": settings.environment,
        "hora_bogota": datetime.now(ZoneInfo("America/Bogota")).isoformat(timespec="seconds"),
    }
