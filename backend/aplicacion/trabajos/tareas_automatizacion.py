"""
Tareas de automatización ejecutadas por el trabajador Celery.

Se pueden programar con Celery Beat o disparar manualmente desde la API.
"""

import logging

from aplicacion.base_datos import FabricaSesion
from aplicacion.servicios.servicio_automatizacion import ServicioAutomatizacion
from aplicacion.trabajos.celery_app import aplicacion_celery

logger = logging.getLogger(__name__)


@aplicacion_celery.task(name="automatizacion.evaluar_reglas")
def evaluar_reglas_automatizacion() -> list[str]:
    """
    Evalúa todas las reglas activas y envía webhooks si corresponde.

    Pensada para ejecutarse cada X minutos vía Celery Beat o Airflow.
    """
    sesion = FabricaSesion()
    try:
        servicio = ServicioAutomatizacion(sesion)
        resultados = servicio.ejecutar_evaluacion_completa()
        logger.info("Evaluación de reglas completada: %s", resultados)
        return resultados
    finally:
        sesion.close()
