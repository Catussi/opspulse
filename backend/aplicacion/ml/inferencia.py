"""
Carga del modelo desde MLflow e inferencia de ventas.
"""

from __future__ import annotations

import os
from functools import lru_cache

import mlflow
import pandas as pd
from mlflow.exceptions import MlflowException
from mlflow.pyfunc import PyFuncModel

from aplicacion.configuracion import obtener_configuracion
from aplicacion.esquemas.prediccion import PrediccionVentaEntrada, PrediccionVentaSalida
from aplicacion.ml.entrenamiento import COLUMNAS_FEATURES


class ModeloNoDisponibleError(Exception):
    """El modelo aún no fue entrenado o MLflow no está accesible."""


@lru_cache
def _configurar_mlflow() -> str:
    """Fija el tracking URI una sola vez por proceso."""
    config = obtener_configuracion()
    os.environ.setdefault("MLFLOW_TRACKING_URI", config.url_mlflow)
    mlflow.set_tracking_uri(config.url_mlflow)
    return config.nombre_modelo_ml


@lru_cache
def _cargar_modelo_produccion() -> tuple[PyFuncModel, str | None]:
    """
    Carga la versión Production del modelo registrado.

    Si no hay versión en Production, intenta con la última versión registrada.
    """
    nombre_modelo = _configurar_mlflow()

    try:
        modelo = mlflow.pyfunc.load_model(f"models:/{nombre_modelo}/Production")
        return modelo, "Production"
    except MlflowException:
        pass

    try:
        from mlflow.tracking import MlflowClient

        cliente = MlflowClient()
        versiones = cliente.search_model_versions(f"name='{nombre_modelo}'")
        if not versiones:
            raise ModeloNoDisponibleError(
                f"No hay versiones del modelo '{nombre_modelo}'. "
                "Ejecuta POST /api/v1/ml/entrenar primero."
            )
        ultima = max(versiones, key=lambda v: int(v.version))
        modelo = mlflow.pyfunc.load_model(f"models:/{nombre_modelo}/{ultima.version}")
        return modelo, ultima.version
    except MlflowException as error:
        raise ModeloNoDisponibleError(
            f"No se pudo cargar el modelo desde MLflow: {error}"
        ) from error


def predecir_venta(entrada: PrediccionVentaEntrada) -> PrediccionVentaSalida:
    """Estima el monto total de un pedido con el modelo registrado."""
    config = obtener_configuracion()
    modelo, version = _cargar_modelo_produccion()

    fila = pd.DataFrame(
        [
            {
                "producto": entrada.producto,
                "region": entrada.region,
                "cantidad": entrada.cantidad,
                "dia_semana": entrada.fecha_pedido.weekday(),
            }
        ]
    )

    prediccion = float(modelo.predict(fila[COLUMNAS_FEATURES])[0])

    return PrediccionVentaSalida(
        monto_predicho=round(prediccion, 2),
        modelo=config.nombre_modelo_ml,
        version_modelo=str(version) if version else None,
    )


def invalidar_cache_modelo() -> None:
    """Limpia cachés tras un re-entrenamiento (útil en pruebas)."""
    _configurar_mlflow.cache_clear()
    _cargar_modelo_produccion.cache_clear()
