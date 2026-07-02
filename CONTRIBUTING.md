# Contribuir a OpsPulse

Gracias por revisar el proyecto. OpsPulse es un repositorio de portfolio; las contribuciones externas son bienvenidas si mejoran claridad, tests o documentación.

## Cómo empezar

1. Clona el repo y lee el [README](README.md).
2. Levanta el stack: `docker compose up --build` o `.\scripts\levantar.ps1` para incluir observabilidad.
3. Backend: `cd backend && py -m pytest pruebas/ -v`
4. Frontend: `cd frontend && npm ci && npm run build`

## Convenciones

- Dominio de negocio en **español** (`ServicioPedidos`, comentarios orientados al lector).
- Cambios pequeños y enfocados; un PR por tema.
- Actualiza README o docs si cambias comportamiento visible.

## Reportar problemas

Abre un issue en GitHub con pasos para reproducir, logs y entorno (OS, Docker, ramas).
