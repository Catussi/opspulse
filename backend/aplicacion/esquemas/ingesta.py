"""
Esquemas para ingesta de datos y eventos de auditoría.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class EventoIngestaRespuesta(BaseModel):
    """Estado de un evento de ingesta consultado por la API."""

    id: int
    fuente: str
    tipo_fuente: str
    estado: str
    filas_exitosas: int
    filas_rechazadas: int
    mensaje_error: str | None
    creado_en: datetime

    model_config = {"from_attributes": True}


class ResultadoIngestaCsv(BaseModel):
    """Respuesta inmediata al subir un archivo CSV."""

    evento_id: int
    mensaje: str
    tarea_id: str = Field(..., description="ID de la tarea Celery en segundo plano")
