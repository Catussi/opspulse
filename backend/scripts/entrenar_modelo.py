"""
Script CLI para entrenar el modelo de predicción de ventas.

Uso (desde backend/ con MLflow accesible):
    py scripts/entrenar_modelo.py

Requiere al menos 8 pedidos en PostgreSQL (seed o ingesta CSV).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aplicacion.base_datos import FabricaSesion, crear_tablas
from aplicacion.ml.entrenamiento import entrenar_y_registrar
from aplicacion.ml.inferencia import invalidar_cache_modelo


def main() -> None:
    crear_tablas()
    sesion = FabricaSesion()
    try:
        resultado = entrenar_y_registrar(sesion)
        invalidar_cache_modelo()
        print(f"Modelo registrado: {resultado.nombre_modelo}")
        print(f"Run ID: {resultado.run_id}")
        print(f"Métricas: {resultado.metricas}")
    finally:
        sesion.close()


if __name__ == "__main__":
    main()
