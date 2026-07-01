"""
Modelo de regla de automatización.

Permite definir condiciones de negocio del tipo:
  "Si ventas del día < umbral → enviar alerta por webhook".

Es el núcleo del módulo de automatización de procesos.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from aplicacion.base_datos import BaseModelo


class ReglaAutomatizacion(BaseModelo):
    """Tabla `reglas_automatizacion`: reglas configurables por el usuario."""

    __tablename__ = "reglas_automatizacion"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Nombre legible para el panel de administración
    nombre: Mapped[str] = mapped_column(String(150))

    # Tipo de condición: ventas_bajas | stock_bajo | anomalia_ml
    tipo_condicion: Mapped[str] = mapped_column(String(64))

    # Valor numérico umbral (ej. monto mínimo de ventas diarias)
    umbral: Mapped[float] = mapped_column(Float)

    # URL a la que se envía el webhook cuando se dispara la regla
    url_webhook: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Si la regla está activa o pausada
    activa: Mapped[bool] = mapped_column(Boolean, default=True)

    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
