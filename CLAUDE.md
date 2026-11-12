# Contexto del proyecto para Claude

Proyecto: sistema web de inventario y trazabilidad de activos TI para Instech (Bogotá),
práctica de Ingeniería de Software (Universidad Manuela Beltrán).

## Arquitectura de 3 capas
- Presentación: Vue 3 + Vite (+ Vue Router y Pinia cuando se necesiten). Interfaz en español.
- Negocio: Python 3.12 + FastAPI + SQLAlchemy 2 + Pydantic v2 + Alembic.
- Datos: PostgreSQL 16.
- Todo se ejecuta con Docker (`docker compose up --build`). Desarrollo en Windows con VS Code. Código en GitHub.

## Requerimientos funcionales
- RF01 Gestión de activos (hoja de vida del equipo): crear, editar, eliminar.
- RF02 Gestión de usuarios con roles y responsables de custodia.
- RF03 Registro de despachos a eventos (actualiza ubicación y responsable).
- RF04 Registro de reingresos con novedades.
- RF05 Control de estado: operativo / en revisión / de baja.
- RF06 Consulta rápida por serial o placa.
- RF07 Bitácora de movimientos por equipo y reportes.

## Reglas de negocio
- RN01: solo se despacha un equipo en estado "operativo".
- RN02: todo movimiento registra fecha, hora y usuario responsable.
- RN03: un reingreso con incidencia pasa el equipo a "en revisión" o "de baja".
- Serial y placa son únicos.

## Convenciones
- Nombres de tablas, campos y mensajes en español.
- Las reglas de negocio viven en `backend/app/services/`, no en los routers.
- Zona horaria America/Bogota.
- Explicar cada paso en español y en lenguaje sencillo: el equipo está aprendiendo.
