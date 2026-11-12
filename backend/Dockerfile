FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# El script se guarda fuera de /code para que el volumen de desarrollo no lo tape.
# sed quita los finales de línea de Windows por si el archivo se editó allá.
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 8000

# Antes de arrancar: aplica migraciones y carga datos iniciales
ENTRYPOINT ["/entrypoint.sh"]
# --reload: en desarrollo la API se reinicia sola al guardar cambios
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
