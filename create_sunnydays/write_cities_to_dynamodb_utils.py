import boto3
import json

dynamodb = boto3.resource('dynamodb')


table_destination = dynamodb.Table('destination')


def write_cities_to_dynamodb():
    f = open('cities.json')
    cities = json.load(f)
    print(cities)
    for item in cities:
        dict = {
            'city' : item['city'],
            'city_id' : item['city_id'],
            'airport' : item['airport'],
            'weather_score' : 0
        }
        table_destination.put_item(Item=dict)
