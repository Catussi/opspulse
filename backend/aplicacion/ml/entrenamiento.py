"""
Entrenamiento del modelo de predicción de ventas.

Lee pedidos históricos de PostgreSQL, entrena un pipeline sklearn y registra
el artefacto en MLflow (tracking + model registry).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from aplicacion.configuracion import obtener_configuracion
from aplicacion.modelos.pedido import Pedido

COLUMNAS_FEATURES = ["producto", "region", "cantidad", "dia_semana"]
COLUMNA_OBJETIVO = "monto_total"
MINIMO_PEDIDOS = 8


@dataclass
class ResultadoEntrenamiento:
    """Resumen del run de entrenamiento."""

    run_id: str
    metricas: dict[str, float]
    nombre_modelo: str
    filas_entrenamiento: int


def _preparar_dataframe(sesion: Session) -> pd.DataFrame:
    """Convierte pedidos de la BD en un DataFrame listo para sklearn."""
    pedidos = sesion.scalars(select(Pedido)).all()
    if len(pedidos) < MINIMO_PEDIDOS:
        raise ValueError(
            f"Se necesitan al menos {MINIMO_PEDIDOS} pedidos para entrenar. "
            f"Hay {len(pedidos)}. Ingesta el CSV de ejemplo o ejecuta el seed."
        )

    filas = [
        {
            "producto": pedido.producto,
            "region": pedido.region,
            "cantidad": pedido.cantidad,
            "dia_semana": pedido.fecha_pedido.weekday(),
            COLUMNA_OBJETIVO: pedido.monto_total,
        }
        for pedido in pedidos
    ]
    return pd.DataFrame(filas)


def _crear_pipeline() -> Pipeline:
    """Pipeline con encoding categórico y regresión Random Forest."""
    preprocesador = ColumnTransformer(
        transformers=[
            (
                "categorias",
                OneHotEncoder(handle_unknown="ignore"),
                ["producto", "region"],
            ),
            ("numericos", "passthrough", ["cantidad", "dia_semana"]),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocesador", preprocesador),
            (
                "modelo",
                RandomForestRegressor(
                    n_estimators=100,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def entrenar_y_registrar(sesion: Session) -> ResultadoEntrenamiento:
    """
    Entrena el modelo con pedidos históricos y lo registra en MLflow.

    Configura MLFLOW_TRACKING_URI desde la configuración de la app.
    """
    config = obtener_configuracion()
    os.environ.setdefault("MLFLOW_TRACKING_URI", config.url_mlflow)
    mlflow.set_tracking_uri(config.url_mlflow)

    df = _preparar_dataframe(sesion)
    x_train, x_test, y_train, y_test = train_test_split(
        df[COLUMNAS_FEATURES],
        df[COLUMNA_OBJETIVO],
        test_size=0.25,
        random_state=42,
    )

    pipeline = _crear_pipeline()

    mlflow.set_experiment(config.experimento_mlflow)

    with mlflow.start_run(run_name="entrenamiento-ventas") as run:
        mlflow.log_param("algoritmo", "RandomForestRegressor")
        mlflow.log_param("filas_totales", len(df))
        mlflow.log_param("filas_entrenamiento", len(x_train))

        pipeline.fit(x_train, y_train)
        predicciones = pipeline.predict(x_test)

        mae = float(mean_absolute_error(y_test, predicciones))
        rmse = float(root_mean_squared_error(y_test, predicciones))
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)

        mlflow.sklearn.log_model(
            pipeline,
            artifact_path="modelo",
            registered_model_name=config.nombre_modelo_ml,
        )

        return ResultadoEntrenamiento(
            run_id=run.info.run_id,
            metricas={"mae": mae, "rmse": rmse},
            nombre_modelo=config.nombre_modelo_ml,
            filas_entrenamiento=len(x_train),
        )
