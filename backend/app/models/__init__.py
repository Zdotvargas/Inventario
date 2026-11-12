"""Importa todos los modelos para que Alembic y SQLAlchemy los encuentren."""
from app.models.activo import Activo
from app.models.catalogos import Categoria, Proveedor, Ubicacion
from app.models.historial import Incidencia, Mantenimiento, Movimiento
from app.models.usuario import Usuario

__all__ = [
    "Activo",
    "Categoria",
    "Incidencia",
    "Mantenimiento",
    "Movimiento",
    "Proveedor",
    "Ubicacion",
    "Usuario",
]
