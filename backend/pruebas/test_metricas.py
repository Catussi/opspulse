"""
Pruebas del endpoint de métricas Prometheus.
"""

from fastapi.testclient import TestClient

from aplicacion.principal import crear_aplicacion


def test_endpoint_metricas_expone_prometheus() -> None:
    """GET /metrics responde 200 y expone series HTTP estándar."""
    cliente = TestClient(crear_aplicacion())
    respuesta = cliente.get("/metrics")

    assert respuesta.status_code == 200
    assert "text/plain" in respuesta.headers["content-type"]
    cuerpo = respuesta.text
    assert "http_requests_total" in cuerpo
    assert "opspulse_ingestas_csv_total" in cuerpo
