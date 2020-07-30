provider "aws" {
  version = "~> 2.0"
  region  = "eu-west-1"
}

resource "aws_s3_bucket" "b" {
  bucket = "my-tf-test-bucket"
  acl    = "private"

  tags = {
    Name        = "My test bucket"
    Environment = "Dev"
  }
}

output "bucket_arn" {
  value = aws_s3_bucket.b.arn
}