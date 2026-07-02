# OpsPulse — levantar stack completo (desarrollo + observabilidad)

Write-Host "OpsPulse: levantando API, frontend, MLflow, Prometheus y Grafana..." -ForegroundColor Cyan
docker compose --profile observabilidad up --build
