"""
Arranque de base de datos: migraciones Alembic y datos de demostración.
"""

from datetime import datetime, timezone

from alembic import command
from alembic.config import Config
from sqlalchemy import func, select

from aplicacion.base_datos import FabricaSesion, motor
from aplicacion.configuracion import obtener_configuracion
from aplicacion.modelos.pedido import Pedido
from aplicacion.modelos.regla_automatizacion import ReglaAutomatizacion


def ejecutar_migraciones() -> None:
    """Aplica migraciones pendientes con Alembic."""
    configuracion = Config("alembic.ini")
    configuracion.set_main_option(
        "sqlalchemy.url",
        obtener_configuracion().url_base_datos,
    )
    command.upgrade(configuracion, "head")


def sembrar_si_vacio() -> None:
    """Inserta pedidos y reglas de demo si la base está vacía."""
    sesion = FabricaSesion()
    try:
        cantidad = sesion.scalar(select(func.count()).select_from(Pedido)) or 0
        if cantidad > 0:
            return

        pedidos_demo = [
            Pedido(
                codigo_pedido="DEMO-001",
                producto="Auriculares Bluetooth",
                cantidad=5,
                precio_unitario=29990,
                region="Valparaiso",
                fecha_pedido=datetime(2026, 6, 10, 12, 0, tzinfo=timezone.utc),
            ),
            Pedido(
                codigo_pedido="DEMO-002",
                producto="Hub USB-C",
                cantidad=10,
                precio_unitario=15990,
                region="Santiago",
                fecha_pedido=datetime(2026, 6, 11, 9, 30, tzinfo=timezone.utc),
            ),
            Pedido(
                codigo_pedido="PED-001",
                producto="Laptop Pro 14",
                cantidad=2,
                precio_unitario=899990,
                region="Valparaiso",
                fecha_pedido=datetime(2026, 6, 1, 10, 30, tzinfo=timezone.utc),
            ),
            Pedido(
                codigo_pedido="PED-002",
                producto="Mouse Inalambrico",
                cantidad=15,
                precio_unitario=19990,
                region="Santiago",
                fecha_pedido=datetime(2026, 6, 1, 11, 0, tzinfo=timezone.utc),
            ),
            Pedido(
                codigo_pedido="PED-003",
                producto="Teclado Mecanico",
                cantidad=8,
                precio_unitario=45990,
                region="Valparaiso",
                fecha_pedido=datetime(2026, 6, 2, 9, 15, tzinfo=timezone.utc),
            ),
            Pedido(
                codigo_pedido="PED-004",
                producto="Monitor 27 pulgadas",
                cantidad=3,
                precio_unitario=249990,
                region="Santiago",
                fecha_pedido=datetime(2026, 6, 2, 14, 20, tzinfo=timezone.utc),
            ),
            Pedido(
                codigo_pedido="PED-005",
                producto="Webcam HD",
                cantidad=12,
                precio_unitario=34990,
                region="Vina del Mar",
                fecha_pedido=datetime(2026, 6, 3, 16, 45, tzinfo=timezone.utc),
            ),
            Pedido(
                codigo_pedido="PED-006",
                producto="Silla Ergonomica",
                cantidad=4,
                precio_unitario=189990,
                region="Santiago",
                fecha_pedido=datetime(2026, 6, 4, 8, 0, tzinfo=timezone.utc),
            ),
            Pedido(
                codigo_pedido="PED-007",
                producto="Dock Thunderbolt",
                cantidad=6,
                precio_unitario=129990,
                region="Valparaiso",
                fecha_pedido=datetime(2026, 6, 5, 17, 30, tzinfo=timezone.utc),
            ),
        ]

        regla_demo = ReglaAutomatizacion(
            nombre="Alerta ventas bajas del día",
            tipo_condicion="ventas_bajas",
            umbral=500000,
            url_webhook=None,
            activa=True,
            descripcion="Dispara alerta si las ventas totales están bajo $500.000 CLP.",
        )

        sesion.add_all(pedidos_demo)
        sesion.add(regla_demo)
        sesion.commit()
    finally:
        sesion.close()


def preparar_base_datos() -> None:
    """Migraciones + seed de demostración en el arranque de la aplicación."""
    from aplicacion.modelos import evento_ingesta, pedido, regla_automatizacion  # noqa: F401

    _ = (evento_ingesta, pedido, regla_automatizacion)
    ejecutar_migraciones()
    sembrar_si_vacio()
