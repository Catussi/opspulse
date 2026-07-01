# OpsPulse

Plataforma de operaciones **data-driven** para retail: ingesta de pedidos, procesamiento asíncrono, métricas operativas y reglas de automatización. La construí para integrar en un solo flujo lo que suelo aplicar en backend Python, datos y despliegue con contenedores.

**Autora:** [Catalina E. Barría Otto](https://github.com/Catussi) · [@Catussi](https://github.com/Catussi)

## Qué resuelve

OpsPulse centraliza el ciclo operativo de un negocio de retail:

1. **Ingesta** — carga de pedidos vía CSV o API  
2. **ETL asíncrono** — validación y carga en segundo plano con Celery  
3. **Almacenamiento** — PostgreSQL con trazabilidad de cada carga  
4. **Métricas** — KPIs agregados consumidos por el dashboard  
5. **Automatización** — reglas de negocio con webhooks (alertas por ventas bajas, etc.)

## Stack

| Capa | Tecnología |
|------|------------|
| Backend | Python 3.12, FastAPI, SQLAlchemy, Pydantic |
| Cola de trabajos | Redis, Celery, Flower |
| Base de datos | PostgreSQL 16 |
| Frontend | Angular 19, TypeScript |
| Contenedores | Docker Compose |
| En desarrollo | Apache Airflow, dbt, Terraform (AWS), MLflow |

## Cómo ejecutarlo

### Con Docker (recomendado)

```powershell
docker compose up --build
```

| Servicio | URL |
|----------|-----|
| API y documentación OpenAPI | http://localhost:8001/api/docs |
| Flower (monitoreo Celery) | http://localhost:5555 |
| Frontend Angular | http://localhost:4200 |
| PostgreSQL (desde el host) | `localhost:5433` |

### Probar ingesta de un CSV

```powershell
curl -X POST "http://localhost:8001/api/v1/ingesta/csv" `
  -H "accept: application/json" `
  -H "Content-Type: multipart/form-data" `
  -F "archivo=@datos/ejemplo/pedidos_ejemplo.csv"
```

### Desarrollo local del backend

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.ejemplo .env

py scripts/sembrar_datos.py
py -m uvicorn aplicacion.principal:aplicacion --reload
```

### Frontend

```powershell
cd frontend
npm install
npm start
```

## Estructura del repositorio

```
opspulse/
├── backend/aplicacion/     # API FastAPI
├── frontend/               # Dashboard Angular
├── datos/                  # CSV de ejemplo y archivos crudos
├── docs/                   # Arquitectura y convenciones
├── infra/terraform/        # Infraestructura AWS
├── orquestacion/airflow/   # Pipelines programados
└── transformaciones/dbt/   # Modelos SQL analíticos
```

## Convenciones

El dominio de negocio está nombrado en español (`ServicioPedidos`, `eventos_ingesta`). Los comentarios del código documentan decisiones y flujos, no solo la sintaxis. Detalle en [docs/CONVENCIONES_CODIGO.md](docs/CONVENCIONES_CODIGO.md).

## Documentación adicional

- [Arquitectura y decisiones técnicas](docs/ARQUITECTURA.md)
