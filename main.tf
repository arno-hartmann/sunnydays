terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-west-2"
}


#HIER ANPASSEN?
data "aws_caller_identity" "current" {}

#HIER ANPASSEN?
locals {
  account_id = data.aws_caller_identity.current.account_id
}


resource "aws_dynamodb_table_item" "destination" {
  table_name = aws_dynamodb_table.destination.name
  hash_key   = aws_dynamodb_table.destination.hash_key
  range_key   = aws_dynamodb_table.destination.range_key
  item = <<ITEM
{
  "city": {"S": "London"},
  "city_id": {"S": "44418"}
}
ITEM
}
resource "aws_dynamodb_table" "destination" {
  name           = "destination"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "city"
  range_key      = "city_id"

  attribute {
    name = "city"
    type = "S"
  }

  attribute {
    name = "city_id"
    type = "S"
  }
}


resource "aws_dynamodb_table" "weather" {
  name           = "weather"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "city"
  range_key      = "date"

  stream_enabled = true
  stream_view_type = "NEW_IMAGE"

  attribute {
    name = "city"
    type = "S"
  }

  attribute {
    name = "date"
    type = "N"
  }
}


module "lambda_weather" {
  source = "./lambda_weather"
  lambda_role = join("" , ["arn:aws:iam::", local.account_id, ":role/LabRole"] )
  weather_table_name = aws_dynamodb_table.weather.name
}