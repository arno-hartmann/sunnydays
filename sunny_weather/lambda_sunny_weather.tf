resource "aws_lambda_function" "rate_weather" {
  filename      = "sunny_weather/deploy-sunny.zip"
  function_name = "lambda_weather_rating"
  role          = var.lambda_role
  handler       = "lambda_weather_rating.lambda_handler"
  memory_size = 512
  timeout = 900
  source_code_hash = filebase64sha256("sunny_weather/deploy-sunny.zip")

  runtime = "python3.9"
  
  environment {
    variables = {
      WEATHER_TABLE_NAME = var.weather_table_name
    }
  }
}