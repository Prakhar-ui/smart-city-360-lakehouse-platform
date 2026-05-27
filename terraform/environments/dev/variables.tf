variable "aws_region" {
  default = "ap-south-1"
}

variable "project_name" {
  default = "smartcity360"
}

variable "environment" {
  default = "dev"
}

variable "instance_type" {
  default = "t3.large"
}

variable "key_name" {}

variable "openweather_api_key" {
  sensitive = true
}

variable "tomtom_api_key" {
  sensitive = true
}

variable "openaq_api_key" {
  sensitive = true
}