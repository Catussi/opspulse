-- Mart de KPIs globales consumido por el dashboard vía API
with base as (
    select * from "opspulse"."staging"."stg_pedidos"
),
producto_top as (
    select producto
    from base
    group by producto
    order by sum(cantidad) desc
    limit 1
),
region_top as (
    select region
    from base
    group by region
    order by sum(monto_total) desc
    limit 1
)
select
    (select count(*) from base) as total_pedidos,
    coalesce((select round(sum(monto_total)::numeric, 2) from base), 0) as monto_total_ventas,
    (select producto from producto_top) as producto_mas_vendido,
    (select region from region_top) as region_top,
    current_timestamp at time zone 'UTC' as actualizado_en