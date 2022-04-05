from decimal import *
from datetime import date, timedelta, datetime
import formatting_Utils
import get_weather_Utils

# Gets today's date and makes it a string
today = date.today()
today_str = formatting_Utils.maketimestring(today)

#Gets the city Name and ID from Database (here 0), will be called in a while/for to get all cities
city = get_weather_Utils.get_location(0)[0]
city_id = get_weather_Utils.get_location(0)[1]

# makes URL for calling the API for weather in City for the day that is given
api_url = get_weather_Utils.make_url_api(city_id, today_str)
#writes weather data to dynamoDB
get_weather_Utils.write_weather_dynamoDB(api_url, city)