provider "aws" {
  version = "~> 2.39"
  region = "us-east-2"
}

variable "TERRAFORM_S3_BUCKET" {}

data "terraform_remote_state" "s3_state" {
  backend = "s3"
  config = {
    bucket = var.TERRAFORM_S3_BUCKET
    region = "us-east-2"
    key = "redup/terraform.tfstate"
  }
}

terraform {
  backend "s3" {}
}
