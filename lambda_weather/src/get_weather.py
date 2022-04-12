from decimal import *
from datetime import date, timedelta, datetime
import formatting_utils
import get_weather_utils

def get_weather_from_api():
    today = date.today()

    cities=[]
    cities = get_weather_utils.get_all_destinations_from_dynamodb()

    for item in cities:
        for x in range(1,4):
            day = today + timedelta( days = x)
            day_str = formatting_utils.maketimestring(day)
        
            api_url = get_weather_utils.determine_url_for_api(item['city_id'], day_str)

            get_weather_utils.write_weather_dynamoDB(api_url, item['city'], x*100)
