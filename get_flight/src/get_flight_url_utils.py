from decimal import *
from datetime import date, timedelta, datetime
import boto3

dynamodb = boto3.resource('dynamodb')


def make_flight_url(origin, destination, departure_date, return_date):
    url = ("https://www.skyscanner.de/transport/fluge/"+ origin+"/"+ destination+"/"+departure_date+"/"+return_date+"/")
    return url

def startdate():
    return date.today() + timedelta(days =1)

def returndate(start_date, trip_length):
    return start_date + timedelta(days = trip_length)

def maketimestring(day):
    return day.strftime("%y%m%d")

def get_all_destinations_from_dynamodb():
    table_destination = dynamodb.Table('destination')
    response = table_destination.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table_destination.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items']) 
    return data 


def write_write_url_to_dynamo(city, city_id, url):
    table_destination = dynamodb.Table('destination')
    table_destination.update_item(
        Key={
            'city': city,
            'city_id': city_id,
        },
        UpdateExpression='SET flight_url = :val1',
        ExpressionAttributeValues={
            ':val1': url
        }
    )

def write_dynamo_sunny(city, city_id, url):
    table_sunny = dynamodb.Table('sunny')
    table_sunny.put_item(
        Item={
            'city': city,
            'city_id': city_id,
            'url': url
        }
    )

def get_sunny_destinations(trip_length):

    min_weatherscore = 0
    for n in range(trip_length):
        min_weatherscore+=1

    city_data = get_all_destinations_from_dynamodb()
    departure_date = maketimestring(startdate())
    return_date = maketimestring(returndate(startdate(),3))
  
    for item in city_data:
        if item['weather_score'] > min_weatherscore:
            url = make_flight_url('FRA', item['airport'], departure_date, return_date)            
            write_dynamo_sunny(item['city'], item['city_id'], url)




