"""
Tareas ETL: procesan archivos CSV en segundo plano.

Esta es la pieza que demuestra el patrón Data Engineer:
  raw (CSV) → validación → transformación → carga en PostgreSQL
"""

import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import select

from aplicacion.base_datos import FabricaSesion
from aplicacion.modelos.evento_ingesta import EventoIngesta
from aplicacion.modelos.pedido import Pedido
from aplicacion.trabajos.celery_app import aplicacion_celery

logger = logging.getLogger(__name__)

# Columnas obligatorias que debe traer cualquier CSV de pedidos
COLUMNAS_REQUERIDAS = {
    "codigo_pedido",
    "producto",
    "cantidad",
    "precio_unitario",
    "region",
    "fecha_pedido",
}


def _validar_columnas(df: pd.DataFrame) -> None:
    """Lanza ValueError si faltan columnas en el archivo."""
    faltantes = COLUMNAS_REQUERIDAS - set(df.columns)
    if faltantes:
        raise ValueError(f"Columnas faltantes en CSV: {', '.join(sorted(faltantes))}")


@aplicacion_celery.task(name="etl.procesar_archivo_csv", bind=True, max_retries=3)
def procesar_archivo_csv(self, evento_id: int, ruta_archivo: str) -> dict:
    """
    Tarea Celery: lee un CSV, valida filas e inserta pedidos nuevos.

    Args:
        evento_id: ID del EventoIngesta para actualizar auditoría.
        ruta_archivo: Ruta absoluta al CSV guardado en /datos/crudos.

    Returns:
        Diccionario con contadores de filas procesadas.
    """
    sesion = FabricaSesion()
    filas_exitosas = 0
    filas_rechazadas = 0

    try:
        evento = sesion.get(EventoIngesta, evento_id)
        if not evento:
            raise ValueError(f"Evento de ingesta {evento_id} no encontrado.")

        evento.estado = "procesando"
        sesion.commit()

        # Leer CSV con pandas
        df = pd.read_csv(Path(ruta_archivo))
        _validar_columnas(df)

        for indice, fila in df.iterrows():
            try:
                codigo = str(fila["codigo_pedido"]).strip()

                # Evitar duplicados: si el código ya existe, se rechaza la fila
                ya_existe = sesion.scalar(
                    select(Pedido).where(Pedido.codigo_pedido == codigo)
                )
                if ya_existe:
                    filas_rechazadas += 1
                    continue

                pedido = Pedido(
                    codigo_pedido=codigo,
                    producto=str(fila["producto"]).strip(),
                    cantidad=int(fila["cantidad"]),
                    precio_unitario=float(fila["precio_unitario"]),
                    region=str(fila.get("region", "sin_region")).strip(),
                    fecha_pedido=pd.to_datetime(fila["fecha_pedido"]).to_pydatetime(),
                )
                sesion.add(pedido)
                filas_exitosas += 1

            except (ValueError, TypeError) as error:
                logger.warning("Fila %s rechazada: %s", indice, error)
                filas_rechazadas += 1

        sesion.commit()

        evento.estado = "completado"
        evento.filas_exitosas = filas_exitosas
        evento.filas_rechazadas = filas_rechazadas
        sesion.commit()

        return {
            "evento_id": evento_id,
            "filas_exitosas": filas_exitosas,
            "filas_rechazadas": filas_rechazadas,
        }

    except Exception as error:
        sesion.rollback()
        evento = sesion.get(EventoIngesta, evento_id)
        if evento:
            evento.estado = "error"
            evento.mensaje_error = str(error)
            sesion.commit()

        logger.exception("Error en ETL del evento %s", evento_id)
        raise self.retry(exc=error, countdown=30)

    finally:
        sesion.close()
