"""
Script para cargar datos de demostración en la base de datos.

Uso (desde la carpeta backend/):
    py scripts/sembrar_datos.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from aplicacion.inicializacion import ejecutar_migraciones, sembrar_si_vacio


def sembrar() -> None:
    ejecutar_migraciones()
    sembrar_si_vacio()
    print("Datos de demostración listos (seed omitido si la BD ya tenía pedidos).")


if __name__ == "__main__":
    sembrar()
