# Infraestructura AWS — Terraform

Configuración de infraestructura como código para el despliegue de OpsPulse en AWS. Está en desarrollo.

## Recursos planificados

| Recurso | Uso |
|---------|-----|
| **S3** | Data lake — archivos CSV crudos antes del ETL |
| **RDS PostgreSQL** | Base de datos de producción |
| **ECS Fargate** | Contenedores de la API FastAPI y el worker Celery |
| **IAM** | Roles con permisos mínimos necesarios |

## Uso previsto

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

El pipeline de CI/CD (GitHub Actions) construirá las imágenes Docker y las publicará antes del deploy. Ver `docs/ARQUITECTURA.md` para el diagrama completo.
