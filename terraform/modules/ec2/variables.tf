variable "project_name" {}
variable "environment" {}
variable "instance_type" {}
variable "key_name" {}
variable "security_group_id" {}
variable "instance_profile_name" {}

variable "openweather_api_key" {
  sensitive = true
}

variable "tomtom_api_key" {
  sensitive = true
}

variable "openaq_api_key" {
  sensitive = true
}