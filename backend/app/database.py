"""Conexión a PostgreSQL con SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Clase base de la que heredarán todas las tablas (Prompt 2)."""


def get_db():
    """Entrega una sesión de base de datos por cada petición y la cierra al final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
