# Modelo entidad-relación

Basado en el formato **FOR-ADM-002 "Hoja de vida del activo"** de Instech y en los
requerimientos RF01–RF07 y reglas RN01–RN03 del documento de la práctica.

> En VS Code el diagrama se ve con la extensión *Markdown Preview Mermaid Support*
> (`Ctrl + Shift + V`). En GitHub se ve automáticamente.

```mermaid
erDiagram
    CATEGORIAS  ||--o{ ACTIVOS : "clasifica"
    PROVEEDORES |o--o{ ACTIVOS : "vendió"
    UBICACIONES ||--o{ ACTIVOS : "ubicación actual"
    USUARIOS    |o--o{ ACTIVOS : "responsable actual"

    ACTIVOS ||--o{ MOVIMIENTOS    : "historial de traslados"
    ACTIVOS ||--o{ MANTENIMIENTOS : "historial de mantenimiento"
    ACTIVOS ||--o{ INCIDENCIAS    : "novedades"

    UBICACIONES |o--o{ MOVIMIENTOS : "origen"
    UBICACIONES ||--o{ MOVIMIENTOS : "destino"
    USUARIOS    ||--o{ MOVIMIENTOS : "responsable / registra"
    MOVIMIENTOS |o--o{ INCIDENCIAS : "detectada en"
    USUARIOS    ||--o{ INCIDENCIAS : "reporta"
    PROVEEDORES |o--o{ MANTENIMIENTOS : "realiza"
    USUARIOS    ||--o{ MANTENIMIENTOS : "responsable / registra"
    INCIDENCIAS |o--o{ MANTENIMIENTOS : "se atiende con"

    ACTIVOS {
        int id PK
        varchar codigo UK "Código del Activo (placa)"
        varchar serial UK "Serial"
        varchar descripcion "Descripción"
        int categoria_id FK "Categoría"
        varchar marca "Marca"
        varchar modelo "Modelo"
        int ubicacion_id FK "Ubicación"
        int responsable_id FK "Responsable"
        varchar estado "Estado Actual"
        date fecha_compra "Fecha de Compra"
        int proveedor_id FK "Proveedor"
        numeric valor_compra "Valor de Compra"
        int vida_util_meses "Vida Útil Estimada"
        text observaciones
    }
    CATEGORIAS {
        int id PK
        varchar nombre UK
        varchar prefijo_codigo
        bool activa
    }
    PROVEEDORES {
        int id PK
        varchar nombre UK
        varchar nit UK
        varchar contacto
        varchar telefono
        varchar correo
    }
    UBICACIONES {
        int id PK
        varchar codigo UK "identificador del evento (obligatorio en eventos)"
        varchar nombre
        varchar tipo "BODEGA, EVENTO, OFICINA, PROVEEDOR"
        varchar direccion
        varchar cliente "eventos"
        date fecha_inicio "eventos"
        date fecha_fin "eventos"
        bool activa
    }
    USUARIOS {
        int id PK
        varchar nombre "Firmas: Nombre"
        varchar documento UK
        varchar cargo "Firmas: Cargo"
        varchar correo UK
        varchar rol "ADMINISTRADOR, OPERATIVO, CONSULTA, CUSTODIO"
        varchar password_hash
        bool activo
    }
    MOVIMIENTOS {
        int id PK
        int activo_id FK
        varchar tipo "INGRESO_INICIAL, DESPACHO, REINGRESO, TRASLADO, CAMBIO_RESPONSABLE"
        timestamptz fecha "Fecha"
        int origen_id FK "Origen"
        int destino_id FK "Destino"
        int responsable_id FK "Responsable"
        int registrado_por_id FK
        varchar estado_activo
        text observaciones "Observaciones"
    }
    MANTENIMIENTOS {
        int id PK
        int activo_id FK
        varchar tipo "PREVENTIVO, CORRECTIVO"
        timestamptz fecha "Fecha"
        timestamptz fecha_fin
        int proveedor_id FK "Proveedor"
        numeric costo "Costo"
        int responsable_id FK "Responsable"
        int registrado_por_id FK
        text descripcion
        varchar estado_resultante
        int incidencia_id FK
    }
    INCIDENCIAS {
        int id PK
        int activo_id FK
        int movimiento_id FK
        timestamptz fecha
        text descripcion
        varchar severidad "LEVE, MODERADA, GRAVE"
        varchar estado_asignado "nunca ACTIVO (RN03)"
        varchar estado "ABIERTA, CERRADA"
        int reportado_por_id FK
        timestamptz fecha_cierre
        text solucion
    }
```

## Correspondencia con el formato FOR-ADM-002

| Bloque del formato | Tabla |
|---|---|
| 1. Información general | `activos` (+ `categorias`, `proveedores`, `ubicaciones`, `usuarios`) |
| 2. Historial de mantenimiento | `mantenimientos` |
| 3. Historial de traslados | `movimientos` |
| 4. Firmas (nombre y cargo) | `usuarios` |
| — (requerido por el documento: incidencias) | `incidencias` |

## Estados del activo

Se usan los cuatro estados del formato de la empresa. Equivalencia con los del documento de la práctica:

| Formato FOR-ADM-002 | Documento de la práctica |
|---|---|
| Activo | Operativo |
| En Mantenimiento | En revisión |
| De Baja | De baja |
| Perdido / Hurtado | (nuevo) |

## Reglas que garantiza la base de datos

- Serial y código del activo únicos, sin distinguir mayúsculas y minúsculas.
- Solo se aceptan los valores definidos para estados, tipos y roles.
- Una incidencia nunca puede dejar el equipo en estado ACTIVO (RN03).
- Todo evento tiene un código identificador único (sin distinguir mayúsculas y minúsculas).
- Valores y costos no pueden ser negativos.
- Un activo con historial no se puede borrar: se da de baja (se conserva la trazabilidad, ISO/IEC 19770-1).
- Movimientos con fecha, responsable y usuario que registra obligatorios (RN02).

Las reglas que dependen del flujo (RN01: solo se despacha un activo en estado ACTIVO y que esté en bodega)
se aplican en la capa de negocio (`backend/app/services/`) en el siguiente sprint.
