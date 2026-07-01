FROM apache/airflow:2.10.4-python3.12

USER root
RUN pip install --no-cache-dir dbt-postgres==1.9.0 apache-airflow-providers-http==4.13.2
USER airflow
