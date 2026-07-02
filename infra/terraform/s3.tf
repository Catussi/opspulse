# Data lake: archivos CSV crudos antes del ETL
resource "aws_s3_bucket" "datos_crudos" {
  bucket = "${local.prefijo}-datos-crudos"
}

resource "aws_s3_bucket_versioning" "datos_crudos" {
  bucket = aws_s3_bucket.datos_crudos.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "datos_crudos" {
  bucket = aws_s3_bucket.datos_crudos.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "datos_crudos" {
  bucket = aws_s3_bucket.datos_crudos.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
