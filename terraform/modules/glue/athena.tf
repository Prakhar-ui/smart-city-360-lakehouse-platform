resource "aws_athena_workgroup" "smartcity360" {
  name = "${var.project_name}-${var.environment}"

  configuration {
    enforce_workgroup_configuration = true

    result_configuration {
      output_location = "s3://${var.data_lake_bucket}/athena-results/"
    }
  }
}