-- Ventas agregadas por día y región (capa intermedia)
select
    date_trunc('day', fecha_pedido)::date as fecha,
    region,
    count(*) as total_pedidos,
    sum(cantidad) as unidades_vendidas,
    round(sum(monto_total)::numeric, 2) as monto_total
from {{ ref('stg_pedidos') }}
group by 1, 2
