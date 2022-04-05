from decimal import *
import boto3
import requests
from datetime import date, timedelta, datetime
import formatting_utils

dynamodb = boto3.resource('dynamodb')


def determine_url_for_api(location_id, day_str):
    url = "https://www.metaweather.com/api/location/" + location_id + "/"+ day_str  + "/"
    return url


def get_all_destinations_from_dynamodb():
    table_destination = dynamodb.Table('destination')
    response = table_destination.scan()
    data = response['Items']
    citylist=[]
    while 'LastEvaluatedKey' in response:
        response = table_destination.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items']) 
    counter = 0
    for items in data:
        cities = {
            "city" : data[counter]['city'],
            "city_id" : data[counter]['city_id']
        }
        citylist.append(cities)
        counter+=1
    return citylist


def write_weather_dynamoDB(api_url, location):
    url = requests.get(api_url)
    response = url.json()
    table_weather = dynamodb.Table('weather')

    counter = 0
    for item in response:
        if not formatting_utils.is_date_recent(response[counter]['created']):
            continue
        else:
            dict = {
                'city'  : location,
                'date'  : counter,
                'id'    : response[counter]['id'],
                'weather_state_name' : response[counter]['weather_state_name'],
                'weather_state_abbr' : response[counter]['weather_state_abbr'],
                'wind_direction_compass' : response[counter]['wind_direction_compass'],
                'created'	: response[counter]['created'],
                'applicable_date'	: response[counter]['applicable_date'],
                'min_temp' : formatting_utils.make_decimal(response[counter]['min_temp']),
                'max_temp' : formatting_utils.make_decimal(response[counter]['max_temp']),
                'the_temp' : formatting_utils.make_decimal(response[counter]['the_temp']),
                'wind_speed' : formatting_utils.make_decimal(response[counter]['wind_speed']),
                'wind_direction' : formatting_utils.make_decimal(response[counter]['wind_direction']),
                'air_pressure' : formatting_utils.make_decimal(response[counter]['air_pressure']),
                'humidity' : response[counter]['humidity'],
                'visibility' : formatting_utils.make_decimal(response[counter]['visibility']),
                'predictability' : response[counter]['predictability']
            }
            table_weather.put_item(Item=dict)
        counter+=1

