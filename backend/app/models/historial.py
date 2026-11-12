"""Bitácora del activo: traslados, mantenimientos e incidencias.

- Movimiento    -> bloque "3. HISTORIAL DE TRASLADOS" (despachos, reingresos...)
- Mantenimiento -> bloque "2. HISTORIAL DE MANTENIMIENTO"
- Incidencia    -> novedades reportadas (daños, fallas, faltantes) - RN03
"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import enum_col
from app.models.catalogos import Proveedor, Ubicacion
from app.models.enums import (
    EstadoActivo,
    EstadoIncidencia,
    SeveridadIncidencia,
    TipoMantenimiento,
    TipoMovimiento,
)
from app.models.usuario import Usuario


class Movimiento(Base):
    """Cada fila del "Historial de traslados": Fecha, Origen, Destino, Responsable, Observaciones.

    RN02: fecha, responsable y quien registra son obligatorios.
    Los movimientos no se editan ni se borran: son el registro de auditoría.
    """
    __tablename__ = "movimientos"
    __table_args__ = (Index("ix_movimientos_activo_fecha", "activo_id", "fecha"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    activo_id: Mapped[int] = mapped_column(ForeignKey("activos.id", ondelete="RESTRICT"))
    tipo: Mapped[TipoMovimiento] = mapped_column(enum_col(TipoMovimiento, "tipo_movimiento"))
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    origen_id: Mapped[int | None] = mapped_column(ForeignKey("ubicaciones.id"))   # vacío en el ingreso inicial
    destino_id: Mapped[int] = mapped_column(ForeignKey("ubicaciones.id"))

    responsable_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))       # quien recibe el equipo
    registrado_por_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))    # quien hace el registro

    estado_activo: Mapped[EstadoActivo] = mapped_column(
        enum_col(EstadoActivo, "estado_activo_mov")
    )  # estado con el que sale o llega el equipo
    observaciones: Mapped[str | None] = mapped_column(Text)

    activo: Mapped["Activo"] = relationship(back_populates="movimientos")  # noqa: F821
    origen: Mapped[Ubicacion | None] = relationship(foreign_keys=[origen_id])
    destino: Mapped[Ubicacion] = relationship(foreign_keys=[destino_id])
    responsable: Mapped[Usuario] = relationship(foreign_keys=[responsable_id])
    registrado_por: Mapped[Usuario] = relationship(foreign_keys=[registrado_por_id])


class Mantenimiento(Base):
    """Cada fila del "Historial de mantenimiento": Fecha, Tipo, Proveedor, Costo, Responsable."""
    __tablename__ = "mantenimientos"
    __table_args__ = (
        CheckConstraint("costo IS NULL OR costo >= 0", name="costo_positivo"),
        Index("ix_mantenimientos_activo_fecha", "activo_id", "fecha"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    activo_id: Mapped[int] = mapped_column(ForeignKey("activos.id", ondelete="RESTRICT"))
    tipo: Mapped[TipoMantenimiento] = mapped_column(enum_col(TipoMantenimiento, "tipo_mantenimiento"))
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_fin: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # vacío = en curso
    proveedor_id: Mapped[int | None] = mapped_column(ForeignKey("proveedores.id"))  # vacío = interno
    costo: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    responsable_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    registrado_por_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    descripcion: Mapped[str] = mapped_column(Text)
    estado_resultante: Mapped[EstadoActivo | None] = mapped_column(
        enum_col(EstadoActivo, "estado_activo_mant")
    )  # cómo quedó el equipo al terminar (ACTIVO o DE_BAJA)
    incidencia_id: Mapped[int | None] = mapped_column(ForeignKey("incidencias.id"))  # si atiende una incidencia

    activo: Mapped["Activo"] = relationship(back_populates="mantenimientos")  # noqa: F821
    proveedor: Mapped[Proveedor | None] = relationship()
    responsable: Mapped[Usuario] = relationship(foreign_keys=[responsable_id])
    registrado_por: Mapped[Usuario] = relationship(foreign_keys=[registrado_por_id])


class Incidencia(Base):
    """Novedad sobre un equipo (daño, falla, faltante). RN03: si se reporta,
    el equipo deja de estar ACTIVO y pasa a EN_MANTENIMIENTO, DE_BAJA o PERDIDO_HURTADO."""
    __tablename__ = "incidencias"
    __table_args__ = (
        CheckConstraint("estado_asignado <> 'ACTIVO'", name="no_activo"),  # RN03 en la BD
        Index("ix_incidencias_activo_fecha", "activo_id", "fecha"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    activo_id: Mapped[int] = mapped_column(ForeignKey("activos.id", ondelete="RESTRICT"))
    movimiento_id: Mapped[int | None] = mapped_column(ForeignKey("movimientos.id"))  # p. ej. el reingreso donde se detectó
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    descripcion: Mapped[str] = mapped_column(Text)
    severidad: Mapped[SeveridadIncidencia] = mapped_column(
        enum_col(SeveridadIncidencia, "severidad_incidencia")
    )
    estado_asignado: Mapped[EstadoActivo] = mapped_column(
        enum_col(EstadoActivo, "estado_activo_inc")
    )
    estado: Mapped[EstadoIncidencia] = mapped_column(
        enum_col(EstadoIncidencia, "estado_incidencia"),
        default=EstadoIncidencia.ABIERTA, server_default=EstadoIncidencia.ABIERTA.value,
    )
    reportado_por_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    fecha_cierre: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    solucion: Mapped[str | None] = mapped_column(Text)

    activo: Mapped["Activo"] = relationship(back_populates="incidencias")  # noqa: F821
    movimiento: Mapped[Movimiento | None] = relationship()
    reportado_por: Mapped[Usuario] = relationship()
