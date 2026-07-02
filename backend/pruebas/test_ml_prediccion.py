"""
Pruebas del pipeline de ML: entrenamiento e inferencia con MLflow local.
"""

from __future__ import annotations

import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from aplicacion.base_datos import BaseModelo
from aplicacion.configuracion import obtener_configuracion
from aplicacion.esquemas.prediccion import PrediccionVentaEntrada
from aplicacion.modelos.pedido import Pedido  # noqa: F401
from aplicacion.ml.entrenamiento import entrenar_y_registrar
from aplicacion.ml.inferencia import invalidar_cache_modelo, predecir_venta


@pytest.fixture
def sesion_con_pedidos() -> Session:
    """SQLite en memoria con pedidos suficientes para entrenar."""
    motor = create_engine("sqlite:///:memory:")
    BaseModelo.metadata.create_all(motor)
    fabrica = sessionmaker(bind=motor)
    sesion = fabrica()

    productos = [
        ("Laptop", "Santiago", 2, 500000),
        ("Mouse", "Valparaiso", 10, 15000),
        ("Teclado", "Santiago", 5, 40000),
        ("Monitor", "Vina del Mar", 3, 200000),
        ("Webcam", "Santiago", 8, 30000),
        ("Hub", "Valparaiso", 12, 12000),
        ("Dock", "Santiago", 4, 90000),
        ("Silla", "Santiago", 1, 250000),
        ("Auriculares", "Valparaiso", 6, 25000),
    ]
    for indice, (producto, region, cantidad, precio) in enumerate(productos, start=1):
        sesion.add(
            Pedido(
                codigo_pedido=f"ML-{indice:03d}",
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio,
                region=region,
                fecha_pedido=datetime(2026, 6, indice % 7 + 1, 12, 0, tzinfo=timezone.utc),
            )
        )
    sesion.commit()
    yield sesion
    sesion.close()


@pytest.fixture
def mlflow_local(monkeypatch: pytest.MonkeyPatch) -> str:
    """Usa un directorio temporal como tracking store de MLflow."""
    directorio = tempfile.mkdtemp()
    uri = Path(directorio).as_uri()
    monkeypatch.setenv("URL_MLFLOW", uri)
    obtener_configuracion.cache_clear()
    invalidar_cache_modelo()
    yield uri
    obtener_configuracion.cache_clear()
    invalidar_cache_modelo()


def test_entrenar_y_predecir_venta(
    sesion_con_pedidos: Session,
    mlflow_local: str,
) -> None:
    """Entrena con pedidos de prueba y devuelve una predicción numérica."""
    resultado = entrenar_y_registrar(sesion_con_pedidos)
    assert resultado.run_id
    assert resultado.metricas["mae"] >= 0

    invalidar_cache_modelo()

    salida = predecir_venta(
        PrediccionVentaEntrada(
            producto="Laptop",
            cantidad=2,
            region="Santiago",
            fecha_pedido=datetime(2026, 6, 10, 12, 0, tzinfo=timezone.utc),
        )
    )
    assert salida.monto_predicho > 0
    assert salida.modelo == "modelo-prediccion-ventas"
