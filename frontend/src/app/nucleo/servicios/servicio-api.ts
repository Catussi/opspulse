/**
 * Cliente HTTP centralizado para la API OpsPulse.
 *
 * Todas las llamadas al backend pasan por aquí para mantener
 * una sola fuente de verdad de URLs y facilitar pruebas.
 */

import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { entorno } from '../../../entornos/entorno';
import {
  Pedido,
  ResumenPedidos,
  ResultadoIngestaCsv,
} from '../modelos/pedido.modelo';

@Injectable({ providedIn: 'root' })
export class ServicioApi {
  private readonly http = inject(HttpClient);
  private readonly base = entorno.urlApi;

  /** KPIs del dashboard. */
  obtenerResumenPedidos(): Observable<ResumenPedidos> {
    return this.http.get<ResumenPedidos>(`${this.base}/api/v1/metricas/resumen-pedidos`);
  }

  /** Lista paginada de pedidos. */
  listarPedidos(limite = 50): Observable<Pedido[]> {
    return this.http.get<Pedido[]>(`${this.base}/api/v1/pedidos`, {
      params: { limite },
    });
  }

  /** Sube un archivo CSV para ingesta asíncrona. */
  subirCsvPedidos(archivo: File): Observable<ResultadoIngestaCsv> {
    const formulario = new FormData();
    formulario.append('archivo', archivo);
    return this.http.post<ResultadoIngestaCsv>(
      `${this.base}/api/v1/ingesta/csv`,
      formulario,
    );
  }
}
