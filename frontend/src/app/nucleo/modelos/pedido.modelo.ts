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

/** Estado de un evento de ingesta (auditoría). */
export interface EventoIngesta {
  id: number;
  fuente: string;
  tipo_fuente: string;
  estado: string;
  filas_exitosas: number;
  filas_rechazadas: number;
  mensaje_error: string | null;
  creado_en: string;
}

/** Entrada para predicción ML de monto de venta. */
export interface PrediccionVentaEntrada {
  producto: string;
  cantidad: number;
  region: string;
  fecha_pedido: string;
}

/** Resultado de predicción ML. */
export interface PrediccionVentaSalida {
  monto_predicho: number;
  modelo: string;
  version_modelo: string | null;
}

/** Respuesta al encolar o completar entrenamiento ML. */
export interface EntrenamientoMlRespuesta {
  mensaje: string;
  tarea_id?: string | null;
  run_id?: string | null;
  metricas?: Record<string, number> | null;
}
