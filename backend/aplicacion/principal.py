"""
Punto de entrada de la API OpsPulse (FastAPI).

Aquí se ensamblan rutas, CORS y el ciclo de vida de la aplicación.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aplicacion.base_datos import crear_tablas
from aplicacion.configuracion import obtener_configuracion
from aplicacion.metricas.instrumentacion import configurar_metricas_http
from aplicacion.rutas import (
    router_automatizacion,
    router_ingesta,
    router_metricas,
    router_pedidos,
    router_salud,
    router_ml,
    router_transformaciones,
)


@asynccontextmanager
async def ciclo_vida_aplicacion(_: FastAPI):
    """
    Se ejecuta al arrancar y al apagar el servidor.

    Al iniciar: crea tablas si no existen (desarrollo).
    """
    crear_tablas()
    yield


def crear_aplicacion() -> FastAPI:
    """Fábrica de la app FastAPI — facilita pruebas unitarias."""
    config = obtener_configuracion()

    app = FastAPI(
        title="OpsPulse API",
        description=(
            "Plataforma de operaciones data-driven: ingesta, ETL, métricas "
            "y automatización para retail/logística."
        ),
        version="0.1.0",
        lifespan=ciclo_vida_aplicacion,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    # Permite que el frontend Angular (puerto 4200) consuma la API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.lista_cors,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Registrar routers (cada módulo agrupa rutas relacionadas)
    app.include_router(router_salud)
    app.include_router(router_pedidos)
    app.include_router(router_ingesta)
    app.include_router(router_metricas)
    app.include_router(router_automatizacion)
    app.include_router(router_transformaciones)
    app.include_router(router_ml)

    configurar_metricas_http(app)

    return app


# Instancia usada por uvicorn: uvicorn aplicacion.principal:aplicacion
aplicacion = crear_aplicacion()
