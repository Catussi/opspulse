# Frontend — OpsPulse

Dashboard Angular 19 que consume la API FastAPI de OpsPulse. Muestra KPIs de pedidos, tabla de ventas recientes y carga de archivos CSV para ingesta.

## Estructura

```
src/app/
├── nucleo/
│   ├── modelos/          # Interfaces TypeScript (Pedido, ResumenPedidos)
│   └── servicios/        # ServicioApi — cliente HTTP centralizado
└── paginas/
    └── panel-operaciones/  # Vista principal del dashboard
```

La URL de la API se configura en `src/entornos/entorno.ts` (por defecto `http://localhost:8000`).

## Desarrollo

```powershell
npm install
npm start
```

La aplicación queda en http://localhost:4200. Requiere que la API esté corriendo en el puerto 8001.

## Build de producción

```powershell
npm run build
```

Los artefactos se generan en `dist/frontend/`.

## Pruebas

```powershell
npm test
```

Generado con [Angular CLI](https://angular.dev/tools/cli) 19. La lógica de negocio vive en el backend; el frontend se limita a presentación y llamadas HTTP.
