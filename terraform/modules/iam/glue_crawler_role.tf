resource "aws_iam_role" "glue_crawler_role" {
  name = "${var.project_name}-${var.environment}-crawler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "glue.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_service_role" {
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_policy" "crawler_s3_policy" {
  name = "${var.project_name}-${var.environment}-crawler-s3"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]

        Resource = [
          "arn:aws:s3:::${var.data_lake_bucket}",
          "arn:aws:s3:::${var.data_lake_bucket}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "crawler_s3_attach" {
  role       = aws_iam_role.glue_crawler_role.name
  policy_arn = aws_iam_policy.crawler_s3_policy.arn
}