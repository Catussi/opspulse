"""
Modelo de evento de ingesta.

Cada vez que subimos un CSV o recibimos un webhook, guardamos un registro
de auditoría: qué archivo llegó, cuántas filas se procesaron y si hubo error.
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from aplicacion.base_datos import BaseModelo


class EventoIngesta(BaseModelo):
    """Tabla `eventos_ingesta`: historial de cargas de datos."""

    __tablename__ = "eventos_ingesta"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Nombre del archivo o identificador del webhook
    fuente: Mapped[str] = mapped_column(String(255))

    # Tipo de origen: csv | webhook | api
    tipo_fuente: Mapped[str] = mapped_column(String(32))

    # Estado del procesamiento: pendiente | procesando | completado | error
    estado: Mapped[str] = mapped_column(String(32), default="pendiente")

    # Filas leídas correctamente
    filas_exitosas: Mapped[int] = mapped_column(Integer, default=0)

    # Filas rechazadas por validación
    filas_rechazadas: Mapped[int] = mapped_column(Integer, default=0)

    # Mensaje de error si estado == error
    mensaje_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
