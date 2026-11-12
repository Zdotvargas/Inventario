"""Catálogos: categorías, proveedores y ubicaciones (bodegas y eventos)."""
from datetime import date

from sqlalchemy import Boolean, CheckConstraint, Date, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin, enum_col
from app.models.enums import TipoUbicacion


class Categoria(Base, TimestampMixin):
    """Campo "Categoría" del formato (portátil, monitor, proyector...)."""
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), unique=True)
    prefijo_codigo: Mapped[str | None] = mapped_column(String(10))  # p. ej. "POR" -> POR-0001
    descripcion: Mapped[str | None] = mapped_column(Text)
    activa: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")


class Proveedor(Base, TimestampMixin):
    """Proveedor de compra y de mantenimiento (campos "Proveedor" del formato)."""
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True)
    nit: Mapped[str | None] = mapped_column(String(20), unique=True)
    contacto: Mapped[str | None] = mapped_column(String(120))
    telefono: Mapped[str | None] = mapped_column(String(30))
    correo: Mapped[str | None] = mapped_column(String(120))
    activo: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")


class Ubicacion(Base, TimestampMixin):
    """Dónde puede estar un equipo: bodega, evento, oficina o proveedor.

    Los eventos se registran aquí con su lugar y fechas; así el campo "Ubicación"
    del formato y los campos "Origen"/"Destino" del historial de traslados
    apuntan siempre a esta tabla.
    """
    __tablename__ = "ubicaciones"
    __table_args__ = (
        # Todo evento debe tener su identificador
        CheckConstraint("tipo <> 'EVENTO' OR codigo IS NOT NULL", name="evento_con_codigo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str | None] = mapped_column(String(50))  # identificador del evento (o de la bodega)
    nombre: Mapped[str] = mapped_column(String(150))
    tipo: Mapped[TipoUbicacion] = mapped_column(enum_col(TipoUbicacion, "tipo_ubicacion"))
    direccion: Mapped[str | None] = mapped_column(String(200))
    cliente: Mapped[str | None] = mapped_column(String(150))          # solo eventos
    fecha_inicio: Mapped[date | None] = mapped_column(Date)           # solo eventos
    fecha_fin: Mapped[date | None] = mapped_column(Date)              # solo eventos
    activa: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    observaciones: Mapped[str | None] = mapped_column(Text)


# El código no se repite (sin distinguir mayúsculas) y se busca rápido.
# Puede quedar vacío en bodegas u oficinas; PostgreSQL permite varios vacíos.
Index("ix_ubicaciones_codigo_lower", func.lower(Ubicacion.codigo), unique=True)
