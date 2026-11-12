"""Datos iniciales del sistema (se pueden ejecutar varias veces sin duplicar).

Uso (con Docker corriendo):
    docker compose exec api python -m app.seed
"""
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Categoria, Ubicacion
from app.models.enums import TipoUbicacion

CATEGORIAS = [
    ("Portátil", "POR"),
    ("Computador de escritorio", "PC"),
    ("Monitor", "MON"),
    ("Tablet", "TAB"),
    ("Celular", "CEL"),
    ("Impresora", "IMP"),
    ("Proyector", "PRY"),
    ("Pantalla / Televisor", "PAN"),
    ("Equipo de red", "RED"),
    ("Radio / Comunicaciones", "RAD"),
    ("Audio", "AUD"),
    ("Lector / Escáner", "LEC"),
    ("UPS / Energía", "UPS"),
    ("Accesorio", "ACC"),
    ("Otro", "OTR"),
]

UBICACIONES = [
    ("Bodega principal", TipoUbicacion.BODEGA),
]


def run() -> None:
    with SessionLocal() as db:
        creadas = 0
        for nombre, prefijo in CATEGORIAS:
            if not db.scalar(select(Categoria).where(Categoria.nombre == nombre)):
                db.add(Categoria(nombre=nombre, prefijo_codigo=prefijo))
                creadas += 1
        for nombre, tipo in UBICACIONES:
            if not db.scalar(select(Ubicacion).where(Ubicacion.nombre == nombre)):
                db.add(Ubicacion(nombre=nombre, tipo=tipo))
                creadas += 1
        db.commit()
        print(f"Datos iniciales listos ({creadas} registros nuevos).")


if __name__ == "__main__":
    run()
