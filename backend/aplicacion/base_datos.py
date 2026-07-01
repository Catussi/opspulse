"""
Conexión a PostgreSQL mediante SQLAlchemy.

Aquí definimos la fábrica de sesiones que usan los servicios y las rutas
para leer y escribir en la base de datos.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from aplicacion.configuracion import obtener_configuracion

configuracion = obtener_configuracion()

# Motor de conexión: pool_pre_ping verifica que la conexión siga viva
motor = create_engine(
    configuracion.url_base_datos,
    pool_pre_ping=True,
)

# Fábrica de sesiones: cada petición HTTP obtiene su propia sesión
FabricaSesion = sessionmaker(autocommit=False, autoflush=False, bind=motor)


class BaseModelo(DeclarativeBase):
    """Clase base para todos los modelos ORM (tablas de la base de datos)."""

    pass


def obtener_sesion() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI: abre una sesión y la cierra al terminar.

    Uso en rutas:
        def mi_ruta(sesion: Session = Depends(obtener_sesion)):
            ...
    """
    sesion = FabricaSesion()
    try:
        yield sesion
    finally:
        sesion.close()


def crear_tablas() -> None:
    """
    Crea las tablas si no existen.

    En producción se prefiere Alembic para migraciones versionadas;
    esto facilita el arranque rápido en desarrollo.
    """
    # Importamos modelos para que SQLAlchemy los registre
    from aplicacion.modelos import evento_ingesta, pedido, regla_automatizacion  # noqa: F401

    BaseModelo.metadata.create_all(bind=motor)
