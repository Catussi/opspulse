"""
Configuración de Celery: cola de trabajos en segundo plano.

Celery usa Redis como broker (mensajes) y backend (resultados).
El trabajador (`trabajador` en docker-compose) ejecuta las tareas definidas aquí.
"""

from celery import Celery

from aplicacion.configuracion import obtener_configuracion

configuracion = obtener_configuracion()

aplicacion_celery = Celery(
    "opspulse",
    broker=configuracion.url_redis,
    backend=configuracion.url_redis,
    include=[
        "aplicacion.trabajos.tareas_etl",
        "aplicacion.trabajos.tareas_automatizacion",
    ],
)

# Configuración recomendada para tareas de ETL
aplicacion_celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Santiago",
    enable_utc=True,
    task_track_started=True,
)
