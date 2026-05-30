output "instance_profile_name" {
  value = aws_iam_instance_profile.instance_profile.name
}

output "glue_role_arn" {
  value = aws_iam_role.glue_role_arn
}