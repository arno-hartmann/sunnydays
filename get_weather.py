from decimal import *
from datetime import date, timedelta, datetime
import formatting_utils
import get_weather_utils


today = date.today()
today_str = formatting_utils.maketimestring(today)

cities=[]
cities = get_weather_utils.get_all_destinations_from_dynamodb()

counter = 0
for items in cities:
    
    api_url = get_weather_utils.determine_url_for_api(cities[counter]['city_id'], today_str)

    get_weather_utils.write_weather_dynamoDB(api_url, cities[counter]['city'])
    counter+=1
