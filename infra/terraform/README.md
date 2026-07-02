# Infraestructura AWS — Terraform

IaC para desplegar OpsPulse en AWS: data lake (S3), PostgreSQL (RDS) y API (ECS Fargate).

## Recursos que crea

| Recurso | Propósito |
|---------|-----------|
| **S3** | Data lake — CSV crudos con versionado y cifrado |
| **RDS PostgreSQL 16** | Base de datos de producción |
| **ECS Fargate** | Contenedor de la API FastAPI |
| **IAM** | Roles mínimos para ECS y acceso a S3 |
| **CloudWatch Logs** | Logs del contenedor API |

Redis/Celery y Airflow pueden añadirse en una segunda iteración (ElastiCache + segundo servicio ECS).

## Requisitos

- [Terraform](https://www.terraform.io/downloads) >= 1.5
- Cuenta AWS con credenciales configuradas (`aws configure`)

## Uso

```powershell
cd infra/terraform
copy terraform.tfvars.example terraform.tfvars
# Editar terraform.tfvars y definir contraseña:
# $env:TF_VAR_db_password = "clave-segura-aqui"

terraform init
terraform plan
terraform apply
```

## Variables importantes

| Variable | Descripción |
|----------|-------------|
| `db_password` | Contraseña RDS (sensible, no commitear) |
| `api_image` | URI de imagen en ECR; si está vacía, solo se crea infra base sin servicio ECS |
| `entorno` | `staging` o `prod` |

## Outputs

Tras `terraform apply`:

```powershell
terraform output rds_endpoint
terraform output s3_bucket_datos_crudos
```

## CI

El workflow `.github/workflows/terraform.yml` ejecuta `fmt`, `validate` y `plan` en cada PR que toque esta carpeta.

## Notas

- Usa la VPC por defecto de la cuenta para simplificar el portafolio.
- En producción real: VPC dedicada, ElastiCache para Redis, secrets en AWS Secrets Manager y backend remoto S3 para el state.
