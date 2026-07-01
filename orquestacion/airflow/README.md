# Orquestación — Apache Airflow

DAGs programados para complementar el procesamiento en tiempo real de Celery. En el MVP las tareas asíncronas las cubre Celery; Airflow entrará para pipelines con dependencias y horarios fijos.

## DAGs planificados

| DAG | Frecuencia | Descripción |
|-----|------------|-------------|
| `etl_pedidos_diario` | Diario 06:00 | Reprocesa CSV pendientes en S3 |
| `evaluar_reglas` | Cada 15 min | Ejecuta `automatizacion.evaluar_reglas` |
| `entrenar_modelo_demanda` | Semanal | Entrenamiento y registro en MLflow |

Los DAGs vivirán en `orquestacion/airflow/dags/` cuando estén implementados.
