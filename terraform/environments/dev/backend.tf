terraform {
    backend "s3" {
        bucket = "smartcity360-terraform-state"
        key = "dev/terraform.tfstate"
        region = "ap-south-1"
        dynamodb_table = "smartcity360-terraform-locks"
        encrypt = true
    }
}