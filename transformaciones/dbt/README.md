# Transformaciones — dbt

Modelos SQL analíticos sobre PostgreSQL. Separan la capa operacional (tablas que escribe la API) de las vistas agregadas que consume el dashboard.

## Capas previstas

```
staging/stg_pedidos.sql       -- Limpieza y tipado desde tabla raw
intermediate/int_ventas.sql   -- Agregados por día y región
marts/mart_kpi_diario.sql     -- KPIs diarios para el panel
```

dbt correrá contra la misma instancia PostgreSQL en desarrollo y contra RDS en producción.
