terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-west-1"
}

#criação do S3
resource "aws_s3_bucket" "bucket" {
  bucket = "desafio5-final"
}

resource "aws_s3_bucket" "bucket" {
  bucket = "ml-redshift-desafio-5"
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.bucket.id
  acl    = "private"
}



resource "aws_redshift_cluster" "redshift_cluster_2" {
  cluster_identifier = "redshift-cluster-2"
  database_name      = "dev"
  master_username    = "awsuser"
  master_password    = "Passw867!*"
  node_type          = "dc2.large"
  cluster_type       = "single-node"
}

