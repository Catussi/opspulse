/**
 * Cliente HTTP centralizado para la API OpsPulse.
 */

import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { entorno } from '../../../entornos/entorno';
import {
  EntrenamientoMlRespuesta,
  EventoIngesta,
  Pedido,
  PrediccionVentaEntrada,
  PrediccionVentaSalida,
  ResumenPedidos,
  ResultadoIngestaCsv,
} from '../modelos/pedido.modelo';

@Injectable({ providedIn: 'root' })
export class ServicioApi {
  private readonly http = inject(HttpClient);
  private readonly base = entorno.urlApi;

  obtenerResumenPedidos(): Observable<ResumenPedidos> {
    return this.http.get<ResumenPedidos>(`${this.base}/api/v1/metricas/resumen-pedidos`);
  }

  listarPedidos(limite = 50): Observable<Pedido[]> {
    return this.http.get<Pedido[]>(`${this.base}/api/v1/pedidos`, {
      params: new HttpParams().set('limite', limite),
    });
  }

  subirCsvPedidos(archivo: File): Observable<ResultadoIngestaCsv> {
    const formulario = new FormData();
    formulario.append('archivo', archivo);
    return this.http.post<ResultadoIngestaCsv>(
      `${this.base}/api/v1/ingesta/csv`,
      formulario,
    );
  }

  consultarEventoIngesta(eventoId: number): Observable<EventoIngesta> {
    return this.http.get<EventoIngesta>(`${this.base}/api/v1/ingesta/eventos/${eventoId}`);
  }

  predecirVenta(datos: PrediccionVentaEntrada): Observable<PrediccionVentaSalida> {
    return this.http.post<PrediccionVentaSalida>(
      `${this.base}/api/v1/ml/predecir-venta`,
      datos,
    );
  }

  entrenarModelo(sincrono = false): Observable<EntrenamientoMlRespuesta> {
    return this.http.post<EntrenamientoMlRespuesta>(
      `${this.base}/api/v1/ml/entrenar`,
      null,
      { params: new HttpParams().set('asincrono', String(!sincrono)) },
    );
  }
}
