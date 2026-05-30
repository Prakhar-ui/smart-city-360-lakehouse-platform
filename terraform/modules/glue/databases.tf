resource "aws_glue_catalog_database" "smartcity360" {
  name = "${var.project_name}_${var.environment}"
}