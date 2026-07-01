"""
Rutas de métricas: KPIs agregados para el dashboard Angular.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from aplicacion.base_datos import obtener_sesion
from aplicacion.esquemas.pedido import PedidoResumen
from aplicacion.servicios.servicio_pedidos import ServicioPedidos

router = APIRouter(prefix="/api/v1/metricas", tags=["Métricas"])


@router.get("/resumen-pedidos", response_model=PedidoResumen)
def obtener_resumen_pedidos(sesion: Session = Depends(obtener_sesion)) -> PedidoResumen:
    """
    Devuelve KPIs calculados en el servidor.

    El frontend solo renderiza; no hace agregaciones pesadas.
    """
    servicio = ServicioPedidos(sesion)
    return servicio.obtener_resumen()
