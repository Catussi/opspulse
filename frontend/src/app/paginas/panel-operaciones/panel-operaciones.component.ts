/**
 * Página principal: panel de operaciones con métricas, tabla y carga CSV.
 */

import { CommonModule, CurrencyPipe, DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';

import { Pedido, ResumenPedidos } from '../../nucleo/modelos/pedido.modelo';
import { ServicioApi } from '../../nucleo/servicios/servicio-api';

@Component({
  selector: 'app-panel-operaciones',
  standalone: true,
  imports: [CommonModule, CurrencyPipe, DatePipe],
  templateUrl: './panel-operaciones.component.html',
  styleUrl: './panel-operaciones.component.scss',
})
export class PanelOperacionesComponent implements OnInit {
  private readonly api = inject(ServicioApi);

  /** KPIs cargados desde el backend */
  resumen = signal<ResumenPedidos | null>(null);

  /** Filas de la tabla de pedidos */
  pedidos = signal<Pedido[]>([]);

  /** Mensaje de feedback para el usuario (éxito o error) */
  mensaje = signal<string | null>(null);

  /** Indica si hay una petición en curso */
  cargando = signal(false);

  ngOnInit(): void {
    this.refrescarDatos();
  }

  /** Recarga métricas y tabla desde la API. */
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

  /**
   * Maneja la selección de archivo CSV en el input.
   * Envía el archivo a la API y muestra el mensaje de respuesta.
   */
  alSeleccionarArchivo(evento: Event): void {
    const input = evento.target as HTMLInputElement;
    const archivo = input.files?.[0];
    if (!archivo) {
      return;
    }

    this.cargando.set(true);
    this.mensaje.set(null);

    this.api.subirCsvPedidos(archivo).subscribe({
      next: (respuesta) => {
        this.mensaje.set(`${respuesta.mensaje} (evento #${respuesta.evento_id})`);
        // Esperamos unos segundos a que Celery termine y refrescamos
        setTimeout(() => this.refrescarDatos(), 3000);
      },
      error: () => {
        this.mensaje.set('Error al subir el CSV. Revisa formato y conexión.');
        this.cargando.set(false);
      },
      complete: () => input.value = '',
    });
  }
}
