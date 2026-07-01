# Convenciones de código — OpsPulse

Definí estas convenciones al iniciar el proyecto para mantener consistencia entre backend, frontend y documentación. Si revisas el código, estos son los criterios que apliqué.

## Nomenclatura

### Español en el dominio, inglés en lo estándar

| Uso español | Se mantiene en inglés |
|-------------|------------------------|
| `ServicioPedidos`, `crear_pedido` | `Docker`, `Redis`, `FastAPI` |
| `eventos_ingesta`, `reglas_automatizacion` | Rutas REST (`/api/v1/...`) |
| Comentarios y docstrings | Nombres de librerías (`pandas`, `celery`) |

### Archivos

- **Python:** `snake_case` → `servicio_pedidos.py`, `tareas_etl.py`
- **Angular:** `kebab-case` en carpetas → `panel-operaciones/`, `servicio-api.ts`

## Comentarios

Cada módulo tiene un docstring que describe su rol en el sistema. Las funciones públicas documentan qué hace, qué recibe, qué devuelve y errores relevantes.

```python
def obtener_resumen(self) -> PedidoResumen:
    """
    Calcula KPIs para el dashboard.

    Agrega totales y detecta el producto y región con más ventas.
    """
```

Evito comentarios que repiten lo obvio (`# incrementa contador`). Prefiero explicar decisiones de negocio o de arquitectura.

## Capas del backend

```
rutas/      →  HTTP: validación de entrada y formato de respuesta
servicios/  →  Lógica de negocio
modelos/    →  Tablas SQLAlchemy
esquemas/   →  Contratos Pydantic (entrada/salida de la API)
trabajos/   →  Tareas Celery (ETL, automatización)
```

Las rutas no ejecutan SQL ni contienen reglas de negocio. Toda la lógica pasa por los servicios.

## Puntos de entrada para revisar el código

Si quieres entender el flujo completo, este es el orden que recomiendo:

1. `aplicacion/servicios/servicio_ingesta.py` — recepción de CSV y encolado en Celery  
2. `aplicacion/trabajos/tareas_etl.py` — validación de columnas y carga en PostgreSQL  
3. `aplicacion/servicios/servicio_automatizacion.py` — evaluación de reglas y webhooks  
4. `docker-compose.yml` — servicios y dependencias del entorno local  
5. `frontend/src/app/paginas/panel-operaciones/` — consumo de la API desde Angular  

## Lo que evito

- Identificadores crípticos (`x`, `tmp`, `data2`)  
- Lógica de negocio dentro de handlers HTTP  
- Mezclar idiomas en un mismo nombre (`get_pedidos`, `fetchPedido`)
