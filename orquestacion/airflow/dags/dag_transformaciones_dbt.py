"""
DAG: dispara transformaciones dbt vía API → Celery → dbt run.

dbt no corre dentro de Airflow; el worker Celery ejecuta el proyecto
montado en /dbt para evitar conflictos de dependencias en la imagen de Airflow.
"""

from datetime import datetime

from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator

with DAG(
    dag_id="transformaciones_dbt",
    description="Encola dbt run en el worker Celery vía API OpsPulse",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    tags=["dbt", "transformaciones"],
) as dag:
    disparar_dbt = HttpOperator(
        task_id="disparar_dbt_run",
        method="POST",
        http_conn_id="opspulse_api",
        endpoint="/api/v1/transformaciones/ejecutar-dbt",
    )
