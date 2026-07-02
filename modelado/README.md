# Modelado — OpsPulse

Scripts y notas para entrenar modelos de machine learning integrados con MLflow.

## Caso de uso

**Predicción de monto de venta** a partir de:

- `producto`
- `region`
- `cantidad`
- `dia_semana` (derivado de `fecha_pedido`)

El modelo es un `RandomForestRegressor` dentro de un pipeline sklearn con `OneHotEncoder` para variables categóricas. Se registra en MLflow como `modelo-prediccion-ventas`.

## Entrenar

### Vía API (recomendado con Docker)

```powershell
# Sincrónico (sin Celery)
curl -X POST "http://localhost:8001/api/v1/ml/entrenar?asincrono=false"

# Asíncrono (worker Celery)
curl -X POST "http://localhost:8001/api/v1/ml/entrenar"
```

### Vía script

```powershell
cd backend
py scripts/entrenar_modelo.py
```

### Requisitos previos

- Al menos **8 pedidos** en PostgreSQL (`py scripts/sembrar_datos.py` o ingesta CSV).
- MLflow corriendo (`http://localhost:5000` con `docker compose up`).

## Predecir

```powershell
curl -X POST "http://localhost:8001/api/v1/ml/predecir-venta" `
  -H "Content-Type: application/json" `
  -d "{\"producto\":\"Laptop Pro 14\",\"cantidad\":2,\"region\":\"Santiago\",\"fecha_pedido\":\"2026-06-10T12:00:00Z\"}"
```

## MLflow UI

Abre http://localhost:5000 para ver experimentos, métricas (MAE, RMSE) y versiones del modelo.

## Airflow

El DAG `entrenar_modelo_ml` (perfil `datos`) re-entrena semanalmente llamando a la API.
