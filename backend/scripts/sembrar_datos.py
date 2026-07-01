"""
Script para cargar datos de demostración en la base de datos.

Uso (desde la carpeta backend/):
    py scripts/sembrar_datos.py
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

# Permite importar el paquete `aplicacion` al ejecutar el script directamente
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import func, select

from aplicacion.base_datos import FabricaSesion, crear_tablas
from aplicacion.modelos.pedido import Pedido
from aplicacion.modelos.regla_automatizacion import ReglaAutomatizacion


def sembrar() -> None:
    """Inserta pedidos y una regla de automatización de ejemplo."""
    crear_tablas()
    sesion = FabricaSesion()

    try:
        cantidad = sesion.scalar(select(func.count()).select_from(Pedido)) or 0
        if cantidad > 0:
            print("La base ya tiene datos. Se omite el seed.")
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
        print("Datos de demostración insertados correctamente.")

    finally:
        sesion.close()


if __name__ == "__main__":
    sembrar()
