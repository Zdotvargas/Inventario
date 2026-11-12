"""Usuarios del sistema y responsables (custodios) de los equipos."""
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, enum_col
from app.models.enums import RolUsuario


class Usuario(Base, TimestampMixin):
    """Persona que usa el sistema o que tiene equipos a cargo.

    Nombre y cargo alimentan el bloque "4. FIRMAS" de la hoja de vida.
    Un CUSTODIO puede no tener contraseña: es responsable de equipos
    pero no entra al sistema.
    """
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120))
    documento: Mapped[str | None] = mapped_column(String(20), unique=True)
    cargo: Mapped[str | None] = mapped_column(String(100))
    correo: Mapped[str | None] = mapped_column(String(120), unique=True)
    telefono: Mapped[str | None] = mapped_column(String(30))
    rol: Mapped[RolUsuario] = mapped_column(enum_col(RolUsuario, "rol_usuario"))
    password_hash: Mapped[str | None] = mapped_column(String(255))  # se usa en el Prompt 3
    activo: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
