"""Piezas comunes a todas las tablas."""
import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column


def enum_col(enum_cls: type[enum.Enum], name: str):
    """Columna de texto que solo acepta los valores del enum (CHECK en PostgreSQL)."""
    return Enum(
        enum_cls,
        name=name,
        native_enum=False,        # se guarda como VARCHAR: más fácil de migrar
        create_constraint=True,   # PostgreSQL rechaza valores fuera de la lista
        length=30,
        validate_strings=True,
    )


class TimestampMixin:
    """Agrega fecha de creación y de última actualización a una tabla."""
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
