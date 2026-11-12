# Instech · Sistema de inventario y trazabilidad de activos TI

Sistema web para registrar despachos, reingresos e incidencias de los equipos tecnológicos
de Instech y consultar de inmediato su ubicación (bodega o evento) y su estado
(operativo, en revisión o de baja).

## Arquitectura (3 capas)

| Capa | Tecnología | Carpeta | URL local |
|---|---|---|---|
| Presentación | Vue 3 + Vite | `frontend/` | http://localhost:5173 |
| Negocio | Python 3.12 + FastAPI | `backend/` | http://localhost:8000/docs |
| Datos | PostgreSQL 16 | (contenedor `db`) | localhost:5432 |

Las tres capas corren en contenedores Docker y se levantan con `docker compose`.

## Requisitos (Windows)

- [Git](https://git-scm.com/download/win)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (activar WSL 2 cuando lo pida)

## Cómo levantar el proyecto

Abre la carpeta en VS Code y abre una terminal (`Ctrl + ñ` o menú *Terminal → New Terminal*):

```powershell
# 1. Crear el archivo de variables (solo la primera vez)
copy .env.example .env

# 2. Construir y levantar las 3 capas
docker compose up --build
```

La primera vez tarda unos minutos porque descarga las imágenes. Cuando veas
`Uvicorn running on http://0.0.0.0:8000` y `VITE ... ready`, abre:

- Interfaz: http://localhost:5173 → debe mostrar las 3 capas en verde.
- Documentación de la API (Swagger): http://localhost:8000/docs

## Comandos útiles

```powershell
docker compose up -d          # levantar en segundo plano
docker compose logs -f api    # ver los mensajes de la API
docker compose ps             # ver qué contenedores están corriendo
docker compose down           # apagar (los datos se conservan)
docker compose down -v        # apagar y BORRAR la base de datos
```

## Estructura

```
backend/
  app/
    main.py        punto de entrada de la API
    config.py      configuración desde .env
    database.py    conexión a PostgreSQL
  Dockerfile
  requirements.txt
frontend/
  src/
    App.vue        pantalla principal
    main.js
  vite.config.js   redirige /api → FastAPI
  Dockerfile
docker-compose.yml
.env.example
```

## Plan de desarrollo (Scrum, 12 sprints)

1. Estructura base y Docker ✅
2. Modelo entidad-relación y migraciones
3. API de activos, usuarios y autenticación
4. Despachos, reingresos, incidencias y reglas de negocio
5. Interfaz en Vue
6. Migración de datos desde Excel
7. Despliegue en producción y manuales
