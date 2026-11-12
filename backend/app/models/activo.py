"""Activo TI: bloque "1. INFORMACIÓN GENERAL" del formato FOR-ADM-002."""
from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin, enum_col
from app.models.catalogos import Categoria, Proveedor, Ubicacion
from app.models.enums import EstadoActivo
from app.models.usuario import Usuario


class Activo(Base, TimestampMixin):
    __tablename__ = "activos"
    __table_args__ = (
        CheckConstraint("valor_compra IS NULL OR valor_compra >= 0", name="valor_positivo"),
        CheckConstraint("vida_util_meses IS NULL OR vida_util_meses > 0", name="vida_util"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # --- Identificación ---
    codigo: Mapped[str] = mapped_column(String(30), unique=True)        # "Código del Activo" (placa)
    serial: Mapped[str] = mapped_column(String(80), unique=True)        # "Serial"
    descripcion: Mapped[str] = mapped_column(String(255))               # "Descripción"
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))  # "Categoría"
    marca: Mapped[str | None] = mapped_column(String(80))               # "Marca"
    modelo: Mapped[str | None] = mapped_column(String(80))              # "Modelo"

    # --- Situación actual (se actualiza con cada movimiento) ---
    ubicacion_id: Mapped[int] = mapped_column(ForeignKey("ubicaciones.id"))           # "Ubicación"
    responsable_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"))     # "Responsable"
    estado: Mapped[EstadoActivo] = mapped_column(
        enum_col(EstadoActivo, "estado_activo"), default=EstadoActivo.ACTIVO,
        server_default=EstadoActivo.ACTIVO.value,
    )                                                                   # "Estado Actual"

    # --- Compra ---
    fecha_compra: Mapped[date | None] = mapped_column(Date)             # "Fecha de Compra"
    proveedor_id: Mapped[int | None] = mapped_column(ForeignKey("proveedores.id"))   # "Proveedor"
    valor_compra: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))  # "Valor de Compra" (COP)
    vida_util_meses: Mapped[int | None] = mapped_column(Integer)        # "Vida Útil Estimada"

    observaciones: Mapped[str | None] = mapped_column(Text)

    # --- Relaciones (para leer los datos relacionados fácilmente) ---
    categoria: Mapped[Categoria] = relationship()
    ubicacion: Mapped[Ubicacion] = relationship()
    responsable: Mapped[Usuario | None] = relationship()
    proveedor: Mapped[Proveedor | None] = relationship()
    movimientos: Mapped[list["Movimiento"]] = relationship(  # noqa: F821
        back_populates="activo", order_by="Movimiento.fecha.desc()"
    )
    mantenimientos: Mapped[list["Mantenimiento"]] = relationship(  # noqa: F821
        back_populates="activo", order_by="Mantenimiento.fecha.desc()"
    )
    incidencias: Mapped[list["Incidencia"]] = relationship(  # noqa: F821
        back_populates="activo", order_by="Incidencia.fecha.desc()"
    )


# Búsqueda rápida por serial o código (RF06) y unicidad sin importar
# mayúsculas/minúsculas: "ABC123" y "abc123" se consideran el mismo equipo.
Index("ix_activos_serial_lower", func.lower(Activo.serial), unique=True)
Index("ix_activos_codigo_lower", func.lower(Activo.codigo), unique=True)
