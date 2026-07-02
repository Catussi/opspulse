terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Descomentar cuando tengas backend remoto (S3 + DynamoDB lock)
  # backend "s3" {
  #   bucket         = "opspulse-terraform-state"
  #   key            = "prod/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "opspulse-terraform-lock"
  #   encrypt        = true
  # }
}
