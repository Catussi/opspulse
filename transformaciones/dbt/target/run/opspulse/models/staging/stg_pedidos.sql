
  create view "opspulse"."staging"."stg_pedidos__dbt_tmp"
    
    
  as (
    -- Capa staging: limpia y tipa los pedidos operacionales
select
    id,
    trim(codigo_pedido) as codigo_pedido,
    trim(producto) as producto,
    cantidad::integer as cantidad,
    precio_unitario::numeric(12, 2) as precio_unitario,
    coalesce(nullif(trim(region), ''), 'sin_region') as region,
    fecha_pedido,
    creado_en,
    round((cantidad * precio_unitario)::numeric, 2) as monto_total
from "opspulse"."public"."pedidos"
  );