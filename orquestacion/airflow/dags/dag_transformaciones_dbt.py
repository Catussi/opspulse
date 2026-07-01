"""
DAG: ejecuta transformaciones dbt sobre PostgreSQL.

Programado diariamente a las 06:00 (America/Santiago).
Materializa staging → intermediate → marts.
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="transformaciones_dbt",
    description="Corre dbt run para actualizar marts analíticos",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    tags=["dbt", "transformaciones"],
) as dag:
    ejecutar_dbt = BashOperator(
        task_id="ejecutar_dbt_run",
        bash_command="cd /opt/dbt && dbt run --profiles-dir /opt/dbt",
    )
