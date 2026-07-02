variable "region" {
  description = "Región AWS de despliegue"
  type        = string
  default     = "us-east-1"
}

variable "entorno" {
  description = "Nombre del entorno (dev, staging, prod)"
  type        = string
  default     = "staging"
}

variable "nombre_proyecto" {
  description = "Prefijo para nombrar recursos"
  type        = string
  default     = "opspulse"
}

variable "db_username" {
  description = "Usuario administrador de PostgreSQL"
  type        = string
  default     = "opspulse"
}

variable "db_password" {
  description = "Contraseña de PostgreSQL (usar TF_VAR_db_password o tfvars)"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "Tamaño de instancia RDS"
  type        = string
  default     = "db.t4g.micro"
}

variable "api_image" {
  description = "Imagen Docker de la API en ECR (ej. 123456789.dkr.ecr.us-east-1.amazonaws.com/opspulse-api:latest)"
  type        = string
  default     = ""
}

variable "allowed_cidr_api" {
  description = "CIDRs permitidos para acceder a la API (0.0.0.0/0 solo para demo)"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
