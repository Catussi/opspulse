"""
Modelo de pedido de venta.

Representa una fila del negocio: cada pedido tiene producto, cantidad,
precio y fecha. Es la entidad central del dashboard operativo.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from aplicacion.base_datos import BaseModelo


class Pedido(BaseModelo):
    """Tabla `pedidos`: ventas registradas por ingesta CSV o API."""

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Identificador externo del pedido (ej. desde ERP o CSV)
    codigo_pedido: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    # Nombre del producto vendido
    producto: Mapped[str] = mapped_column(String(200), index=True)

    # Unidades vendidas
    cantidad: Mapped[int] = mapped_column(Integer)

    # Precio unitario en la moneda del negocio
    precio_unitario: Mapped[float] = mapped_column(Float)

    # Región o tienda de origen (útil para analítica)
    region: Mapped[str] = mapped_column(String(100), default="sin_region")

    # Momento en que se registró el pedido en el sistema origen
    fecha_pedido: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Momento en que OpsPulse ingirió el registro
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    @property
    def monto_total(self) -> float:
        """Calcula el total del pedido (cantidad × precio)."""
        return round(self.cantidad * self.precio_unitario, 2)
