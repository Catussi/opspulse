"""
Configuración de métricas HTTP con prometheus-fastapi-instrumentator.
"""

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def configurar_metricas_http(app: FastAPI) -> None:
    """
    Expone GET /metrics con latencia, códigos HTTP y tamaño de respuestas.

    Excluye health checks y el propio endpoint de métricas para no inflar series.
    """
    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        excluded_handlers=[
            "/metrics",
            "/salud",
            "/salud/listo",
        ],
    ).instrument(app).expose(
        app,
        endpoint="/metrics",
        include_in_schema=False,
    )
