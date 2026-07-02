"""Configuración compartida de pytest."""

import os

# Evita migraciones/seed contra PostgreSQL real durante pruebas unitarias.
os.environ.setdefault("ENTORNO", "pruebas")
