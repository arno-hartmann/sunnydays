resource "aws_lambda_function" "flight_url" {
  filename      = "get_flight/deploy-flight.zip"
  function_name = "lambda_flight_url"
  role          = var.lambda_role
  handler       = "lambda_flight_url.lambda_handler"
  memory_size = 512
  timeout = 900
  source_code_hash = filebase64sha256("get_flight/deploy-flight.zip")

  runtime = "python3.9"
  
  environment {
    variables = {
      WEATHER_TABLE_NAME = var.sunny_table_name
      DESTINATION_TABLE_NAME = var.sunny_table_name
    }
  }
}