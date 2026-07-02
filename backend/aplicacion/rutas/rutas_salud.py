"""
Rutas de salud: usadas por Docker, Kubernetes y monitoreo.
"""

import redis
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from aplicacion.base_datos import obtener_sesion
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
def verificar_listo(sesion: Session = Depends(obtener_sesion)) -> dict:
    """
    Readiness check: valida PostgreSQL y Redis antes de recibir tráfico.
    """
    config = obtener_configuracion()
    dependencias: dict[str, str] = {}

    try:
        sesion.execute(text("SELECT 1"))
        dependencias["postgres"] = "ok"
    except Exception as error:
        dependencias["postgres"] = f"error: {error}"

    try:
        cliente_redis = redis.from_url(config.url_redis)
        cliente_redis.ping()
        dependencias["redis"] = "ok"
    except Exception as error:
        dependencias["redis"] = f"error: {error}"

    if all(valor == "ok" for valor in dependencias.values()):
        return {
            "estado": "listo",
            "mensaje": "La API puede recibir peticiones.",
            "dependencias": dependencias,
        }

    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={
            "estado": "no_listo",
            "dependencias": dependencias,
        },
    )
