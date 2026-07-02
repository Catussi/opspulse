"""
Rutas de automatización: disparo manual o programado de reglas de negocio.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from aplicacion.base_datos import obtener_sesion
from aplicacion.trabajos.tareas_automatizacion import evaluar_reglas_automatizacion

router = APIRouter(prefix="/api/v1/automatizacion", tags=["Automatización"])


@router.post("/evaluar")
def disparar_evaluacion_reglas(sesion: Session = Depends(obtener_sesion)) -> dict:
    """
    Encola la evaluación de reglas activas en Celery.

    Usado por Airflow y por operadores para forzar una corrida.
    """
    _ = sesion  # reservado para validaciones futuras (ej. auth)
    tarea = evaluar_reglas_automatizacion.delay()
    return {
        "mensaje": "Evaluación de reglas encolada.",
        "tarea_id": tarea.id,
    }
