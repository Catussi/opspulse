"""
Esquemas Pydantic para predicción de ventas con ML.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class PrediccionVentaEntrada(BaseModel):
    """Datos de un pedido hipotético para estimar el monto de venta."""

    producto: str = Field(..., min_length=1, max_length=200, examples=["Laptop Pro 14"])
    cantidad: int = Field(..., ge=1, examples=[3])
    region: str = Field(..., min_length=1, max_length=100, examples=["Santiago"])
    fecha_pedido: datetime = Field(
        ...,
        description="Fecha del pedido; el modelo usa el día de la semana como feature.",
    )


class PrediccionVentaSalida(BaseModel):
    """Resultado de la predicción de monto de venta."""

    monto_predicho: float = Field(..., description="Monto total estimado en CLP.")
    modelo: str = Field(..., description="Nombre del modelo registrado en MLflow.")
    version_modelo: str | None = Field(
        default=None,
        description="Versión del modelo en el Model Registry (si está disponible).",
    )


class EntrenamientoRespuesta(BaseModel):
    """Respuesta al encolar o completar un entrenamiento."""

    mensaje: str
    tarea_id: str | None = None
    run_id: str | None = None
    metricas: dict[str, float] | None = None
