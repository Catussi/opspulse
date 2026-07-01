"""
DAG: dispara la evaluación de reglas de automatización vía API.

Cada 15 minutos llama al endpoint interno que encola la tarea Celery.
"""

from datetime import datetime

from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator

with DAG(
    dag_id="evaluar_reglas_automatizacion",
    description="Evalúa reglas de negocio y webhooks cada 15 minutos",
    start_date=datetime(2026, 1, 1),
    schedule="*/15 * * * *",
    catchup=False,
    tags=["automatizacion", "celery"],
) as dag:
    disparar_evaluacion = HttpOperator(
        task_id="disparar_evaluacion_reglas",
        method="POST",
        http_conn_id="opspulse_api",
        endpoint="/api/v1/automatizacion/evaluar",
    )
