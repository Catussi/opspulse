"""
Tarea Celery: re-entrenar el modelo de predicción de ventas.
"""

from aplicacion.base_datos import FabricaSesion
from aplicacion.ml.entrenamiento import entrenar_y_registrar
from aplicacion.ml.inferencia import invalidar_cache_modelo
from aplicacion.trabajos.celery_app import aplicacion_celery


@aplicacion_celery.task(name="entrenar_modelo_ventas", bind=True)
def entrenar_modelo_ventas(self) -> dict:
    """Lee pedidos de PostgreSQL, entrena y registra el modelo en MLflow."""
    sesion = FabricaSesion()
    try:
        resultado = entrenar_y_registrar(sesion)
        invalidar_cache_modelo()
        return {
            "run_id": resultado.run_id,
            "metricas": resultado.metricas,
            "nombre_modelo": resultado.nombre_modelo,
            "filas_entrenamiento": resultado.filas_entrenamiento,
        }
    finally:
        sesion.close()
