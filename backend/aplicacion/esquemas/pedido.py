"""
Esquemas del dominio Pedido.

Pydantic separa lo que recibe la API (Crear) de lo que devuelve (Respuesta).
Así validamos automáticamente sin mezclar lógica con el modelo ORM.
"""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class PedidoCrear(BaseModel):
    """Datos necesarios para registrar un pedido nuevo."""

    codigo_pedido: str = Field(..., min_length=1, max_length=64, description="ID único del pedido")
    producto: str = Field(..., min_length=1, max_length=200)
    cantidad: int = Field(..., gt=0, description="Debe ser mayor a cero")
    precio_unitario: float = Field(..., ge=0)
    region: str = Field(default="sin_region", max_length=100)
    fecha_pedido: datetime

    @field_validator("codigo_pedido")
    @classmethod
    def codigo_sin_espacios(cls, valor: str) -> str:
        """Evita códigos con espacios accidentales."""
        return valor.strip()


class PedidoRespuesta(BaseModel):
    """Pedido tal como lo ve el cliente de la API."""

    id: int
    codigo_pedido: str
    producto: str
    cantidad: int
    precio_unitario: float
    region: str
    fecha_pedido: datetime
    monto_total: float

    model_config = {"from_attributes": True}


class PedidoResumen(BaseModel):
    """Métricas agregadas para el dashboard."""

    total_pedidos: int
    monto_total_ventas: float
    producto_mas_vendido: str | None
    region_top: str | None
