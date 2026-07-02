"""
Rutas de machine learning: entrenamiento y predicción de ventas.
"""

from fastapi import APIRouter, HTTPException, status
from aplicacion.esquemas.prediccion import (
    EntrenamientoRespuesta,
    PrediccionVentaEntrada,
    PrediccionVentaSalida,
)
from aplicacion.ml.entrenamiento import entrenar_y_registrar
from aplicacion.ml.inferencia import ModeloNoDisponibleError, invalidar_cache_modelo, predecir_venta
from aplicacion.metricas.prometheus import ENTRENAMIENTOS_ML, PREDICCIONES_ML
from aplicacion.trabajos.tareas_ml import entrenar_modelo_ventas

router = APIRouter(prefix="/api/v1/ml", tags=["Machine Learning"])


@router.post("/predecir-venta", response_model=PrediccionVentaSalida)
def predecir_monto_venta(entrada: PrediccionVentaEntrada) -> PrediccionVentaSalida:
    """
    Predice el monto total de un pedido con el modelo registrado en MLflow.

    Requiere haber entrenado previamente vía POST /entrenar.
    """
    try:
        salida = predecir_venta(entrada)
        PREDICCIONES_ML.labels(estado="exito").inc()
        return salida
    except ModeloNoDisponibleError as error:
        PREDICCIONES_ML.labels(estado="modelo_no_disponible").inc()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error


@router.post("/entrenar", response_model=EntrenamientoRespuesta)
def disparar_entrenamiento(asincrono: bool = True) -> EntrenamientoRespuesta:
    """
    Entrena el modelo de ventas con pedidos históricos.

    Por defecto encola la tarea en Celery. Con `asincrono=false` entrena en la misma petición
    (útil en desarrollo sin worker).
    """
    if asincrono:
        tarea = entrenar_modelo_ventas.delay()
        ENTRENAMIENTOS_ML.labels(modo="asincrono").inc()
        return EntrenamientoRespuesta(
            mensaje="Entrenamiento del modelo encolado en Celery.",
            tarea_id=tarea.id,
        )

    from aplicacion.base_datos import FabricaSesion

    sesion = FabricaSesion()
    try:
        resultado = entrenar_y_registrar(sesion)
        invalidar_cache_modelo()
        ENTRENAMIENTOS_ML.labels(modo="sincrono").inc()
        return EntrenamientoRespuesta(
            mensaje="Modelo entrenado y registrado en MLflow.",
            run_id=resultado.run_id,
            metricas=resultado.metricas,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error
    finally:
        sesion.close()
