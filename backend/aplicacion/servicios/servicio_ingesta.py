"""
Servicio de ingesta: registra eventos y delega el procesamiento a Celery.

Flujo:
  1. El usuario sube un CSV por la API.
  2. Guardamos un EventoIngesta con estado 'pendiente'.
  3. Encolamos una tarea Celery que procesa el archivo en segundo plano.
"""

import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from aplicacion.configuracion import obtener_configuracion
from aplicacion.modelos.evento_ingesta import EventoIngesta
from aplicacion.trabajos.tareas_etl import procesar_archivo_csv


class ServicioIngesta:
    """Coordina la recepción de archivos y el encolado de trabajos ETL."""

    def __init__(self, sesion: Session) -> None:
        self._sesion = sesion

    def registrar_ingesta_csv(self, nombre_archivo: str, contenido: bytes) -> tuple[EventoIngesta, str]:
        """
        Guarda el CSV en disco, crea el evento de auditoría y encola el ETL.

        Returns:
            Tupla (evento, id_tarea_celery)
        """
        # Carpeta configurable: en Docker es /datos/crudos; en local puede ser relativa
        carpeta_crudos = Path(obtener_configuracion().ruta_datos_crudos)
        carpeta_crudos.mkdir(parents=True, exist_ok=True)

        # Nombre único para evitar colisiones si suben el mismo archivo dos veces
        nombre_unico = f"{uuid.uuid4().hex}_{nombre_archivo}"
        ruta_archivo = carpeta_crudos / nombre_unico
        ruta_archivo.write_bytes(contenido)

        evento = EventoIngesta(
            fuente=nombre_unico,
            tipo_fuente="csv",
            estado="pendiente",
        )
        self._sesion.add(evento)
        self._sesion.commit()
        self._sesion.refresh(evento)

        # Encolar procesamiento asíncrono (no bloquea la respuesta HTTP)
        resultado_tarea = procesar_archivo_csv.delay(
            evento_id=evento.id,
            ruta_archivo=str(ruta_archivo),
        )

        return evento, resultado_tarea.id
