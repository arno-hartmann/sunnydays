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


data "aws_caller_identity" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
}

resource "aws_dynamodb_table" "destination" {
  name           = "destination"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "city"
  range_key      = "city_id"

  stream_enabled = true
  stream_view_type = "NEW_IMAGE"

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

resource "aws_dynamodb_table" "sunny" {
  name           = "sunny"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "city"
  #range_key      = "date"


  stream_enabled = true
  stream_view_type = "NEW_IMAGE"


  attribute {
    name = "city"
    type = "S"
  }
}


module "lambda_weather" {
  source = "./lambda_weather"
  lambda_role = join("" , ["arn:aws:iam::", local.account_id, ":role/LabRole"] )
  weather_table_name = aws_dynamodb_table.weather.name
}


module "sunny_weather" {
  source = "./sunny_weather"
  lambda_role = join("" , ["arn:aws:iam::", local.account_id, ":role/LabRole"] )
  weather_table_name = aws_dynamodb_table.weather.name
  destination_table_name = aws_dynamodb_table.destination.name

resource "aws_lambda_event_source_mapping" "lambda_get_weather_sm" {
  event_source_arn  = aws_dynamodb_table.destination.stream_arn
  function_name     = module.lambda_weather.write_to_dynamodb_lambda.arn
  starting_position = "LATEST"
}

resource "aws_cloudwatch_event_rule" "time_to_get_weather" {
  name        = "time_to_get_weather"
  description = "Get Lamda get_weather twice a day"
  schedule_expression = var.schedule_expression
}
resource "aws_cloudwatch_event_target" "lambda_get_weather_cw" {
  rule      = aws_cloudwatch_event_rule.time_to_get_weather.name
  target_id = "call_lambda_weather"
  arn       = module.lambda_weather.write_to_dynamodb_lambda.arn
}

variable "schedule_expression" {
  default     = "cron(25 6 * * ? *)"
  description = "the aws cloudwatch event rule scheule expression that specifies when the scheduler runs. Default is 5 minuts past the hour. for debugging use 'rate(5 minutes)'. See https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = module.lambda_weather.write_to_dynamodb_lambda.arn
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.time_to_get_weather.arn

}