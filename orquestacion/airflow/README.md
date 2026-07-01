# Orquestación — Apache Airflow

Airflow programa pipelines que complementan el procesamiento en tiempo real de Celery.

## DAGs

| DAG | Schedule | Acción |
|-----|----------|--------|
| `transformaciones_dbt` | Diario 06:00 | `dbt run` sobre PostgreSQL |
| `evaluar_reglas_automatizacion` | Cada 15 min | `POST /api/v1/automatizacion/evaluar` |

## Levantar Airflow

Requiere la base `airflow` en PostgreSQL. Si el volumen ya existía antes de esta fase:

```powershell
docker compose exec -T postgres psql -U opspulse -d opspulse -f /docker-entrypoint-initdb.d/02-crear-db-airflow.sql
```

Luego:

```powershell
docker compose --profile datos up airflow
```

- **UI:** http://localhost:8081
- **Usuario:** `admin` / `admin`

## Conexión HTTP

El DAG de automatización usa la conexión `opspulse_api` apuntando a `http://api:8000` (configurada por variable de entorno en `docker-compose.yml`).
