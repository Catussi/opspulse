"""
Servicio de pedidos: lógica de negocio sobre la tabla `pedidos`.

Las rutas HTTP no deberían consultar SQL directamente; delegan aquí.
"""

from sqlalchemy import func, select, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from aplicacion.esquemas.pedido import PedidoCrear, PedidoResumen
from aplicacion.modelos.pedido import Pedido


class ServicioPedidos:
    """Operaciones de lectura y escritura de pedidos."""

    def __init__(self, sesion: Session) -> None:
        self._sesion = sesion

    def crear_pedido(self, datos: PedidoCrear) -> Pedido:
        """
        Inserta un pedido nuevo si el código no existe.

        Raises:
            ValueError: si ya existe un pedido con el mismo codigo_pedido.
        """
        existente = self._sesion.scalar(
            select(Pedido).where(Pedido.codigo_pedido == datos.codigo_pedido)
        )
        if existente:
            raise ValueError(f"El pedido '{datos.codigo_pedido}' ya está registrado.")

        pedido = Pedido(
            codigo_pedido=datos.codigo_pedido,
            producto=datos.producto,
            cantidad=datos.cantidad,
            precio_unitario=datos.precio_unitario,
            region=datos.region,
            fecha_pedido=datos.fecha_pedido,
        )
        self._sesion.add(pedido)
        self._sesion.commit()
        self._sesion.refresh(pedido)
        return pedido

    def listar_pedidos(self, limite: int = 50, desplazamiento: int = 0) -> list[Pedido]:
        """Devuelve pedidos paginados, del más reciente al más antiguo."""
        consulta = (
            select(Pedido)
            .order_by(Pedido.fecha_pedido.desc())
            .offset(desplazamiento)
            .limit(limite)
        )
        return list(self._sesion.scalars(consulta).all())

    def obtener_resumen(self) -> PedidoResumen:
        """
        Calcula KPIs para el dashboard.

        Si existe el mart de dbt (`marts.mart_resumen_pedidos`), lo usa.
        Si no, calcula en línea sobre la tabla operacional.
        """
        resumen_mart = self._obtener_resumen_desde_mart()
        if resumen_mart:
            return resumen_mart

        return self._calcular_resumen_operacional()

    def _obtener_resumen_desde_mart(self) -> PedidoResumen | None:
        """Lee KPIs pre-calculados por dbt, si el mart ya fue materializado."""
        try:
            fila = self._sesion.execute(
                text(
                    """
                    SELECT total_pedidos, monto_total_ventas,
                           producto_mas_vendido, region_top
                    FROM marts.mart_resumen_pedidos
                    LIMIT 1
                    """
                )
            ).first()
        except (ProgrammingError, OperationalError):
            self._sesion.rollback()
            return None

        if not fila:
            return None

        return PedidoResumen(
            total_pedidos=int(fila.total_pedidos),
            monto_total_ventas=round(float(fila.monto_total_ventas), 2),
            producto_mas_vendido=fila.producto_mas_vendido,
            region_top=fila.region_top,
        )

    def _calcular_resumen_operacional(self) -> PedidoResumen:
        """Agregación directa sobre `pedidos` (fallback sin dbt)."""
        total_pedidos = self._sesion.scalar(select(func.count(Pedido.id))) or 0

        monto_total = self._sesion.scalar(
            select(func.sum(Pedido.cantidad * Pedido.precio_unitario))
        ) or 0.0

        # Producto con mayor cantidad vendida
        fila_producto = self._sesion.execute(
            select(Pedido.producto, func.sum(Pedido.cantidad).label("total"))
            .group_by(Pedido.producto)
            .order_by(func.sum(Pedido.cantidad).desc())
            .limit(1)
        ).first()

        # Región con mayor monto vendido
        fila_region = self._sesion.execute(
            select(Pedido.region, func.sum(Pedido.cantidad * Pedido.precio_unitario).label("monto"))
            .group_by(Pedido.region)
            .order_by(func.sum(Pedido.cantidad * Pedido.precio_unitario).desc())
            .limit(1)
        ).first()

        return PedidoResumen(
            total_pedidos=total_pedidos,
            monto_total_ventas=round(float(monto_total), 2),
            producto_mas_vendido=fila_producto[0] if fila_producto else None,
            region_top=fila_region[0] if fila_region else None,
        )
