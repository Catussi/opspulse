"""
DAG: re-entrenamiento semanal del modelo de predicción de ventas.

Llama POST /api/v1/ml/entrenar para encolar el entrenamiento en Celery.
"""

from datetime import datetime

from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator

with DAG(
    dag_id="entrenar_modelo_ml",
    description="Re-entrena el modelo de ventas con pedidos históricos",
    schedule="0 3 * * 0",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ml", "opspulse"],
) as dag:
    disparar_entrenamiento = SimpleHttpOperator(
        task_id="entrenar_modelo_ventas",
        http_conn_id="opspulse_api",
        endpoint="/api/v1/ml/entrenar",
        method="POST",
        headers={"Content-Type": "application/json"},
        log_response=True,
    )
