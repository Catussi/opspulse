"""Esquemas para endpoints de salud y monitoreo."""

from pydantic import BaseModel


class RespuestaSalud(BaseModel):
    """Respuesta estándar de /salud — usada por Docker y balanceadores."""

    estado: str
    servicio: str
    entorno: str
    version: str
