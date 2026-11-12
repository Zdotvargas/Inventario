"""Listas de valores permitidos (catálogos fijos).

Se basan en el formato FOR-ADM-002 "Hoja de vida del activo" de Instech.
"""
import enum


class EstadoActivo(str, enum.Enum):
    """Estado Actual del activo (casillas del formato FOR-ADM-002)."""
    ACTIVO = "ACTIVO"                        # operativo, disponible para despacho
    EN_MANTENIMIENTO = "EN_MANTENIMIENTO"    # en revisión / reparación
    DE_BAJA = "DE_BAJA"                      # retirado definitivamente
    PERDIDO_HURTADO = "PERDIDO_HURTADO"      # no se encuentra o fue robado


class TipoUbicacion(str, enum.Enum):
    BODEGA = "BODEGA"
    EVENTO = "EVENTO"
    OFICINA = "OFICINA"
    PROVEEDOR = "PROVEEDOR"   # p. ej. el equipo está en el taller de un proveedor


class TipoMovimiento(str, enum.Enum):
    """Tipos de registro del "Historial de traslados"."""
    INGRESO_INICIAL = "INGRESO_INICIAL"          # alta del activo en el sistema
    DESPACHO = "DESPACHO"                        # salida de bodega hacia un evento
    REINGRESO = "REINGRESO"                      # regreso del evento a bodega
    TRASLADO = "TRASLADO"                        # cualquier otro cambio de ubicación
    CAMBIO_RESPONSABLE = "CAMBIO_RESPONSABLE"    # misma ubicación, nuevo custodio


class TipoMantenimiento(str, enum.Enum):
    PREVENTIVO = "PREVENTIVO"
    CORRECTIVO = "CORRECTIVO"


class SeveridadIncidencia(str, enum.Enum):
    LEVE = "LEVE"
    MODERADA = "MODERADA"
    GRAVE = "GRAVE"


class EstadoIncidencia(str, enum.Enum):
    ABIERTA = "ABIERTA"
    CERRADA = "CERRADA"


class RolUsuario(str, enum.Enum):
    ADMINISTRADOR = "ADMINISTRADOR"   # todo, incluida la gestión de usuarios
    OPERATIVO = "OPERATIVO"           # registra despachos, reingresos, incidencias
    CONSULTA = "CONSULTA"             # solo consulta y reportes
    CUSTODIO = "CUSTODIO"             # responsable de equipos, sin acceso al sistema
