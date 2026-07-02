resource "aws_security_group" "ecs_api" {
  name        = "${local.prefijo}-ecs-api"
  description = "API FastAPI en ECS Fargate"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP publico"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_api
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_cluster" "principal" {
  name = "${local.prefijo}-cluster"
}

resource "aws_cloudwatch_log_group" "api" {
  name              = "/ecs/${local.prefijo}-api"
  retention_in_days = 14
}

resource "aws_ecs_task_definition" "api" {
  count                    = var.api_image != "" ? 1 : 0
  family                   = "${local.prefijo}-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name  = "api"
      image = var.api_image
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]
      environment = [
        { name = "ENTORNO", value = var.entorno },
        { name = "URL_BASE_DATOS", value = "postgresql+psycopg://${var.db_username}:${var.db_password}@${aws_db_instance.postgres.address}:5432/opspulse" },
        { name = "URL_REDIS", value = var.url_redis != "" ? var.url_redis : "redis://placeholder:6379/0" },
        { name = "RUTA_DATOS_CRUDOS", value = "s3://${aws_s3_bucket.datos_crudos.bucket}/" }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.api.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "api"
        }
      }
      essential = true
    }
  ])
}

resource "aws_ecs_service" "api" {
  count           = var.api_image != "" ? 1 : 0
  name            = "${local.prefijo}-api"
  cluster         = aws_ecs_cluster.principal.id
  task_definition = aws_ecs_task_definition.api[0].arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.ecs_api.id]
    assign_public_ip = true
  }

  depends_on = [aws_db_instance.postgres]
}
