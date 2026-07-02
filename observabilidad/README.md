# Observabilidad — OpsPulse

Stack de **Prometheus** + **Grafana** para monitorear la API, Celery y Redis en desarrollo local.

## Levantar

Requiere el stack base (`api`, `redis`, `trabajador`):

```powershell
docker compose --profile observabilidad up --build
```

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| Grafana | http://localhost:3000 | `admin` / `admin` |
| Prometheus | http://localhost:9090 | — |
| Métricas API | http://localhost:8001/metrics | — |
| Celery exporter | http://localhost:9808/metrics | — |

El dashboard **OpsPulse — Operaciones** se provisiona automáticamente en Grafana.

## Qué se monitorea

| Fuente | Métricas |
|--------|----------|
| **FastAPI** | Latencia HTTP, peticiones por ruta, códigos de estado (`GET /metrics`) |
| **Negocio** | `opspulse_ingestas_csv_total`, `opspulse_predicciones_ml_total`, `opspulse_entrenamientos_ml_total` |
| **Celery** | Tareas exitosas/fallidas, workers activos (celery-exporter) |
| **Redis** | Memoria usada, clientes conectados (redis-exporter) |

## Arquitectura

```
API (/metrics) ──┐
Celery exporter ─┼──► Prometheus ──► Grafana
Redis exporter ──┘
```

## Instrumentación en código

- `prometheus-fastapi-instrumentator` en `aplicacion/metricas/instrumentacion.py`
- Contadores de negocio en `aplicacion/metricas/prometheus.py`
- Health checks en `/salud` quedan excluidos de las series HTTP para no generar ruido

## Producción

En AWS el siguiente paso sería scrapear targets desde ECS (Service Discovery) o usar Amazon Managed Prometheus. La configuración de Terraform actual cubre logs en CloudWatch; este stack local modela el patrón previo a un despliegue gestionado.
