# Orquestación — Apache Airflow

Airflow programa pipelines que complementan el procesamiento en tiempo real de Celery.

## DAGs

| DAG | Schedule | Acción |
|-----|----------|--------|
| `transformaciones_dbt` | Diario 06:00 | `POST /api/v1/transformaciones/ejecutar-dbt` → Celery → `dbt run` |
| `evaluar_reglas_automatizacion` | Cada 15 min | `POST /api/v1/automatizacion/evaluar` |

Airflow no ejecuta dbt directamente: solo orquesta llamadas HTTP a la API. El worker Celery corre `dbt run` con el proyecto montado en `/dbt`.

## Levantar Airflow

Requiere la base `airflow` en PostgreSQL. Si el volumen ya existía antes de esta fase:

```powershell
docker compose exec -T postgres psql -U opspulse -d opspulse -f /docker-entrypoint-initdb.d/02-crear-db-airflow.sql
```

Luego (la primera vez puede tardar 2–3 min mientras instala paquetes):

```powershell
docker compose --profile datos up airflow
```

- **UI:** http://localhost:8081
- **Usuario:** `admin` / `admin`

## Conexión HTTP

El DAG de automatización usa la conexión `opspulse_api` apuntando a `http://api:8000` (configurada por variable de entorno en `docker-compose.yml`).
