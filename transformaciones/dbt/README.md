# Transformaciones dbt — OpsPulse

Modelos SQL que separan la capa operacional (`public.pedidos`) de las vistas analíticas consumidas por la API.

## Capas

| Esquema | Modelo | Descripción |
|---------|--------|-------------|
| `staging` | `stg_pedidos` | Limpieza y tipado de pedidos |
| `intermediate` | `int_ventas_diarias` | Agregados por día y región |
| `marts` | `mart_resumen_pedidos` | KPIs globales para el dashboard |
| `marts` | `mart_ventas_diarias` | Serie temporal de ventas |

## Ejecutar

Con el stack Docker arriba:

```powershell
# Desde la raíz del proyecto
docker compose run --rm dbt run

# O con el script
.\scripts\ejecutar_dbt.ps1
```

Después de `dbt run`, el endpoint `/api/v1/metricas/resumen-pedidos` lee `marts.mart_resumen_pedidos` automáticamente.

## Verificar

```powershell
docker compose exec postgres psql -U opspulse -d opspulse -c "SELECT * FROM marts.mart_resumen_pedidos;"
```
