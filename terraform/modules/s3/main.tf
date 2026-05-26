resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-datalake-${var.environment}"
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.data_lake.id

  versioning_configuration {
    status = "Enabled"
  }
}