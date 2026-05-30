resource "aws_glue_crawler" "bronze" {
  name          = "${var.project_name}-bronze-crawler"
  role          = var.glue_role_arn
  database_name = aws_glue_catalog_database.smartcity360.name

  s3_target {
    path = "s3://${var.bucket_name}/bronze/"
  }

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "UPDATE_IN_DATABASE"
  }
}