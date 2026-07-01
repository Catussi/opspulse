"""Rutas HTTP de la API (controladores)."""

from aplicacion.rutas.rutas_ingesta import router as router_ingesta
from aplicacion.rutas.rutas_metricas import router as router_metricas
from aplicacion.rutas.rutas_pedidos import router as router_pedidos
from aplicacion.rutas.rutas_salud import router as router_salud

__all__ = [
    "router_salud",
    "router_pedidos",
    "router_ingesta",
    "router_metricas",
]
