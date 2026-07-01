"""
Tarea Celery: ejecuta transformaciones dbt sobre PostgreSQL.

Airflow dispara esta tarea vía POST /api/v1/transformaciones/ejecutar-dbt
"""

import logging
import subprocess

from aplicacion.trabajos.celery_app import aplicacion_celery

logger = logging.getLogger(__name__)


@aplicacion_celery.task(name="transformaciones.ejecutar_dbt")
def ejecutar_dbt_run() -> dict:
    """
    Corre `dbt run` contra el proyecto montado en /dbt.

    Returns:
        Resultado con código de salida y últimas líneas del log.
    """
    resultado = subprocess.run(
        ["dbt", "run", "--profiles-dir", "/dbt"],
        cwd="/dbt",
        capture_output=True,
        text=True,
        check=False,
    )

    if resultado.returncode != 0:
        logger.error("dbt run falló:\n%s", resultado.stderr)
        raise RuntimeError(f"dbt run terminó con código {resultado.returncode}")

    logger.info("dbt run completado correctamente.")
    return {
        "codigo_salida": resultado.returncode,
        "salida": resultado.stdout[-2000:],
    }
