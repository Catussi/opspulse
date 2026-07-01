"""
Pruebas del servicio de pedidos.

Ejecutar desde backend/:
    py -m pytest pruebas/ -v
"""

from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from aplicacion.base_datos import BaseModelo
from aplicacion.esquemas.pedido import PedidoCrear
from aplicacion.modelos.pedido import Pedido  # noqa: F401 — registra tabla en metadata
from aplicacion.servicios.servicio_pedidos import ServicioPedidos


@pytest.fixture
def sesion_prueba() -> Session:
    """Base SQLite en memoria para pruebas rápidas sin Docker."""
    motor = create_engine("sqlite:///:memory:")
    BaseModelo.metadata.create_all(motor)
    Fabrica = sessionmaker(bind=motor)
    sesion = Fabrica()
    yield sesion
    sesion.close()


def test_crear_pedido_y_obtener_resumen(sesion_prueba: Session) -> None:
    """Verifica que un pedido se guarda y aparece en el resumen."""
    servicio = ServicioPedidos(sesion_prueba)

    datos = PedidoCrear(
        codigo_pedido="TEST-001",
        producto="Producto Prueba",
        cantidad=2,
        precio_unitario=1000,
        region="Valparaiso",
        fecha_pedido=datetime.now(timezone.utc),
    )
    pedido = servicio.crear_pedido(datos)
    assert pedido.id is not None

    resumen = servicio.obtener_resumen()
    assert resumen.total_pedidos == 1
    assert resumen.monto_total_ventas == 2000


def test_no_permite_codigo_duplicado(sesion_prueba: Session) -> None:
    """El mismo codigo_pedido debe rechazarse con ValueError."""
    servicio = ServicioPedidos(sesion_prueba)
    datos = PedidoCrear(
        codigo_pedido="DUP-001",
        producto="A",
        cantidad=1,
        precio_unitario=10,
        fecha_pedido=datetime.now(timezone.utc),
    )
    servicio.crear_pedido(datos)

    with pytest.raises(ValueError):
        servicio.crear_pedido(datos)
