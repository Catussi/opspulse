"""
Rutas de salud: usadas por Docker, Kubernetes y monitoreo.
"""

from fastapi import APIRouter

from aplicacion.configuracion import obtener_configuracion
from aplicacion.esquemas.salud import RespuestaSalud

router = APIRouter(tags=["Salud"])

VERSION_API = "0.1.0"


@router.get("/salud", response_model=RespuestaSalud)
def verificar_salud() -> RespuestaSalud:
    """
    Endpoint liviano: responde 200 si la API está arriba.

    No consulta la base de datos; ideal para health checks rápidos.
    """
    config = obtener_configuracion()
    return RespuestaSalud(
        estado="ok",
        servicio="opspulse-api",
        entorno=config.entorno,
        version=VERSION_API,
    )


@router.get("/salud/listo")
def verificar_listo() -> dict:
    """
  Readiness check: confirma que la app puede atender tráfico.

  En versiones futuras aquí se validará conexión a PostgreSQL y Redis.
  """
    return {"estado": "listo", "mensaje": "La API puede recibir peticiones."}
