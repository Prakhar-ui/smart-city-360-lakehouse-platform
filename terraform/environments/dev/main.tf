module "s3" {
  source = "../../modules/s3"

  project_name = var.project_name
  environment  = var.environment
}

module "security_group" {
  source = "../../modules/security_group"

  project_name = var.project_name
}

module "iam" {
  source = "../../modules/iam"

  project_name = var.project_name
}

module "ec2" {
  source = "../../modules/ec2"

  project_name          = var.project_name
  environment           = var.environment
  instance_type         = var.instance_type
  key_name              = var.key_name
  security_group_id     = module.security_group.security_group_id
  instance_profile_name = module.iam.instance_profile_name
}