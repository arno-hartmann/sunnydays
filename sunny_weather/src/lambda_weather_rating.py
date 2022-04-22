from weather_rating_sunny import weather_rating_to_dynamo


def lambda_handler(event, context):  
    weather_rating_to_dynamo()