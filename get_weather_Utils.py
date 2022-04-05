from decimal import *
import boto3
import requests
from datetime import date, timedelta, datetime
import formatting_Utils



def make_url_api(location_id, day_str):
    url = "https://www.metaweather.com/api/location/" + location_id + "/"+ day_str  + "/"
    print("API-URL aus Funktion make_url_api: ", url)
    return url


def get_location(number):
    dynamodb = boto3.resource('dynamodb')
    table_destination = dynamodb.Table('destination')
    response = table_destination.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table_destination.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    city = response['Items'][number]['city']
    city_id = response['Items'][number]['city_id']
    print(city, city_id)
    return [city, city_id]



def write_weather_dynamoDB(api_url, location):
    url = requests.get(api_url)
    response = url.json()

    dynamodb = boto3.resource('dynamodb')

    table_weather = dynamodb.Table('weather')


    counter = 0
    for item in response:
        
        #city in DB
        # date = applicable_date
        report = counter
        id = response[counter]['id']
        weather_state_name = response[counter]['weather_state_name']
        weather_state_abbr = response[counter]['weather_state_abbr']
        wind_direction_compass = response[counter]['wind_direction_compass']
        created = response[counter]['created']
        applicable_date = response[counter]['applicable_date']
        min_temp = formatting_Utils.make_decimal(response[counter]['min_temp'])
        max_temp = formatting_Utils.make_decimal(response[counter]['max_temp'])
        the_temp = formatting_Utils.make_decimal(response[counter]['the_temp'])
        wind_speed = formatting_Utils.make_decimal(response[counter]['wind_speed'])
        wind_direction = formatting_Utils.make_decimal(response[counter]['wind_direction'])
        air_pressure = formatting_Utils.make_decimal(response[counter]['air_pressure'])
        humidity = response[counter]['humidity']
        visibility = formatting_Utils.make_decimal(response[counter]['visibility'])
        predictability = response[counter]['predictability']
        
        if formatting_Utils.is_date_recent(created):
            dict = {
                'city'  : location,
                'date'  : counter,
                'id'    : id,
                'weather_state_name' : weather_state_name,
                'weather_state_abbr' : weather_state_abbr,
                'wind_direction_compass' : wind_direction_compass,
                'created'	: created,
                'applicable_date'	: applicable_date,
                'min_temp' : min_temp,
                'max_temp' : max_temp,
                'the_temp' : the_temp,
                'wind_speed' : wind_speed,
                'wind_direction' : wind_direction,
                'air_pressure' : air_pressure,
                'humidity' : humidity,
                'visibility' : visibility,
                'predictability' : predictability
            }
            print("Writing:", created)
            table_weather.put_item(Item=dict)
        counter+=1

