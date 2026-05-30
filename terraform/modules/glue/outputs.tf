output "glue_database_name" {
  value = aws_glue_catalog_database.smartcity360.name
}

output "athena_workgroup" {
  value = aws_athena_workgroup.smartcity360.name
}