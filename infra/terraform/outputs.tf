output "s3_bucket_datos_crudos" {
  description = "Bucket S3 para archivos CSV crudos"
  value       = aws_s3_bucket.datos_crudos.bucket
}

output "rds_endpoint" {
  description = "Host de PostgreSQL (solo accesible desde VPC/ECS)"
  value       = aws_db_instance.postgres.address
}

output "rds_port" {
  value = aws_db_instance.postgres.port
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.principal.name
}

output "ecs_service_name" {
  description = "Servicio ECS de la API (vacío si api_image no está configurada)"
  value       = length(aws_ecs_service.api) > 0 ? aws_ecs_service.api[0].name : null
}
