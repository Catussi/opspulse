/** Representa un pedido devuelto por la API. */
export interface Pedido {
  id: number;
  codigo_pedido: string;
  producto: string;
  cantidad: number;
  precio_unitario: number;
  region: string;
  fecha_pedido: string;
  monto_total: number;
}

/** KPIs agregados para el panel principal. */
export interface ResumenPedidos {
  total_pedidos: number;
  monto_total_ventas: number;
  producto_mas_vendido: string | null;
  region_top: string | null;
}

/** Respuesta al subir un CSV. */
export interface ResultadoIngestaCsv {
  evento_id: number;
  mensaje: string;
  tarea_id: string;
}
