"""
Pruebas de endpoints de salud y readiness.
"""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from aplicacion.base_datos import BaseModelo, obtener_sesion
from aplicacion.modelos.pedido import Pedido  # noqa: F401
from aplicacion.principal import crear_aplicacion


def test_salud_liviano() -> None:
    cliente = TestClient(crear_aplicacion())
    respuesta = cliente.get("/salud")
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "ok"


@patch("aplicacion.rutas.rutas_salud.redis.from_url")
def test_salud_listo_con_dependencias(mock_redis: MagicMock) -> None:
    mock_redis.return_value.ping.return_value = True

    motor = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    BaseModelo.metadata.create_all(motor)
    fabrica = sessionmaker(bind=motor)
    app = crear_aplicacion()

    def sesion_prueba() -> Session:
        sesion = fabrica()
        try:
            yield sesion
        finally:
            sesion.close()

    app.dependency_overrides[obtener_sesion] = sesion_prueba
    cliente = TestClient(app)

    respuesta = cliente.get("/salud/listo")
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "listo"
    assert cuerpo["dependencias"]["postgres"] == "ok"
    assert cuerpo["dependencias"]["redis"] == "ok"
