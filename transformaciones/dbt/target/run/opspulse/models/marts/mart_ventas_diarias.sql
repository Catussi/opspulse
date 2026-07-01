
  
    

  create  table "opspulse"."marts"."mart_ventas_diarias__dbt_tmp"
  
  
    as
  
  (
    -- Serie diaria de ventas para reportes y gráficos futuros
select
    fecha,
    sum(total_pedidos) as total_pedidos,
    sum(unidades_vendidas) as unidades_vendidas,
    round(sum(monto_total)::numeric, 2) as monto_total
from "opspulse"."intermediate"."int_ventas_diarias"
group by fecha
order by fecha desc
  );
  