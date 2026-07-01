"""
Rutas de pedidos: CRUD básico y consultas para el dashboard.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from aplicacion.base_datos import obtener_sesion
from aplicacion.esquemas.pedido import PedidoCrear, PedidoRespuesta
from aplicacion.servicios.servicio_pedidos import ServicioPedidos

router = APIRouter(prefix="/api/v1/pedidos", tags=["Pedidos"])


@router.get("", response_model=list[PedidoRespuesta])
def listar_pedidos(
    limite: int = Query(50, ge=1, le=200, description="Cantidad máxima de resultados"),
    desplazamiento: int = Query(0, ge=0, description="Filas a saltar para paginación"),
    sesion: Session = Depends(obtener_sesion),
) -> list[PedidoRespuesta]:
    """Lista pedidos paginados para la tabla del frontend."""
    servicio = ServicioPedidos(sesion)
    pedidos = servicio.listar_pedidos(limite=limite, desplazamiento=desplazamiento)
    return [
        PedidoRespuesta(
            id=p.id,
            codigo_pedido=p.codigo_pedido,
            producto=p.producto,
            cantidad=p.cantidad,
            precio_unitario=p.precio_unitario,
            region=p.region,
            fecha_pedido=p.fecha_pedido,
            monto_total=p.monto_total,
        )
        for p in pedidos
    ]


@router.post("", response_model=PedidoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    datos: PedidoCrear,
    sesion: Session = Depends(obtener_sesion),
) -> PedidoRespuesta:
    """Registra un pedido individual vía API (útil para integraciones)."""
    servicio = ServicioPedidos(sesion)
    try:
        pedido = servicio.crear_pedido(datos)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error

    return PedidoRespuesta(
        id=pedido.id,
        codigo_pedido=pedido.codigo_pedido,
        producto=pedido.producto,
        cantidad=pedido.cantidad,
        precio_unitario=pedido.precio_unitario,
        region=pedido.region,
        fecha_pedido=pedido.fecha_pedido,
        monto_total=pedido.monto_total,
    )
