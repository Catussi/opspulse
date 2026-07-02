resource "aws_security_group" "rds" {
  name        = "${local.prefijo}-rds"
  description = "PostgreSQL OpsPulse"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description     = "PostgreSQL desde ECS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_api.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_subnet_group" "principal" {
  name       = "${local.prefijo}-db"
  subnet_ids = data.aws_subnets.default.ids
}

resource "aws_db_instance" "postgres" {
  identifier             = "${local.prefijo}-postgres"
  engine                 = "postgres"
  engine_version         = "16"
  instance_class         = var.db_instance_class
  allocated_storage      = 20
  storage_type           = "gp3"
  db_name                = "opspulse"
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.principal.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false
  skip_final_snapshot    = var.entorno != "prod"
  deletion_protection    = var.entorno == "prod"

  backup_retention_period = 7
}
