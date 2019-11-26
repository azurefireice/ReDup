provider "aws" {
  version = "~> 2.39"
  region = "us-east-2"
}

variable "TERRAFORM_S3_BUCKET" {}

terraform {
  backend "s3" {}
}

data "terraform_remote_state" "state" {
  backend = "s3"
  config = {
    bucket = var.TERRAFORM_S3_BUCKET
    region = "us-east-2"
    key = "redup/terraform.tfstate"
  }
}
