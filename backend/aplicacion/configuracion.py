"""
Configuración central de OpsPulse.

Lee variables de entorno (o un archivo .env) y las expone como un objeto
tipado. Así evitamos valores mágicos repartidos por todo el código.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    """Parámetros de la aplicación cargados desde el entorno."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Nombre del entorno: desarrollo | pruebas | produccion
    entorno: str = "desarrollo"

    # Cadena de conexión a PostgreSQL
    url_base_datos: str = "postgresql+psycopg://opspulse:opspulse_dev@localhost:5432/opspulse"

    # URL de Redis para Celery y caché
    url_redis: str = "redis://localhost:6379/0"

    # Clave para firmar tokens JWT (cambiar en producción)
    clave_secreta_jwt: str = "cambiar-en-produccion"

    # Orígenes permitidos para CORS (frontend Angular)
    cors_origenes: str = "http://localhost:4200"

    # Carpeta donde se guardan CSV antes del ETL (Docker: /datos/crudos)
    ruta_datos_crudos: str = "/datos/crudos"

    @property
    def lista_cors(self) -> list[str]:
        """Convierte la cadena de orígenes en una lista para FastAPI."""
        return [origen.strip() for origen in self.cors_origenes.split(",")]


@lru_cache
def obtener_configuracion() -> Configuracion:
    """
    Devuelve una instancia única de configuración (patrón singleton).

    El caché evita releer el .env en cada petición HTTP.
    """
    return Configuracion()
