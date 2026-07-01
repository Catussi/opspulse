"""
Rutas para disparar transformaciones dbt desde la API o Airflow.
"""

from fastapi import APIRouter

from aplicacion.trabajos.tareas_dbt import ejecutar_dbt_run

router = APIRouter(prefix="/api/v1/transformaciones", tags=["Transformaciones"])


@router.post("/ejecutar-dbt")
def disparar_dbt() -> dict:
    """
    Encola `dbt run` en el worker Celery.

    Airflow llama este endpoint en el DAG `transformaciones_dbt`.
    """
    tarea = ejecutar_dbt_run.delay()
    return {
        "mensaje": "Transformaciones dbt encoladas.",
        "tarea_id": tarea.id,
    }
