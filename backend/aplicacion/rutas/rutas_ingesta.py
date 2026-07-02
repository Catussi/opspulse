"""
Rutas de ingesta: subida de CSV y consulta de eventos de auditoría.
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from aplicacion.base_datos import obtener_sesion
from aplicacion.esquemas.ingesta import EventoIngestaRespuesta, ResultadoIngestaCsv
from aplicacion.modelos.evento_ingesta import EventoIngesta
from aplicacion.metricas.prometheus import INGESTAS_CSV
from aplicacion.servicios.servicio_ingesta import ServicioIngesta

router = APIRouter(prefix="/api/v1/ingesta", tags=["Ingesta"])


@router.post("/csv", response_model=ResultadoIngestaCsv, status_code=status.HTTP_202_ACCEPTED)
async def subir_csv_pedidos(
    archivo: UploadFile = File(..., description="Archivo CSV con columnas de pedidos"),
    sesion: Session = Depends(obtener_sesion),
) -> ResultadoIngestaCsv:
    """
    Sube un CSV y encola su procesamiento en segundo plano.

    La respuesta es inmediata (202 Accepted); el ETL corre en Celery.
    """
    if not archivo.filename or not archivo.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se aceptan archivos con extensión .csv",
        )

    contenido = await archivo.read()
    if not contenido:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo está vacío.",
        )

    servicio = ServicioIngesta(sesion)
    evento, tarea_id = servicio.registrar_ingesta_csv(archivo.filename, contenido)
    INGESTAS_CSV.labels(estado="aceptada").inc()

    return ResultadoIngestaCsv(
        evento_id=evento.id,
        mensaje="Archivo recibido. El procesamiento continúa en segundo plano.",
        tarea_id=tarea_id,
    )


@router.get("/eventos/{evento_id}", response_model=EventoIngestaRespuesta)
def consultar_evento_ingesta(
    evento_id: int,
    sesion: Session = Depends(obtener_sesion),
) -> EventoIngesta:
    """Consulta el estado de un evento de ingesta (útil para polling desde el frontend)."""
    evento = sesion.get(EventoIngesta, evento_id)
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evento {evento_id} no encontrado.",
        )
    return evento
