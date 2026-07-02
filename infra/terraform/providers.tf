provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Proyecto   = "opspulse"
      Gestionado = "terraform"
      Entorno    = var.entorno
    }
  }
}
