#!/bin/sh
# Se ejecuta cada vez que arranca el contenedor de la API.
set -e

echo ">> Aplicando migraciones de la base de datos..."
alembic upgrade head

echo ">> Cargando datos iniciales..."
python -m app.seed

echo ">> Iniciando la API..."
exec "$@"
