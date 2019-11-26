provider "aws" {
  version = "~> 2.39"
  region = "us-east-2"
}

variable "AWS_S3_TERRAFORM_BUCKET_NAME" {
  type = string
}

terraform {
  backend "s3" {
    bucket = var.AWS_S3_TERRAFORM_BUCKET_NAME
    key = "redup/terraform.tfstate"
    region = "us-east-2"
  }
}