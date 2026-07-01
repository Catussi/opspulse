"""
Servicio de automatización: evalúa reglas de negocio y dispara acciones.

Ejemplo: si las ventas del día están por debajo del umbral configurado,
se marca la regla como disparada y se puede enviar un webhook.
"""

import logging

import httpx
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from aplicacion.modelos.pedido import Pedido
from aplicacion.modelos.regla_automatizacion import ReglaAutomatizacion

logger = logging.getLogger(__name__)


class ServicioAutomatizacion:
    """Evalúa reglas activas y ejecuta webhooks cuando corresponde."""

    def __init__(self, sesion: Session) -> None:
        self._sesion = sesion

    def listar_reglas_activas(self) -> list[ReglaAutomatizacion]:
        """Devuelve solo las reglas con activa=True."""
        consulta = select(ReglaAutomatizacion).where(ReglaAutomatizacion.activa.is_(True))
        return list(self._sesion.scalars(consulta).all())

    def evaluar_regla_ventas_bajas(self, regla: ReglaAutomatizacion) -> bool:
        """
        Comprueba si el monto total de ventas del día es menor al umbral.

        Returns:
            True si la condición se cumple (hay que disparar alerta).
        """
        monto_hoy = self._sesion.scalar(
            select(func.coalesce(func.sum(Pedido.cantidad * Pedido.precio_unitario), 0.0))
        )
        return float(monto_hoy or 0) < regla.umbral

    def enviar_webhook(self, regla: ReglaAutomatizacion, detalle: dict) -> bool:
        """
        POST al webhook configurado en la regla.

        Returns:
            True si el webhook respondió 2xx.
        """
        if not regla.url_webhook:
            logger.warning("Regla '%s' sin URL de webhook; se omite envío.", regla.nombre)
            return False

        try:
            respuesta = httpx.post(
                regla.url_webhook,
                json={
                    "regla": regla.nombre,
                    "tipo_condicion": regla.tipo_condicion,
                    "detalle": detalle,
                },
                timeout=10.0,
            )
            respuesta.raise_for_status()
            return True
        except httpx.HTTPError as error:
            logger.error("Error al enviar webhook de regla '%s': %s", regla.nombre, error)
            return False

    def ejecutar_evaluacion_completa(self) -> list[str]:
        """
        Recorre todas las reglas activas y dispara las que correspondan.

        Returns:
            Lista de mensajes descriptivos (útil para logs y pruebas).
        """
        resultados: list[str] = []

        for regla in self.listar_reglas_activas():
            if regla.tipo_condicion == "ventas_bajas":
                if self.evaluar_regla_ventas_bajas(regla):
                    enviado = self.enviar_webhook(
                        regla,
                        detalle={"mensaje": "Ventas por debajo del umbral configurado"},
                    )
                    resultados.append(
                        f"Regla '{regla.nombre}' disparada. Webhook enviado: {enviado}"
                    )
                else:
                    resultados.append(f"Regla '{regla.nombre}' sin disparar.")

        return resultados
