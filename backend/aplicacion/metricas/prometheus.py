"""
Métricas Prometheus personalizadas de OpsPulse.

Las contadores de negocio se exponen junto a las métricas HTTP de la API en GET /metrics.
Las tareas Celery se monitorean vía celery-exporter en el stack de observabilidad.
"""

from prometheus_client import Counter

INGESTAS_CSV = Counter(
    "opspulse_ingestas_csv_total",
    "Ingestas CSV aceptadas por la API",
    ["estado"],
)

PREDICCIONES_ML = Counter(
    "opspulse_predicciones_ml_total",
    "Predicciones de venta servidas por el endpoint ML",
    ["estado"],
)

ENTRENAMIENTOS_ML = Counter(
    "opspulse_entrenamientos_ml_total",
    "Solicitudes de entrenamiento del modelo ML",
    ["modo"],
)
