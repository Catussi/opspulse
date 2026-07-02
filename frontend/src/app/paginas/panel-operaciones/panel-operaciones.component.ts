/**
 * Página principal: panel de operaciones con métricas, ingesta, ML y pedidos.
 */

import { CommonModule, CurrencyPipe, DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import {
  Pedido,
  PrediccionVentaSalida,
  ResumenPedidos,
} from '../../nucleo/modelos/pedido.modelo';
import { ServicioApi } from '../../nucleo/servicios/servicio-api';

@Component({
  selector: 'app-panel-operaciones',
  standalone: true,
  imports: [CommonModule, CurrencyPipe, DatePipe, FormsModule],
  templateUrl: './panel-operaciones.component.html',
  styleUrl: './panel-operaciones.component.scss',
})
export class PanelOperacionesComponent implements OnInit {
  private readonly api = inject(ServicioApi);

  resumen = signal<ResumenPedidos | null>(null);
  pedidos = signal<Pedido[]>([]);
  mensaje = signal<string | null>(null);
  cargando = signal(false);
  estadoIngesta = signal<string | null>(null);

  mlProducto = 'Laptop Pro 14';
  mlCantidad = 2;
  mlRegion = 'Santiago';
  mlFecha = '2026-06-10T12:00';
  prediccion = signal<PrediccionVentaSalida | null>(null);
  entrenandoMl = signal(false);

  ngOnInit(): void {
    this.refrescarDatos();
  }

  refrescarDatos(): void {
    this.cargando.set(true);
    this.api.obtenerResumenPedidos().subscribe({
      next: (datos) => this.resumen.set(datos),
      error: () => this.mensaje.set('No se pudo cargar el resumen. ¿Está la API arriba?'),
    });

    this.api.listarPedidos().subscribe({
      next: (lista) => this.pedidos.set(lista),
      error: () => this.mensaje.set('No se pudo cargar la lista de pedidos.'),
      complete: () => this.cargando.set(false),
    });
  }

  alSeleccionarArchivo(evento: Event): void {
    const input = evento.target as HTMLInputElement;
    const archivo = input.files?.[0];
    if (!archivo) {
      return;
    }

    this.cargando.set(true);
    this.mensaje.set(null);
    this.estadoIngesta.set('Enviando archivo…');

    this.api.subirCsvPedidos(archivo).subscribe({
      next: (respuesta) => {
        this.mensaje.set(respuesta.mensaje);
        this.seguirEventoIngesta(respuesta.evento_id);
      },
      error: () => {
        this.mensaje.set('Error al subir el CSV. Revisa formato y conexión.');
        this.estadoIngesta.set(null);
        this.cargando.set(false);
      },
      complete: () => {
        input.value = '';
      },
    });
  }

  private seguirEventoIngesta(eventoId: number, intento = 0): void {
    if (intento > 25) {
      this.estadoIngesta.set('Tiempo de espera agotado. Revisa Flower o Celery.');
      this.cargando.set(false);
      return;
    }

    this.api.consultarEventoIngesta(eventoId).subscribe({
      next: (evento) => {
        this.estadoIngesta.set(
          `Evento #${evento.id}: ${evento.estado} — ${evento.filas_exitosas} filas OK, ${evento.filas_rechazadas} rechazadas`,
        );

        if (evento.estado === 'completado') {
          this.mensaje.set(`Ingesta completada (${evento.filas_exitosas} pedidos).`);
          this.refrescarDatos();
          return;
        }

        if (evento.estado === 'error') {
          this.mensaje.set(evento.mensaje_error ?? 'Error en el procesamiento del CSV.');
          this.cargando.set(false);
          return;
        }

        setTimeout(() => this.seguirEventoIngesta(eventoId, intento + 1), 2000);
      },
      error: () => {
        this.estadoIngesta.set('No se pudo consultar el estado de la ingesta.');
        this.cargando.set(false);
      },
    });
  }

  predecirVenta(): void {
    this.cargando.set(true);
    this.prediccion.set(null);

    this.api
      .predecirVenta({
        producto: this.mlProducto,
        cantidad: this.mlCantidad,
        region: this.mlRegion,
        fecha_pedido: new Date(this.mlFecha).toISOString(),
      })
      .subscribe({
        next: (resultado) => {
          this.prediccion.set(resultado);
          this.mensaje.set('Predicción generada correctamente.');
        },
        error: () => {
          this.mensaje.set(
            'No se pudo predecir. Entrena el modelo primero (botón Entrenar modelo).',
          );
        },
        complete: () => this.cargando.set(false),
      });
  }

  entrenarModelo(): void {
    this.entrenandoMl.set(true);
    this.mensaje.set('Entrenando modelo en la API…');

    this.api.entrenarModelo(true).subscribe({
      next: (respuesta) => {
        const metricas = respuesta.metricas
          ? ` MAE: ${respuesta.metricas['mae']?.toFixed(0)}`
          : '';
        this.mensaje.set(`${respuesta.mensaje}${metricas}`);
      },
      error: () => this.mensaje.set('Falló el entrenamiento. ¿MLflow está arriba?'),
      complete: () => this.entrenandoMl.set(false),
    });
  }
}
