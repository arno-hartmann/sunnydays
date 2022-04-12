from get_weather import get_weather_from_api  

def lambda_handler(event, context):   
    get_weather_from_api()

