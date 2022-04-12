resource "aws_lambda_function" "write_to_dynamo" {
  filename      = "lambda_weather/deploy-weather.zip"
  function_name = "lambda_get_weather"
  role          = var.lambda_role
  handler       = "lambda_weather_function.lambda_handler"
  memory_size = 512
  timeout = 900
  source_code_hash = filebase64sha256("lambda_weather/deploy-weather.zip")

  runtime = "python3.9"
  
  environment {
    variables = {
      WEATHER_TABLE_NAME = var.weather_table_name
    }
  }
}